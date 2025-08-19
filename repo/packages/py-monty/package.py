# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMonty(PythonPackage):
    """Monty is the missing complement to Python."""

    homepage = "https://github.com/materialsvirtuallab/monty"
    pypi = "monty/monty-2025.3.3.tar.gz"

    license("MIT", checked_by="edoardob90")

    version("2025.3.3", sha256="16c1eb54b2372e765c2f3f14cff01cc76ab55c3cc12b27d49962fb8072310ae0")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-six", type=("build", "run"), when="@:1")
