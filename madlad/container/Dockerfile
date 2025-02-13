FROM ubuntu:focal

# metainformation
LABEL org.opencontainers.image.version="4.0.0"
LABEL org.opencontainers.image.authors="Zihan Zhang"
LABEL org.opencontainers.image.source="https://zhangzi.web.cern.ch"

ARG DEBIAN_FRONTEND=noninteractive
ENV LD_LIBRARY_PATH=/usr/local/lib:/usr/lib:/lib

RUN apt update -y && apt upgrade -y

RUN apt install -y binutils cmake dpkg-dev g++ gcc libssl-dev git libx11-dev \
    libxext-dev libxft-dev libxpm-dev python3 libtbb-dev libgif-dev

RUN apt install -y gfortran libpcre3-dev \
    libglu1-mesa-dev libglew-dev libftgl-dev \
    libfftw3-dev libcfitsio-dev libgraphviz-dev \
    libavahi-compat-libdnssd-dev libldap2-dev \
    python3-dev python3-numpy libxml2-dev libkrb5-dev \
    libgsl-dev qtwebengine5-dev nlohmann-json3-dev libmysqlclient-dev \
    libgl2ps-dev \
    liblzma-dev libxxhash-dev liblz4-dev libzstd-dev

RUN apt install -y nano vim rsync wget unzip ghostscript bc \
    python3-pip python3-six

# Link Python
RUN ln -fs /usr/bin/python3 /usr/bin/python

# Install ROOT
RUN cd /tmp \
 && git clone --branch latest-stable --depth=1 https://github.com/root-project/root.git root_src \
 && mkdir root_build && cd root_build \
 && cmake ../root_src && cmake --build . -- install

# Install HepMC2
RUN cd /tmp \
 && wget https://hepmc.web.cern.ch/hepmc/releases/HepMC-2.06.11.tar.gz \
 && tar -zxf HepMC-2.06.11.tar.gz \
 && mkdir HepMC_build && cd HepMC_build \
 && cmake -DCMAKE_INSTALL_PREFIX=/usr/local -Dmomentum=GEV -Dlength=MM ../HepMC-2.06.11 \
 && make && make test && make install

# Clean up
RUN rm -rf /tmp/*

USER root
