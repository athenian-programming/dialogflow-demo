import ast

from question import Question


class Session(object):
    SESSION_PREFIX = 'session-'
    INDEX_PREFIX = 'question_index-'
    SOURCE_KEY = 'source'
    ANSWERS_KEY = 'answers'
    QUESTIONS = [Question.create('Will the Warriors be NBA champs?'),
                 Question.create('Should people be allowed to smoke on sidewalks?'),
                 Question.create('Will Tiger Woods win another major?'),
                 Question.create('Do you sleep more than 8 hours?'),
                 Question.create('Are you tired of these questions?')]

    def __init__(self, redis, session_id, source, answers):
        self.__redis = redis
        self.__session_id = session_id
        self.__source = source
        self.__answers = answers

    @staticmethod
    def clear_all(redis):
        sessions = Session.all_sessions(redis)
        for s in sessions.values():
            s.delete()

    @staticmethod
    def exists(redis, session_id):
        return redis.exists(Session.SESSION_PREFIX + session_id)

    @staticmethod
    def all_sessions(redis):
        keys = redis.keys(Session.SESSION_PREFIX + '*')
        sessions = {}
        for key in keys:
            # Convert from byte array to string
            k = key.decode('utf-8')
            # Strip session prefix and fetch session object
            sessions[k] = Session.fetch(redis, k.replace(Session.SESSION_PREFIX, ''))
        return sessions

    @staticmethod
    def create(redis, session_id, source):
        # Add KV for session info
        redis.set(Session.SESSION_PREFIX + session_id,
                  {Session.SOURCE_KEY: source, Session.ANSWERS_KEY: {}})

        # Add KV for questions_index value for each session
        redis.set(Session.INDEX_PREFIX + session_id, -1)
        return Session(redis, session_id, source, {})

    @staticmethod
    def fetch(redis, session_id):
        # Fetch Session from redis
        session_json = redis.get(Session.SESSION_PREFIX + session_id)

        # Use ast.literal_eval() instead of json.loads() because json values require double quote and redis uses single quotes
        session_obj = ast.literal_eval(session_json.decode('utf-8'))

        session = Session(redis,
                          session_id,
                          session_obj[Session.SOURCE_KEY],
                          session_obj[Session.ANSWERS_KEY])

        # Fetch question_index from redis
        question_index_obj_json = redis.get(Session.INDEX_PREFIX + session_id)
        session.__question_index = ast.literal_eval(question_index_obj_json.decode('utf-8'))
        return session

    def delete(self):
        self.__redis.delete(Session.SESSION_PREFIX + self.__session_id)
        self.__redis.delete(Session.INDEX_PREFIX + self.__session_id)

    def next_question(self, answer):
        # Record answer from previous question if not first time through
        if (self.__question_index > -1):
            self.__answers[self.__question_index] = answer

            # Save session to redis
            self.__redis.set(Session.SESSION_PREFIX + self.__session_id,
                             {Session.SOURCE_KEY: self.__source, Session.ANSWERS_KEY: self.__answers})

        # Increment question index
        self.__redis.incr(Session.INDEX_PREFIX + self.__session_id)
        self.__question_index = self.__question_index + 1

        if self.__question_index == len(Session.QUESTIONS) - 1:
            question = 'I am tired and I have no more questions for you.'
        else:
            question = self.current_question.question
        return question

    def get_answer(self, index):
        try:
            return self.__answers[index]
        except KeyError:
            return None

    @property
    def current_question(self):
        return Session.QUESTIONS[self.__question_index]

    def __str__(self):
        s = 'session_id: [{}] source: [{}]\n'.format(self.__session_id, self.__source)
        for q in Session.QUESTIONS:
            s += '{} answer: [{}]\n'.format(q, self.get_answer(q.id))
        return s
