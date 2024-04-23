import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:permission_handler/permission_handler.dart';
import 'download.dart';

class Settings extends StatefulWidget{
  const Settings({super.key});

  @override
  State<Settings> createState() => _SettingsState();

}

class _SettingsState extends State<Settings>{
  String url = '';
  String data = '';
  String result = '0';
  TextEditingController _controller = TextEditingController();

  Future<String> get_Data(String url) async {
    http.Response response = await http.get(Uri.parse(url));
    return response.body;
  }
  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: <Widget>[
          Row(),
          Row(
            children: [
              Text("Device IP address:"),
              TextField(
              ),
            ],
          ),

        ],
      ),
    );
  }

  static void download_file(){
    download('I am a test file'.codeUnits,'test.txt');
  }

  static Future<bool> _permissionRequest() async {
    PermissionStatus result;
    result = await Permission.storage.request();
    if (result.isGranted) {
      return true;
    } else {
      return false;
    }
  }
}


