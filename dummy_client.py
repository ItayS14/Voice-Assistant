import requests

SERVER_URL = 'http://localhost:5000'


def main():
    s = requests.Session()

    print('Login: ', login(s, 'abc', 'asfdF123123411').text)
    print('Register: ', register(s, 'abc', 'asfdF123123411', 'avs@gmail.com').text)
    print('Logout: ', logout(s).text)
    print('Logout: ', logout(s).text)

def register(s, username, password, email):
    """
    The function will register to the server
    :param s: The requests session (requests.Session)
    :return: requests.Response
    """
    register_data = {
        'username' : username,
        'password' : password,
        'email' : email
    }

    return s.post(SERVER_URL + '/register', register_data)


def login(s, auth, password):
    """
    The function will login to the server
    :param s: The requests session (requests.Session)
    :return: requests.Response
    """
    login_data = {
        'auth' : auth,
        'password' : password,
    }

    return s.post(SERVER_URL + '/login', login_data)


def logout(s):
    """
    The function will logout a user from the server
    :param s: The requests session (requests.Session)
    :return: requests.Response
    """
    return s.get(SERVER_URL + '/logout')

if __name__ == '__main__':
    main()