class Session(object):

    def __init__(self, session_id, source):
        self.__session_id = session_id
        self.__source = source

    def __str__(self):
        return self.__session_id + " " + self.__source
