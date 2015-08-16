from gitlab import *


class Fennec(object):

    @classmethod
    def groups(cls, gl):
        """
        return a list of group objects
        :return: list
        """
        return gl.Group()

    @classmethod
    def find_members(cls, groups):
        """
        :param groups: is a list of group objects
        :return: a dictionary of groups and list of its members names
        """
        """
        {'group1': ['member1', 'member2'],
         'group2': ['member1', 'member2']
        }
        """
        members = {group.name: [member.name for member in group.Member()] for group in groups}

        return members

    def find_projects(self, groups):
        pass

