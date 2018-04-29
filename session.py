import ast

from question import Question


class Session(object):
    SESSION_PREFIX = 'session-'
    INDEX_PREFIX = 'question_index-'
    QUESTIONS = [Question(0, "Will the Warriors be NBA champs?"),
                 Question(1, "Should people be allowed to smoke on sidewalks?"),
                 Question(2, "Will Tiger win another major?"),
                 Question(3, "Do you sleep more than 8 hours?"),
                 Question(4, "Are you tired of these quesrtions?")]

    def __init__(self, redis, session_id, source):
        self.__redis = redis
        self.__session_id = session_id
        self.__source = source

    @staticmethod
    def clear_all(redis):
        sessions = Session.all_sessions(redis)
        for s in sessions:
            s.delete()

    @staticmethod
    def exists(redis, session_id):
        return redis.exists(Session.SESSION_PREFIX + session_id)

    @staticmethod
    def all_sessions(redis):
        keys = redis.keys(Session.SESSION_PREFIX + '*')
        sessions = {}
        for key in keys:
            sessions[key] = Session.fetch(redis, key.decode("utf-8").replace(Session.SESSION_PREFIX, ''))
        return sessions

    @staticmethod
    def create(redis, session_id, source):
        redis.set(Session.SESSION_PREFIX + session_id, {"source": source})
        redis.set(Session.INDEX_PREFIX + session_id, -1)
        return Session(redis, session_id, source)

    @staticmethod
    def fetch(redis, session_id):
        session_json = redis.get(Session.SESSION_PREFIX + session_id)
        session_obj = ast.literal_eval(session_json.decode("utf-8"))
        question_index_obj_json = redis.get(Session.INDEX_PREFIX + session_id)
        question_index_obj = ast.literal_eval(question_index_obj_json.decode("utf-8"))
        session = Session(redis, session_id, session_obj['source'])
        session.__question_index = question_index_obj
        return session

    def delete(self):
        self.__redis.delete(Session.SESSION_PREFIX + self.__session_id)
        self.__redis.delete(Session.INDEX_PREFIX + self.__session_id)

    def next_question(self, answer):
        if self.__question_index == 4:
            return "Please stop asking me questions."

        # Record answer from previous question
        ##if (self.__question_index > -1):
        ##    self.current_question.answer = answer
        self.__redis.incr('question_index-' + self.__session_id)
        self.__question_index = self.__question_index + 1

        question = self.current_question.question
        return question

    @property
    def current_question(self):
        return Session.QUESTIONS[self.__question_index]

    def __str__(self):
        s = "session_id: [{}] source: [{}]\n".format(self.__session_id, self.__source)
        for q in Session.QUESTIONS:
            s += "{}\n".format(q)
        return s
