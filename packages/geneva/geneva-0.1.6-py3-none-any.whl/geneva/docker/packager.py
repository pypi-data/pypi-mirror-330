# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import hashlib
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Literal

import attrs
import docker
import docker.models
import docker.models.images
import docker.utils
import docker.utils.json_stream
from ._state import PackagingState
from jinja2 import Environment, FileSystemLoader

_CUDA_BASE = "nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04"
_CPU_BASE = "ubuntu:24.04"


_LOG = logging.getLogger(__name__)


def _get_base_dockerfile(
    backend: Literal["dataflow"],
    python_tool_chain: Literal["uv"],
    additional_pip_dependencies: list[str] | None = None,
    cuda: bool = False,
) -> str:
    if additional_pip_dependencies is None:
        additional_pip_dependencies = []
    module_location = Path(__file__).parent
    env = Environment(loader=FileSystemLoader(module_location), autoescape=True)
    # Load a template
    template = env.get_template(f"_base_{python_tool_chain}_{backend}.Dockerfile.j2")

    post_install_command = ""

    if additional_pip_dependencies:
        packages = " ".join(additional_pip_dependencies)
        post_install_command = f"RUN pip install {packages}"

    context = {
        "base_image": _CUDA_BASE if cuda else _CPU_BASE,
        "post_install_command": post_install_command,
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
    }
    return template.render(context)


def _get_incremental_dockerfile(
    backend: Literal["dataflow"],
    python_tool_chain: Literal["uv"],
    incremental_base: str,
) -> str:
    module_location = Path(__file__).parent
    env = Environment(loader=FileSystemLoader(module_location), autoescape=True)
    template = env.get_template(
        f"_incremental_{python_tool_chain}_{backend}.Dockerfile.j2"
    )

    context = {"incremental_base_image": incremental_base}

    return template.render(context)


@attrs.define
class DockerWorkspacePackager:
    """Local workspace docker packager"""

    # Docker client
    client: docker.DockerClient = attrs.field(
        factory=docker.from_env,
        kw_only=True,
    )

    additional_pip_dependencies: list[str] = attrs.field(factory=list, kw_only=True)

    # Path to the packaging cache
    state_store_path: Path = attrs.field(
        default=Path(os.environ.get("XDG_CONFIG_DIR", "~/.cache"))
        / "_geneva/ws_packager",
        converter=Path,
        kw_only=True,
    )

    _state: PackagingState = attrs.field(init=False)

    # support only uv for now
    python_tool_chain: Literal["uv"] = attrs.field(default="uv", kw_only=True)

    registry: str = attrs.field(
        default=os.environ.get("GENEVA_DOCKER_REGISTRY", ""), kw_only=True
    )

    image_name: str = attrs.field(
        default=os.environ.get("GENEVA_DOCKER_IMAGE_NAME", ""), kw_only=True
    )

    def __attrs_post_init__(self) -> None:
        self._state = PackagingState(self.state_store_path)

    def _image_name(self, tag: str) -> str:
        return f"{self.registry}/{self.image_name}:{tag}"

    def build(
        self,
        image_tag: str,
        cuda: bool = False,
        platform: Literal["linux/amd64", "linux/arm64"] = "linux/amd64",
    ) -> str:
        """Build a docker image"""

        # this context determines which base image (if there is one)
        # to use for incremental builds
        #
        # sort the item tuples so that the hash is deterministic
        # from potential order changes
        built_context = sorted(
            {
                "platform": platform,
                "cuda": cuda,
                "backend": "dataflow",
                "additional_pip_dependencies": self.additional_pip_dependencies,
                "python_tool_chain": self.python_tool_chain,
                "python_version": sys.version_info,
            }.items()
        )

        context_hash = hashlib.md5(str(built_context).encode()).hexdigest()

        if (
            incremental_image := self._state.current_incremental_image(context_hash)
        ) is not None:
            dockerfile = _get_incremental_dockerfile(
                backend="dataflow",
                python_tool_chain=self.python_tool_chain,
                incremental_base=incremental_image,
            )
            is_incremental = True
        else:
            dockerfile = _get_base_dockerfile(
                backend="dataflow",
                python_tool_chain=self.python_tool_chain,
                additional_pip_dependencies=self.additional_pip_dependencies,
                cuda=cuda,
            )
            is_incremental = False

        image_name = self._image_name(image_tag)
        subprocess.run(
            [
                "docker",
                "build",
                "-f",
                "-",
                "-t",
                image_name,
                "--platform",
                platform,
                ".",
            ],
            input=dockerfile.encode(),
            env={"DOCKER_BUILDKIT": "1", **os.environ.copy()},
            check=True,
        )

        # avoid setting incremental image on incremental builds
        # this is because the last layer of the incremental image
        # could be very large and overlaps with the incoming changes
        # TODO: we should trigger a full build of the incremental
        # base image based on some heuristic, e.g. change size, deps, etc.
        if not is_incremental:
            self._state.set_incremental_image(context_hash, image_name)

        return image_name

    def push(self, image_tag: str) -> None:
        """Push a docker image"""
        self.client.images.push(self._image_name(image_tag))


def register_packager_parser(subparsers) -> None:
    packager_parser = subparsers.add_parser(
        "package", description="Build local workspace and push docker image"
    )
    packager_parser.add_argument(
        "--docker-image",
        dest="image_name",
        required=True,
        help="The name of the image to build.",
    )
    packager_parser.add_argument(
        "--cuda",
        dest="cuda",
        action="store_true",
        default=False,
        help="Use CUDA base image.",
    )
    packager_parser.add_argument(
        "--platform",
        dest="platform",
        choices=["linux/amd64", "linux/arm64"],
        help="The platform to build the image for.",
    )
    packager_parser.set_defaults(func=run)


def run(args) -> None:
    packager = DockerWorkspacePackager()
    image = packager.build(
        image_tag=args.image_name,
        cuda=args.cuda,
        platform=args.platform,
    )

    _LOG.info("Built image %s, pushing to %s", image.id, args.image_name)
    packager.client.images.push(args.image_name)
    _LOG.info("Pushed image %s", args.image_name)
