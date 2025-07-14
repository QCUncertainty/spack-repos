# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install sigma
#
# You can edit this file again by typing:
#
#     spack edit sigma
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

import os

from spack.package import *
from spack_repo.builtin.build_systems.cmake import CMakePackage


class Sigma(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/QCUncertainty/sigma"
    url = (
        "https://github.com/QCUncertainty/sigma/archive/refs/tags/v1.0.tar.gz"
    )
    git = "https://github.com/QCUncertainty/sigma.git"  # For the latest commit

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers("jwaldrop107", "zachcran")

    license("Apache-2.0", checked_by="zachcran")

    # Latest commit from GitHub
    # "This download method is untrusted, and is not recommended. Branches are
    # moving targets, so the commit you get when you install the package likely
    # won’t be the same commit that was used when the package was first written."
    #                                          ~~~~ From the Spack docs
    version("main", branch="main", preferred=True)

    # Versions from git tags
    version(
        "1.0",
        sha256="ea2317e6f31eed4d4c489cc56d248d10d93588cb170d718e3ffb00435329e0bc",
    )

    variant(
        "eigen",
        default=True,
        description="Include Eigen compatibility headers",
    )
    variant("docs", default=False, description="Build documentation")
    # Will also set BUILD_DOCS
    variant(
        "only-docs", default=False, description="Only build documentation."
    )
    variant(
        "docs-fail-on-warning",
        default=False,
        description="Documentation build will fail from warnings.",
    )
    variant(
        "tests",
        default=False,
        description="Build unit tests",
    )

    # Runtime dependencies
    depends_on("cxx", type="build")
    depends_on(
        "eigen",
        when="+eigen",
    )

    # Test dependencies
    depends_on("catch2", when="+tests")

    # Sanity check tests during installation
    sanity_check_is_file = [
        join_path("include", "sigma", "sigma.hpp"),
        join_path("lib", "sigma", "cmake", "sigmaConfig.cmake"),
        join_path("lib", "sigma", "cmake", "sigmaConfigVersion.cmake"),
        join_path("lib", "sigma", "cmake", "sigma-target.cmake"),
    ]

    sanity_check_is_dir = [
        join_path("include", "sigma"),
        join_path("lib", "sigma"),
        join_path("lib", "sigma", "cmake"),
    ]

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_TESTING", "tests"),
            self.define_from_variant("BUILD_DOCS", "docs"),
            self.define_from_variant("ONLY_BUILD_DOCS", "only-docs"),
            self.define_from_variant(
                "DOCS_FAIL_ON_WARNING", "docs-fail-on-warning"
            ),
            self.define_from_variant("ENABLE_EIGEN_SUPPORT", "eigen"),
        ]

        if "CMAKE_TOOLCHAIN_FILE" in os.environ:
            args.append(
                f"-DCMAKE_TOOLCHAIN_FILE={os.environ["CMAKE_TOOLCHAIN_FILE"]}"
            )
        args.append("-DCMAKE_MESSAGE_LOG_LEVEL=DEBUG")
        args.append("-DCMAKE_POLICY_DEFAULT_CMP0152=NEW")
        args.append("-Wno-dev")

        return args
