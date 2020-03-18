import 'package:requests/requests.dart';

const SERVER_URL = 'http://10.0.0.24:5000';
const ROUTES = ['translate', 'exchange', 'search', 'calculate'];
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

dynamic parse(String query) async {
  final res = await Requests.get('$SERVER_URL/parse/$query');
  return res.json();
}


dynamic translate(String language, String content) async {
  final res = await Requests.get('$SERVER_URL/translate?dest_lang=$language&data=$content');
  return res.json();
}

dynamic exchange(String from_coin, String to_coin, String amount) async { // change string to int on server and here
  final res = await Requests.get('$SERVER_URL/translate?from_coin=$from_coin&to_coin=$to_coin&amount=$amount');
  return res.json();
}

dynamic calculate(String expression) async {
  final res = await Requests.get('$SERVER_URL/calculate?expresion=$expression');
  return res.json;
}

dynamic getPasswordResetToken(String email) async {
  final res = await Requests.post('$SERVER_URL/get_password_reset_token',
  body: {
    'email': email
  },
  bodyEncoding: RequestBodyEncoding.FormURLEncoded);
  return res.json();
}

dynamic validateCode(String code, String email) async {
  final res = await Requests.post('$SERVER_URL/validate_code',
  body: {
    'code': code,
    'email': email
  },
  bodyEncoding: RequestBodyEncoding.FormURLEncoded);
  return res.json();
}

dynamic newPassword(String token, String password) async {
  final res = await Requests.post('$SERVER_URL/new_password/$token',
  body: {
    'password': password,
  },
  bodyEncoding: RequestBodyEncoding.FormURLEncoded);
  return res.json();
}

dynamic serverMethods(Map<String, dynamic> params) async {
  String route = ROUTES[params['route'] - 100];
  String paramsEncoded = encodeMap(params["params"]);
  final res = await Requests.get('$SERVER_URL/$route?$paramsEncoded');
  print('$SERVER_URL/$route?$paramsEncoded');
  return res.json();
}

String encodeMap(Map data) {
  return data.keys.map((key) => "${Uri.encodeComponent(key)}=${Uri.encodeComponent(data[key])}").join("&");
}