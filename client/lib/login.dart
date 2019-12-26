import 'package:flutter/material.dart';
import 'package:circular_check_box/circular_check_box.dart';

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
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: <Widget>[
            Image.asset('assets/voice_asistant_icon.png', scale: 3),
            Text('Login', style: TextStyle(fontSize: 30, fontWeight: FontWeight.bold)),
            Text('Please login to continue using our app.', style: TextStyle(fontWeight: FontWeight.w300)),
            TextFormField(
              decoration: InputDecoration(
                labelText: "Username or Email",
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(4))),
            ),
            TextFormField( //TODO: add option to show the password for a moment
              obscureText: true, 
              decoration: InputDecoration(
                labelText: "Password",
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(4))),
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: <Widget>[
                Row(children: <Widget>[
                  CircularCheckBox(
                    value: rememberMe,
                    onChanged: (bool value) {
                      setState(() {
                        rememberMe = value;
                    });},
                    ),
                    Text("Remember me")
                ]),
                FlatButton(child: Text('Forgot password?'),)
              ]),
              Container(
                height: 70,
                width: double.infinity,
                child: FlatButton(
                        color: Colors.black87,
                        textColor: Colors.white,
                        child: Text('Login'),
                        onPressed: () {},
                      )
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  Text("Don't have an account?", style: TextStyle(fontWeight: FontWeight.w300),),
                  FlatButton(
                    child: Text('Sign Up', style: TextStyle(color: Colors.blue)),
                  )
              ],)
            ],
          ),
      )
    );
  }
}

