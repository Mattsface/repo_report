#/usr/bin/env python
#
# CLI for creating Gitlab report
# Version 0.1.0
# Create a status report of the repos present on the Gitlab server
# Output in the following formats:
# HTML

import argparse
import email
from gitlab import *
from fennec.fennec import Fennec, FennecMail
from os.path import expanduser
import ConfigParser



def main():
    args = parse_arguments()
    try:
        config = import_config(args.config_file)
    except IOError:
        print "Unable to located ~/.python-gitlab.cfg"
        sys.exit(1)

    gitlab_key = config.get(section='local', option='private_token')
    gitlab_url = config.get(section='local', option='url')

    try:
        gl = connect_to_gitlab(gitlab_key, gitlab_url)
    except GitlabAuthenticationError:
        print "AuthenticationError when connecting to Gitlab Server"
    except GitlabConnectionError:
        print "Unable to connect to Gitlab server"
    except GitlabError:
        print "Oops, unknown Gitlab error "

    groups = Fennec.groups(gl)
    members = Fennec.find_members(groups)
    namespace_projects = Fennec.find_namespace_projects(gl, groups)
    forked_projects = Fennec.find_forked_namespace_projects(gl)
    fennecmessage = FennecMail(groups=groups, members=members, projects=namespace_projects,
                               forked_projects=forked_projects)

    print fennecmessage.render_message()


def import_config(config_file=None):
    """
    import config file
    """
    config = ConfigParser.ConfigParser()

    if config_file is None:
        home = expanduser('~')
        config_file = "{}/.python-gitlab.cfg".format(home)

    config.readfp(open(config_file))
    return config


def parse_arguments():
    """
    Parse command line for arguments
    :return: args
    """

    parser = argparse.ArgumentParser()

    output = parser.add_mutually_exclusive_group(required=True)
    output.add_argument('-e', action='store_true', dest='email', help="Send an email")
    output.add_argument('-j', action='store_true', dest='json', help="This won't do shit, not implemented yet")

    parser.add_argument('-c', action='store', dest='config_file', help="Location of python-gitlab.cfg")

    args = parser.parse_args()
    return args


def connect_to_gitlab(key, url):
    """
    Connect to Gitlab API

    :param key: Gitlab Private Token
    :param url: Gitlab URL
    :return: Gitlab connection object
    """
    gl = Gitlab(url=url, private_token=key, ssl_verify=False)
    gl.auth()
    return gl


def send_mail(msg):
    pass

if __name__ == "__main__":
    main()