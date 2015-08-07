import unittest
from fennec.fennec import Fennec
from mock import MagicMock
from gitlab import *


class TestFennec(unittest.TestCase):
    def setUp(self):
        """
        Set up object mock
        """
        gl = Gitlab()
        gl.auth = MagicMock(None)
        gl.Group = MagicMock()

    def tearDown(self):
        pass

    def test_namespace_collection(self):
        fen = Fennec()


    def test_failed_namespace_collection(self):
        pass

    def test_repos_in_namespace_collection(self):
        pass

    def test_failed_repos_in_namespace_collection(self):
        pass


