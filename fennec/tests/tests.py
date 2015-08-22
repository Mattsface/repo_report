import unittest
from fennec.fennec import Fennec, FennecMail
from fennec.bin import fen_cli
from os import remove
from gitlab import Gitlab
from gitlab import Group
from gitlab import GroupMember
from gitlab import Project
from mock import patch, MagicMock, Mock, call


# monkey patches!
class FakeGroup(Group):
    def __init__(self, name):
        self.name = name

    def Member(self, **kwargs):
        pass


class FakeGitlab(Gitlab):
    def __init__(self):
        pass


class FakeGroupMember(GroupMember):
    def __init__(self, name):
        self.name = name


class FakeProject(Project):
    def __init__(self, name, forked_from_project=None):
        self.name = name
        self.forked_from_project = forked_from_project


class TestFennec(unittest.TestCase):
    def setUp(self):
        """
        Set up object mock
        """
        self.gl = FakeGitlab
        self.fennec = Fennec()
        self.groups = ['group1', 'group2', 'group3']

    @patch.object(Gitlab, 'Group')
    def test_group_collection(self, mock_group):
        # arrange
        expected_groups = [FakeGroup('i') for i in range(3)]
        mock_group.return_value = expected_groups

        # act
        results = self.fennec.groups(self.gl)

        # assert
        self.assertEqual(expected_groups, results)
        self.assertEqual(isinstance(results[0], Group), True)
        self.assertEqual(len(results), 3)

    @patch.object(FakeGroup, 'Member')
    def test_find_members(self, mock_member):

        # arrange
        expected_results = {'group1': ['member1', 'member2', 'member3'],
                            'group2': ['member1', 'member2', 'member3'],
                            'group3': ['member1', 'member2', 'member3']}

        fakegroups = [FakeGroup(group) for group in expected_results.iterkeys()]
        fakemembers = [FakeGroupMember(member) for member in ['member1', 'member2', 'member3']]
        mock_member.return_value = fakemembers

        # act
        results = self.fennec.find_members(fakegroups)

        # assert TODO Add more tests
        self.assertEqual(expected_results, results)

    @patch.object(Gitlab, 'Project')
    def test_find_namespace_projects(self, mock_project):

        # arrange
        expected_results = {'group1': ['project1', 'project2', 'project3'],
                            'group2': ['project4', 'project5', 'project6'],
                            'group3': ['project7', 'project8', 'project9']}

        fake_projects_group1 = [FakeProject(project) for project in ['project1', 'project2', 'project3']]
        fake_projects_group2 = [FakeProject(project) for project in ['project4', 'project5', 'project6']]
        fake_projects_group3 = [FakeProject(project) for project in ['project7', 'project8', 'project9']]
        for project in fake_projects_group1:
            setattr(project, 'namespace', FakeGroup('group1'))

        for project in fake_projects_group2:
            setattr(project, 'namespace', FakeGroup('group2'))

        for project in fake_projects_group3:
            setattr(project, 'namespace', FakeGroup('group3'))

        fake_groups = [FakeGroup(group) for group in self.groups]
        fake_projects = fake_projects_group1 + fake_projects_group2 + fake_projects_group3

        forked_project = FakeProject('forked_project')
        setattr(forked_project, 'forked_from_project', dict(path='testpast', name='project2', namespace='not_a_group'))
        setattr(forked_project, 'namespace', FakeGroup('group3'))
        fake_projects.append(forked_project)
        mock_project.return_value = fake_projects

        # act
        results = self.fennec.find_namespace_projects(self.gl, fake_groups)

        # assert
        self.assertEqual(expected_results, results)

    @patch.object(Gitlab, 'Project')
    def test_find_forked_namespace_projects(self, mock_project):

        # arrange
        expected_results = {'forked_group': ['forked_project']}

        fake_projects_group1 = [FakeProject(project) for project in ['project1', 'project2', 'project3']]
        fake_projects_group2 = [FakeProject(project) for project in ['project4', 'project5', 'project6']]
        fake_projects_group3 = [FakeProject(project) for project in ['project7', 'project8', 'project9']]
        for project in fake_projects_group1:
            setattr(project, 'namespace', FakeGroup('group1'))

        for project in fake_projects_group2:
            setattr(project, 'namespace', FakeGroup('group2'))

        for project in fake_projects_group3:
            setattr(project, 'namespace', FakeGroup('group3'))

        fake_projects = fake_projects_group1 + fake_projects_group2 + fake_projects_group3

        forked_project = FakeProject('forked_project')
        setattr(forked_project, 'forked_from_project', dict(path='testpast', name='project2', namespace='forked_group'))
        setattr(forked_project, 'namespace', FakeGroup('forked_group'))
        fake_projects.append(forked_project)
        mock_project.return_value = fake_projects

        # act
        results = self.fennec.find_forked_namespace_projects(self.gl)

        # assert
        self.assertEqual(expected_results, results)


class TestFennecMail(unittest.TestCase):
    def setUp(self):
        """
        Set up object mock
        """
        self.gl = FakeGitlab
        self.fennec = Fennec()
        self.groups = ['group1', 'group2', 'group3']

        self.member_dict = {'group1': ['member1', 'member2', 'member3'],
                            'group2': ['member4', 'member5', 'member6'],
                            'group3': ['member7', 'member8', 'member9']}

        self.project_dict = {'group1': ['project1', 'project2', 'project3'],
                             'group2': ['project4', 'project5', 'project6'],
                             'group3': ['project7', 'project8', 'project9']}

        self.forked_dict = {'user1': ['project1'],
                            'user2': ['project2', 'project3']}

    def test_render_message(self):
        # TODO make this test not suck
        # arrange
        message = FennecMail(groups=self.groups, members=self.member_dict, projects=self.project_dict,
                             forked_projects=self.forked_dict)
        # act
        rendered_messsage = message.render_message()

        # assert
        self.assertEqual(isinstance(rendered_messsage, unicode), "Expected {}, but got {}".format("unicode", isinstance(rendered_messsage)))


class TestFenCLI(unittest.TestCase):
    def setUp(self):

        self.python_gitlab_filename = 'python-gitlab.cfg'

# wtf? #TODO Fix this
        self.python_gitlab = """
[global]
# required setting
default = local

# optional settings
ssl_verify = False
timeout = 5

[local]
url = https://gitlab.test.com
private_token = blahblahblah
ssl_verify = False
"""

        with file(self.python_gitlab_filename, 'w') as f:
            f.write(self.python_gitlab)

    def tearDown(self):
        remove(self.python_gitlab_filename)

    def test_import_config(self):
        # arrange
        expected_gitlab_key = 'blahblahblah'
        expected_gitlab_url = 'https://gitlab.test.com'
        expected_default = 'local'

        # act
        config = fen_cli.import_config(self.python_gitlab_filename)
        gitlab_url = config.get(section='local', option='url')
        gitlab_key = config.get(section='local', option='private_token')
        gitlab_default = config.get(section='global', option='local')
        # assert

        self.assertEqual(expected_gitlab_key, gitlab_key, "Expected {}, but got {}".format(expected_gitlab_key,
                                                                                           gitlab_key))
        self.assertEqual(expected_gitlab_url, gitlab_url, "Expected {}, but got {}".format(expected_gitlab_url,
                                                                                           gitlab_url))
        self.assertEqual(expected_default, gitlab_default, "Expected {}, but got {}".format(expected_default,
                                                                                            gitlab_default))

    def test_failed_import_config(self):
        pass

    def test_connect_to_gitlab(self):
        pass

    def test_failed_connect_gitlab(self):
        pass

    def test_send_mail(self):
        pass
        # need monkey test