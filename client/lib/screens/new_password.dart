import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:client/app_template.dart';
import 'package:client/custom_widgets/app_form.dart';
import 'package:client/custom_widgets/app_button.dart';
import 'package:rflutter_alert/rflutter_alert.dart';
import 'package:client/utils/network.dart';
import 'package:google_fonts/google_fonts.dart';

// CupertinoActivityIndicator
class NewPassScreenArguments {
  final String token;
  NewPassScreenArguments(this.token);
}
class NewPasswordPage extends StatelessWidget {
  final _formKey = GlobalKey<FormState>();
  String token;
  String newPassword;
  
  NewPasswordPage({Key key, @required this.token}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final NewPassScreenArguments args = ModalRoute.of(context).settings.arguments;
    this.token = args.token;
    return AppTemplate(
      widgets: <Widget>[
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
          )
        ),
        SizedBox(height: 30),
        AppButton(
          text: 'Submit',
          func: () {
            _sendRequest(context);  
          },
         ),
      ]
    );
  }
  _sendRequest(BuildContext context) {
    _formKey.currentState.save();
    newPasswordRequest(token,newPassword).then((res) {
      if (res[0]) {
        print(res);
        Alert(context: context, title: "Success", desc: 'You have successfully reset your password. You are now being sent to the login page.', type: AlertType.success).show(); //For now    
        Navigator.pushNamedAndRemoveUntil(context, "/login", (r) => false);
      } else {
        Alert(context: context, title: "Server Error", desc: '$res', type: AlertType.error).show(); //For now
      }
    });
  }
}