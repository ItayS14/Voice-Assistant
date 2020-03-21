import 'package:flutter/material.dart';
//forms for the login system
class AppForm extends StatefulWidget {
  final String hint;
  final bool isPassword;
  final onSaved;
  final validator;
  final int maxLength;

  AppForm({Key key, @required this.hint, this.isPassword = false, this.onSaved, this.validator, this.maxLength = 150}) : super(key: key);

  @override
  AppFormState createState() => AppFormState();
}

class AppFormState extends State<AppForm> {
  bool _showForm = false;

  @override
  Widget build(BuildContext context) {
    return TextFormField(
      obscureText: widget.isPassword? !_showForm : false, //only obscure the text if it password form
      decoration: InputDecoration(
        suffixIcon: widget.isPassword? GestureDetector( //only add the icon if it is password form
          onTap: () {
            setState(() {
              _showForm = !_showForm;
            });
          },
          child: Icon(_showForm ? Icons.visibility : Icons.visibility_off)) : null,
        labelText: widget.hint,
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(4)),
        counterText: "", // Hide the amount of chars the user can enter
        ),
        onSaved: widget.onSaved,
        validator: widget.validator,
        maxLength: widget.maxLength,
    );
  }
}