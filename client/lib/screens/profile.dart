import 'package:flutter/material.dart';
import 'package:client/app_template.dart';
import 'package:client/custom_widgets/profile_text_box.dart';
import 'package:client/utils/network.dart';
import 'package:image_picker/image_picker.dart';
import 'package:image_cropper/image_cropper.dart';
import 'package:shared_preferences/shared_preferences.dart';


class ProfilePage extends StatefulWidget {
  const ProfilePage({Key key}) : super(key: key);

  @override
  _ProfilePageState createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> {
  String username, email, imgUrl;
  final NetworkHandler _networkHandler = NetworkHandler();


  @override
  Widget build(BuildContext context) {    
    return FutureBuilder(
      future: _networkHandler.profile(),
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
    if (res[0]) {
      username = res[1]['username'];
      email = res[1]['email'];
      imgUrl = res[1]['image'];
    }

    return AppTemplate(
      widgets: <Widget>[
        SizedBox(height: 25),
        Stack(
          children: <Widget>[
            Container(height: MediaQuery.of(context).size.height * 0.6),
            Positioned(
              top: MediaQuery.of(context).size.height * 0.17,
              left: 38,
              child: CircleAvatar(
                backgroundImage: NetworkImage(imgUrl),
                radius: 120 // Change this to be fitted to screen size
              )
            ),
            Positioned(
              top: 60.0,
              child: _buildLogoutButton(context)
            ),
            Positioned(
              child: FloatingActionButton(
                child: Icon(Icons.camera_alt),
                onPressed: () => _uploadPicutre(ImageSource.camera)
              ),
              bottom: 70,
              left: 30
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

  _uploadPicutre(ImageSource source) async {
      var image = await ImagePicker.pickImage(source: source);
      var croppedFile = image != null ? await ImageCropper.cropImage(
        sourcePath: image.path,
      ) : null;
      if (croppedFile != null)  // In case that user pressed on return button at any point
      {
        setState(() {
          _networkHandler.uploadImage(croppedFile).then((_) {});    
        });
      }
  }

  _buildLogoutButton(context){
    return  IconButton(
      iconSize: 30,
      icon: Icon(Icons.exit_to_app),
      onPressed: () {
        SharedPreferences.getInstance().then((instance) => instance.setBool('RememberMe', false));
        _networkHandler.logout().then((res) {
          Navigator.pushReplacementNamed(context, '/login'); // Might cause troubles in auto login - check it later
        });
      },
    );
  }
}