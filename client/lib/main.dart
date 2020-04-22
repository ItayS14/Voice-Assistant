import 'package:client/screens/pass_reset.dart';
import 'package:flutter/material.dart';
import 'package:client/screens/login.dart';
import 'package:client/screens/register.dart';
import 'package:client/scaffold_setup.dart';
import 'package:client/screens/validate_code.dart';
import 'package:client/screens/new_password.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:requests/requests.dart';
import 'package:client/utils/network.dart';


bool remember;

void main() async {
  NetworkHandler _networkHandler = NetworkHandler();
  WidgetsFlutterBinding.ensureInitialized();
  SharedPreferences.getInstance().then((instance) {
    remember = instance.getBool('RememberMe') ?? false;
    if (!remember)
      _networkHandler.deleteCookies();
     runApp(MyApp());
  });

}

class MyApp extends StatefulWidget{
  @override 
  State<StatefulWidget> createState()  {
    return MyAppState();
  }
}
class MyAppState extends State<MyApp>{
    @override 
    Widget build(BuildContext context ){
      return MaterialApp(
        theme: ThemeData(primaryColor: Colors.black),
        initialRoute: remember ? '/main' : '/login',
        routes: {
          '/main' : (_) => ScaffoldSetup(), 
          '/login' : (_) => _scaffoldWrap(LoginPage()),
          '/register': (_) => _scaffoldWrap(RegisterPage()),
          '/pass_reset': (_) => _scaffoldWrap((PassResetPage())),
          '/validate_code': (_) => _scaffoldWrap(ValidateCodePage()),
          '/new_password': (_) => _scaffoldWrap(NewPasswordPage())
        },
      );
    }

    // Wrapping a page inside a scaffold widget
    _scaffoldWrap(Widget page) {
      return Scaffold(
        body: page
      );
    } 
}

