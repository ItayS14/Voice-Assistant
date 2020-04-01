import 'package:flutter/material.dart';
import 'package:client/screens/profile.dart';
import 'package:client/screens/speech.dart';

class ScaffoldSetup extends StatefulWidget {
  ScaffoldSetup({Key key}) : super(key: key);

  @override
  _ScaffoldSetupState createState() => _ScaffoldSetupState();
}

class _ScaffoldSetupState extends State<ScaffoldSetup> {
  int _selectedIndex = 0;
  final _pageOptions = <Widget>[
    SpeechRecognitionScreen(),
    ProfilePage()
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
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
    );
  }
}