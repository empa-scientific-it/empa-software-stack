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
#     spack install py-ppafm
#
# You can edit this file again by typing:
#
#     spack edit py-ppafm
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PyPpafm(PythonPackage):
    """Classical force field model for simulating atomic force microscopy images."""

    homepage = "https://github.com/Probe-Particle/ProbeParticleModel"
    pypi = "ppafm/ppafm-0.3.2.tar.gz"

    maintainers("NikoOinonen", "yakutovicha", "edoardob90")

    license("MIT License", checked_by="edoardob90")

    version("0.3.2", sha256="ca6f2a885af6201bdf230ea39af6dce569ca506499c6775ed6cc0b736b839168")
    version("0.4.0", sha256="f02a2c3f08f42bc8f243b9a730753a7f4c1ad93e00d63860f51820b39caf24be")

    # Build dependencies
    depends_on("py-setuptools@61.2:", type="build")
    depends_on("python@3.8:", type=("build", "run"))

    # Runtime dependencies
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pydantic", type=("build", "run"))
    depends_on("py-toml", type=("build", "run"))

    #
    # NOTE: py-reikna is not available in Spack, so we cannot enable OpenCL support
    #
    # variant("opencl", default=False, description="Enable OpenCL support")
    # depends_on("py-pyopencl", type=("build", "run"), when="+opencl")
    # depends_on("py-reikna", type=("build", "run"), when="+opencl")
    # depends_on("py-ase", type=("build", "run"), when="+opencl")
    # Not sure if this is needed
    # depends_on("py-pyqt5", type=("build", "run"), when="+opencl platform=windows")
