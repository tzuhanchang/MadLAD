from typing import Optional, Tuple


def fastjet_build(version: str) -> Tuple[str,str]:
    version_number = version.split('.')
    if len(version_number) != 3:
        raise ValueError("Fastjet version number provided not found. Please check list of available versions at 'http://fastjet.fr/all-releases.html'.")

    download_link = f"http://fastjet.fr/repo/fastjet-{version}.tar.gz"

    docker_command = f"""RUN cd /tmp \\
 && wget {download_link} \\
 && tar -zxf fastjet-{version}.tar.gz \\
 && cd fastjet-{version} && ./configure --prefix=/usr/local \\
 && sudo make && sudo make check && sudo make install

"""
    
    singularity_command = f"""    cd /tmp
    wget {download_link}
    tar -zxf fastjet-{version}.tar.gz
    cd fastjet-3.4.0 && ./configure --prefix=/usr/local
    sudo make && sudo make check && sudo make install

"""
    return docker_command, singularity_command


def delphes_build(version: str) -> Tuple[str,str]:
    version_number = version.split('.')
    if len(version_number) != 3:
        raise ValueError("Delphes version number provided not found. Please check list of available versions at 'https://cp3.irmp.ucl.ac.be/projects/delphes/wiki/Releases'.")

    download_link = f"http://cp3.irmp.ucl.ac.be/downloads/Delphes-{version}.tar.gz"

    docker_command = f"""RUN cd /tmp \\
 && wget {download_link} \\
 && tar -zxf Delphes-{version}.tar.gz && mkdir Delphes_build && cd Delphes_build \\
 && cmake ../Delphes-{version} && sudo make install

"""
    
    singularity_command = f"""    cd /tmp
    wget {download_link}
    tar -zxf Delphes-{version}.tar.gz && mkdir Delphes_build && cd Delphes_build
    cmake ../Delphes-{version} && sudo make install

"""
    return docker_command, singularity_command

def lhapdf_build(version: str) -> Tuple[str,str]:
    version_number = version.split('.')
    if len(version_number) != 3:
        raise ValueError("LHAPDF version number provided not found. Please check list of available versions at 'https://lhapdf.hepforge.org/downloads'.")

    download_link = f"https://lhapdf.hepforge.org/downloads/?f=LHAPDF-{version}.tar.gz"

    docker_command = f"""RUN cd /tmp \\
 && wget {download_link} -O LHAPDF-{version}.tar.gz \\
 && tar -zxf LHAPDF-{version}.tar.gz && cd LHAPDF-{version} \\
 && ./configure LIBS="-L/usr/local/lib/python3.9" --prefix=/usr/local \\
 && sudo make && sudo make install

"""
    
    singularity_command = f"""    cd /tmp
    wget {download_link} -O LHAPDF-{version}.tar.gz
    tar -zxf LHAPDF-{version}.tar.gz && cd LHAPDF-{version}
    ./configure LIBS="-L/usr/local/lib/python3.9" --prefix=/usr/local
    sudo make && sudo make install

"""
    return docker_command, singularity_command


def pythia8_build(version: str) -> Tuple[str,str]:
    version_number = version.split('.')
    if len(version_number) != 2:
        raise ValueError("PYTHIA 8 version number provided not found. Please check list of available versions at 'https://pythia.org/releases'.")
    
    release = version_number[-1]
    series = release[0]

    download_link = f"https://pythia.org/download/pythia8{series}/pythia8{release}.tar"

    docker_command = f"""RUN cd /tmp \\
 && wget {download_link} \\
 && tar -xf pythia8{release}.tar && cd pythia8{release} \\
 && ./configure --prefix=/usr/local --with-hepmc2=/usr/local --with-hepmc2-include=/usr/local/include --with-lhapdf6=/usr/local --with-lhapdf6-plugin=LHAPDF6.h \\
 && sudo make && sudo make install

"""
    singularity_command = f"""    cd /tmp
    wget {download_link}
    tar -xf pythia8{release}.tar && cd pythia8{release}
    ./configure --prefix=/usr/local --with-hepmc2=/usr/local --with-hepmc2-include=/usr/local/include --with-lhapdf6=/usr/local --with-lhapdf6-plugin=LHAPDF6.h
    sudo make && sudo make install

"""
    return docker_command, singularity_command
    

def mg5_build(version: Optional[str] = None, external: Optional[str] = None) -> Tuple[str,str]:
    if version is not None:
        version_number = version.split('.')
        if len(version_number) < 3:
            raise ValueError("MadGraph5 version number provided not found. Please check list of available versions at 'https://launchpad.net/mg5amcnlo/+download'.")

        series = f"{version_number[0]}.0"
        release = f"{version_number[0]}.{version_number[1]}.x"
        download_link = f"https://launchpad.net/mg5amcnlo/{series}/{release}/+download/MG5_aMC_v{version}.tar.gz"
        if release[0] == "2":
            download_link = f"https://launchpad.net/mg5amcnlo/lts/{release}/+download/MG5_aMC_v{version}.tar.gz"
        file_name = download_link.split("/")[-1]

        docker_command = f"""RUN sudo mkdir /app && cd /app && sudo mkdir MG5_aMC \\
 && sudo wget {download_link} \\
 && sudo tar -zxf {file_name} -C MG5_aMC --strip-components 1 && cd MG5_aMC \\
 && sudo ln -fs /app/MG5_aMC/bin/mg5_aMC /usr/local/bin/mg5 \\
 && sudo sed -i 's/# pythia8_path = .\/HEPTools\/pythia8/pythia8_path = \/usr\/local/' ./input/mg5_configuration.txt \\
 && sudo sed -i 's/# delphes_path = .\/Delphes/delphes_path = \/usr\/local/' ./input/mg5_configuration.txt \\
 && sudo sed -i 's/# lhapdf_py3 = lhapdf-config/lhapdf_py3 = \/usr\/local\/bin\/lhapdf-config/' ./input/mg5_configuration.txt \\
 && sudo sed -i 's/# fastjet = fastjet-config/fastjet = \/usr\/local\/bin\/fastjet-config/' ./input/mg5_configuration.txt \\
 && cd /tmp && echo -e "import model loop_sm-no_b_mass\\ninstall mg5amc_py8_interface\\ngenerate p p > t t~ [QCD]\\noutput mg5_test_run" > mg5_exec_card \\
 && sudo /usr/local/bin/mg5 mg5_exec_card && cd /

"""
        singularity_command = f"""    sudo mkdir /app && cd /app && sudo mkdir MG5_aMC
    sudo wget {download_link}
    sudo tar -zxf {file_name} -C MG5_aMC --strip-components 1 && cd MG5_aMC
    sudo ln -fs /app/MG5_aMC/bin/mg5_aMC /usr/local/bin/mg5
    sudo sed -i 's/# pythia8_path = .\/HEPTools\/pythia8/pythia8_path = \/usr\/local/' ./input/mg5_configuration.txt
    sudo sed -i 's/# delphes_path = .\/Delphes/delphes_path = \/usr\/local/' ./input/mg5_configuration.txt
    sudo sed -i 's/# lhapdf_py3 = lhapdf-config/lhapdf_py3 = \/usr\/local\/bin\/lhapdf-config/' ./input/mg5_configuration.txt
    sudo sed -i 's/# fastjet = fastjet-config/fastjet = \/usr\/local\/bin\/fastjet-config/' ./input/mg5_configuration.txt
    cd /tmp && echo -e "import model loop_sm-no_b_mass\\ninstall mg5amc_py8_interface\\ngenerate p p > t t~ [QCD]\\noutput mg5_test_run" > mg5_exec_card
    sudo /usr/local/bin/mg5 mg5_exec_card && cd /

"""
    
    if external is not None:
        docker_command = f"""RUN sudo mkdir -p /app/MG5_aMC
COPY {external} /app/MG5_aMC
RUN cd /app/MG5_aMC \\
 && sudo ln -fs /app/MG5_aMC/bin/mg5_aMC /usr/local/bin/mg5 \\
 && sudo sed -i 's/# pythia8_path = .\/HEPTools\/pythia8/pythia8_path = \/usr\/local/' ./input/mg5_configuration.txt \\
 && sudo sed -i 's/# delphes_path = .\/Delphes/delphes_path = \/usr\/local/' ./input/mg5_configuration.txt \\
 && sudo sed -i 's/# lhapdf_py3 = lhapdf-config/lhapdf_py3 = \/usr\/local\/bin\/lhapdf-config/' ./input/mg5_configuration.txt \\
 && sudo sed -i 's/# fastjet = fastjet-config/fastjet = \/usr\/local\/bin\/fastjet-config/' ./input/mg5_configuration.txt \\
 && cd /tmp && echo -e "import model loop_sm-no_b_mass\\ninstall mg5amc_py8_interface\\ngenerate p p > t t~ [QCD]\\noutput mg5_test_run" > mg5_exec_card \\
 && sudo /usr/local/bin/mg5 mg5_exec_card && cd /

"""
        singularity_command = f"""    sudo mkdir /app && sudo mv /tmp/MG5_aMC /app/ && cd /app/MG5_aMC
    sudo ln -fs /app/MG5_aMC/bin/mg5_aMC /usr/local/bin/mg5
    sudo sed -i 's/# pythia8_path = .\/HEPTools\/pythia8/pythia8_path = \/usr\/local/' ./input/mg5_configuration.txt
    sudo sed -i 's/# delphes_path = .\/Delphes/delphes_path = \/usr\/local/' ./input/mg5_configuration.txt
    sudo sed -i 's/# lhapdf_py3 = lhapdf-config/lhapdf_py3 = \/usr\/local\/bin\/lhapdf-config/' ./input/mg5_configuration.txt
    sudo sed -i 's/# fastjet = fastjet-config/fastjet = \/usr\/local\/bin\/fastjet-config/' ./input/mg5_configuration.txt
    cd /tmp && echo -e "import model loop_sm-no_b_mass\\ninstall mg5amc_py8_interface\\ngenerate p p > t t~ [QCD]\\noutput mg5_test_run" > mg5_exec_card
    sudo /usr/local/bin/mg5 mg5_exec_card && cd /

"""
    
    if version is None and external is None:
        raise ValueError("Please provide either MadGraph version you want to install or the MadGraph directory you want to use with the container.")

    return docker_command, singularity_command
