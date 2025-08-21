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
#     spack install fresnel
#
# You can edit this file again by typing:
#
#     spack edit fresnel
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Fresnel(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url = "https://github.com/glotzerlab/fresnel/releases/download/v0.13.7/fresnel-0.13.7.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers("github_user1", "github_user2")

    # FIXME: Add the SPDX identifier of the project's license below.
    # See https://spdx.org/licenses/ for a list. Upon manually verifying
    # the license, set checked_by to your Github username.
    license("UNKNOWN", checked_by="github_user1")

    version("0.13.7", sha256="aa39f3d625ba4132f86edcc49f64800e033d68c6d5af237dd3287a20d9293c48")
    version("0.13.6", sha256="0b85682607cca547d7e2713f613cbaf4a5e84c9fa123e6872e0400859248f86f")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    # FIXME: Add dependencies if required.
    depends_on("py-pybind11")
    depends_on("py-numpy")
    depends_on("embree")
    depends_on("qhull")

    variant("cpu", default=True, description="Enable CPU support")
    variant("gpu", default=False, description="Enable GPU support")

    depends_on("embree", when="+cpu")
    depends_on("cuda", when="+gpu")

    def cmake_args(self):
        args = []
        if "+cpu" in self.spec:
            args.append(self.define("ENABLE_EMBREE", True))
        
        if "+gpu" in self.spec:
            args.append(self.define("BUILD_OPTIX", True))

        return args
