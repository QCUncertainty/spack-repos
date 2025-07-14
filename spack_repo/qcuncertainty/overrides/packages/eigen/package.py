from spack.package import depends_on
from spack_repo.builtin.packages.eigen.package import Eigen as BuiltinEigen


class Eigen(BuiltinEigen):
    """Override of builtin.eigen to add missing Fortran language dependency."""

    depends_on("fortran", type="build")
