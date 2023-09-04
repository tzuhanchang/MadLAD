import os
import subprocess
from madlad.utils import is_running_in_docker_container


def get_model(model_name: str, model_dict: str = "/app/MG5_aMC_v2_9_16/models"):
    if is_running_in_docker_container():
        pass
    else:
        raise ValueError("`get_model` is not designed to run outside a container!")
    
    get_list = subprocess.Popen(["wget","http://madgraph.phys.ucl.ac.be/models_db.dat"])
    get_list.wait()

    lookup_dict = {}
    with open('models_db.dat', 'r') as file:
        for line in file:
            columns = line.strip().split()
            if len(columns) == 2:
                name, content = columns[0], columns[1]
                lookup_dict[name] = content

    link = ""
    for key in list(lookup_dict.keys()):
        if model_name in key or key in model_name:
            link = lookup_dict[key]
            fname = key
        if model_name == key:
            link = lookup_dict[key]
            fname = key

    if link == "":
        raise ValueError("Model not found in the database.")

    delete_list = subprocess.Popen(["rm","models_db.dat"])
    delete_list.wait()

    if os.path.exists(model_dict+"/{}".format(fname)) != True:
        download = subprocess.Popen(["sudo","wget","-P",model_dict+"/",link])
        download.wait()
        unzip    = subprocess.Popen(["sudo","unzip",model_dict+"/{}.zip".format(fname),"-d",model_dict])
        unzip.wait()
        testcard = open('tmp.dat','w')
        testcard.write("""convert model %s/%s
"""%(model_dict,fname))
        testcard.close()
        convert = subprocess.Popen(["sudo", "/usr/local/bin/mg5", "tmp.dat"])
        convert.wait()
        cleanup = subprocess.Popen(["rm", "tmp.dat"])
        cleanup.wait()