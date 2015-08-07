
class Fennec(object):
    def __init__(self, gl):
        self.gl = gl

    def group_look_up(self):
        """
        return a list of group objects
        :return:
        """
        try:
            self.gl.Group()
        except StandardError as e:
            raise StandardError(e)




