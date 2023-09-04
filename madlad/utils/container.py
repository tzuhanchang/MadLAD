def is_running_in_docker_container():
    try:
        with open('/proc/1/cgroup', 'r') as f:
            for line in f:
                if 'docker' in line or 'lxc' in line:
                    return True
        return False
    except FileNotFoundError:
        return False