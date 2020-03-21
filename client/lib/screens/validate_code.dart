import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:client/app_template.dart';
import 'package:client/custom_widgets/app_form.dart';
import 'package:client/custom_widgets/app_button.dart';
import 'package:client/custom_widgets/bottom_button.dart';
import 'package:rflutter_alert/rflutter_alert.dart';
import 'package:client/utils/network.dart';
import 'package:google_fonts/google_fonts.dart';

// CupertinoActivityIndicator
class CodeScreenArguments {
  final String email;
  CodeScreenArguments(this.email);
}
class ValidateCodePage extends StatelessWidget {
  final _formKey = GlobalKey<FormState>();
  final String email;
  String code;
  
  ValidateCodePage({Key key, @required this.email}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final CodeScreenArguments args = ModalRoute.of(context).settings.arguments;
    return AppTemplate(
      widgets: <Widget>[
        Container(
          child: Image.asset('assets/voice_asistant_icon.png', scale: 2),
          alignment: Alignment.center,
          height: MediaQuery.of(context).size.height * 0.5
        ),
        Text(
          'A 6-characters code has been sent to your email. Check it out and put it right here.',
           style: GoogleFonts.lora(),
         ),
        SizedBox(height: 30),
        Form(
          key: _formKey,
          child: AppForm(
            hint: 'Please enter the code here',
            onSaved: (input) => code=input,
          )
        ),
        SizedBox(height: 30),
        AppButton(
          text: 'Submit',
          func: () {
            _sendRequest(context);
            Alert(context: context, title: "Server Error", desc: '$email', type: AlertType.error).show(); //For now       
          },
         ),
      ]
    );
  }
  _sendRequest(BuildContext context) {
    _formKey.currentState.save();
    validateCode(code,email).then((res) {
      if (res[0]) {
        print(res);
        Navigator.of(context).pushNamed('/new_password');
      } else {
        Alert(context: context, title: "Server Error", desc: '$res', type: AlertType.error).show(); //For now
      }
    });
  }
}