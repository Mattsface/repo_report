import unittest
from fennec.fennec import Fennec
from gitlab import Gitlab
from gitlab import Group
from gitlab import GroupMember
from gitlab import Project
from mock import patch, MagicMock, Mock, call


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
        fake_projects_group3 = [FakeProject(project) for project in ['project7', 'project8', 'project7']]
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

        fake_projects.append(forked_project)
        mock_project.return_value = fake_projects

        # act
        results = self.fennec.find_namespace_projects(self.gl, fake_groups)

        # assert
        self.assertEqual(expected_results, results)
