import 'package:flutter/material.dart';

//Template for every page in the login system 
class LoginSystemTemplate extends StatelessWidget {
  final widgets;
  const LoginSystemTemplate({Key key, this.widgets}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
          child: Container(
            margin: EdgeInsets.only(left: 25, right: 25),
            child: Column(
              children: widgets
            )
          )
      )
    );
  }
}