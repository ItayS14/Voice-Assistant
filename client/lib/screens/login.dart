import 'package:flutter/material.dart';
import 'package:circular_check_box/circular_check_box.dart';
import 'package:client/custom_widgets/app_form.dart';
import 'package:client/custom_widgets/app_button.dart';
import 'package:client/app_template.dart';
import 'package:client/custom_widgets/bottom_button.dart';
import 'package:client/utils/network.dart';
import 'package:rflutter_alert/rflutter_alert.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:client/screens/profile.dart';
import 'package:client/config.dart';
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';


class LoginPage extends StatefulWidget{ 

  @override
  LoginPageState createState() => LoginPageState(); 
}

class LoginPageState extends State<LoginPage> {
  final _formKey = GlobalKey<FormState>();
  bool _rememberMe = true;
  String _auth, _password;
  NetworkHandler _networkHandler = NetworkHandler();
  @override
  Widget build(BuildContext context){
    // try to login if remember was checked last time
    return AppTemplate(
      widgets: <Widget>[
        SizedBox(height: 60),
        Image.asset('assets/voice_asistant_icon.png', scale: 3),
        SizedBox(height: 14),
        Text('Login', style: TextStyle(fontSize: 30, fontWeight: FontWeight.bold)),
        Text('Please login to continue using our app.', style: TextStyle(fontWeight: FontWeight.w300)),
        SizedBox(height: 20),
        _buildForms(),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: <Widget>[
            Row(children: <Widget>[
              CircularCheckBox(
                value: _rememberMe,
                activeColor: Colors.black87,
                onChanged: (bool value) {
                  setState(() {
                    _rememberMe = value;
                });},
              ),
              Text("Remember me")
            ]),
            FlatButton(
              child: Text(
                'Forgot password?',
                style: GoogleFonts.quicksand(),
                ),
              onPressed: () {
               Navigator.pushReplacementNamed(context, '/pass_reset');
             },
             )
        ]),
        SizedBox(height: 15),
        AppButton(
          text: 'Login', 
          func: _login
        ),
        BottomButton(
          text: "Don't have an account?", 
          buttonText: 'Sign Up',
          onPressed: () => Navigator.pushReplacementNamed(context, '/register')
        )
      ]
    );
  }

  _login() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    _formKey.currentState.save();

    _networkHandler.login(_auth, _password).then((res) {
      prefs.setBool('RememberMe', _rememberMe).then((_){});
      if (res[0])
      {
        Navigator.pushReplacementNamed(context, '/main');
      }
      else {
        Alert(context: context, title: "Error!", desc: ProtocolErrors[res[1]], type: AlertType.error).show(); //For now
      }
    });
  }

  //The function will build the forms for the login screen
  Form _buildForms(){
    return Form(
      key: _formKey,
      child: Column(
        children: <Widget>[
          AppForm(
            hint: "Username or Email",
            onSaved: (input) => _auth = input,
          ),
          SizedBox(height: 20),
          AppForm(
            hint: 'Password',
            isPassword: true,
            onSaved: (input) => _password = input,
          )
        ]
      )
    );
  }
}

