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
  int _counter = 0;

  void _incrementCounter() {
    setState(() {
      _counter++;
    });
  }

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
          const Text(
            'You have pushed the button this many times:',
          ),
          Text(
            '$_counter',
            style: Theme.of(context).textTheme.headlineMedium,
          ),
          ElevatedButton(
              onPressed: () async {
                download_file();
              },
              child: const Text("Download File")),
          TextField( onChanged: (val) {
            url = 'http://127.0.0.1:5000/test?query='+val.toString();
          },),
          TextButton(onPressed: () async {
            data = await get_Data(url);
            var json = jsonDecode(data);
            setState(() {
              result = json['output'];
            });
          }, child: Text('Send Data')),
          Text(
            result,
            style: Theme.of(context).textTheme.headlineMedium,
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


