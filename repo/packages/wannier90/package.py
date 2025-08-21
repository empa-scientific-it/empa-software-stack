# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Wannier90(MakefilePackage):
    """Wannier90 calculates maximally-localised Wannier functions (MLWFs)"""

    url = "https://github.com/wannier-developers/wannier90/archive/refs/heads/develop.tar.gz"

    maintainers("AndresOrtegaGuerrero")

    license("GPL-3.0-or-later", checked_by="AndresOrtegaGuerrero")

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



