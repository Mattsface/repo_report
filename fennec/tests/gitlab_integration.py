import unittest
from fennec.fennec import Fennec
from gitlab import Gitlab
from gitlab import Group
from gitlab import GroupMember
from mock import patch, MagicMock, Mock, call


class FakeGroup(Group):
    name = None

    def __init__(self):
        pass

    def Member(self, **kwargs):
        pass


class FakeGitlab(Gitlab):
    def __init__(self):
        pass


class FakeGroupMember(GroupMember):
    def __init__(self):
        pass




class TestFennec(unittest.TestCase):

    def setUp(self):
        """
        Set up object mock
        """
        self.fennec = Fennec(FakeGitlab())


    @patch.object(Gitlab, 'Group')
    def test_group_collection(self, mock_group):
        """
        Verify
        :return:
        """
        # arrange
        expected_groups = [FakeGroup() for i in range(3)]
        mock_group.return_value = expected_groups

        # act
        results = self.fennec.groups()

        # assert
        self.assertEqual(expected_groups, results)
        self.assertEqual(isinstance(results[0], Group), True)
        self.assertEqual(len(results), 3)

    @patch.object(FakeGroup, 'Member')
    def test_find_members(self, mock_member):

        # arrange
        expected_results = {'group1': ['member1', 'member2'],
                            'group2': ['member1', 'member2']}

        fakefuckinggroup = FakeGroup()
        fakefuckinggroup.name = 'group1'
        mock_member.return_value = [fakefuckinggroup]
        # act

        results = self.fennec.find_members(gl.Groups())


        # assert
        self.assertEqual(expected_results, results)





