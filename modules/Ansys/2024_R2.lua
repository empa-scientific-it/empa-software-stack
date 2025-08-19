help([[
Description
===========
CAE/Multiphysics engineering simulations software.

More information
================
- Homepage: http://ansys.com/
]])

whatis("Description: CAE/Multiphysics engineering simulations software.")
whatis("Homepage: https://ansys.com")
whatis("URL: https://ansys.com")

local root = "/capstor/store/cscs/empa/em00/apps/ansys/2024_R2/bin/v242"
local bin = pathJoin(root, "ansys/bin")

conflict("Ansys")

-- Detect architecture
local arch = capture("uname -m"):gsub("\n", "")

-- Construct path to user-local libs
local user_lib64 = pathJoin(os.getenv("HOME"), ".local", arch, "lib64")
local user_lib   = pathJoin(os.getenv("HOME"), ".local", arch, "lib")

-- Prepend to LD_LIBRARY_PATH
prepend_path("LD_LIBRARY_PATH", user_lib64)
prepend_path("LD_LIBRARY_PATH", user_lib)

-- Ansys root
prepend_path("PATH", bin)
setenv("ANSYS_ROOT", root)
setenv("ANSYS_BIN", bin)
setenv("AWP_ROOT242", root)
setenv("ANSYS_VERSION", "2024_R2_v242")
setenv("ANSYSLMD_LICENSE_FILE", "1055@ansyslic.empa.ch")

-- Fluent variables
prepend_path("PATH", pathJoin(root, "fluent/bin"))
setenv("FLUENT_INC", pathJoin(root, "fluent"))
