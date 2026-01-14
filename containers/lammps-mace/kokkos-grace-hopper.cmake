# Preset: Enable Kokkos for ARMv9 Grace host + Hopper90 GPU
# Kokkos core package
set(PKG_KOKKOS                   ON CACHE BOOL   "" FORCE)

# Backends
set(Kokkos_ENABLE_SERIAL         ON CACHE BOOL   "" FORCE)
set(Kokkos_ENABLE_CUDA           ON CACHE BOOL   "" FORCE)
set(Kokkos_ENABLE_OPENMP         ON CACHE BOOL   "" FORCE)

# Architectures
set(Kokkos_ARCH_ARMV9_GRACE      ON CACHE BOOL   "" FORCE)
set(Kokkos_ARCH_HOPPER90         ON CACHE BOOL   "" FORCE)

# Optional: use CUFFT for FFTs
set(FFT_KOKKOS                   "CUFFT" CACHE STRING "" FORCE)

# Silence deprecation warnings
set(Kokkos_ENABLE_DEPRECATION_WARNINGS OFF CACHE BOOL "" FORCE)
