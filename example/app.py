import falcon
from example.db.manager import DBManager
from example.resources import scores
from example.resources import users
from example.middleware import translator, session_manager, serializer
from example import config
from falcon_jwt_checker import JwtChecker


class Application(falcon.API):
    def __init__(self):
        mgr = DBManager(config.DATABASE_URL)
        mgr.setup()

        jwt_checker = JwtChecker(secret=config.SECRET_KEY, exempt_routes=['/login'],
                                 algorithm='HS256')

        super(Application, self).__init__(
            middleware=[jwt_checker, serializer.SerializerMiddleware(), translator.JSONTranslator(),
                        session_manager.DatabaseSessionManager(mgr.DBSession)],
            media_type='application/json')

        # Create our resources
        scores_res = scores.ScoreResource()
        single_score = scores.SingleScoreResource()

        users_res = users.UserResource()
        login = users.Self()
        # Build routes
        self.add_route('/scores', scores_res)
        self.add_route('/scores/{score_id}', single_score)
        self.add_route('/users/', users_res)
        self.add_route('/login', login)


api = application = Application()

