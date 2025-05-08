import os
import json

from typing import Optional, List


def get_model(model_names: List|str, model_dict: str = "/app/MG5_aMC/models", build_method: Optional[str] = "Docker") -> str:
    r"""Download and install MG5 model defined in process file to build singularity image.

    Args:
        model_name (str): model name.
        model_dict (str, optional): MG5 path. (default: :obj:`str`='/app/MG5_aMC/models')
    """
    build_method = build_method.lower()
    assert build_method == "docker" or build_method == "singularity"

    try:
        tmp = model_names[0]
        model_names = model_names
    except TypeError:
        model_names = [model_names]

    with open("madlad/db/models_db.json", "r") as f:
        lookup_dict = json.load(f)

    main_model_names = [model_name.split("-")[0] for model_name in model_names]
    to_write = []
    for key in list(lookup_dict.keys()):
        for main_model_name in main_model_names:
            if main_model_name == key and (main_model_name != "MSSM_SLHA2" or main_model_name != "loop_sm" or main_model_name != "taudecay_UFO"):
                
                file_name = os.path.basename(lookup_dict[key])
                if ".zip" in file_name:
                    extract_command = "unzip"
                elif ".tar.gz" in file_name or ".tgz" in file_name :
                    extract_command = "tar -zxvf"

                if build_method == "docker":
                    to_write += [
                        "cd %s"%(model_dict),
                        "wget %s"%(lookup_dict[key]),
                        "%s %s"%(extract_command, file_name),
                        "cd /tmp",
                        "echo -e \"convert model %s/%s\" > convert.dat"%(model_dict, main_model_name),
                        "/usr/local/bin/mg5 convert.dat",
                        "rm convert.dat"
                    ]
                elif build_method == "singularity":
                    to_write += [
                        "mkdir -p /home/atreus/singularity-build/models",
                        "cd /home/atreus/singularity-build/models",
                        "wget %s"%(lookup_dict[key]),
                        "%s %s"%(extract_command, file_name),
                        "mv * %s"%(model_dict),
                        "echo -e \"convert model %s/%s\" > convert.dat"%(model_dict, main_model_name),
                        "/usr/local/bin/mg5 convert.dat",
                        "rm convert.dat"
                    ]

    if to_write == []:
        raise ValueError("Model not found in the MadGraph database. If you think this is an error, please report to https://github.com/tzuhanchang/MadLAD.git.")

    write_out = ""
    if build_method == "docker":
        for idx, line in enumerate(to_write):
            if idx == 0:
                write_out += "RUN %s \ \n"%(line)
            elif idx == len(to_write) - 1:
                write_out += " && %s \n"%(line)
            else:
                write_out += " && %s \ \n"%(line)
    
    elif build_method == "singularity":
        for idx, line in enumerate(to_write):
                write_out += "    %s \n"%(line)

    return write_out


def get_pdfset(pdf_ids: List|int, pdfsets_dict: Optional[str] = "/usr/local/share/LHAPDF", build_method: Optional[str] = "Docker") -> str:
    r"""Download and install PDF set defined in process file to build image.

    Args:
        pdf_id (List|int): LHAPDF ID.
        pdfsets_dict (str, optional): LHAPDF path. (default: :obj:`str`='/usr/local/share/LHAPDF')
    """
    build_method = build_method.lower()
    assert build_method == "docker" or build_method == "singularity"

    try:
        tmp = pdf_ids[0]
        is_int = False
    except TypeError:
        is_int = True

    with open("madlad/db/pdfs_db.json", "r") as f:
        all_pdfs = json.load(f)
        if is_int:
            try:
                if build_method == "docker":
                    pdf_links = "wget http://lhapdfsets.web.cern.ch/lhapdfsets/current/%s.tar.gz && tar -zxf %s.tar.gz"%(all_pdfs[str(pdf_ids)],all_pdfs[str(pdf_ids)])
                elif build_method == "singularity":
                    pdf_links = "wget http://lhapdfsets.web.cern.ch/lhapdfsets/current/%s.tar.gz && tar -zxf %s.tar.gz"%(all_pdfs[str(pdf_ids)],all_pdfs[str(pdf_ids)])
            except KeyError:
                raise ValueError("PDF ID not found in the LHAPDF database. If you think this is an error, please report to https://github.com/tzuhanchang/MadLAD.git.")
        else:
            try:
                if build_method == "docker":
                    pdf_links = [ "wget http://lhapdfsets.web.cern.ch/lhapdfsets/current/%s.tar.gz && tar -zxf %s.tar.gz"%(all_pdfs[str(pdf_id)],all_pdfs[str(pdf_id)]) for pdf_id in pdf_ids ]
                elif build_method == "singularity":
                    pdf_links = [ "wget http://lhapdfsets.web.cern.ch/lhapdfsets/current/%s.tar.gz && tar -zxf %s.tar.gz"%(all_pdfs[str(pdf_id)],all_pdfs[str(pdf_id)]) for pdf_id in pdf_ids ]
            except KeyError:
                raise ValueError("PDF ID not found in the LHAPDF database. If you think this is an error, please report to https://github.com/tzuhanchang/MadLAD.git.")

    write_out = ""
    if build_method == "docker":
        to_write = ["cd %s"%(pdfsets_dict)].append(pdf_links) if is_int else ["cd %s"%(pdfsets_dict)]+pdf_links

        for idx, line in enumerate(to_write):
            if idx == 0:
                write_out += "RUN %s \ \n"%(line)
            elif idx == len(to_write) - 1:
                write_out += " && %s \n"%(line)
            else:
                write_out += " && %s \ \n"%(line)
    
    elif build_method == "singularity":
        to_write = [
            "",
            "mkdir -p /home/atreus/singularity-build/pdfs",
            "cd /home/atreus/singularity-build/pdfs",
            pdf_links,
            "mv * %s"%(pdfsets_dict)
        ] if is_int else [
            "",
            "mkdir -p /home/atreus/singularity-build/pdfs",
            "cd /home/atreus/singularity-build/pdfs",
        ]+pdf_links+["mv * %s"%(pdfsets_dict)]

        for idx, line in enumerate(to_write):
                write_out += "    %s \n"%(line)

    return write_out