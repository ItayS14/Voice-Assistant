import 'package:flutter/material.dart';
import 'package:client/app_template.dart';
import 'package:rflutter_alert/rflutter_alert.dart';
import 'package:speech_to_text/speech_recognition_result.dart';
import 'package:speech_to_text/speech_to_text.dart';
import 'package:client/utils/network.dart';

class SpeechRecognitionScreen extends StatefulWidget {
  SpeechRecognitionScreen({Key key}) : super(key: key);

  @override
  _SpeechRecognitionScreenState createState() => _SpeechRecognitionScreenState();
}

class _SpeechRecognitionScreenState extends State<SpeechRecognitionScreen> {
  SpeechToText _speech;  
  bool _isAvailable = false;
  String _header = "Hello, How can i help you?";
  String _text = "";

  @override
  void initState(){
    super.initState();
    _initSpeechState();
  }

  Future<void> _initSpeechState() async {
    _speech  = SpeechToText();
    _isAvailable = await _speech.initialize();
  }

  @override
  Widget build(BuildContext context) {
    return AppTemplate(
      widgets: <Widget>[
        Container(
          height: MediaQuery.of(context).size.height * 0.8,
          padding: EdgeInsets.symmetric(vertical: MediaQuery.of(context).size.height * 0.1),
          alignment: Alignment.topLeft,
          child: Text(_header, style: TextStyle(fontSize: 25),),
        ),
        Text(_text),
        Align(
          alignment: Alignment.bottomCenter,
          child: RaisedButton(
            child: Icon(Icons.mic),
            onPressed: _startListening    
          ),
        )
      ],
    );
  }

  _startListening() {
    _header = "I'm listening...";
    setState(() {});
    if (_isAvailable) {
      _speech.listen(onResult: (SpeechRecognitionResult result) {
          _text = "${result.recognizedWords}";
          if(result.finalResult) {
            parse(_text).then(_onResult);
          }
          setState(() {});
      });
    }
  }

  _onResult(res) {
    Alert(context: context, title: 'Result', desc: '${res}', type: AlertType.info).show();
  }
}