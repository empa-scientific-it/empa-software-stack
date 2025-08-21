# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Wannier90(MakefilePackage):
    """Wannier90 calculates maximally-localised Wannier functions (MLWFs)"""

    url = "https://github.com/wannier-developers/wannier90/archive/refs/heads/develop.tar.gz"

    maintainers("AndresOrtegaGuerrero")

    license("GPL-3.0-or-later", checked_by="AndresOrtegaGuerrero")

    version("develop", branch="develop")
    version("3.1.0", sha256="40651a9832eb93dec20a8360dd535262c261c34e13c41b6755fa6915c936b254")
    version("3.0.0", sha256="f196e441dcd7b67159a1d09d2d7de2893b011a9f03aab6b30c4703ecbf20fe5b")
    version("2.1.0", sha256="ee90108d4bc4aa6a1cf16d72abebcb3087cf6c1007d22dda269eb7e7076bddca")
    version("2.0.1", sha256="05ea7cd421a219ce19d379ad6ae3d9b1a84be4ffb367506ffdfab1e729309e94")
    
    # Dependencies 

    depends_on("fortran")
    depends_on("mpi")
    depends_on("openblas")

    variant("mpi", default=True, description="Enable MPI support")


    def setup_build_environment(self, env):

        if "+mpi" in self.spec:
            env.set("COMMS", "mpi")
            env.set("MPIF90", self.spec.mpifc)

        env.set("FC", self.spec["fortran"].command.path)
        env.set("CC", self.spec.mpicc)
        env.set("F90", self.spec.mpifc)

        libs = self.spec["openblas"].libs
        env.set("LIBS", libs.ld_flags)
        
        env.append_flags("FFLAGS", "-O3 -fPIC -g -fallow-argument-mismatch")
        env.append_flags("LDFLAGS", "-O3 -fPIC")

    def install(self, spec, prefix):

        if "+mpi" in spec:
            make("lib", "COMMS=mpi")

        # Only wannier90.x and postw90.x
        make("default")



