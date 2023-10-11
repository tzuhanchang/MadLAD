import os
import json
import subprocess

from typing import Optional


def get_pdfset(pdf_id: int, pdfsets_dict: Optional[str] = "/usr/local/share/LHAPDF"):
    r"""Download and install PDF set defined in process file.

    Args:
        pdf_id (int): LHAPDF ID.
        pdfsets_dict (str, optional): LHAPDF path. (default: :obj:`str`='/usr/local/share/LHAPDF')
    """
    with open("madlad/db/pdfs_db.json", "r") as f:
        try:
            pdf_name = json.load(f)[str(pdf_id)]
        except KeyError:
            raise ValueError("PDF ID not found in the LHAPDF database. If you think this is an error, please report to https://github.com/tzuhanchang/MadLAD.git.")

    if os.path.exists(os.path.join(pdfsets_dict,pdf_name)) is not True:
        download = subprocess.Popen(["sudo","wget","-P",pdfsets_dict+"/","http://lhapdfsets.web.cern.ch/lhapdfsets/current/%s.tar.gz"%(pdf_name)])
        download.wait()
        unzip    = subprocess.Popen(["sudo","tar","-zxf",pdfsets_dict+"/%s.tar.gz"%(pdf_name),"-C",pdfsets_dict+"/"])
        unzip.wait()


def get_pdfset_singularity(pdf_id: int, pdfsets_dict: Optional[str] = "/usr/local/share/LHAPDF") -> str:
    r"""Download and install PDF set defined in process file to build singularity image.

    Args:
        pdf_id (int): LHAPDF ID.
        pdfsets_dict (str, optional): LHAPDF path. (default: :obj:`str`='/usr/local/share/LHAPDF')
    """
    with open("madlad/db/pdfs_db.json", "r") as f:
        try:
            pdf_name = json.load(f)[str(pdf_id)]
        except KeyError:
            raise ValueError("PDF ID not found in the LHAPDF database. If you think this is an error, please report to https://github.com/tzuhanchang/MadLAD.git.")

    to_write = """
    cd %s
    wget http://lhapdfsets.web.cern.ch/lhapdfsets/current/%s.tar.gz && tar -zxf %s.tar.gz"""%(pdfsets_dict, pdf_name, pdf_name)

    return to_write