class Question(object):
    COUNTER = 0

    def __init__(self, id, text):
        self.__question_id = id
        self.__question = text

    @staticmethod
    def create(text):
        q = Question(Question.COUNTER, text)
        Question.COUNTER += 1
        return q

    @property
    def id(self):
        return self.__question_id

    @property
    def question(self):
        return self.__question

    def __str__(self):
        return '    Question: {} {}'.format(self.__question_id, self.__question)
