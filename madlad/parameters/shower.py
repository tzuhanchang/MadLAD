import yaml
import warnings

from omegaconf import DictConfig, OmegaConf


def edit_shower(cfg: DictConfig) -> None:
    """Edit `run_card.dat` under the MadGraph process path :obj:`process_dir`.
    
    Args:
        process_dir (optional: str): aMC process directory.
        settings (optional: madlad.utils.config): settings.
    """
    save_dir = cfg['gen']['block_model']['save_dir']

    try:
        settings = yaml.load(OmegaConf.to_yaml(cfg['gen']['block_shower']['settings']), Loader=yaml.SafeLoader)
        # Operate on lower case settings, and choose the capitalization MG5 has as the default (or all lower case)
        for s in list(settings.keys()):
            if s.lower() not in settings:
                settings[s.lower()] = settings[s]
                del settings[s]

        defaultCard = open(save_dir+"/Cards/shower_card_default.dat", 'r')
        newCard = open(save_dir+'/Cards/shower_card.dat', 'w')
        used_settings = []
        for line in iter(defaultCard):
            if not line.strip().startswith('#'): # line commented out
                command = line.split('#', 1)[0]
                comment = line.split('#', 1)[1] if '#' in line else ''
                if '=' in command:
                    setting = command.split('=')[0] #.strip()
                    stripped_setting = setting.strip()
                    oldValue = '='.join(command.split('=')[1:])
                    if stripped_setting.lower() in settings:
                        # if setting set to 'None' it will be removed from run_card
                        if settings[stripped_setting.lower()] is None:
                            line=''
                            print('Removing '+stripped_setting+'.')
                            used_settings += [ stripped_setting.lower() ]
                        else:
                            line = setting+'= '+oldValue.replace(oldValue.strip(), str(settings[stripped_setting.lower()]))
                            if comment != '':
                                line += '#' + comment
                            print('Setting '+stripped_setting+' = '+str(settings[stripped_setting.lower()]))
                            used_settings += [ stripped_setting.lower() ]
            newCard.write(line.strip()+'\n')

        # Clean up unused options
        for asetting in settings:
            if asetting in used_settings:
                continue
            if settings[asetting] is None:
                continue
            warnings.warn('Option '+asetting+' was not in the default shower_card.  Adding by hand a setting to '+str(settings[asetting]) )
            newCard.write( str(asetting)+' = '+str(settings[asetting])+'\n')
    except:
        pass

    try:
        decays   = yaml.load(OmegaConf.to_yaml(cfg['gen']['block_shower']['decays']), Loader=yaml.SafeLoader)
        # Write decays
        for channel in decays:
            print(f"Writting channel {channel}.")
            newCard.write( channel+'\n')
    except:
        pass

    # close files
    defaultCard.close()
    newCard.close()
    print('Finished modification of shower card.')