from datetime import datetime, date

from bson.objectid import ObjectId

from flask import Flask
from flask.json import JSONEncoder

from flask_rest_api import FlaskRestApi
# from post_api_class import PostApi
from post_api_router import post_router


class MongoJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(0, (datetime, date)):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)


def app_factory():
    app = Flask(__name__)
    app.json_encoder = MongoJSONEncoder

    FlaskRestApi() \
        .add_resource(post_router, '/posts', id_type='string') \
        .registration(app)

    @app.route('/')
    def index():
        return 'This is home page!'

    return app
