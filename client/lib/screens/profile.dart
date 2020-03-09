import 'package:flutter/material.dart';
import 'package:client/app_template.dart';
import 'package:client/custom_widgets/profile_text_box.dart';

class ProfilePage extends StatelessWidget {
  const ProfilePage({Key key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return AppTemplate(
      widgets: <Widget>[
        Container(
          height: MediaQuery.of(context).size.height * 0.6,
          alignment: Alignment.center,
          child: CircleAvatar(
            backgroundImage: NetworkImage('https://avatars0.githubusercontent.com/u/8264639?s=460&v=4'),
            radius: 120 // Change this to be fitted to screen size
          ),
        ),
        ProfileTextBox(
                    header: 'Username',
                    text: 'Test Username'
                  ),
        SizedBox(height: MediaQuery.of(context).size.height * 0.03),
        ProfileTextBox(
          header: 'Email',
          text: 'test@gmail.com'
        )
      ],
    );
  }
}