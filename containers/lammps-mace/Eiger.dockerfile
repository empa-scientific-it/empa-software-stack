# ============================
# Stage 1: build toolchain
# ============================
ARG UBUNTU=22.04
FROM ubuntu:${UBUNTU} AS builder
ENV DEBIAN_FRONTEND=noninteractive

#Build args for this stage
ARG PYTORCH_VERSION=2.5.1
ARG MACE_VERSION=0.3.14
ARG LAMMPS_REPO=https://github.com/empa-scientific-it/lammps.git
ARG LAMMPS_BRANCH=mace-features

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake git ca-certificates \
    python3 python3-venv python3-pip python3-dev \
    cython3 \
    openmpi-bin libopenmpi-dev \
    automake autoconf \
    wget \
    libgsl-dev \
    libblas-dev liblapack-dev \
    libfftw3-dev \
    pkg-config \
    gfortran \
    intel-mkl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for building
RUN groupadd -r lammps && useradd -r -g lammps -d /home/lammps -m lammps

# Optional: Python venv for clean pip installs
ENV VENV=/opt/venv
RUN python3 -m venv $VENV && chown -R lammps:lammps $VENV
ENV PATH="$VENV/bin:$PATH"

USER lammps

# PyTorch CPU only (needed for LAMMPS compilation) - pinned version
RUN pip install --upgrade pip wheel setuptools && \
    pip install --no-cache-dir \
    --index-url https://download.pytorch.org/whl/cpu \
    torch==${PYTORCH_VERSION} \
    torchvision \
    torchaudio

# Clone your LAMMPS fork/branch
USER root
RUN mkdir -p /opt && chown lammps:lammps /opt
USER lammps
WORKDIR /opt
RUN git clone --depth 1 --branch ${LAMMPS_BRANCH} ${LAMMPS_REPO} lammps
WORKDIR /opt/lammps

# (If you still need your patch, keep it)
# COPY --chown=lammps:lammps diag_suppress.patch .
# RUN patch -p0 < diag_suppress.patch

# Build lib-pace library with the same ABI as libtorch
RUN CXXFLAGS="-D_GLIBCXX_USE_CXX11_ABI=0 ${CXXFLAGS}" \
    CPPFLAGS="-D_GLIBCXX_USE_CXX11_ABI=0 ${CPPFLAGS}" \
    make -C src lib-pace args="-b"

# Configure & build (CPU: MPI+OpenMP; shared libs; same packages as the GPU image except Kokkos)
RUN export CXXFLAGS="-D_GLIBCXX_USE_CXX11_ABI=0 ${CXXFLAGS}" \
    CPPFLAGS="-D_GLIBCXX_USE_CXX11_ABI=0 ${CPPFLAGS}" && \
    mkdir -p build && cd build && \
    cmake ../cmake \
    -D CMAKE_BUILD_TYPE=Release \
    -D CMAKE_INSTALL_PREFIX=/opt/lammps \
    -D BUILD_MPI=ON \
    -D BUILD_OMP=ON \
    -D BUILD_SHARED_LIBS=ON \
    -D CMAKE_C_STANDARD=11 \
    -D CMAKE_CXX_STANDARD=17 \
    -D PKG_ML-MACE=ON \
    -D PKG_ML-PACE=ON \
    -D PKG_MANYBODY=ON \
    -D PKG_BODY=ON \
    -D PKG_MOLECULE=ON \
    -D PKG_PLUMED=ON \
    -D DOWNLOAD_PLUMED=ON \
    -D PLUMED_MODE=static \
    -D PKG_ML-QUIP=ON \
    -D DOWNLOAD_QUIP=ON \
    -D PKG_OPT=ON \
    -D PKG_KSPACE=ON \
    -D PKG_RIGID=ON \
    -D PKG_EXTRA-FIX=ON \
    # Set MKL include directory before PyTorch config is loaded
    -D MKL_INCLUDE_DIR="/usr/include/mkl" \
    # Point CMake at Torch's CMake package files using PyTorch's official utility
    -D CMAKE_PREFIX_PATH="$(python -c 'import torch.utils; print(torch.utils.cmake_prefix_path)')" \
    && cmake --build . -j"$(nproc)" && cmake --install .

# ============================
# Stage 2: runtime
# ============================
FROM ubuntu:${UBUNTU} AS runtime
ENV DEBIAN_FRONTEND=noninteractive

# Build args for runtime stage
ARG MACE_VERSION=0.3.14

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv \
    openmpi-bin libopenmpi3 \
    libgsl27 libgslcblas0 \
    libblas3 liblapack3 \
    libfftw3-3 \
    libgfortran5 \
    intel-mkl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for runtime
RUN groupadd -r lammps && useradd -r -g lammps -d /home/lammps -m lammps

# Bring Python environment with Torch CPU
COPY --from=builder --chown=lammps:lammps /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"

# Install mace-torch in runtime stage - pinned version
RUN pip install --no-cache-dir mace-torch==${MACE_VERSION}

# Bring LAMMPS install (bin + libs)
COPY --from=builder --chown=lammps:lammps /opt/lammps /opt/lammps
ENV PATH="/opt/lammps/bin:${PATH}"
ENV LD_LIBRARY_PATH="/opt/lammps/lib:${LD_LIBRARY_PATH}"

# Register TORCH_LIB and MKL_LIB with the dynamic linker
# This avoids the need of manually setting them in LD_LIBRARY_PATH
ENV TORCH_LIB="/opt/venv/lib/python3.10/site-packages/torch/lib"
ENV MKL_LIB="/usr/lib/x86_64-linux-gnu"
RUN printf "%s\n" "$TORCH_LIB" "$MKL_LIB" > /etc/ld.so.conf.d/torch-mkl.conf && ldconfig

# Alternatively, at the "builder" stage, tell CMake to use RPATH:
# -DCMAKE_INSTALL_RPATH="$TORCH_LIB;$MKL_LIB" -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON

# Switch to non-root user
USER lammps
WORKDIR /home/lammps
CMD ["bash"]
