import requests
import json
import datetime

URL = 'http://localhost:8765/api/'

REGISTER = 'account/register/'
CHANGE_PASSWORD = 'account/change_password/'
UPDATE_USER = 'account/update/'
TOKEN = 'token/'
TOKEN_REFRESH = f'{TOKEN}refresh/'
TASKS = 'tasks/'
TASKS_CHILD = f'{TASKS}child/'


USERNAME = 'test111'
EMAIL = 'test111@example.invalid'
PASSWORD = 'test111test111'

NEW_USERNAME = 'test1111'
NEW_EMAIL = 'test1111@example.invalid'
NEW_PASSWORD = 'test1111test1111'


def register(username, email, password1, password2):
    data = {
        'username': username,
        'password1': password1,
        'password2': password2,
        'email': email,
    }

    return requests.post(
        url=f'{URL}{REGISTER}',
        data=data
    )


def update_user(token, user_id, new_username, new_email):
    headers = get_headers(token)

    data = {
        'username': new_username,
        'email': new_email
    }

    return requests.put(
        url=f'{URL}{UPDATE_USER}{user_id}',
        headers=headers,
        data=data
    )


def change_password(token, user_id, old_password, new_password1, new_password2):
    headers = get_headers(token)
    
    data = {
        'old_password': old_password,
        'new_password1': new_password1,
        'new_password2': new_password2
    }

    return requests.put(
        url=f'{URL}{CHANGE_PASSWORD}{user_id}',
        headers=headers,
        data=data
    )


def get_token(username, password):
    data = {
        'username': username,
        'password': password
    }

    response = requests.post(
        url=f'{URL}{TOKEN}',
        data=data
    )

    content = json.loads(response.content)

    refresh_token = content['refresh']
    access_token = content['access']
    user_id = content['user_id']

    return refresh_token, access_token, user_id


def get_refresh_token(refresh):
    data = {
        'refresh': refresh
    }

    response = requests.post(
        url=f'{URL}{TOKEN_REFRESH}',
        data=data
    )

    content = json.loads(response.content)

    refresh_token = content['refresh']
    access_token = content['access']

    return refresh_token, access_token


def get_headers(token):
    return {
        'Authorization': f'Bearer {token}'
    }


def get_tasks(token, user_id):
    headers = get_headers(token)

    data = {
        'user': user_id
    }

    response = requests.get(
        url=f'{URL}{TASKS}',
        headers=headers,
        data=data
    )

    return json.loads(response.content)


def get_task_detail(token, user_id, task_id):
    headers = get_headers(token)

    data = {
        'user': user_id
    }

    response = requests.get(
        url=f'{URL}{TASKS}{task_id}',
        headers=headers,
        data=data
    )

    return json.loads(response.content)


def get_task_child(token, user_id, task_id):
    headers = get_headers(token)

    data = {
        'user': user_id
    }

    response = requests.get(
        url=f'{URL}{TASKS_CHILD}{task_id}',
        headers=headers,
        data=data
    )

    return json.loads(response.content)


def create_task(token, user_id, parent_id=None, title=None, description=None, due_date=None):
    headers = get_headers(token)

    data = {
        'user': user_id,
        'parent': parent_id,
        'title': title,
        'description': description,
        'due_date': due_date,
    }

    response = requests.post(
        url=f'{URL}{TASKS}',
        headers=headers,
        data=data
    )

    return json.loads(response.content)


def update_task(token, user_id, task_id, new_title):
    headers = get_headers(token)

    data = {
        'user': user_id,
        'title': new_title
    }

    response = requests.put(
        url=f'{URL}{TASKS}{task_id}/',
        headers=headers,
        data=data
    )

    return json.loads(response.content)


def delete_task(token, user_id, task_id):
    headers = get_headers(token)

    data = {
        'user': user_id,
    }

    return requests.delete(
        url=f'{URL}{TASKS}{task_id}/',
        headers=headers,
        data=data
    )


if __name__ == '__main__':
    now = datetime.datetime.now()

    # response = register(USERNAME, EMAIL, PASSWORD, PASSWORD)

    # refresh_token, access_token, user_id = get_token(USERNAME, PASSWORD)
    # refresh_token, access_token = get_refresh_token(refresh_token)

    # response = change_password(access_token, user_id, PASSWORD, NEW_PASSWORD, NEW_PASSWORD)
    # response = update_user(access_token, user_id, NEW_USERNAME, NEW_EMAIL)

    # create_task(access_token, user_id, 'task1', 'description1', now)
    # create_task(access_token, user_id, 'task2', 'description2', now)
    # create_task(access_token, user_id, 'ede95c32-e161-4817-b27f-c73ea91ea2b1', 'task3', 'description3', now)
    # create_task(access_token, user_id, 'ede95c32-e161-4817-b27f-c73ea91ea2b1', 'task4', 'description4', now)
    # response = create_task('asdf', user_id, 'task5', 'description5', now)
    
    # update_task(access_token, user_id, 'c5acdca7-4aab-4700-ab2c-af2dd53e01b9', 'test task 456')
    # delete_task(access_token, user_id, '9c0cf6c0-c45b-422c-8e7e-73e5970ddb6d')
    
    # tasks = get_tasks(access_token, user_id)
    # task = get_task_detail(access_token, user_id, 'ede95c32-e161-4817-b27f-c73ea91ea2b1')
    # child = get_task_child('asdf', user_id, 'ede95c32-e161-4817-b27f-c73ea91ea2b1')