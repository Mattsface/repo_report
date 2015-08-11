
class Fennec(object):
    def __init__(self, gl):
        self.gl = gl

    def groups(self):
        """
        return a list of group objects
        :return:
        """
        try:
            return self.gl.Group()
        except StandardError as e:
            raise StandardError(e)




