import 'package:flutter/material.dart';
import 'package:client/app_template.dart';
import 'package:client/custom_widgets/profile_text_box.dart';
import 'package:client/utils/network.dart';


class ProfilePage extends StatelessWidget {
  const ProfilePage({Key key}) : super(key: key);

  @override
  Widget build(BuildContext context) {    
    return FutureBuilder(
      future: profile(),
      builder: (context, snapshot) {
        switch (snapshot.connectionState) {
          case ConnectionState.done:
            return _onFinished(context, snapshot.data);
          default:
            return Align(alignment: Alignment.center, child: CircularProgressIndicator(strokeWidth: 10));
        }
      },
    );
  }

  _onFinished(context, res) {
    String username, email, img_url;
    print(res);
    if (res[0]) {
      username = res[1]['username'];
      email = res[1]['email'];
      img_url = res[1]['image'];
    }

    return AppTemplate(
      widgets: <Widget>[
        Stack(
          children: <Widget>[
            Container(height: MediaQuery.of(context).size.height * 0.6),
            Positioned(
              top: MediaQuery.of(context).size.height * 0.17,
              left: 38,
              child: CircleAvatar(
                backgroundImage: NetworkImage(img_url),
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
                    text: username
                  ),
        SizedBox(height: MediaQuery.of(context).size.height * 0.03),
        ProfileTextBox(
          header: 'Email',
          text: email
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