import 'package:flutter/material.dart';
import 'package:client/login.dart';
import 'package:client/register.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget{
    @override 
    Widget build(BuildContext context){
      return MaterialApp(
        theme: ThemeData(primaryColor: Colors.black),
        home: LoginPage(),
        routes: {
          '/login' : (_) => LoginPage(),
          '/register': (_) => RegisterPage(),
        },
      );
    }
}

