import requests


def get_user_repos(username):
    '''Функция, возращающая репозитория пользователя по имени на гитхабе'''
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)

    if response.status_code == 200:
        repositories_data = response.json()
        return repositories_data
    else:
        return None


def create_repo(access_token, repo_name, repo_descr=None):
    '''Создания репозитория по токену'''
    url = f"https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {access_token}",
    }
    data = {
        "name": repo_name,
        "description": repo_descr,
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        repo_data = response.json()
        return repo_data
    else:
        return None