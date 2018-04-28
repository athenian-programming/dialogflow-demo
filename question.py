class Question(object):
    def __init__(self, id, text):
        self.__question_id = id
        self.__question = text
        self.__answer = None

    @property
    def id(self):
        return self.__question_id

    @property
    def question(self):
        return self.__question

    @property
    def answer(self):
        return self.__answer

    @answer.setter
    def answer(self, answer):
        self.__answer = answer

    def __str__(self):
        return "    question_id: {} answer: {}".format(self.__question_id, self.__answer)
