import unittest
from fennec.fennec import Fennec
from mock import MagicMock, Mock, call


class TestFennec(unittest.TestCase):

    def setUp(self):
        """
        Set up object mock
        """
        class Gitlab(object):
            _groupList = None

            def auth(self):
                return None

            def Group(self):
                return self._groupList

        class Group(Gitlab):
            _name = None

            def name(self):
                return self._name

        testname = self.id().split(".")[2]

        if testname == "test_group_collection":
            group_list = ['group1', 'group2', 'group3', 'group4']
            self.gl = Mock(spec=Gitlab)
            self.gl.Group.return_value = [Mock(spec=Group, _new_name=group) for group in group_list]
        else:
            pass

    def tearDown(self):
        print "Tearing down tests"

    def test_group_collection(self):
        expected_list = ['group1', 'group2', 'group3', 'group4']
        fen = Fennec(self.gl)
        actually_list = [group.name for group in fen.groups()]
        self.assertEqual(actually_list, expected_list, "Expected {}, but got {}".format(actually_list, expected_list))

    def test_failed_namespace_collection(self):
        pass

    def test_repos_in_namespace_collection(self):
        pass

    def test_failed_repos_in_namespace_collection(self):
        pass


