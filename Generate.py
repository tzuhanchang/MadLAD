import argparse
import subprocess

from madlad.parameters import edit_madspin, edit_run, edit_scales, copy_param_card, make_process

from madlad.utils import config, get_model, get_pdfset, is_running_in_docker_container, is_running_in_singularity_container


def argparser():
    parser = argparse.ArgumentParser(description='Run event generation')
    parser.add_argument('-c', '--config', type=str,  required=True, 
                        help='Configuration/settings file.')
    parser.add_argument('-p', '--mg5',    type=str,  required=False, default="mg5", 
                        help='MadGraph_aMC@NLO full path (default: mg5).')
    parser.add_argument('--launch_from', type=str, required=False, default=None,
                        help='Launch the generation from a saved production (default: None).')
    parser.add_argument('--auto_launch', action=argparse.BooleanOptionalAction,
                        help='Launch the generation after processing (default: False).')
    parser.add_argument('-y', '--assume_yes', action=argparse.BooleanOptionalAction,
                        help='Assume yes if prompted. (NOT recommended) (default: False)')
    return parser.parse_args()


if __name__ == '__main__':
    args = argparser()

    settings = config(args.config)

    in_container = False
    use_singularity = False

    if is_running_in_docker_container():
        in_container = True
        use_singularity = False
    
    if is_running_in_singularity_container():
        in_container = False
        use_singularity = True

    if in_container is False and use_singularity is False:
        raise RuntimeError("MadLAD is designed to be used inside a containerised environment. You MUST use either Docker or Singularity.")


    if args.launch_from is not None:
        if in_container:
            get_model(settings.model['model'])

        if in_container:
            get_pdfset(settings.run['lhaid'])

        ecard = open('mg5_exec_card','w')
        ecard.write("launch {}".format(args.launch_from))
        ecard.close()

        gen = subprocess.Popen(["%s"%(args.mg5), "mg5_exec_card"])
        gen.wait()

    else:
        if hasattr(settings,'model'):
            if in_container:
                get_model(settings.model['model'])
            make_process(settings=settings,madgraph_path=str(args.mg5))
        else:
            raise ValueError("No process provided")

        if hasattr(settings,'run'):
            if in_container:
                get_pdfset(settings.run['lhaid'])
            edit_run(settings=settings)

        if hasattr(settings,'param'):
            copy_param_card(settings=settings)

        if hasattr(settings,'madspin'):
            edit_madspin(settings=settings)

        if hasattr(settings,'scales'):
            edit_scales(settings=settings)

        if args.auto_launch:
            ecard = open('mg5_exec_card','w')
            ecard.write("launch {}".format(settings.process_dir))
            ecard.close()

            gen = subprocess.Popen(["%s"%(args.mg5), "mg5_exec_card"])
            gen.wait()