#/usr/bin/env python
#
# CLI for creating Gitlab report
# Version 0.1.0
# Create a status report of the repos present on the Gitlab server
# Output in the following formats:
# HTML
# JSON


# TODO Figure out what python modules I'll need
import argparse
import email
from gitlab import *
import ConfigParser



def main():
    args = parse_arguments()
    config = import_config(args.config_file)

    # lets get this party started?
    # TODO Party



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
    output.add_argument('-j', action='store', dest='json', type=bool, help="Password for role account")

    parser.add_argument('-c', action='store', dest='config_file', help="Location of python-gitlab.cfg")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()