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

prepend_path("PATH", bin)
prepend_path("PATH", pathJoin(root, "fluent/bin"))
setenv("ANSYS_ROOT", root)
setenv("ANSYS_BIN", bin)
setenv("AWP_ROOT242", root)
setenv("ANSYS_VERSION", "2024_R2_v242")
setenv("ANSYSLMD_LICENSE_FILE", "1055@ansyslic.empa.ch")
