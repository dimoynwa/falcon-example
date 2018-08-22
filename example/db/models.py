from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from example.db import utils
from example import log


class BaseModel(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    created_at = Column(DateTime, default=func.now())
    modified_at = Column(DateTime, default=func.now(), onupdate=func.now())

    @property
    def as_dict(self):
        log.LOG.debug('---->Into as_dict')
        intersection = set(self.__table__.columns.keys())  # & set(self.FIELDS)
        log.LOG.debug('Fields : {}'.format(intersection))
        return dict(map(
            lambda key:
            (key,
             (lambda value: utils.alchemyencoder(value) if value else None)
             (getattr(self, key))),
            intersection))

    @classmethod
    def find_one(cls, session, id):
        return session.query(cls).filter(cls.get_id() == id).one()

    def save(self, session):
        with session.begin():
            session.add(self)

    @classmethod
    def get_all(cls, session):
        models = []
        with session.begin():
            query = session.query(cls)
            models = query.all()
        return models

    @classmethod
    def get_id(cls):
        pass

    FIELDS = {
        'created_at': utils.alchemyencoder,
        'modified_at': utils.alchemyencoder,
    }


Base = declarative_base(cls=BaseModel)


class Score(Base):
    id = Column(Integer, primary_key=True)
    username = Column(String(128), unique=True)
    company = Column(String(128))
    score = Column(Integer, default=0)

    def __init__(self, username, company, score=0):
        self.username = username
        self.company = company
        self.score = score

    # @declared_attr
    # def __tablename__(self):
    #     return self.__name__.lower()

    # @property
    # def as_dict(self):
    #     return {
    #         'username': self.username,
    #         'company': self.company,
    #         'score': self.score,
    #         'id': self.id
    #     }
    @classmethod
    def get_id(cls):
        return Score.id

    FIELDS = {
        'username': str,
        'company': str,
        'score': str
    }

    FIELDS.update(Base.FIELDS)


class User(Base):
    user_id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False, unique=True)
    email = Column(String(320), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    @classmethod
    def get_id(cls):
        return User.user_id

    @classmethod
    def find_by_email(cls, session, email):
        return session.query(User).filter(User.email == email).one()

    @classmethod
    def find_by_username(cls, session, username):
        return session.query(User).filter(User.username == username).one()

    @property
    def as_dict(self):
        d = super(User, self).as_dict
        del d['password']
        return d
