import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:permission_handler/permission_handler.dart';
import 'download.dart';
import 'package:flutter/services.dart';
import "dart:math" show pi;
import 'video_stream.dart';

class LandView extends StatefulWidget{
  const LandView({super.key});

  @override
  State<LandView> createState() => _LandState();

}

class _LandState extends State<LandView>{
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
    return CallbackShortcuts(
      bindings: <ShortcutActivator, VoidCallback>{
        const SingleActivator(LogicalKeyboardKey.arrowUp): () {

        },
        const SingleActivator(LogicalKeyboardKey.arrowDown): () {

        },
        const SingleActivator(LogicalKeyboardKey.arrowLeft): () {

        },
        const SingleActivator(LogicalKeyboardKey.arrowRight): () {

        },
        const SingleActivator(LogicalKeyboardKey.space): () {

        },
      },
      child: Focus(
        autofocus: true,
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              SizedBox(
                width: .9 * MediaQuery.of(context).size.width,
                height: .55  * MediaQuery.of(context).size.height,
                child: VideoStream(),
              ),
              Row (
                  mainAxisAlignment: MainAxisAlignment.center,
                  children:[
                    Column(
                      children: [
                        ElevatedButton(
                          onPressed: () async {
                            url = 'http://127.0.0.1:5000/test?query=clockwise';
                            data = await get_Data(url);
                            var json = jsonDecode(data);
                            setState(() {
                              result = json['output'];
                            });
                          },
                          child: const Icon(
                            Icons.redo_outlined,
                          ),
                        ),
                        Transform.rotate(
                            angle: 180 * pi / 180,
                            child:
                            ElevatedButton(
                              onPressed: () async {
                                url = 'http://127.0.0.1:5000/test?query=anticlockwise';
                                data = await get_Data(url);
                                var json = jsonDecode(data);
                                setState(() {
                                  result = json['output'];
                                });
                              },
                              child: const Icon(
                                Icons.undo_outlined,
                              ),
                            ),
                        ),
                      ]
                    ),
                    Column(
                      children: [
                        ElevatedButton(
                          onPressed: () async {
                            url = 'http://127.0.0.1:5000/test?query=forward';
                            data = await get_Data(url);
                            var json = jsonDecode(data);
                            setState(() {
                              result = json['output'];
                            });
                          },
                          child: const Icon(
                            Icons.keyboard_arrow_up_outlined,
                          ),
                        ),
                        Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children:[
                              ElevatedButton(
                                onPressed: () async {
                                  url = 'http://127.0.0.1:5000/test?query=right';
                                  data = await get_Data(url);
                                  var json = jsonDecode(data);
                                  setState(() {
                                    result = json['output'];
                                  });
                                },
                                child: const Icon(
                                  Icons.keyboard_arrow_left_outlined,
                                ),
                              ),
                              ElevatedButton(
                                onPressed: () async {
                                  url = 'http://127.0.0.1:5000/test?query=stop';
                                  data = await get_Data(url);
                                  var json = jsonDecode(data);
                                  setState(() {
                                    result = json['output'];
                                  });
                                },
                                child: const Icon(
                                  Icons.pause,
                                ),
                              ),
                              ElevatedButton(
                                onPressed: () async {
                                  url = 'http://127.0.0.1:5000/test?query=right';
                                  data = await get_Data(url);
                                  var json = jsonDecode(data);
                                  setState(() {
                                    result = json['output'];
                                  });
                                },
                                child: const Icon(
                                  Icons.keyboard_arrow_right_outlined,
                                ),
                              ),
                            ]
                        ),
                        ElevatedButton(
                          onPressed: () async {
                            url = 'http://127.0.0.1:5000/test?query=backward';
                            data = await get_Data(url);
                            var json = jsonDecode(data);
                            setState(() {
                              result = json['output'];
                            });
                          },
                          child: const Icon(
                            Icons.keyboard_arrow_down_outlined,
                          ),
                        ),
                      ]
                    ),
                    Column(
                        children: [
                          ElevatedButton(
                            onPressed: () async {
                              url = 'http://127.0.0.1:5000/test?query=up';
                              data = await get_Data(url);
                              var json = jsonDecode(data);
                              setState(() {
                                result = json['output'];
                              });
                            },
                            child: const Icon(
                              Icons.arrow_upward_outlined,
                            ),
                          ),
                          ElevatedButton(
                            onPressed: () async {
                              url = 'http://127.0.0.1:5000/test?query=down';
                              data = await get_Data(url);
                              var json = jsonDecode(data);
                              setState(() {
                                result = json['output'];
                              });
                            },
                            child: const Icon(
                              Icons.arrow_downward_outlined,
                            ),
                          ),
                        ]
                    ),
                  ]
                ),
                Text(
                  'Moving '+result,
                  style: Theme.of(context).textTheme.headlineMedium,
                ),
              ],
          ),
        ),
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


