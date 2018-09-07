import datetime

from flask_rest_api.crud_router import CrudRouter
from flask_rest_api import abort_json, get_page_request, PageRequestNotFound

from dao import PostDAO, PostDoesntExist

post_router = CrudRouter()
posts = PostDAO()


def abort_if_id_doesnt_exist(post_id):
    abort_json("Post with id={} doesn't exist".format(post_id), 404)


def post_date_preprocessor(post):
    post['date'] = datetime.datetime.strptime(post['date'], "%Y-%m-%d %H:%M:%S")
    return


@post_router.create
def create_post(post):
    post_date_preprocessor(post)
    post_id, post = posts.create_post(post)
    return post_id, post


@post_router.readall
def get_all_posts():
    try:
        page, quantity = get_page_request(exc_if_params_not_exist=True)
    except PageRequestNotFound:
        return posts.get_all_posts()
    return posts.get_posts_limit_offset(quantity, (page - 1) * quantity)


@post_router.readone
def get_post(post_id):
    try:
        return posts.get_post(post_id)
    except PostDoesntExist:
        abort_if_id_doesnt_exist(post_id)


@post_router.update
def update_post(post_id, post):
    post_date_preprocessor(post)
    try:
        return posts.update_post(post_id, post)
    except PostDoesntExist:
        abort_if_id_doesnt_exist(post_id)


@post_router.delete
def delete_post(post_id):
    try:
        return posts.delete_post(post_id)
    except PostDoesntExist:
        abort_if_id_doesnt_exist(post_id)
