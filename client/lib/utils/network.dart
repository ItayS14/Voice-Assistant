import 'package:requests/requests.dart';

const SERVER_URL = 'http://10.0.2.2:5000';

// The function will login a user to the app
dynamic login(String auth, String password) async {
  final res = await Requests.post('$SERVER_URL/login', 
  body: {
    'auth': auth, 
    'password': password
  }, 
  bodyEncoding: RequestBodyEncoding.FormURLEncoded);
  return res.json();
}

// The function will logout the user from the app
dynamic logout() async {
  final res = await Requests.get('$SERVER_URL/logout');
  return res.json();
}

// The function will register a user to the appl
dynamic register(String username, String password, String email) async {
  final res = await Requests.post('$SERVER_URL/register', 
  body: {
    'username': username, 
    'password': password,
    'email': email
  },
  bodyEncoding: RequestBodyEncoding.FormURLEncoded); 
  return res.json();
}
