import unittest
from fennec.fennec import Fennec
from gitlab import Gitlab
from gitlab import Group
from gitlab import GroupMember
from gitlab import Project
from mock import patch, MagicMock, Mock, call


class FakeGroup(Group):

    name = None

    def __init__(self, name):
        self.name = name

    def Member(self, **kwargs):
        pass


class FakeGitlab(Gitlab):
    def __init__(self):
        pass


class FakeGroupMember(GroupMember):
    name = None

    def __init__(self, name):
        self.name = name


class FakeProject(Project):
    pass


class TestFennec(unittest.TestCase):

    def setUp(self):
        """
        Set up object mock
        """
        self.gl = FakeGitlab
        self.fennec = Fennec()


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

        # assert
        self.assertEqual(expected_results, results)

    @patch.object(FakeGroup, 'Projects')
    def test_find_projects(self):

        # arrange


        # act


        # assert
        pass
