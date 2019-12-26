import 'package:flutter/material.dart';
import 'package:client/app_form.dart';

class RegisterPage extends StatefulWidget {
  RegisterPage({Key key}) : super(key: key);

  @override
  RegisterPageState createState() => RegisterPageState();
}

class RegisterPageState extends State<RegisterPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body:  Container(
          margin: const EdgeInsets.only(left: 25.0, right: 25.0),
          alignment: Alignment.center,
          child: Column(
          children: <Widget>[
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
            SizedBox(height: 15),
            Container(
                height: 70,
                width: double.infinity,
                child: RaisedButton(
                        color: Colors.black87,
                        textColor: Colors.white,
                        child: Text('Login', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 20),),
                        onPressed: () {},
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(4))
                      )
              ),
            ])
          ),
      );
  }
}