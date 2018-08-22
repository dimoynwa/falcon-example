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

    def on_get(self, _: falcon.Request, resp: falcon.Response, **params):
        for the_key, the_value in params.items():
            log.LOG.debug('Param : {} : {}'.format(the_key, the_value))
        model_list = models.Score.get_all(self.session)
        scores = [model.as_dict for model in model_list]

        log.LOG.debug('Found {} scores in DB'.format(scores.__len__()))

        resp.body = scores

    def on_post(self, req: falcon.Request, resp: falcon.Response, **params):
        js = req.context['data']
        log.LOG.debug('Data : {}'.format(js))
        sc = models.Score(js['username'], js['company'], js['score'])
        sc.save(self.session)

        resp.body = {
            'id': sc.id
        }
        resp.status = falcon.HTTP_CREATED

    def on_put(self, req: falcon.Request, resp: falcon.Response, **params):
        js = req.context['data']
        sc = models.Score(username=js['username'], id=js['id'], company=js['company'], score=js['score'])
        sc.save(self.session)
        resp.body = sc
        resp.status = falcon.HTTP_OK


class SingleScoreResource(BaseResource):
    serializers = {
        'post': schema.ScorePostSchema,
        'put': schema.ScorePutSchema
    }

    def on_get(self, req: falcon.Request, resp: falcon.Response, score_id, **params):
        log.LOG.debug('Into Resource GET')
        score = models.Score.find_one(self.session, score_id)

        log.LOG.debug('Found score : {}'.format(score))

        resp.body = score.as_dict

    def on_put(self, req: falcon.Request, resp: falcon.Response, score_id, **params):
        log.LOG.debug('Into Resource PUT')

        score = models.Score.find_one(self.session, score_id)
        js = req.context['data']
        score.score = js['score']
        score.company = js['company']
        score.username = js['username']

        score.save(self.session)
