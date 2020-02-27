import 'package:flutter/material.dart';
import 'package:client/login_system_template.dart';

class SpeechRecognitionScreen extends StatefulWidget {
  SpeechRecognitionScreen({Key key}) : super(key: key);

  @override
  _SpeechRecognitionScreenState createState() => _SpeechRecognitionScreenState();
}

class _SpeechRecognitionScreenState extends State<SpeechRecognitionScreen> {
  @override
  Widget build(BuildContext context) {
    return LoginSystemTemplate(
      widgets: <Widget>[
        Container(
          height: MediaQuery.of(context).size.height * 0.8,
          padding: EdgeInsets.symmetric(vertical: MediaQuery.of(context).size.height * 0.1),
          alignment: Alignment.topLeft,
          child: Text('Hello world! Translate what a beautifull day to Hebrew', style: TextStyle(fontSize: 25),),
        ),
        Align(
          alignment: Alignment.bottomCenter,
          child: FloatingActionButton(
              onPressed:  () {},
              child: Icon(Icons.mic),
            )
        )
      ],
    );
  }
}