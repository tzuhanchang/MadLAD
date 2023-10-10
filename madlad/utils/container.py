def is_running_in_docker_container():
    try:
        with open('/proc/1/cgroup', 'r') as f:
            for line in f:
                if 'docker' in line or 'lxc' in line:
                    return True
            confirmation = input("MadLAD is designed to be used inside a containerised environment. You are NOT recommended to continue if you are not in one.\nAre you sure you want to continue? (y/n): ")
            if confirmation.lower() == 'y':
                return True
            else:
                raise RuntimeError("User chooses not to continue.")
    except FileNotFoundError:
        confirmation = input("MadLAD is designed to be used inside a containerised environment. You are NOT recommended to continue if you are not in one.\nAre you sure you want to continue? (y/n): ")
        if confirmation.lower() == 'y':
            return True
        else:
            raise RuntimeError("User chooses not to continue.")