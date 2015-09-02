from gitlab import *
from jinja2 import Template
import smtplib


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


        collected_projects = {}

        for project in gl.Project(all=True):

            project_namespace = project.namespace.name

            if Fennec.is_forked(project):
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

        forked_projects = {}

        for project in gl.Project(all=True):

            project_namespace = project.namespace.name

            if not Fennec.is_forked(project):
                continue
            elif project_namespace in forked_projects:
                forked_projects[project_namespace].append(project.name)
            else:
                forked_projects[project_namespace] = []
                forked_projects[project_namespace].append(project.name)

        return forked_projects

    @classmethod
    def is_forked(cls, project):
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

class FennecMail(object):

    # TODO Add Multiple templates
    # FIXME I'm not seeing eveything I want to see as the admin user
    # FIXME I need to read up on the permissions of the admin user and read what read permissions he has


    email_template = """\
    <p />
    <span style="font-weight: bold; font-size: 14px;">Gitlab Repo report lists Groups with their members and projects (Sorry my HTML blows)</span>
    <p />
    <br />
    <table cellpadding="5" cellspacing="0">
    <h4> Groups: </h4>
    <ul>
    {% for group in groups %}
        <li> {{ group.name }} </li>
    {% endfor %}
    </ul>
    <h4> Members: </h4>
    {% for group, users in members.items() %}
        <h5>Group: {{ group }}</h5>
        <ul>
        {% for member in users %}
            <li>{{ member }} </li>
        {% endfor %}
        </ul>
    {% endfor %}
    <h4> Projects: </h4>
    {% for group, repos in projects.items() %}
        <h5>Group: {{ group }}</h5>
        <ul>
        {% for project in repos %}
            <li>{{ project }} </li>
        {% endfor %}
        </ul>
    {% endfor %}
    <h4> Forked Projects: </h4>
    {% for namespace, projects in forked_projects.items() %}
        <h5>Namespace: {{ namespace }}</h5>
        <ul>
            {% for project in projects %}
            <li>{{ project }}</li>
            {% endfor %}
        </ul>
    {% endfor %}
    </table>
    <p />
    <br />
    """

    def __init__(self, **kwargs):
        self.groups = kwargs.get('groups')
        self.members = kwargs.get('members')
        self.projects = kwargs.get('projects')
        self.forked_projects = kwargs.get('forked_projects')

    def render_message(self):
        template = Template(self.email_template)
        return template.render(groups=self.groups, members=self.members, projects=self.projects,
                               forked_projects=self.forked_projects)






