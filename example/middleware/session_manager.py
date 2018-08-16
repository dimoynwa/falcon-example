import falcon
from example import log


class DatabaseSessionManager(object):
    def __init__(self, session):
        self.session_maker = session

    def process_resource(self, _: falcon.Request, __: falcon.Response, resource, params):
        resource.session = self.session_maker()

    def process_response(self, _: falcon.Request, __: falcon.Response, resource, req_succeeded):
        if hasattr(resource, 'session'):
            if not req_succeeded:
                log.LOG.debug('Request not successful')
                resource.session.rollback()
            self.session_maker.remove()
