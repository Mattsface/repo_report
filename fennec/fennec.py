
from gitlab import *


class Fennec(object):
    def __init__(self, gl):
        self.gl = gl

    def groups(self):
        """
        return a list of group objects
        :return: list
        """
        return self.gl.Group()

    def find_members(self, groups):
        """

        :param groups: is a list of group objects
        :return: a dictionary of groups and members
        """
        """
        {'group1': ['member1', 'member2'],
         'group2': ['member1', 'member2']
        }
        """
        members = {group.name: group.Member() for group in groups}

        return members




