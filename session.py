from question import Question


class Session(object):

    def __init__(self, session_id, source):
        self.__session_id = session_id
        self.__source = source
        self.__questions = [Question(0, "What do you thing about gun control 1"),
                            Question(1, "What do you thing about gun control 2"),
                            Question(2, "What do you thing about gun control 3"),
                            Question(3, "What do you thing about gun control 4"),
                            Question(4, "What do you thing about gun control 5")]
        self.__question_index = -1

    def next_question(self, answer):
        # Record answer from previous question
        if (self.__question_index > -1):
            self.current_question.answer = answer
        self.__question_index = self.__question_index + 1
        question = (self.current_question).question
        return question

    @property
    def current_question(self):
        return self.__questions[self.__question_index]

    def __str__(self):
        s = "session_id: [{}] source: [{}]\n".format(self.__session_id, self.__source)
        for q in self.__questions:
            s += "{}\n".format(q)
        return s
