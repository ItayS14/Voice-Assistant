import 'package:flutter/material.dart';
import 'package:double_back_to_close_app/double_back_to_close_app.dart';

//Template for every page in the login system 
class AppTemplate extends StatelessWidget {
  final widgets;
  const AppTemplate({Key key, this.widgets}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return DoubleBackToCloseApp(
      child:  SingleChildScrollView(
        child: Container(
          margin: EdgeInsets.only(left: 25, right: 25),
          child: Column(
            children: widgets
          )
        )
      ),
      snackBar: SnackBar(
        content: Text('Tap back again to leave')
      )
    );
  }
}