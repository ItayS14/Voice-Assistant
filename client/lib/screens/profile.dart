import 'package:flutter/material.dart';
import 'package:client/app_template.dart';
import 'package:client/custom_widgets/profile_text_box.dart';
import 'package:client/utils/network.dart';

class ProfileArguments {
  final String img_url;
  final String username;
  final String email;

  ProfileArguments({this.img_url, this.username, this.email});
}

class ProfilePage extends StatelessWidget {
  const ProfilePage({Key key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final ProfileArguments args = ModalRoute.of(context).settings.arguments;
    
    return AppTemplate(
      widgets: <Widget>[
        Stack(
          children: <Widget>[
            Container(height: MediaQuery.of(context).size.height * 0.6),
            Positioned(
              top: MediaQuery.of(context).size.height * 0.17,
              left: 38,
              child: CircleAvatar(
                backgroundImage: NetworkImage(args.img_url),
                radius: 120 // Change this to be fitted to screen size
              )
            ),
            Positioned(
              top: 60.0,
              child: _buildLogoutButton(context)
            )
          ],
        ),
        ProfileTextBox(
                    header: 'Username',
                    text: args.username
                  ),
        SizedBox(height: MediaQuery.of(context).size.height * 0.03),
        ProfileTextBox(
          header: 'Email',
          text: args.email
        )
      ],
    );
  }

  _buildLogoutButton(context){
    return  IconButton(
      iconSize: 30,
      icon: Icon(Icons.exit_to_app),
      onPressed: () {
        logout().then((res) {
          print(res);
          Navigator.of(context).pop(); // Might cause troubles in auto login - check it later
        });
      },
    );
  }
}