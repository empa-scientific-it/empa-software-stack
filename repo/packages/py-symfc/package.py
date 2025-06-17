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
#     spack install py-symfc
#
# You can edit this file again by typing:
#
#     spack edit py-symfc
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PySymfc(PythonPackage):
    """Symfc is a Python package for symmetry analysis of phonon spectra."""

    homepage = "https://github.com/symfc/symfc"

    url = "https://github.com/symfc/symfc/archive/refs/tags/v1.3.4.tar.gz"

    license("BSD-3-Clause", checked_by="edoardob90")

    version("1.3.4", sha256="8fee56b22bf8d867b3625adb7e792416ed36314cb7cb8e823a40a69b9c740f92")
    version("1.0.1", sha256="da77f188432c81850c4f92d473fc65e727e754f7eb6de6c2bd1f5a05f2170356")
    version("1.0.0", sha256="b58969a3514665cecca9d14a3cd428ba5e0b4300f0d64a60f366097531948c4c")

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy@:1.10,1.11.3:", type=("build", "run"))
    depends_on("py-spglib", type=("build", "run"))
