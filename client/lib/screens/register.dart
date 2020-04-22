import 'package:flutter/material.dart';
import 'package:client/custom_widgets/app_form.dart';
import 'package:client/custom_widgets/app_button.dart';
import 'package:client/app_template.dart';
import 'package:client/custom_widgets/bottom_button.dart';
import 'package:client/utils/network.dart';
import 'package:client/config.dart';


import 'package:rflutter_alert/rflutter_alert.dart';

class RegisterPage extends StatefulWidget {
  RegisterPage({Key key}) : super(key: key);

  @override
  RegisterPageState createState() => RegisterPageState();
}

class RegisterPageState extends State<RegisterPage> {
  final _formKey = GlobalKey<FormState>();
  String _username, _password, _email;
  final NetworkHandler _networkHandler = NetworkHandler();


  @override
  Widget build(BuildContext context) {
    return AppTemplate(
      widgets: <Widget>[
        SizedBox(height: 30),
        Image.asset('assets/voice_asistant_icon.png', scale: 3),
        SizedBox(height: 14),
        Text('Register', style: TextStyle(fontSize: 30, fontWeight: FontWeight.bold)),
        Text('Please register to the app.', style: TextStyle(fontWeight: FontWeight.w300)),
        
        SizedBox(height: 20),
        _buildForm(),
        SizedBox(height: 10),
        AppButton(
          func: () => _register(),
          text: 'Create an account'
        ),
        BottomButton(
          text: "Already have an account?",
          buttonText: "Login",
          onPressed: () => Navigator.pushReplacementNamed(context, '/login'),
        )
      ]
    );
  }
  
  //The function will register to the app
  _register() {
    _formKey.currentState.save();
    if (_formKey.currentState.validate())
    {
      _networkHandler.register(_username, _password, _email).then((res) {
        if (res[0])
          Navigator.pushReplacementNamed(context, '/login');
        else
          Alert(context: context, title: "Error!", desc: res[1], type: AlertType.error).show(); //For now

      });
    }
  }
  //The function will build the forms of the register page
  Form _buildForm(){
    return Form(
      key: _formKey,
      child: Column(
        children: <Widget>[
          AppForm(
          hint: 'Username',
          onSaved: (input) => _username = input
          ),
          SizedBox(height: 10),
          AppForm(
            hint: 'Email',
            onSaved: (input) => _email = input
          ),
          SizedBox(height: 10),
          AppForm(
            hint: 'Password',
            isPassword: true,
            onSaved: (input) => _password = input
          ),
          SizedBox(height: 10),
          AppForm(
            hint: 'Re-enter password',
            isPassword: true,
            validator: (value) => value == _password ? null : "Passwords must match", // For the validator to work must save state first
          )
        ]
      )
    );
  }
}