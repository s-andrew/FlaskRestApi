from flask import request, jsonify, make_response


def create(decorated_function):
    entity = request.get_json()
    entity_id, entity = decorated_function(entity)
    response = make_response(jsonify(entity), 201)
    response.headers['Location'] = request.path + str(entity_id)
    return response


def readall(decorated_function):
    return jsonify(decorated_function())


def readone(decorated_function, entity_id):
    entity = decorated_function(entity_id)
    return jsonify(entity)


def update(decorated_function, entity_id):
    entity = request.get_json()
    return jsonify(decorated_function(entity_id, entity)), 201


def delete(decorated_function, entity_id):
    decorated_function(entity_id)
    return '', 204
