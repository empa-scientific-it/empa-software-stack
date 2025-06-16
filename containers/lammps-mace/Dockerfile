# Multi-stage Dockerfile for LAMMPS + MACE with rebuilt OpenMPI
ARG BASE_TAG=25.01-py3

### Stage 1: Build ###
FROM nvcr.io/nvidia/pytorch:${BASE_TAG} AS builder

ENV DEBIAN_FRONTEND=noninteractive

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    cmake \
    build-essential \
    python3-venv \
    automake \
    autoconf \
    wget \
    libgsl-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Reinstall OpenMPI
ARG OMPI_PATH=/opt/hpcx/ompi
ARG OMPI_VER=4.1.7
RUN rm -rf ${OMPI_PATH} && \
    wget -q https://download.open-mpi.org/release/open-mpi/v${OMPI_VER%.*}/openmpi-${OMPI_VER}.tar.gz && \
    tar xf openmpi-${OMPI_VER}.tar.gz && \
    cd openmpi-${OMPI_VER} && \
    ./configure --prefix=${OMPI_PATH} \
    --with-libfabric=/opt/amazon/efa/ \
    --with-cuda=/usr/local/cuda \
    --with-cuda-libdir=/usr/local/cuda/lib64/stubs && \
    make -j$(nproc) && make install && ldconfig && \
    cd .. && rm -rf openmpi-${OMPI_VER}.tar.gz openmpi-${OMPI_VER}

# Clone and build LAMMPS
ARG LAMMPS_REPO=https://github.com/empa-scientific-it/lammps.git
ARG LAMMPS_BRANCH=mace-features
WORKDIR /opt
RUN git clone --depth 1 --branch ${LAMMPS_BRANCH} ${LAMMPS_REPO} lammps
WORKDIR /opt/lammps

# Set host compilers & CUDA/MPI roots
ENV CC=/usr/bin/gcc \
    CXX=/usr/bin/g++ \
    MPICC=/opt/hpcx/ompi/bin/mpicc \
    MPICXX=/opt/hpcx/ompi/bin/mpicxx \
    CUDA_HOME=/usr/local/cuda \
    CUDA_LIB_PATH=/usr/local/cuda-12.8/compat/lib.real \
    CMAKE_CUDA_COMPILER=/opt/lammps/lib/kokkos/bin/nvcc_wrapper

# Prepend the real CUDA libs for both configure and runtime
ENV LD_LIBRARY_PATH=${CUDA_LIB_PATH}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}

# Apply patch to CMakeLists.txt
COPY diag_suppress.patch .
RUN patch -p0 < diag_suppress.patch

# Build LAMMPS with Kokkos support
RUN mkdir build-grace && cd build-grace && \
    cmake \
    -C packages.cmake \
    -C kokkos-skx-pascal61.cmake \
    # -C kokkos-grace-hopper.cmake \
    ../cmake \
    -D CMAKE_INSTALL_PREFIX=/opt/lammps \
    -D CMAKE_PREFIX_PATH="${MPI_HOME};/usr/local/lib/python3.12/dist-packages/torch/share/cmake" \
    -D CMAKE_CXX_STANDARD=17 \
    -D CMAKE_CXX_STANDARD_REQUIRED=ON \
    -D CMAKE_C_COMPILER=$CC \
    -D CMAKE_CXX_COMPILER=$CXX \
    -D CMAKE_CUDA_TOOLKIT_ROOT_DIR=${CUDA_HOME} \
    -D CUDAToolkit_ROOT=${CUDA_HOME} \
    -D CMAKE_CUDA_TOOLKIT_INCLUDE_DIRECTORIES=${CUDA_HOME}/include \
    -D CMAKE_CUDA_IMPLICIT_LINK_DIRECTORIES=${CUDA_HOME}/lib64 \
    -D BUILD_MPI=ON \
    -D BUILD_OMP=ON \
    -D BUILD_SHARED_LIBS=ON \
    -D PKG_ML-MACE=ON \
    -D PKG_MANYBODY=ON \
    -D PKG_BODY=ON \
    -D PKG_MOLECULE=ON \
    -D PKG_ML-PACE=ON \
    -D PKG_PLUMED=ON \
    -D DOWNLOAD_PLUMED=ON \
    -D PLUMED_MODE=static \
    -D PKG_ML-QUIP=ON \
    -D DOWNLOAD_QUIP=ON \
    -D PKG_OPT=ON \
    -D PKG_KSPACE=ON \
    -D PKG_RIGID=ON \
    -D PKG_EXTRA-FIX=ON \
    -D GSL_INCLUDE_DIR=/usr/include \
    -D GSL_LIBRARY=/usr/lib/x86_64-linux-gnu/libgsl.so && \
    make -j"$(nproc)" && \
    make install && \
    cd ..

### Stage 2: Runtime ###
FROM nvcr.io/nvidia/pytorch:${BASE_TAG} AS runtime

ENV DEBIAN_FRONTEND=noninteractive

# Install minimal runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-venv \
    wget \
    libgsl27 libgslcblas0 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python runtime packages
RUN pip install --upgrade pip && \
    pip install mace-torch

# Copy OpenMPI and LAMMPS from builder
COPY --from=builder /opt/hpcx/ompi /opt/hpcx/ompi
COPY --from=builder /opt/lammps /opt/lammps

# Set runtime environment
ENV PATH="/opt/hpcx/ompi/bin:/opt/lammps/bin:${PATH}"
ENV LD_LIBRARY_PATH="/opt/hpcx/ompi/lib:${LD_LIBRARY_PATH}"

# Default to interactive shell
CMD ["bash"]
