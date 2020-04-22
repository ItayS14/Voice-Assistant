import 'dart:io';

import 'package:client/config.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:client/app_template.dart';
import 'package:client/custom_widgets/app_form.dart';
import 'package:client/custom_widgets/app_button.dart';
import 'package:rflutter_alert/rflutter_alert.dart';
import 'package:client/utils/network.dart';
import 'package:google_fonts/google_fonts.dart';

// Struct for this screen's arguments
class NewPassScreenArguments {
  final String token;
  NewPassScreenArguments(this.token);
}

class NewPasswordPage extends StatelessWidget {
  final _formKey = GlobalKey<FormState>();
  String newPassword;
  NetworkHandler _networkHandler = NetworkHandler();
  
  NewPasswordPage({Key key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final NewPassScreenArguments args = ModalRoute.of(context).settings.arguments;
    return AppTemplate(
      widgets: <Widget>[
        Align(
        alignment: Alignment.topLeft,      
        child: IconButton(
        padding: new EdgeInsets.fromLTRB(20,50,0,0), 
        icon: Icon(Icons.home),
        onPressed: () {
          Navigator.pushReplacementNamed(context, "/login");
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
          'Please enter your new desired password here.',
           style: GoogleFonts.lora(),
         ),
        SizedBox(height: 30),
        Form(
          key: _formKey,
          child: AppForm(
            hint: 'Enter the password',
            onSaved: (input) => newPassword = input,
            isPassword: true,
          )
        ),
        SizedBox(height: 30),
        AppButton(
          text: 'Submit',
          func: () {
            _sendRequest(context, args.token);  
          },
         ),
      ]
    );
  }
  /*
  This function will send the new password request to the server
  Input: context and the token receieved in the last step (validate code)
  Output: none (alerts the user if there's an error)
  */
  _sendRequest(BuildContext context, String token) {
    _formKey.currentState.save();
    _networkHandler.newPasswordRequest(token,newPassword).then((res) {
      if (res[0]) {
        Alert(
          context: context, 
          title: "Success", 
          desc: 'You have successfully reset your password. You are now being sent to the login page.', 
          type: AlertType.success,
        ).show().then((_) => Navigator.pushReplacementNamed(context, "/login")); //For now    
      } else {
        Alert(context: context, title: "Server Error", desc: res[1], type: AlertType.error).show(); 
      }
    });
  }
}