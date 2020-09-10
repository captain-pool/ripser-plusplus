FROM nvidia/cuda:10.2-cudnn8-devel-ubuntu18.04
MAINTAINER Adrish
ENV DEBIAN_FRONTEND=noninteractive
ADD ./ /rpp
RUN apt-get -y update \
    && apt-get -y install freeglut3-dev \
                       libglew-dev   \
                       wget          \
                       curl          \
                       python3       \
                       python3-pip   \
                       python3-tk    \
                       build-essential \
                       git
ENV CMAKE_DOWNLINK=https://github.com/Kitware/CMake/releases/download/v3.18.2/cmake-3.18.2-Linux-x86_64.sh
RUN apt remove --purge cmake &&\
    wget ${CMAKE_DOWNLINK} -O cmake.sh &&\
    bash cmake.sh --skip-license --prefix=/usr/local --exclude-subdir
RUN mkdir -p /rpp/build
WORKDIR /root/
ENV CONDA_URL https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
#ENV CONDA_URL https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh
RUN wget ${CONDA_URL} -O conda3.sh &&\
    bash conda3.sh -b -p /root/conda3 &&\
    rm -f conda3.sh
RUN echo "source /root/conda3/bin/activate" >> /root/.bashrc &&\
    bash -c "source /root/conda3/bin/activate; conda update -n base -c defaults conda; conda create -n topo python=3.6; conda activate topo; conda install -y gudhi -c conda-forge"
RUN bash -c "source /root/conda3/bin/activate; conda activate topo; conda install -y pytorch torchvision cudatoolkit=10.1 -c pytorch;"
RUN bash -c "source /root/conda3/bin/activate; conda activate topo; conda install -y -c conda-forge matplotlib "
RUN bash -c "source /root/conda3/bin/activate; conda activate topo; pip3 install numpy open3d"

WORKDIR /rpp/build
ARG NUM_FORKS=4
RUN cmake .. && make -j ${NUM_FORKS}
ENV RIPSERPP_BIN_PATH=/rpp/build/ripser++
WORKDIR /tmp
