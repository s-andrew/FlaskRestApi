import json
from requests import get, post, put, delete
from requests.models import Response
import datetime

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

new_post = {
    'author': 'Api Tester',
    'date': datetime.datetime(2018, 8, 21, 15, 55, 44, 830000).strftime("%Y-%m-%d %H:%M:%S"),
    'tags': ['rest', 'python', 'flask'],
    'text': "It's a new post!"
}

update_post = {
    'date': datetime.datetime(2018, 8, 21, 15, 55, 44, 830000).strftime("%Y-%m-%d %H:%M:%S"),
    'text': "It's a new post!"
}


def print_test(name: str, response: Response) -> None:
    try:
        text = response.json()
    except json.JSONDecodeError:
        text = response.reason
    print('{:<20} [{}] {!s}'.format(name, response.status_code, text))
    return


if __name__ == '__main__':
    print_test('Get all posts', get('http://localhost:5000/posts/'))
    create = post('http://localhost:5000/posts/', data=json.dumps(new_post), headers=headers)
    print_test('Create post', create)
    new_post_url = create.headers['Location']
    print_test('Fail create post', post('http://localhost:5000/posts/', data='Aloha!', headers=headers))
    print_test('Get created post', get(new_post_url))
    print_test('Update created post', put(new_post_url, data=json.dumps(update_post), headers=headers))
    print_test('Get all posts', get('http://localhost:5000/posts/'))
    print_test('Get page', get('http://localhost:5000/posts/?p=2&q=1'))
    print_test('Delete created post', delete(new_post_url))
    print_test('Get all posts', get('http://localhost:5000/posts/'))
