import 'package:flutter/material.dart';
import 'package:client/screens/login.dart';
import 'package:client/screens/register.dart';
import 'package:client/screens/speech.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget{
    @override 
    Widget build(BuildContext context){
      return MaterialApp(
        theme: ThemeData(primaryColor: Colors.black),
        home: SpeechRecognitionScreen(),
        routes: {
          '/login' : (_) => LoginPage(),
          '/register': (_) => RegisterPage(),
        },
      );
    }
}

