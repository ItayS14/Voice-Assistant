import 'package:flutter/material.dart';
import 'package:circular_check_box/circular_check_box.dart';
import 'package:client/app_form.dart';

class LoginPage extends StatefulWidget{
  @override
  LoginPageState createState() => LoginPageState(); 
}

class LoginPageState extends State<LoginPage> {
  bool rememberMe = true;

  @override
  Widget build(BuildContext context){
    return Scaffold(
      body:  Container(
          margin: const EdgeInsets.only(left: 25.0, right: 25.0),
          child: Column(
          children: <Widget>[
            SizedBox(height: 50),
            Image.asset('assets/voice_asistant_icon.png', scale: 3),
            SizedBox(height: 10),
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
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  Text("Don't have an account?", style: TextStyle(fontWeight: FontWeight.w300),),
                  FlatButton(
                    child: Text('Sign Up', style: TextStyle(color: Colors.blue)),
                  )
              ],),
            ],
          ),
      )
    );
  }
}

