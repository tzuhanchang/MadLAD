import warnings

from madlad.utils import config
from typing import Optional


def edit_run(settings: Optional[config] = None):
    """Edit `run_card.dat` under the MadGraph process path :obj:`process_dir`.
    
    Args:
        process_dir (optional: str): aMC process directory.
        settings (optional: madlad.utils.config): settings.
    """
    save_dir = settings.process_dir
    settings = settings.run

    # Operate on lower case settings, and choose the capitalization MG5 has as the default (or all lower case)
    for s in list(settings.keys()):
        if s.lower() not in settings:
            settings[s.lower()] = settings[s]
            del settings[s]

    # Get beamenergy
    if 'beamenergy' in settings:
        beamEnergy=settings['beamenergy']
        settings.pop('beamenergy')
    if 'ebeam1' not in settings:
        settings['ebeam1']=beamEnergy
    if 'ebeam2' not in settings:
        settings['ebeam2']=beamEnergy
    # Make sure nevents is an integer
    if 'nevents' in settings:
        settings['nevents'] = int(settings['nevents'])

    defaultCard = open(save_dir+"/Cards/run_card_default.dat", 'r')
    newCard = open(save_dir+'/Cards/run_card.dat', 'w')
    used_settings = []
    for line in iter(defaultCard):
        if not line.strip().startswith('#'): # line commented out
            command = line.split('!', 1)[0]
            comment = line.split('!', 1)[1] if '!' in line else ''
            if '=' in command:
                setting = command.split('=')[-1] #.strip()
                stripped_setting = setting.strip()
                oldValue = '='.join(command.split('=')[:-1])
                if stripped_setting.lower() in settings:
                    # if setting set to 'None' it will be removed from run_card
                    if settings[stripped_setting.lower()] is None:
                        line=''
                        print('Removing '+stripped_setting+'.')
                        used_settings += [ stripped_setting.lower() ]
                    else:
                        line = oldValue.replace(oldValue.strip(), str(settings[stripped_setting.lower()]))+'='+setting
                        if comment != '':
                            line += '  !' + comment
                        print('Setting '+stripped_setting+' = '+str(settings[stripped_setting.lower()]))
                        used_settings += [ stripped_setting.lower() ]
        newCard.write(line.strip()+'\n')

    # Clean up unused options
    for asetting in settings:
        if asetting in used_settings:
            continue
        if settings[asetting] is None:
            continue
        warnings.warn('Option '+asetting+' was not in the default run_card.  Adding by hand a setting to '+str(settings[asetting]) )
        newCard.write( ' '+str(settings[asetting])+'   = '+str(asetting)+'\n')
    # close files
    defaultCard.close()
    newCard.close()
    print('Finished modification of run card.')