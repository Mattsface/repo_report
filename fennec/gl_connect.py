from gitlab import *



class GitlabConnect(object):
    def __init__(self, token, url, connection=None):
        self.token = token
        self.url = url
        self.connection = connection

    def connect_to_api(self):
        pass


