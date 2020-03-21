import 'package:client/screens/pass_reset.dart';
import 'package:flutter/material.dart';
import 'package:client/screens/login.dart';
import 'package:client/screens/register.dart';
import 'package:client/scaffold_setup.dart';
import 'package:client/screens/validate_code.dart';
import 'package:client/screens/new_password.dart';

void main() => runApp(MyApp());

class MyApp extends StatefulWidget{
  @override 
  State<StatefulWidget> createState() {
    return MyAppState();
  }
}
class MyAppState extends State<MyApp>{
    @override 
    Widget build(BuildContext context ){
      return MaterialApp(
        theme: ThemeData(primaryColor: Colors.black),
        initialRoute: '/login',
        routes: {
          '/main' : (_) => ScaffoldSetup(), 
          '/login' : (_) => _scaffoldWrap(LoginPage()),
          '/register': (_) => _scaffoldWrap(RegisterPage()),
          '/pass_reset': (_) => _scaffoldWrap((PassResetPage())),
          '/validate_code': (_) => _scaffoldWrap(ValidateCodePage(email:null)),
          '/new_password': (_) => _scaffoldWrap(NewPasswordPage(token: null))
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

