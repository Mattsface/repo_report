#/usr/bin/env python
#
# CLI for creating Gitlab report
# Version 0.1.0
# Create a status report of the repos present on the Gitlab server
# Output in the following formats:
# HTML



# TODO Figure out what python modules I'll need
import argparse
import email
from gitlab import *
from fennec.fennec import Fennec, FennecMail
import ConfigParser



def main():
    args = parse_arguments()
    config = import_config(args.config_file)

    #TODO add the correct keys
    gitlab_key = config.get()
    gitlab_url = config.get()

    gl = connect_to_gitlab()

    groups = Fennec.groups(gl)
    members = Fennec.find_members(groups)
    namespace_projects = Fennec.find_namespace_projects(gl, groups)
    forked_projects = Fennec.find_forked_namespace_projects(gl)
    html_message = FennecMail(groups=groups,
                              members=members,
                              projects=namespace_projects,
                              forked_projects=forked_projects)

    try:
        send_mail()
    except:
        pass



def import_config(config_file=None):
    """
    import config file
    """
    config = ConfigParser.ConfigParser()

    if config_file is None:
        config_file = "~/.python-gitlab.cfg"
    try:
        config.readfp(open(config_file))
        return config
    except IOError:
        print "Unable to open config file, place it in ~/.python-gitlab.cfg"
        sys.exit(1)


def parse_arguments():
    """
    Parse command line for arguments
    :return: args
    """

    parser = argparse.ArgumentParser()

    output = parser.add_mutually_exclusive_group(required=True)
    output.add_argument('-e', action='store', dest='email', type=bool, help="Length of random password to be created")
    output.add_argument('-j', action='store', dest='json', type=bool, help="This won't do shit")

    parser.add_argument('-c', action='store', dest='config_file', help="Location of python-gitlab.cfg")

    args = parser.parse_args()
    return args

def connect_to_gitlab():
    pass


def send_mail(msg):
    pass

if __name__ == "__main__":
    main()