import falcon
from example.db.manager import DBManager
from example.resources import scores
from example.middleware import translator, session_manager, serializer
from example import config


class Application(falcon.API):
    def __init__(self):
        mgr = DBManager(config.DATABASE_URL)
        mgr.setup()
        super(Application, self).__init__(
            middleware=[serializer.SerializerMiddleware(), translator.JSONTranslator(),
                        session_manager.DatabaseSessionManager(mgr.DBSession)],
            media_type='application/json')

        # Create our resources
        scores_res = scores.ScoreResource()

        # Build routes
        self.add_route('/scores', scores_res)


api = application = Application()
