FROM centos:centos7

# metainformation
LABEL org.opencontainers.image.version = "3.0.0"
LABEL org.opencontainers.image.authors = "Zihan Zhang"
LABEL org.opencontainers.image.source = "https://zhangzi.web.cern.ch"
LABEL org.opencontainers.image.base.name="docker.io/library/centos:centos7"

RUN yum update -y && yum groupinstall "Development Tools" -y \
 && yum install -y zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel \
    readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel libXpm-devel \
    libXext-devel wget which ghostscript

RUN yum install -y epel-release redhat-lsb-core gcc-gfortran pcre-devel \
    mesa-libGL-devel mesa-libGLU-devel glew-devel ftgl-devel mysql-devel \
    fftw-devel cfitsio-devel graphviz-devel libuuid-devel \
    avahi-compat-libdns_sd-devel openldap-devel \
    libxml2-devel gsl-devel readline-devel qt5-qtwebengine-devel \
    R-devel R-Rcpp-devel R-RInside-devel

RUN cd /tmp \
 && wget https://github.com/Kitware/CMake/releases/download/v3.28.3/cmake-3.28.3.tar.gz \
 && tar -zxf cmake-3.28.3.tar.gz && cd cmake-3.28.3 \
 && ./bootstrap && make && make install 

# Install ROOT
RUN cd /tmp \
 && wget https://root.cern/download/root_v6.24.08.source.tar.gz \
 && tar -zxf root_v6.24.08.source.tar.gz && mkdir root_build && cd root_build \
 && cmake ../root-6.24.08 && cmake --build . -- install

# Install Python=3.10
RUN cd /tmp \
 && wget https://www.python.org/ftp/python/3.9.17/Python-3.9.17.tgz \
 && tar -zxf Python-3.9.17.tgz && cd Python-3.9.17 \
 && ./configure --enable-optimizations && make altinstall \
 && ln -fs /usr/local/bin/python3.9 /usr/bin/python3 \
 && ln -fs /usr/local/bin/pip3.9 /usr/bin/pip3 \
 && ln -fs /usr/local/bin/python3.9 /usr/bin/python \
 && ln -fs /usr/local/bin/pip3.9 /usr/bin/pip

# Install HepMC2
RUN cd /tmp \
 && wget http://hepmc.web.cern.ch/hepmc/releases/hepmc2.06.09.tgz \
 && tar -zxf hepmc2.06.09.tgz && cd hepmc2.06.09 \
 && ./configure --prefix=/usr/local --with-momentum=GEV --with-length=MM --build=aarch64-unknown-linux-gnu \
 && make && make check && make install

RUN pip install --upgrade setuptools \
 && pip install yaml \
 && pip install six \
 && ln -fs /usr/bin/python2.7 /usr/bin/python \
 && ln -fs /usr/bin/pip2.7 /usr/bin/pip

RUN rm -rf /tmp/*

RUN yum install sudo -y \
 && sudo localedef -c -f UTF-8 -i en_US en_US.UTF-8

RUN useradd atreus \
 && usermod -aG wheel atreus \
 && echo "%wheel  ALL=(ALL)       NOPASSWD: ALL" | tee -a /etc/sudoers 

RUN ln -fs /usr/local/bin/python3.9 /usr/bin/python

USER atreus

ENV HOME=/home/atreus
RUN chmod 777 /home/atreus \
 && ln -fs /mnt /home/atreus/data

WORKDIR /home/atreus