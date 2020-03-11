import 'package:flutter/material.dart';
import 'package:client/app_template.dart';
import 'package:rflutter_alert/rflutter_alert.dart';
import 'package:speech_to_text/speech_recognition_result.dart';
import 'package:speech_to_text/speech_to_text.dart';
import 'package:client/utils/network.dart';
import 'package:flutter_tts/flutter_tts.dart';

class SpeechRecognitionScreen extends StatefulWidget {
  SpeechRecognitionScreen({Key key}) : super(key: key);

  @override
  _SpeechRecognitionScreenState createState() => _SpeechRecognitionScreenState();
}

class _SpeechRecognitionScreenState extends State<SpeechRecognitionScreen> {
  SpeechToText _speech;  
  FlutterTts _tts;
  bool _isAvailable = false;
  String _header = "Hello, How can i help you?";
  String _text = "";

  @override
  void initState(){
    super.initState();
    _initSpeechState();
    _initTts();
  }

  Future<void> _initTts() async {
    _tts = FlutterTts();
    await _tts.setLanguage("en-US");
    await _tts.setSpeechRate(1.0);
    await _tts.setVolume(1.0);
    await _tts.setPitch(1.0);
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
    if (res[0]) {  // If parsing didn't fail
      serverMethods(res[1]).then((newRes) {
        print(newRes);
        if (newRes[0]) { // If executing one of the commands didn't fail
          _infoAlert(newRes[1]);
        }
        else {
          _errorAlert(newRes);
        }
      });
    }
    else {
      _errorAlert(res);
    }

  }

  _errorAlert(text){
    Alert(context: context, title: 'Error', desc: '$text', type: AlertType.error).show();
    _tts.speak('Sorry, that command is not supported');
  }

  _infoAlert(text){
    Alert(context: context, title: 'Result', desc: '$text', type: AlertType.info).show();
    _tts.speak('$text');
  }
}