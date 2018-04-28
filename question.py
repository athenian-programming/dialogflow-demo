class Question(object):
    # static counter for ids -- usually done in DBMS
    id_counter = 0

    def __init__(self, text):
        Question.id_counter = Question.id_counter + 1
        self.__question_id = Question.id_counter
        self.__text = text

    @property
    def id(self):
        return self.__question_id

    @property
    def text(self):
        return self.__text
