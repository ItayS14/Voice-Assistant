import 'package:flutter/material.dart';
import 'package:client/app_form.dart';
import 'package:client/app_button.dart';
import 'package:client/login_system_template.dart';
import 'package:client/bottom_button.dart';

class RegisterPage extends StatefulWidget {
  RegisterPage({Key key}) : super(key: key);

  @override
  RegisterPageState createState() => RegisterPageState();
}

class RegisterPageState extends State<RegisterPage> {
  final _formKey = GlobalKey<FormState>();
  String _username, _password, _email;

  @override
  Widget build(BuildContext context) {
    return LoginSystemTemplate(
      widgets: <Widget>[
        SizedBox(height: 30),
        Image.asset('assets/voice_asistant_icon.png', scale: 3),
        SizedBox(height: 14),
        Text('Register', style: TextStyle(fontSize: 30, fontWeight: FontWeight.bold)),
        Text('Please register to the app.', style: TextStyle(fontWeight: FontWeight.w300)),
        
        SizedBox(height: 20), //TODO: create widget that holds multiple forms with corrcet padding between them
        _buildForm(),
        SizedBox(height: 10),
        AppButton(
          func: () {
            _formKey.currentState.save();
            if (_formKey.currentState.validate())
              print('Good');
          },
          text: 'Create an account'
        ),
        BottomButton(
          text: "Already have an account?",
          buttonText: "Login",
          onPressed: () => Navigator.of(context).pop(),
        )
      ]
    );
  }
  
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
            validator: (value) => value == _password ? null : "Confirm Password should match password", // For the validator to work must save state first
          )
        ]
      )
    );
  }
}