import 'package:flutter/material.dart';
import 'package:client/app_form.dart';
import 'package:client/app_button.dart';
import 'package:client/login_system_template.dart';

class RegisterPage extends StatefulWidget {
  RegisterPage({Key key}) : super(key: key);

  @override
  RegisterPageState createState() => RegisterPageState();
}

class RegisterPageState extends State<RegisterPage> {
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
        AppForm(
          hint: 'Username'
        ),
        SizedBox(height: 10),
        AppForm(
          hint: 'Email'
        ),
        SizedBox(height: 10),
        AppForm(
          hint: 'Password',
          isPassword: true,
        ),
        SizedBox(height: 10),
        AppForm(
          hint: 'Re-enter password',
          isPassword: true,
          ),
        SizedBox(height: 10),
        AppButton(
          func: () {},
          text: 'Create an account'
        ),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text("Already have an account?", style: TextStyle(fontWeight: FontWeight.w300),),
            FlatButton(
              child: Text('Login', style: TextStyle(color: Colors.blue)),
              onPressed: () {
                Navigator.of(context).pop(); // ERROR: No animation
              },
            )]
          )
      ]
    );
  }
}