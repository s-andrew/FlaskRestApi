from bson.objectid import ObjectId

import pymongo


class PostDoesntExist(Exception):
    pass


class PostDAO:
    def __init__(self):
        client = pymongo.MongoClient('localhost', 27017)
        self.posts = client.test_database.posts
        return

    def exist_post(self, post_id):
        print('Check post with id={}'.format(post_id))
        post = self.posts.find_one({'_id': ObjectId(post_id)})
        if post is None:
            raise PostDoesntExist("Post with id={} doesn't exist".format(post_id))
        print('Post with id={} exist!'.format(post_id))
        return

    def get_all_posts(self):
        return list(self.posts.find())

    def get_posts_limit_offset(self, limit, offset=0):
        return list(self.posts.find().skip(offset).limit(limit))

    def get_post(self, post_id):
        self.exist_post(post_id)
        return self.posts.find_one({'_id': ObjectId(post_id)})

    def create_post(self, post):
        post_id = self.posts.insert_one(post).inserted_id
        post = self.posts.find_one({'_id': ObjectId(post_id)})
        return post_id, post

    def delete_post(self, post_id):
        self.exist_post(post_id)
        self.posts.delete_one({'_id': ObjectId(post_id)})
        return

    def update_post(self, post_id, post):
        self.exist_post(post_id)
        self.posts.update_one({'_id': ObjectId(post_id)}, {'$set': post}, upsert=False)
        return self.posts.find_one({'_id': ObjectId(post_id)}, post)
