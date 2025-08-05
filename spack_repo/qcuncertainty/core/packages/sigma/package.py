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

from spack import package as pkg
from spack_repo.builtin.build_systems.cmake import CMakePackage


class Sigma(CMakePackage):
    """Sigma is a header-only C++ library for uncertainty propagation
    throughout mathematical operations on floating point values, inspired
    by uncertainties for Python and Measurements.jl for Julia.
    """

    homepage = "https://github.com/QCUncertainty/sigma"
    url = (
        "https://github.com/QCUncertainty/sigma/archive/refs/tags/v1.0.tar.gz"
    )
    git = "https://github.com/QCUncertainty/sigma.git"  # For the latest commit

    pkg.maintainers("jwaldrop107", "zachcran")

    pkg.license("Apache-2.0", checked_by="zachcran")

    # Latest commit from GitHub
    # "This download method is untrusted, and is not recommended. Branches are
    # moving targets, so the commit you get when you install the package likely
    # won’t be the same commit that was used when the package was first
    # written."
    #                                          ~~~~ From the Spack docs
    pkg.version("main", branch="main", preferred=True)

    # Versions from git tags
    pkg.version(
        "1.0",
        sha256="ea2317e6f31eed4d4c489cc56d248d10d93588cb170d718e3ffb00435329e0bc",
    )

    pkg.variant(
        "eigen",
        default=True,
        description="Include Eigen compatibility headers",
    )
    pkg.variant("docs", default=False, description="Build documentation")
    # Will also set BUILD_DOCS
    pkg.variant(
        "only-docs", default=False, description="Only build documentation."
    )
    pkg.variant(
        "docs-fail-on-warning",
        default=False,
        description="Documentation build will fail from warnings.",
    )
    pkg.variant(
        "cxxstd",
        default="17",
        # NOTE: Comma after "17" is necessary so Spack doesn't split it into
        #       individual characters
        values=("17",),
        multi=False,
        description="Use the specified C++ standard when building",
        sticky=True,
    )

    # Runtime dependencies
    pkg.depends_on("cxx", type="build")
    pkg.depends_on(
        "eigen",
        when="+eigen",
    )

    # Test dependencies
    pkg.depends_on("catch2", type=("build", "test"))

    # Sanity check tests during installation
    sanity_check_is_file = [
        pkg.join_path("include", "sigma", "sigma.hpp"),
        pkg.join_path("lib", "sigma", "cmake", "sigmaConfig.cmake"),
        pkg.join_path("lib", "sigma", "cmake", "sigmaConfigVersion.cmake"),
        pkg.join_path("lib", "sigma", "cmake", "sigma-target.cmake"),
    ]

    sanity_check_is_dir = [
        pkg.join_path("include", "sigma"),
        pkg.join_path("lib", "sigma"),
        pkg.join_path("lib", "sigma", "cmake"),
    ]

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_DOCS", "docs"),
            self.define_from_variant("ONLY_BUILD_DOCS", "only-docs"),
            self.define_from_variant(
                "DOCS_FAIL_ON_WARNING", "docs-fail-on-warning"
            ),
            self.define_from_variant("ENABLE_EIGEN_SUPPORT", "eigen"),
            self.define("BUILD_TESTING", self.run_tests),
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
        ]

        if "CMAKE_TOOLCHAIN_FILE" in os.environ:
            args.append(
                f"-DCMAKE_TOOLCHAIN_FILE={os.environ["CMAKE_TOOLCHAIN_FILE"]}"
            )
        # TODO: +debug flag? +verbose flag?
        args.append(self.define("CMAKE_MESSAGE_LOG_LEVEL", "DEBUG"))
        # Silence FetchContent by default
        args.append(self.define("FETCHCONTENT_QUIET", True))
        args.append("-Wno-dev")
        # https://cmake.org/cmake/help/latest/policy/CMP0152.html
        # Added in 3.28; OLD is deprecated now
        args.append(self.define("CMAKE_POLICY_DEFAULT_CMP0152", "NEW"))

        # DEBUG REMOVE ME
        args.append(
            self.define(
                "FETCHCONTENT_SOURCE_DIR_NWX_CMAKE",
                "/home/zachcran/workspaces/nwchemex/repos_dev/nwxcmake",
            )
        )

        return args
