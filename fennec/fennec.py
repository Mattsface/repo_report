from gitlab import *


class Fennec(object):

    @staticmethod
    def groups(gl):
        """
        return a list of group objects
        :param gl: a gitlab connection object
        :return: list
        """
        return gl.Group()

    @staticmethod
    def find_members(groups):
        """
        :param groups: A list of gitlab group objects
        :return: a dictionary of groups and list of its members names
        """
        # TODO make this return the objects, not strings
        members = {group.name: [member.name for member in group.Member()] for group in groups}

        return members

    @staticmethod
    def find_namespace_projects(gl, groups):
        """
        :param gl groups: A gitlab connection, and the list of gitlab groups
        :return dict: A dictionary of groups and their projects
        """
        # TODO make this return the objects, not strings
        def is_forked(project):
            """
            Returns True of False if the project is forked
            :param project: a project object
            :return: boolean
            """
            try:
                if project.forked_from_project:
                    return True
            except AttributeError:
                return False

        collected_projects = {}

        for project in gl.Project():

            project_namespace = project.namespace.name

            if is_forked(project):
                continue
            elif project_namespace in collected_projects:
                collected_projects[project_namespace].append(project.name)
            else:
                collected_projects[project_namespace] = []
                collected_projects[project_namespace].append(project.name)
        return collected_projects

    @staticmethod
    def find_forked_namespace_projects(gl):
        """
        :param gl:
        :return dict: A dictionary of forked projects
        """
        # TODO make this return the objects, not strings
        def is_forked(project):
            """
            Returns True of False if the project is forked
            :param project: a project object
            :return: boolean
            """
            try:
                if project.forked_from_project:
                    return True
            except AttributeError:
                return False

        forked_projects = {}

        for project in gl.Project():

            project_namespace = project.namespace.name

            if not is_forked(project):
                continue
            elif project_namespace in forked_projects:
                forked_projects[project_namespace].append(project.name)
            else:
                forked_projects[project_namespace] = []
                forked_projects[project_namespace].append(project.name)
        return forked_projects



