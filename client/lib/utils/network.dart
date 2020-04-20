import 'dart:convert';
import 'dart:io';
import 'package:client/utils/app_exceptions.dart';
import 'dart:async';
import 'package:requests/requests.dart';



class NetworkHandler {
  static const _serverUrl = 'http://10.0.2.2:5000';
  static final NetworkHandler _networkHandler = NetworkHandler._internal();

  NetworkHandler._internal();

  
  factory NetworkHandler() {
    return _networkHandler;
  }

  Future<dynamic> _generalRequest(params, route, { isGetRequest = true }) async {
    var responseJson;
    try {
      if(isGetRequest) {
        String encodeParams = _encodeMap(params);
        final response = await Requests.get(_serverUrl +  route + (encodeParams == null ? '' : '?' + _encodeMap(params)));
        responseJson = _returnResponse(response);
      }
      else {
        final response = await  Requests.post(_serverUrl + route, body: params, bodyEncoding: RequestBodyEncoding.FormURLEncoded);
        responseJson = _returnResponse(response);
      }
    }
    catch (e)
    {
      return [false, 16];
    }
    return responseJson;
  }

  dynamic _returnResponse(Response response) {
    switch (response.statusCode) {
      case 200:
        return json.decode(response.content());
      case 400:
        throw BadRequestException(response.toString());
      case 401:
      case 403:
        throw UnauthorisedException(response.toString());
      case 500:
      default:
        throw FetchDataException(
            'Error occured while Communication with Server with StatusCode : ${response.statusCode}');
    }
  }

  String _encodeMap(Map data) {
    return data == null ? null : data.keys.map((key) => "${Uri.encodeComponent(key)}=${Uri.encodeComponent(data[key])}").join("&");
  }

  dynamic parse(String query) async {
    return  _generalRequest(null, '/parse/$query');
  } 

  dynamic serverMethods(Map<String, dynamic> params) async {
    String route = params['route'];
    var body = params['params'];
    return  _generalRequest(body, route);
  } 

  dynamic login(String auth, String password) async {
    var params =  {
      'auth': auth, 
      'password': password
    };

    return _generalRequest(params, '/login', isGetRequest: false);
  }

  // The function will logout the user from the app
  dynamic logout() async {
    return  _generalRequest(null, '/logout');
  }

  // The function will register a user to the application
  dynamic register(String username, String password, String email) async {
    var params =  {
      'username': username, 
      'password': password,
      'email': email
    };
    var res =  _generalRequest(params, '/register', isGetRequest: false);
    //if(res[0])
      //Requests.clearStoredCookies(Requests.getHostname(_serverUrl));
    return res;
  }

  dynamic getPasswordResetToken(String email) async {
    var params = {
      'email': email
    };
    return _generalRequest(params, '/get_password_reset_token',isGetRequest: false);
  }

  dynamic validateCode(String code, String email) async {
    var params = {
      'code': code,
      'email': email
    };
    return await _generalRequest(params, '/validate_code',isGetRequest: false);
  }

  dynamic newPasswordRequest(String token, String password) async {
    var params = {
      'password': password,
    };
    return await _generalRequest(params, '/new_password',isGetRequest: false);
  }

  dynamic profile() async {
    return await _generalRequest(null, '/profile');
  }
  
  dynamic uploadImage(File image) async {
    var params =  {
      'file_name': image.path.split('/').last,
      'img': base64Encode(image.readAsBytesSync())
    };
    return await _generalRequest(params, '/update_img', isGetRequest: false);
  }

  void deleteCookies() => Requests.clearStoredCookies(Requests.getHostname(_serverUrl));
}