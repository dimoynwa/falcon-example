import falcon
from example.db import models
from example.resources import BaseResource
from example import log
from example.schemas import schema
from example.utils import auth
from example import config
import jwt


class UserResource(BaseResource):
    serializers = {
        'post': schema.UserPostSchema
    }

    def on_get(self, req: falcon.Request, resp: falcon.Response, **params):
        all_users = models.User.get_all(self.session)
        all_b = [u.as_dict for u in all_users]

        resp.body = all_b

    def on_post(self, req: falcon.Request, resp: falcon.Response, **params):
        js = req.context['data']
        log.LOG.debug('Data : {}'.format(js))

        user = models.User()
        user.username = js['username']
        user.password = auth.hash_password(js['password']).decode('utf-8')
        user.email = js['email']

        user.save(self.session)

        resp.status = falcon.HTTP_CREATED
        resp.body = {
            "user_id": user.user_id
        }


class Self(BaseResource):
    def on_post(self, req: falcon.Request, resp: falcon.Response):
        data = req.context['data']
        username = data['username']
        password = data['password']

        user = models.User.find_by_username(self.session, username)
        if auth.verify_password(password, user.password.encode('utf-8')):
            body = {
                'user_id': user.user_id
            }
            token = jwt.encode(body, config.SECRET_KEY)
            resp.body = {
                'token': token.decode("utf-8")
            }
        else:
            resp.status = falcon.HTTP_BAD_REQUEST
