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
#     spack install py-phonopy
#
# You can edit this file again by typing:
#
#     spack edit py-phonopy
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PyPhonopy(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://phonopy.github.io/phonopy/"

    url = "https://github.com/phonopy/phonopy/archive/refs/tags/v2.25.0.tar.gz"

    license("BSD-3-Clause", checked_by="edoardob90")

    version("2.25.0", sha256="8ff052d680dfd3d2820143c8efc326e6865521ee92cb525d4cb98aa6c0fb60a0")

    depends_on("c", type="build")
    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-scikit-build", type="build")
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-numpy@1.17.0:", type=("build", "run"))
    depends_on("py-matplotlib@2.2.2:", type=("build", "run"))
    depends_on("py-spglib@1.3:", type=("build", "run"))
    depends_on("py-h5py@3.0:", type=("build", "run"))
    depends_on("py-symfc@1.3:", type=("build", "run"))