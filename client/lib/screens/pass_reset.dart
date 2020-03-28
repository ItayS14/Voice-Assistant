import 'package:client/screens/validate_code.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:client/app_template.dart';
import 'package:client/custom_widgets/app_form.dart';
import 'package:client/custom_widgets/app_button.dart';
import 'package:client/custom_widgets/bottom_button.dart';
import 'package:rflutter_alert/rflutter_alert.dart';
import 'package:client/utils/network.dart';
import 'package:client/config.dart';


// CupertinoActivityIndicator

class PassResetPage extends StatelessWidget {
  final _formKey = GlobalKey<FormState>();
  String email = "";
  
  PassResetPage({Key key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return AppTemplate(
      widgets: <Widget>[
        Container(
          child: Image.asset('assets/voice_asistant_icon.png', scale: 2),
          alignment: Alignment.center,
          height: MediaQuery.of(context).size.height * 0.5
        ),
        Form(
          key: _formKey,
          child: AppForm(
            hint: "Enter your email",
            onSaved: (input) => email = input,
          )  
        ),
        SizedBox(height: 30),
        AppButton(
          text: 'Submit',
          func: () {
            _sendRequest(context);    
          },
        ),
        SizedBox(height: 20),
        BottomButton(
          text: "Remember your password?",
          buttonText: "Go Back",
          onPressed: () => Navigator.of(context).pop()
        )
      ]
    );
  }
  _sendRequest(BuildContext context) {
    _formKey.currentState.save();
    getPasswordResetToken(email).then((res) {
      if (res[0]) {
        print('pass reset email $email');
        Navigator.pushNamed( context,
        '/validate_code',
         arguments: CodeScreenArguments(email)
         );
      } else {
        Alert(context: context, title: "Server Error", desc: ProtocolErrors[res[1] - 1], type: AlertType.error).show(); //For now
      }
    });
  }
}