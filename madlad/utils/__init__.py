from .container import is_running_in_docker_container, is_running_in_singularity_container
from .settings import config

__all__ = [
    'is_running_in_docker_container',
    'is_running_in_singularity_container',
    'config'
]
