import os
import json
import subprocess

from glob import glob
from typing import Optional


def get_model(model_name: str, model_dict: Optional[str] = "/app/MG5_aMC_*/models"):
    r"""Download and install MG5 model defined in process file.

    Args:
        model_name (str): model name.
        model_dict (str, optional): MG5 path. (default: :obj:`str`='/app/MG5_aMC_v2_9_16/models')
    """
    model_dict = glob(model_dict)[0]

    with open("madlad/db/models_db.json", "r") as f:
        lookup_dict = json.load(f)

    main_model_name = model_name.split("-")[0]
    if os.path.exists(os.path.join(model_dict,main_model_name)) is not True:
        link = ""
        for key in list(lookup_dict.keys()):
            if main_model_name == key:
                link = lookup_dict[key]
                model_name = key
            if main_model_name == "MSSM_SLHA2" or main_model_name == "loop_sm" or main_model_name == "taudecay_UFO":
                return ""

        if link == "":
            raise ValueError("Model not found in the MadGraph database. If you think this is an error, please report to https://github.com/tzuhanchang/MadLAD.git.")

        download = subprocess.Popen(["sudo","wget","-P",model_dict+"/",link])
        download.wait()

        file_name = os.path.basename(link)
        if ".zip" in file_name:
            unzip = subprocess.Popen(["sudo","unzip",os.path.join(model_dict,file_name),"-d",model_dict])
        elif ".tar.gz" in file_name or ".tgz" in file_name :
            unzip = subprocess.Popen(["sudo","tar","-zxvf",os.path.join(model_dict,file_name),"--directory",model_dict])
        unzip.wait()

        testcard = open('/tmp/convert.dat','w')
        testcard.write("""convert model %s/%s
    """%(model_dict,model_name))
        testcard.close()
        convert = subprocess.Popen(["sudo", "/usr/local/bin/mg5", "/tmp/convert.dat"])
        convert.wait()
        cleanup = subprocess.Popen(["rm", "/tmp/convert.dat"])
        cleanup.wait()


def get_model_singularity(model_name: str, model_dict: str = "/app/MG5_aMC_v2_9_16/models") -> str:
    r"""Download and install MG5 model defined in process file to build singularity image.

    Args:
        model_name (str): model name.
        model_dict (str, optional): MG5 path. (default: :obj:`str`='/app/MG5_aMC_v2_9_16/models')
    """
    with open("madlad/db/models_db.json", "r") as f:
        lookup_dict = json.load(f)

    main_model_name = model_name.split("-")[0]
    link = ""
    for key in list(lookup_dict.keys()):
        if main_model_name == key:
            link = lookup_dict[key]
            model_name = key
        if main_model_name == "MSSM_SLHA2" or main_model_name == "loop_sm" or main_model_name == "taudecay_UFO":
            return ""

    if link == "":
        raise ValueError("Model not found in the MadGraph database. If you think this is an error, please report to https://github.com/tzuhanchang/MadLAD.git.")
    
    file_name = os.path.basename(link)
    if ".zip" in file_name:
        extract_command = "unzip"
    elif ".tar.gz" in file_name or ".tgz" in file_name :
        extract_command = "tar -zxvf"

    to_write = """
    cd %s
    wget %s
    %s %s
    cd /tmp
    echo -e "convert model %s/%s" > convert.dat
    /usr/local/bin/mg5 convert.dat
    rm convert.dat
    """%(model_dict, link, extract_command, file_name, model_dict, model_name)

    return to_write