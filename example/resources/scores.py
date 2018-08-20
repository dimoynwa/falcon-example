import falcon
import json
from example.db import models
from example.resources import BaseResource
from example import log
from example.schemas import schema


class ScoreResource(BaseResource):
    serializers = {
        'post': schema.ScorePostSchema,
        'put': schema.ScorePutSchema
    }

    def on_get(self, _: falcon.Request, resp: falcon.Response):
        model_list = models.Score.get_all(self.session)
        scores = [model.as_dict for model in model_list]

        log.LOG.debug('Found {} scores in DB'.format(scores.__len__()))

        resp.body = scores

    def on_post(self, req: falcon.Request, resp: falcon.Response):
        js = req.context['data']
        log.LOG.debug('Data : {}'.format(js))
        sc = models.Score(js['username'], js['company'], js['score'])
        sc.save(self.session)

        resp.body = {
            'id': sc.id
        }
        resp.status = falcon.HTTP_CREATED

    def on_put(self, req: falcon.Request, resp: falcon.Response):
        js = req.context['data']
        sc = models.Score(username=js['username'], id=js['id'], company=js['company'], score=js['score'])
        sc.save(self.session)
        resp.body = sc
        resp.status = falcon.HTTP_OK
