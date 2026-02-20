# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCleedpy(PythonPackage):
    """Python port of the CLEED code for Low-Energy Electron Diffraction (LEED) calculations."""

    homepage = "https://github.com/empa-scientific-it/cleedpy"
    pypi = "cleedpy/cleedpy-0.1.5.tar.gz"

    maintainers("yakutovicha")

    license("MIT", checked_by="yakutovicha")

    version("0.1.5", sha256="dd59141993c15759b55833383fd80ec2e1567328df9837d485128aa38b1ae6c3")

    # Python version requirement
    depends_on("python@3.10:", type=("build", "run"))

    # Build dependencies - uses scikit-build-core which requires CMake
    depends_on("py-scikit-build-core@0.10:", type="build")
    depends_on("cmake@3.15:", type="build")

    # Runtime dependencies
    depends_on("py-ase", type=("build", "run"))
    depends_on("py-click", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pydantic", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-typer", type=("build", "run"))
