import 'package:flutter/material.dart';

class ProfileTextBox extends StatelessWidget {
  String text;
  String header;

  ProfileTextBox({Key key, @required this.text, @required this.header}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: <Widget>[
        Padding(
          padding: EdgeInsets.only(bottom: 3),
          child:Text(header)
        ),
        Container(
              child: Text(text),
              padding: EdgeInsets.all(10),
              alignment: Alignment.centerLeft,
              decoration: BoxDecoration(
                border: Border.all()
              ),
        ),
      ],
    );
  }
}