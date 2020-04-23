import 'dart:convert';
import 'dart:io';
import 'dart:async';
import 'package:requests/requests.dart';


// The class handles all the network activities of the application
class NetworkHandler {
  static const _serverUrl = 'http://10.0.0.24:5000';
  static final NetworkHandler _networkHandler = NetworkHandler._internal();

  NetworkHandler._internal();
  
  // This class is a "singleton", meaning there is only one instance of it, no matter where it's called in the code.
  factory NetworkHandler() {
    return _networkHandler;
  }
  
  /*
    This function will send a request to the server
    Input: the parameters to send in the request, route to go to in the server and get or post request
    Output: a list representing the response
  */
  Future<dynamic> _generalRequest(params, route, { isGetRequest = true }) async {
    var responseJson;
    try {
      print(params);
      Response response;
      if(isGetRequest) 
        response = await Requests.get(_serverUrl +  route + _encodeMap(params), timeoutSeconds: 30);
      else 
        response = await  Requests.post(_serverUrl + route, body: params, bodyEncoding: RequestBodyEncoding.FormURLEncoded, timeoutSeconds: 30);
      response.throwForStatus();
      responseJson = json.decode(response.content());
    }
    on HTTPException catch (e) {
      return [false, 'HTTP Error, status code: ${e.response.statusCode}'];
    }
    catch (e) {
      print(e);
      return [false, 'General error\nplease close the app and try again.'];
    }
    return responseJson;
  }
  
  /*
    This function will encode the parameters for the GET request (if there are any)
    Input: a dictionary of the names and values of the parameters
    Output: a string representing the names and values of the parameters ("?key1=value1&key2=value2...")
  */
  String _encodeMap(Map data) {
    return data == null ? '' : '?' + data.keys.map((key) => "${Uri.encodeComponent(key)}=${Uri.encodeComponent(data[key])}").join("&");
  }

  // The function will call the /parse route in the server and will return its response
  Future<dynamic> parse(String query) async {
    return _generalRequest({'text' : query}, '/parse');
  } 
  
  /*
    This function will call any of the server methods (for example, translate or calculate) and will return the response
    Input: a dictionary containing the route to call in the server and parameters to pass to that route
    Output: the response from the server to the request
  */
  Future<dynamic> serverMethods(Map<String, dynamic> params) async {
    String route = params['route'];
    var body = params['params'];
    return _generalRequest(body, route);
  } 

  // The function will perform a login for the user to the app with its credentials 
  Future<dynamic> login(String auth, String password) async {
    var params =  {
      'auth': auth, 
      'password': password
    };

    return _generalRequest(params, '/login', isGetRequest: false);
  }

  // The function will logout the user from the app
  Future<dynamic> logout() async {
    return  _generalRequest(null, '/logout');
  }

  // The function will register a user to the application
  Future<dynamic> register(String username, String password, String email) async {
    var params =  {
      'username': username, 
      'password': password,
      'email': email
    };
    var res =  _generalRequest(params, '/register', isGetRequest: false);
    return res;
  }

  // The function will request the server to send a reset token to an email
  Future<dynamic> getPasswordResetToken(String email) async {
    var params = {
      'email': email
    };
    return _generalRequest(params, '/get_password_reset_token',isGetRequest: false);
  }

  // The function will send a requesst to the server to validate the code
  Future<dynamic> validateCode(String code, String email) async {
    var params = {
      'code': code,
      'email': email
    };
    return _generalRequest(params, '/validate_code',isGetRequest: false);
  }

  // The function will update the password stored for a user
  Future<dynamic> newPasswordRequest(String token, String password) async {
    var params = {
      'password': password,
    };
    return _generalRequest(params, '/new_password/$token',isGetRequest: false);
  }

  // The function will call the profile route in the server and will return its response 
  // The response contains the name, email and image of the user
  Future<dynamic> profile() async {
    return _generalRequest(null, '/profile');
  }
  
  /*
    This function will upload an image to the server
    input: File image - the image file to upload
    output: Future<dynamic> - result from the server 
  */
  Future<dynamic> uploadImage(File image) async {
    var params =  {
      'file_name': image.path.split('/').last,
      'img': base64Encode(image.readAsBytesSync()) // The server need the img to be encoded as base64
    };
    return _generalRequest(params, '/update_img', isGetRequest: false);
  }

  // The function will clear the cookies stored in the shared preferences
  void deleteCookies() => Requests.clearStoredCookies(Requests.getHostname(_serverUrl));
}