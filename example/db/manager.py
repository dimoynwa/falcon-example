import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import scoping

# Needed by the setup method as we want to make sure
# all models are loaded before we call create_all(...)
from example.db import models
from example import config
from example import log


class DBManager(object):
    def __init__(self, connection=None):
        self.connection = connection

        self.engine = sqlalchemy.create_engine(self.connection, echo=config.DB_ECHO)
        self.DBSession = scoping.scoped_session(
            orm.sessionmaker(
                bind=self.engine,
                autocommit=config.DB_AUTOCOMMIT
            )
        )


    @property
    def session(self):
        return self.DBSession()

    def setup(self):
        try:
            models.Base.metadata.create_all(self.engine)
        except Exception as e:
            log.LOG.error('Cannot create DataBase : {}'.format(e))
