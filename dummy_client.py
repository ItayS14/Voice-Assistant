import requests

SERVER_URL = 'http://localhost:5000'


def main():
    s = requests.Session()

    #print('Login: ', login(s, 'abc', 'asfdF123123411').text)
    #print('Request: ', request_reset_password(s,'jday.david.2002@gmail.com').text)
    print('Reset: ', reset_password(s,'eyJ1c2VyX2lkIjoxfQ.XeqPBw.ZODG4SO9kGiQ8acGbptsAX3cOEU','212456724716714256471asdf78aA'))
    #print('Logout: ', logout(s))


def register(s, username, password, email):
    """
    The function will register to the server
    :param s: The requests session (requests.Session)
    :return: requests.Response
    """
    register_data = {
        'username': username,
        'password': password,
        'email': email
    }

    return s.post(SERVER_URL + '/register', register_data)


def login(s, auth, password):
    """
    The function will login to the server
    :param s: The requests session (requests.Session)
    :return: requests.Response
    """
    login_data = {
        'auth': auth,
        'password': password,
    }

    return s.post(SERVER_URL + '/login', login_data)


def logout(s):
    """
    The function will logout a user from the server
    :param s: The requests session (requests.Session)
    :return: requests.Response
    """
    return s.get(SERVER_URL + '/logout')


def request_reset_password(s,email):
    """
    This function will ask for a password reset (send an email to the user)
    :param s: The requests session (requests.Session)
    :return: requests.response
    """
    data = {
        'email':email
    }
    return s.post(SERVER_URL + "/password_reset",data)


def reset_password(s, token, new_password):
    """
    This function will reset the password with a token
    :param s: The requests session (requests.Session)
    :param token: the validity token (str)
    :param new_password: the new password to change in the server (str)
    :return: requests.response
    """
    data = {
        'password': new_password
    }
    return s.post(SERVER_URL + "/password_reset/" + token, data)


if __name__ == '__main__':
    main()
