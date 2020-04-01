import 'package:flutter/material.dart';

class BottomButton extends StatelessWidget {
  final String text;
  final String buttonText;
  final onPressed;

  const BottomButton({Key key, @required this.text, @required this.buttonText, @required this.onPressed}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Row(
    mainAxisAlignment: MainAxisAlignment.center,
    children: <Widget>[
      Text(text, style: TextStyle(fontWeight: FontWeight.w300),),
      FlatButton(
        child: Text(buttonText, style: TextStyle(color: Colors.blue)),
        onPressed: onPressed
      )]
    );
  }
}