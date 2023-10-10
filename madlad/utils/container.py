def is_running_in_docker_container():
    try:
        with open('/proc/1/cgroup', 'r') as f:
            for line in f:
                if 'docker' in line or 'lxc' in line:
                    return True
            confirmation = input("Docker container environment is not detected. You are not recommended to use auto model/PDF download.\nAre you sure you want to continue? (y/n): ")
            return confirmation.lower() == 'y'
    except FileNotFoundError:
        confirmation = input("Docker container environment is not detected. You are not recommended to use auto model/PDF download.\nAre you sure you want to continue? (y/n): ")
        return confirmation.lower() == 'y'