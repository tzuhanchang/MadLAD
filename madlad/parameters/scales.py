import warnings

from omegaconf import DictConfig


def edit_scales(cfg: DictConfig) -> None:
    r"""Use a custom dynmaical scale by editing `setscales.f` under :obj:`process_dir`/SubProcesses.

    Args:
        process_dir (optional: str): aMC process directory.
        settings (optional: madlad.utils.config): settings.
    """
    save_dir = cfg['gen']['block_model']['save_dir']
    try:
        order = cfg['gen']['block_model']['order'].lower()
    except KeyError:
        order = "nlo"
    settings = cfg['gen']['block_sf']

    if 'custom_scales' not in list(settings.keys()):
        raise ValueError("Cannot find `custom_scales`, please provide it in config.")

    fileN = save_dir+'/SubProcesses/setscales.f'

    mark_i = "      elseif(dynamical_scale_choice.eq.0) then" if order=="lo" else "      elseif(dynamical_scale_choice.eq.10) then"
    mark_f = "      else"

    with open(fileN, 'r') as file:
        lines = file.readlines()

    start_index = -1
    end_index = -1

    for i, line in enumerate(lines):
        if mark_i in line:
            start_index = i
        elif mark_f in line and start_index != -1:
            end_index = i
            break

    if start_index != -1 and end_index != -1:
        del lines[start_index+1:end_index]

        lines.insert(start_index + 1, '\n'.join(settings['custom_scales']) + '\n')

        with open(fileN, 'w') as file:
            file.writelines(lines)

    else:
        warnings.warn("Scale factors are not modified, please check the configuration file.")
