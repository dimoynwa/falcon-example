import falcon.status_codes as status

from marshmallow import ValidationError

from example.errors import HTTPError  # it's our new HTTPError


class SerializerMiddleware:

    def process_resource(self, req, resp, resource, params):
        req_data = req.context.get('data') or req.params

        try:
            serializer = resource.serializers[req.method.lower()]
        except (AttributeError, IndexError, KeyError):
            return
        else:
            try:
                req.context['serializer'] = serializer().load(
                    data=req_data
                ).data
            except ValidationError as err:
                raise HTTPError(status=status.HTTP_422, errors=err.messages)