from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base, declared_attr


class BaseModel(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    created_at = Column(DateTime, default=func.now())
    modified_at = Column(DateTime, default=func.now(), onupdate=func.now())


Base = declarative_base(cls=BaseModel)


class Score(Base):
    id = Column(Integer, primary_key=True)
    username = Column(String(128), unique=True)
    company = Column(String(128))
    score = Column(Integer, default=0)

    def __init__(self, username, company, score):
        self.username = username
        self.company = company
        self.score = score

    # @declared_attr
    # def __tablename__(self):
    #     return self.__name__.lower()

    @property
    def as_dict(self):
        return {
            'username': self.username,
            'company': self.company,
            'score': self.score,
            'id': self.id
        }

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
