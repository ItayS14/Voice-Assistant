import 'package:flutter/material.dart';
import 'package:circular_check_box/circular_check_box.dart';
import 'package:client/app_form.dart';
import 'package:client/app_button.dart';
import 'package:client/login_system_template.dart';

class LoginPage extends StatefulWidget{
  @override
  LoginPageState createState() => LoginPageState(); 
}

class LoginPageState extends State<LoginPage> {
  bool rememberMe = true;

  @override
  Widget build(BuildContext context){
    return LoginSystemTemplate(
      widgets: <Widget>[
        SizedBox(height: 60),
        Image.asset('assets/voice_asistant_icon.png', scale: 3),
        SizedBox(height: 14),
        Text('Login', style: TextStyle(fontSize: 30, fontWeight: FontWeight.bold)),
        Text('Please login to continue using our app.', style: TextStyle(fontWeight: FontWeight.w300)),
        SizedBox(height: 20),
        AppForm(
          hint: "Username or Email",
        ),
        SizedBox(height: 20),
        AppForm(
          hint: 'Password',
          isPassword: true,
        ),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: <Widget>[
            Row(children: <Widget>[
              CircularCheckBox(
                value: rememberMe,
                activeColor: Colors.black87,
                onChanged: (bool value) {
                  setState(() {
                    rememberMe = value;
                });},
              ),
              Text("Remember me")
            ]),
            FlatButton(child: Text('Forgot password?'))
        ]),
        SizedBox(height: 15),
        AppButton(
          text: 'Login', 
          func: () {}
        ),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text("Don't have an account?", style: TextStyle(fontWeight: FontWeight.w300),),
            FlatButton(
              child: Text('Sign Up', style: TextStyle(color: Colors.blue),),
              onPressed: () {
                Navigator.of(context).pushNamed('/register');
              },
            )
          ]
       )    
      ]
    );
  }
}

