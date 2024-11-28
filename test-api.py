import requests
import json
import datetime

URL = 'http://localhost:8765/api/'

ACCOUNT = 'account/'
REGISTER = f'{ACCOUNT}register/'
DELETE = f'{ACCOUNT}delete/'
UPDATE_USER = f'{ACCOUNT}update/'
CHANGE_PASSWORD = f'{ACCOUNT}change_password/'

TOKEN = 'token/'
TOKEN_REFRESH = f'{TOKEN}refresh/'

TASKS = 'tasks/'


USERNAME = 'test1'
EMAIL = 'test1@example.invalid'
PASSWORD = 'test1test1'

NEW_USERNAME = 'test1111'
NEW_EMAIL = 'test1111@example.invalid'
NEW_PASSWORD = 'test1111test1111'


def register(username, email, password1, password2):
    data = {
        'username': username,
        'email': email,
        'password1': password1,
        'password2': password2,
    }

    response = requests.post(
        url=f'{URL}{REGISTER}',
        data=data
    )

    return json.loads(response.content)


def update_account(token, user_id, new_username, new_email):
    headers = get_headers(token)

    data = {
        'username': new_username,
        'email': new_email
    }

    response = requests.put(
        url=f'{URL}{UPDATE_USER}{user_id}',
        headers=headers,
        data=data
    )

    return json.loads(response.content)


def change_password(token, user_id, old_password, new_password1, new_password2):
    headers = get_headers(token)
    
    data = {
        'old_password': old_password,
        'new_password1': new_password1,
        'new_password2': new_password2
    }

    response = requests.put(
        url=f'{URL}{CHANGE_PASSWORD}{user_id}',
        headers=headers,
        data=data
    )

    return json.loads(response.content)


def delete_account(token, user_id):
    headers = get_headers(token)

    response = requests.delete(
        url=f'{URL}{DELETE}{user_id}',
        headers=headers
    )

    return json.loads(response.content)


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


def get_headers(token, user_id):
    return {
        'Authorization': f'Bearer {token}',
        'user': user_id
    }


def get_tasks(token, user_id):
    headers = get_headers(token, user_id)

    response = requests.get(
        url=f'{URL}{TASKS}',
        headers=headers,
    )

    return json.loads(response.content)


def get_task_detail(token, user_id, task_id):
    headers = get_headers(token, user_id)

    response = requests.get(
        url=f'{URL}{TASKS}{task_id}/',
        headers=headers,
    )

    return json.loads(response.content)


def create_task(token, user_id, parent_uuid=None, title=None, description=None, due_date=None):
    headers = get_headers(token, user_id)

    data = {
        'parent_uuid': parent_uuid,
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
    headers = get_headers(token, user_id)

    data = {
        'title': new_title
    }

    response = requests.put(
        url=f'{URL}{TASKS}{task_id}/',
        headers=headers,
        data=data
    )

    return json.loads(response.content)


def update_task_done_state(token, user_id, task_id, is_done):
    headers = get_headers(token, user_id)

    data = {
        'is_done': is_done
    }

    response = requests.put(
        url=f'{URL}{TASKS}{task_id}/',
        headers=headers,
        data=data
    )

    return json.loads(response.content)


def delete_task(token, user_id, task_id):
    headers = get_headers(token, user_id)

    response = requests.delete(
        url=f'{URL}{TASKS}{task_id}/',
        headers=headers,
    )

    return json.loads(response.content)


if __name__ == '__main__':
    now = datetime.datetime.now()

    # response = register(USERNAME, EMAIL, PASSWORD, PASSWORD)

    refresh_token, access_token, user_id = get_token(USERNAME, PASSWORD)
    # refresh_token, access_token = get_refresh_token(refresh_token)

    # response = change_password(access_token, user_id, PASSWORD, NEW_PASSWORD, NEW_PASSWORD)
    # response = update_account(access_token, user_id, NEW_USERNAME, NEW_EMAIL)
    # response = delete_account(access_token, user_id)

    # response = create_task(
    #     token=access_token,
    #     user_id=user_id,
    #     title='test1',
    #     description='description1',
    #     due_date=now
    # )

    # response = create_task(
    #     token=access_token,
    #     user_id=user_id,
    #     parent_uuid='',
    #     title='test2',
    #     description='description2',
    #     due_date=now
    # )
    
    # response = update_task(
    #     token=access_token,
    #     user_id=user_id,
    #     task_id='',
    #     new_title=''
    # )
    
    # response = delete_task(
    #     token=access_token,
    #     user_id=user_id,
    #     task_id=''
    # )

    # response = update_task_done_state(
    #     token=access_token,
    #     user_id=user_id,
    #     task_id='17fec1d4-d868-44ed-8854-9d68fce44d00',
    #     is_done=True
    # )

    # print(response)
    
    tasks = get_tasks(access_token, user_id)
    print(tasks)
    # task = get_task_detail(access_token, user_id, '')