import falcon.status_codes as status

from marshmallow import ValidationError

from example.errors import HTTPError  # it's our new HTTPError
from example import log


class SerializerMiddleware:

    def process_resource(self, req, resp, resource, params):
        req_data = req.context.get('data') or req.params
        log.LOG.debug('Going to find serializer')
        try:
            serializer = resource.serializers[req.method.lower()]
            log.LOG.debug('serializer FOUND')
        except (AttributeError, IndexError, KeyError):
            log.LOG.debug('Cannot find serializer')
            return
        else:
            try:
                log.LOG.debug('Going to validate body : {}'.format(req_data))
                req.context['serializer'] = serializer().load(
                    data=req_data
                ).data
            except ValidationError as err:
                raise HTTPError(status=status.HTTP_422, errors=err.messages)
