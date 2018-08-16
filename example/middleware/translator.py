import json
import falcon
from example import log


class JSONTranslator(object):
    def process_request(self, req: falcon.Request, _):
        log.LOG.debug('JSONTranslator-> Process request')
        if req.method == 'GET':
            log.LOG.debug('JSONTranslator->  Method is GET')
            return
        log.LOG.debug('JSONTranslator-> Method is POST')
        if req.content_type == 'application/json':
            try:
                raw_json = req.stream.read()
            except Exception:
                message = 'Read Error'
                raise falcon('Bad request', message)
            req.context['data'] = json.loads(raw_json.decode('utf-8'))

        else:
            req.context['data'] = None

    def process_response(self, _: falcon.Request, resp: falcon.Response, resource=None):
        log.LOG.debug('JSONTranslator-> Process response')

        if resp.body:
            log.LOG.debug('JSONTranslator-> body : {}'.format(resp.body))
            #resp.body = json.dumps(resp.body, ensure_ascii=False)
