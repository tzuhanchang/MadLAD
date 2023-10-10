import os
import re
import subprocess


def get_model(model_name: str, model_dict: str = "/app/MG5_aMC_v2_9_16/models"):
    match = re.search(r"^(.*?)-", model_name)

    if match:
        model_name = match.group(1)

    if os.path.exists(os.path.join(model_dict,model_name)) is not True:
        if os.path.isfile("/tmp/models_db.dat") is False:
            get_list = subprocess.Popen(["wget","-P","/tmp/","http://madgraph.phys.ucl.ac.be/models_db.dat"])
            get_list.wait()

        lookup_dict = {}
        with open('/tmp/models_db.dat', 'r') as file:
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

        download = subprocess.Popen(["sudo","wget","-P",model_dict+"/",link])
        download.wait()
        unzip    = subprocess.Popen(["sudo","unzip",model_dict+"/{}.zip".format(fname),"-d",model_dict])
        unzip.wait()

        testcard = open('/tmp/convert.dat','w')
        testcard.write("""convert model %s/%s
"""%(model_dict,fname))
        testcard.close()
        convert = subprocess.Popen(["sudo", "/usr/local/bin/mg5", "/tmp/convert.dat"])
        convert.wait()
        cleanup = subprocess.Popen(["rm", "/tmp/convert.dat"])
        cleanup.wait()