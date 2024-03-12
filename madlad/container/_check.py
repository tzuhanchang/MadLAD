import os

def is_running_in_docker_container():
    try:
        with open('/proc/1/cgroup', 'r') as f:
            for line in f:
                if 'docker' in line or 'lxc' in line:
                    return True
        return False
    except FileNotFoundError:
        return False

def is_running_in_singularity_container():
    try:
        if os.environ['SINGULARITY_NAME'] != "":
            return True
        else:
            return False
    except KeyError:
        return False