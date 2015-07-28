import unittest
from fennec.fennec import Fennec
from fennec.gl_connect import GitlabConnect
import ConfigParser

# Requires a config.ini file in the test folder
# DO NOT COMMIT the config.ini file, it is ignored for a reason




class TestFennec(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_namespace_collection(self):
        pass

    def test_failed_namespace_collection(self):
        pass

    def test_repos_in_namespace_collection(self):
        pass

    def test_failed_repos_in_namespace_collection(self):
        pass



class TestGitLabConnect(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_gitlab_connect_success(self):
        pass

    def test_gitlab_connect_failed(self):
        pass
