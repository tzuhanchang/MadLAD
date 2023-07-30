import warnings


def modify_run_card(process_dir: str = None, settings: dict = {}):
    """Build a new run_card.dat from an existing one.
    This function can get a fresh runcard from DATAPATH or start from the process directory.
    Settings is a dictionary of keys (no spaces needed) and values to replace.
    """

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

    defaultCard = open(process_dir+"/Cards/run_card_default.dat", 'r')
    newCard = open(process_dir+'/Cards/run_card.dat', 'w')
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
