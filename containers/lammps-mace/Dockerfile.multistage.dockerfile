# Multi-stage Dockerfile for LAMMPS + MACE with rebuilt OpenMPI
ARG BASE_TAG=25.01-py3

### Stage 1: Build ###
FROM nvcr.io/nvidia/pytorch:${BASE_TAG} AS builder

ENV DEBIAN_FRONTEND=noninteractive

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git cmake \
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

# Set MPI compilers before building LAMMPS
ENV CC=/opt/hpcx/ompi/bin/mpicc \
    CXX=/opt/hpcx/ompi/bin/mpicxx \
    MPI_HOME=/opt/hpcx/ompi \
    NVCC_WRAPPER_DEFAULT_COMPILER=/opt/hpcx/ompi/bin/mpicxx

# Clone and build LAMMPS
ARG LAMMPS_REPO=https://github.com/empa-scientific-it/lammps.git
ARG LAMMPS_BRANCH=mace-features
WORKDIR /opt
RUN git clone --depth 1 --branch ${LAMMPS_BRANCH} ${LAMMPS_REPO} lammps

WORKDIR /opt/lammps
RUN mkdir build-grace && cd build-grace && \
    cmake ../cmake \
    -D CMAKE_INSTALL_PREFIX=/opt/lammps \
    -D CMAKE_PREFIX_PATH="/usr/local/lib/python3.12/dist-packages/torch/share/cmake;/opt/hpcx/ompi" \
    -D CMAKE_CXX_STANDARD=17 \
    -D CMAKE_CXX_STANDARD_REQUIRED=ON \
    -D CMAKE_C_COMPILER=$CC \
    -D CMAKE_CXX_COMPILER=$CXX \
    -D CMAKE_CUDA_COMPILER=/opt/lammps/lib/kokkos/bin/nvcc_wrapper \
    -D MPI_CXX_SKIP_MPICXX=TRUE \
    -D MPI_CXX_ADDITIONAL_INCLUDE_DIRS="/opt/hpcx/ompi/include" \
    -D MPI_CXX_LIBRARIES="/opt/hpcx/ompi/lib/libmpi.so;/usr/lib/x86_64-linux-gnu/libdl.so" \
    -D BUILD_MPI=ON \
    -D BUILD_OMP=ON \
    -D BUILD_SHARED_LIBS=ON \
    -D PKG_KOKKOS=ON \
    -D Kokkos_ENABLE_SERIAL=ON \
    -D Kokkos_ENABLE_CUDA=ON \
    -D Kokkos_ENABLE_OPENMP=ON \
    -D Kokkos_ARCH_SKX=ON \
    -D Kokkos_ARCH_PASCAL61=ON \
    -D FFT_KOKKOS=CUFFT \
    -D Kokkos_ENABLE_DEPRECATION_WARNINGS=OFF \
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
    apt-get install -y --no-install-recommends python3-venv wget && \
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
