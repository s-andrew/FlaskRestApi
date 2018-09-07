from collections import namedtuple

from flask import abort, jsonify, make_response, request, Flask

from .abstract_resource import AbstractResource

Resource = namedtuple('Resource', 'resource url_prefix id_type')
PageRequest = namedtuple('PageRequest', 'page quantity')


class PageRequestNotFound(Exception):
    pass


def get_page_request(default: dict=None, names: dict=None, exc_if_params_not_exist: bool=False):
    if default is None:
        default = dict(page=1, quantity=25)
    if names is None:
        names = dict(page='p', quantity='q')
    p = request.args.get(names['page'])
    q = request.args.get(names['quantity'])
    if exc_if_params_not_exist and (p is None or q is None):
        raise PageRequestNotFound('GET parameters {} and {} not found'.format(names['page'], names['quantity']))
    if not p.isdigit():
        raise TypeError('GET param {} must be int'.format(names['page']))
    if not q.isdigit():
        raise TypeError('GET param {} must be int'.format(names['quantity']))
    p = int(p) if p is not None else default['page']
    q = int(q) if q is not None else default['quantity']
    return PageRequest(p, q)


def abort_json(message: str, code: int):
    return abort(make_response(jsonify(message=message), code))


class FlaskRestApi:
    def __init__(self, resources: list=None):
        if resources is None:
            resources = []
        self.resources = resources
        return

    def add_resource(self, resource: AbstractResource, url_prefix: str, id_type: str=None):
        if url_prefix[0] != '/':
            raise ValueError('urls must start with a leading slash')
        self.resources.append(Resource(resource, url_prefix, id_type))
        return self

    def registration(self, app: Flask, url_prefix: str='/'):
        if url_prefix[0] != '/':
            raise ValueError('urls must start with a leading slash')
        if url_prefix[-1] == '/':
            url_prefix = url_prefix[:-1]
        for resource_pack in self.resources:
            resource = resource_pack.resource
            resource_url = resource_pack.url_prefix
            if resource_url[-1] != '/':
                resource_url += '/'
            url = url_prefix + resource_url
            id_type = resource_pack.id_type
            self.__registration_resource(app, resource, url, id_type=id_type)

    @staticmethod
    def __registration_resource(app: Flask, resource: AbstractResource, url: str, id_type: str=None):
        url_with_id = url + '<{}entity_id>'.format('' if id_type is None else id_type + ':')
        endpoint_prefix = url.replace('/', '_')
        app.add_url_rule(url, view_func=resource.get_create_view_func(),
                         methods=['POST'], endpoint=endpoint_prefix+'create')
        app.add_url_rule(url, view_func=resource.get_readall_view_func(),
                         methods=['GET'], endpoint=endpoint_prefix+'readall')
        app.add_url_rule(url_with_id, view_func=resource.get_readone_view_func(),
                         methods=['GET'], endpoint=endpoint_prefix+'readone')
        app.add_url_rule(url_with_id, view_func=resource.get_update_view_func(),
                         methods=['PUT'], endpoint=endpoint_prefix+'update')
        app.add_url_rule(url_with_id, view_func=resource.get_delete_view_func(),
                         methods=['DELETE'], endpoint=endpoint_prefix+'delete')
