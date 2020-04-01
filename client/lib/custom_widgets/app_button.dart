import 'package:flutter/material.dart';
//Buttons for the login system
class AppButton extends StatelessWidget {
  final func;
  final String text;

  const AppButton({Key key, @required this.func, @required this.text}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 70,
      width: double.infinity,
      child: RaisedButton(
              color: Colors.black87,
              textColor: Colors.white,
              child: Text(text, style: TextStyle(fontWeight: FontWeight.bold, fontSize: 20),),
              onPressed: func,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(4))
            )
    );
  }
}