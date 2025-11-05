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
#     spack install py-cubehandler
#
# You can edit this file again by typing:
#
#     spack edit py-cubehandler
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PyCubehandler(PythonPackage):
    """Python package for handling cube files."""

    homepage = "https://github.com/nanotech-empa/cubehandler"
    pypi = "cubehandler/cubehandler-0.1.0.tar.gz"

    # Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers("yakutovicha", "cpignedoli")

    # Add the SPDX identifier of the project's license below.
    # See https://spdx.org/licenses/ for a list. Upon manually verifying
    # the license, set checked_by to your Github username.
    license("MIT", checked_by="yakutovicha")

    version("0.1.0", sha256="94922ae7a33d4c7a2f444e196b4c3c85f8a3e83e6eaddfb96b812e05779362d9")
    version("0.2.0", sha256="db6e9e40f3d661118aed9b4cacfbb1f0fad5b69b6c0c627ab0b74661fe9c85f5")

    # Only add the python/pip/wheel dependencies if you need specific versions
    # or need to change the dependency type. Generic python/pip/wheel dependencies are
    # added implicity by the PythonPackage base class.
    depends_on("python@3.10:", type=("build", "run"))

    depends_on("py-flit-core", type="build")

    # Add additional dependencies if required.
    depends_on("py-ase", type=("run"))
    depends_on("py-click", type=("run"))
    depends_on("py-scikit-image", type=("run"))
