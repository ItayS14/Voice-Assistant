import 'package:flutter/material.dart';
import 'package:client/screens/login.dart';
import 'package:client/screens/register.dart';
import 'package:client/scaffold_setup.dart';

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

