FROM centos:centos7

# metainformation
LABEL org.opencontainers.image.version = "1.0.0"
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
 && wget https://github.com/Kitware/CMake/releases/download/v3.27.0/cmake-3.27.0.tar.gz \
 && tar -zxf cmake-3.27.0.tar.gz && cd cmake-3.27.0 \
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

# Install Delphes
RUN cd /tmp \
 && wget http://cp3.irmp.ucl.ac.be/downloads/Delphes-3.5.0.tar.gz \
 && tar -zxf Delphes-3.5.0.tar.gz && mkdir Delphes_build && cd Delphes_build \
 && cmake ../Delphes-3.5.0 && make install

# Install LHAPDF6
RUN cd /tmp \
 && wget https://lhapdf.hepforge.org/downloads/?f=LHAPDF-6.3.0.tar.gz -O LHAPDF-6.3.0.tar.gz \
 && tar -zxf LHAPDF-6.3.0.tar.gz && cd LHAPDF-6.3.0 \
 && ./configure --prefix=/usr/local \
 && make && make install

# Install HepMC2
RUN cd /tmp \
 && wget http://hepmc.web.cern.ch/hepmc/releases/hepmc2.06.09.tgz \
 && tar -zxf hepmc2.06.09.tgz && cd hepmc2.06.09 \
 && ./configure --prefix=/usr/local --with-momentum=GEV --with-length=MM --build=aarch64-unknown-linux-gnu \
 && make && make check && make install

# Install Pythia8
RUN cd /tmp \
 && wget https://pythia.org/download/pythia83/pythia8306.tar \
 && tar -xf pythia8306.tar && cd pythia8306 \
 && ./configure --prefix=/usr/local --with-hepmc2=/usr/local --with-hepmc2-include=/usr/local/include --with-lhapdf6=/usr/local --with-lhapdf6-plugin=LHAPDF6.h \
 && make && make install

# Install Fastjet
RUN cd /tmp \
 && wget http://fastjet.fr/repo/fastjet-3.4.0.tar.gz \
 && tar -zxf fastjet-3.4.0.tar.gz \
 && cd fastjet-3.4.0 && ./configure --prefix=/usr/local \
 && make && make check && make install

RUN ln -fs /usr/bin/python2.7 /usr/bin/python \
 && ln -fs /usr/bin/pip2.7 /usr/bin/pip \
 && pip3 install six

# Install MadGraph5
RUN mkdir /app && cd /app \
 && wget https://launchpad.net/mg5amcnlo/3.0/3.5.x/+download/MG5aMC_LTS_v2.9.16.tar.gz \
 && tar -zxf MG5aMC_LTS_v2.9.16.tar.gz && cd MG5_aMC_v2_9_16 \
 && ln -fs /app/MG5_aMC_v2_9_16/bin/mg5_aMC /usr/local/bin/mg5 \
 && sed -i 's/# pythia8_path = .\/HEPTools\/pythia8/pythia8_path = \/usr\/local/' ./input/mg5_configuration.txt \
 && sed -i 's/# delphes_path = .\/Delphes/delphes_path = \/usr\/local/' ./input/mg5_configuration.txt \
 && sed -i 's/# lhapdf_py3 = lhapdf-config/lhapdf_py3 = \/usr\/local\/bin\/lhapdf-config/' ./input/mg5_configuration.txt \
 && sed -i 's/# fastjet = fastjet-config/fastjet = \/usr\/local\/bin\/fastjet-config/' ./input/mg5_configuration.txt \
 && cd /tmp && echo -e "import model loop_sm-no_b_mass\ninstall mg5amc_py8_interface\ngenerate p p > t t~ [QCD]\noutput mg5_test_run" > mg5_exec_card \
 && mg5 mg5_exec_card && cd /

RUN rm -rf /tmp/*

RUN yum install sudo -y \
 && sudo localedef -c -f UTF-8 -i en_US en_US.UTF-8

RUN useradd atreus \
 && usermod -aG wheel atreus \
 && echo "%wheel  ALL=(ALL)       NOPASSWD: ALL" | tee -a /etc/sudoers 

USER atreus

ENV HOME=/home/atreus
RUN chmod 777 /home/atreus \
 && ln -fs /mnt /home/atreus/data

WORKDIR /home/atreus

