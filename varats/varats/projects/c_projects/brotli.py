"""Project file for brotli."""
import typing as tp

import benchbuild as bb
from benchbuild.utils.cmd import mkdir, make
from benchbuild.utils.settings import get_number_of_jobs
from plumbum import local

from varats.containers.containers import get_base_image, ImageBase
from varats.paper_mgmt.paper_config import project_filter_generator
from varats.project.project_util import (
    ProjectBinaryWrapper,
    wrap_paths_to_binaries,
    BinaryType,
    verify_binaries,
)
from varats.project.varats_project import VProject
from varats.utils.git_util import ShortCommitHash
from varats.utils.settings import bb_cfg


class Brotli(VProject):
    """Brotli compression format."""

    NAME = 'brotli'
    GROUP = 'c_projects'
    DOMAIN = 'compression'

    SOURCE = [
        bb.source.Git(
            remote="https://github.com/google/brotli.git",
            local="brotli_git",
            refspec="HEAD",
            limit=None,
            shallow=False,
            version_filter=project_filter_generator("brotli")
        )
    ]

    CONTAINER = get_base_image(ImageBase.DEBIAN_10
                              ).run('apt', 'install', '-y', 'cmake')

    @staticmethod
    def binaries_for_revision(
        revision: ShortCommitHash  # pylint: disable=W0613
    ) -> tp.List[ProjectBinaryWrapper]:
        return wrap_paths_to_binaries([("out/brotli", BinaryType.EXECUTABLE)])

    def run_tests(self) -> None:
        pass

    def compile(self) -> None:
        """Compile the project."""
        brotli_version_source = local.path(self.source_of_primary)

        c_compiler = bb.compiler.cc(self)
        mkdir(brotli_version_source / "out")
        with local.cwd(brotli_version_source / "out"):
            with local.env(CC=str(c_compiler)):
                bb.watch(local["../configure-cmake"])()
            bb.watch(make)("-j", get_number_of_jobs(bb_cfg()))

        with local.cwd(brotli_version_source):
            verify_binaries(self)

    @classmethod
    def get_cve_product_info(cls) -> tp.List[tp.Tuple[str, str]]:
        return [("google", "brotli")]