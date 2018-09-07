import datetime

from flask_rest_api.crud_resource import CrudResource
from flask_rest_api import abort_json, get_page_request, PageRequestNotFound
from dao import PostDAO, PostDoesntExist

posts = PostDAO()


def abort_if_id_doesnt_exist(post_id):
    abort_json("Post with id={} doesn't exist".format(post_id), 404)


def post_date_preprocessor(post):
    post['date'] = datetime.datetime.strptime(post['date'], "%Y-%m-%d %H:%M:%S")
    return


# class YourApiClass(CrudResource):
#     def create(self, post):
#         YOUR CODE
#
#     def readall(self):
#         YOUR CODE
#
#     def readone(self, post_id):
#         YOUR CODE
#
#     def update(self, post_id, post):
#         YOUR CODE
#
#     def delete(self, post_id):
#         YOUR CODE


class PostApi(CrudResource):
    def create(self, post):
        post_date_preprocessor(post)
        post_id, post = posts.create_post(post)
        return post_id, post

    def readall(self):
        try:
            page, quantity = get_page_request(exc_if_params_not_exist=True)
        except PageRequestNotFound:
            return posts.get_all_posts()
        return posts.get_posts_limit_offset(quantity, (page - 1) * quantity)

    def readone(self, post_id):
        try:
            return posts.get_post(post_id)
        except PostDoesntExist:
            abort_if_id_doesnt_exist(post_id)

    def update(self, post_id, post):
        post_date_preprocessor(post)
        try:
            return posts.update_post(post_id, post)
        except PostDoesntExist:
            abort_if_id_doesnt_exist(post_id)

    def delete(self, post_id):
        try:
            return posts.delete_post(post_id)
        except PostDoesntExist:
            abort_if_id_doesnt_exist(post_id)
