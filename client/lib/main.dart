import 'package:flutter/material.dart';
import 'package:client/screens/login.dart';
import 'package:client/screens/register.dart';
import 'package:client/screens/speech.dart';
import 'package:client/screens/profile.dart';

void main() => runApp(MyApp());

class MyApp extends StatefulWidget{
  @override 
  State<StatefulWidget> createState() {
    return MyAppState();
  }
}
class MyAppState extends State<MyApp>{
  int _selectedIndex = 0;
  final _pageOptions = <Widget>[
    SpeechRecognitionScreen(),
    ProfilePage()
  ];

    @override 
    Widget build(BuildContext context ){
      return MaterialApp(
        theme: ThemeData(primaryColor: Colors.black),
        home: Scaffold(
          body: _pageOptions[_selectedIndex],
          bottomNavigationBar:  BottomNavigationBar(
          items: const <BottomNavigationBarItem>[
              BottomNavigationBarItem(
                icon: Icon(Icons.home),
                title: Text("Home")
              ),
              BottomNavigationBarItem(
                icon: Icon(Icons.person),
                title: Text("Profile")
              )
            ],
            selectedItemColor: Colors.blue[800],
            currentIndex: _selectedIndex,
            onTap: (int index) {
              setState(() {
                _selectedIndex = index;
              });
            },
          )
        ),
        routes: {
          '/login' : (_) => LoginPage(),
          '/register': (_) => RegisterPage(),
        },
      );
    }
}

