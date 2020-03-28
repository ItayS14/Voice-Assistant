import 'package:client/screens/new_password.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:client/app_template.dart';
import 'package:client/custom_widgets/app_form.dart';
import 'package:client/custom_widgets/app_button.dart';
import 'package:rflutter_alert/rflutter_alert.dart';
import 'package:client/utils/network.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:client/config.dart';

// CupertinoActivityIndicator
class CodeScreenArguments {
  final String email;
  CodeScreenArguments(this.email);
}

class ValidateCodePage extends StatelessWidget {
  final _formKey = GlobalKey<FormState>();
  final int codeLen = 6;
  String code;

  ValidateCodePage({Key key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final CodeScreenArguments args = ModalRoute.of(context).settings.arguments;
    return AppTemplate(
      widgets: <Widget>[
        Align(
        alignment: Alignment.topLeft,      
        child: IconButton(
        icon: Icon(Icons.home),
        onPressed: () {
          Navigator.pushNamedAndRemoveUntil(context, "/login", (r) => false);
        },
        tooltip: 'Go back home',
        color: Colors.teal,
        iconSize: 40,
        ),
        ),
        Container(
          child: Image.asset('assets/voice_asistant_icon.png', scale: 2),
          alignment: Alignment.center,
          height: MediaQuery.of(context).size.height * 0.5
        ),
        Text(
          'A $codeLen-characters code has been sent to your email. Check it out and put it right here.',
           style: GoogleFonts.lora(),
         ),
        SizedBox(height: 30),
        Form(
          key: _formKey,
          child: AppForm(
            hint: 'Please enter the code here',
            onSaved: (input) => code = input.toUpperCase(),
            maxLength: codeLen,
          )
        ),
        SizedBox(height: 30),
        AppButton(
          text: 'Submit',
          func: () {
            _sendRequest(context, args.email);  
          },
         ),
      ]
    );
  }
  _sendRequest(BuildContext context, String email) {
    _formKey.currentState.save();
    validateCode(code,email).then((res) {
      if (res[0]) {
        Navigator.pushNamed(context,
          '/new_password',
          arguments: NewPassScreenArguments(res[1]['token']),
          );
      } else {
        Alert(context: context, title: "Server Error", desc: ProtocolErrors[res[1] - 1], type: AlertType.error).show(); //For now
      }
    });
  }
}