import 'package:flutter/material.dart';
import 'package:client/app_template.dart';
import 'package:speech_to_text/speech_recognition_result.dart';
import 'package:speech_to_text/speech_to_text.dart';
import 'package:requests/requests.dart';

class SpeechRecognitionScreen extends StatefulWidget {
  SpeechRecognitionScreen({Key key}) : super(key: key);

  @override
  _SpeechRecognitionScreenState createState() => _SpeechRecognitionScreenState();
}

class _SpeechRecognitionScreenState extends State<SpeechRecognitionScreen> {
  SpeechToText _speech;  
  bool _isAvailable = false;
  String _text = "Hello, How can i help you?";
  
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
          child: Text(_text, style: TextStyle(fontSize: 25),),
        ),
        Align(
          alignment: Alignment.bottomCenter,
          child: GestureDetector(
            child: FloatingActionButton(
                child: Icon(Icons.mic),
            ),
            onLongPress: () {
              print('listening');
              _startListening();
            },
            onLongPressEnd: (LongPressEndDetails _) {
              print('Stoped listening: $_text');
              _stopListening();
            },
          )
        )
      ],
    );
  }

  _startListening() {
    if (_isAvailable){
      _speech.listen(onResult: (SpeechRecognitionResult result) {
          _text = "${result.recognizedWords} - ${result.finalResult}";
        });
      }
    setState(() { });
  }

  _stopListening() {
    _speech.stop();
    setState(() {});
  }
}