import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:permission_handler/permission_handler.dart';
import 'download.dart';

class SubmergedView extends StatefulWidget {
  const SubmergedView({super.key});

  @override
  State<SubmergedView> createState() => _SubmergedState();
}

class _SubmergedState extends State<SubmergedView> {
  String url = '';
  String data = '';
  String result = '0';
  int _counter = 0;
  List<Widget> widgets = [];

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
    String content = '';
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: <Widget>[
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              DragTarget<String>(
                onAcceptWithDetails: (details) {
                  var txt = TextEditingController();
                  setState(() {
                    widgets.add(Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Expanded(
                              flex: 1,
                              child: Container(
                                  margin: EdgeInsets.only(
                                      top: .0125 *
                                          MediaQuery.of(context).size.height),
                                  child: Text(
                                    details.data,
                                    style: DefaultTextStyle.of(context)
                                        .style
                                        .apply(fontSizeFactor: 1),
                                  ))),
                          Expanded(
                              flex: 2,
                              child: Container(
                                  margin: EdgeInsets.only(
                                      right: .01 *
                                          MediaQuery.of(context).size.width),
                                  child: TextField()))
                        ]));
                    txt.text = details.data;
                  });
                },
                builder: (
                  BuildContext context,
                  List<dynamic> accepted,
                  List<dynamic> rejected,
                ) {
                  return Container(
                      width: .6 * MediaQuery.of(context).size.width,
                      height: .6 * MediaQuery.of(context).size.height,
                      decoration: BoxDecoration(
                          border: Border.all(color: Colors.grey)
                      ),
                      child: ListView(
                        children: List.generate(
                            widgets.length,
                            (e) => //need to create and maintain dynamic list here
                                Container(
                                  margin: EdgeInsets.only(left: 10),
                                  height: 30,
                                  width: 30,
                                  child: widgets[e],
                                )),
                      ));
                },
              ),

              Container(
                margin: EdgeInsets.only(
                    left: .05 *
                        MediaQuery.of(context).size.width),
                padding: EdgeInsets.only(left:.02 * MediaQuery.of(context).size.width, right:.02 * MediaQuery.of(context).size.width),
                decoration: BoxDecoration(
                    border: Border.all(color: Colors.grey)
                ),
                height: .6 * MediaQuery.of(context).size.height,
                width: .2 * MediaQuery.of(context).size.width,
                child: Column(
                  children: [
                    Container(
                      margin: EdgeInsets.only(top:.01 * MediaQuery.of(context).size.width),
                        child: Draggable<String>(
                        feedback: Text(
                            'Forward',
                            style: TextStyle(fontSize: 14, color: Colors.black, fontWeight: FontWeight.normal),

                        ),
                        child: Text('Forward',
                            style: TextStyle(fontSize: .02 * MediaQuery.of(context).size.width),
                        ),
                        data: 'Forward',
                        onDraggableCanceled: (velocity, offset) {},
                      ),
                    ),
                    Container(
                      margin: EdgeInsets.only(top:.01 * MediaQuery.of(context).size.width),
                      child: Draggable<String>(
                        feedback: Text(
                          'Backward',
                          style: TextStyle(fontSize: 14, color: Colors.black, fontWeight: FontWeight.normal),

                        ),
                        child: Text('Backward',
                          style: TextStyle(fontSize: .02 * MediaQuery.of(context).size.width),
                        ),
                        data: 'Backward',
                        onDraggableCanceled: (velocity, offset) {},
                      ),
                    ),
                    Container(
                      margin: EdgeInsets.only(top:.01 * MediaQuery.of(context).size.width),
                      child: Draggable<String>(
                        feedback: Text(
                          'Left',
                          style: TextStyle(fontSize: 14, color: Colors.black, fontWeight: FontWeight.normal),

                        ),
                        child: Text('Left',
                          style: TextStyle(fontSize: .02 * MediaQuery.of(context).size.width),
                        ),
                        data: 'Left',
                        onDraggableCanceled: (velocity, offset) {},
                      ),
                    ),

                    Container(
                      margin: EdgeInsets.only(top:.01 * MediaQuery.of(context).size.width),
                      child: Draggable<String>(
                        feedback: Text(
                          'Right',
                          style: TextStyle(fontSize: 14, color: Colors.black, fontWeight: FontWeight.normal),

                        ),
                        child: Text('Right',
                          style: TextStyle(fontSize: .02 * MediaQuery.of(context).size.width),
                        ),
                        data: 'Right',
                        onDraggableCanceled: (velocity, offset) {},
                      ),
                    ),

                    Container(
                      margin: EdgeInsets.only(top:.01 * MediaQuery.of(context).size.width),
                      child: Draggable<String>(
                        feedback: Text(
                          'Clockwise',
                          style: TextStyle(fontSize: 14, color: Colors.black, fontWeight: FontWeight.normal),

                        ),
                        child: Text('Clockwise',
                          style: TextStyle(fontSize: .02 * MediaQuery.of(context).size.width),
                        ),
                        data: 'Clockwise',
                        onDraggableCanceled: (velocity, offset) {},
                      ),
                    ),

                    Container(
                      margin: EdgeInsets.only(top:.01 * MediaQuery.of(context).size.width),
                      child: Draggable<String>(
                        feedback: Text(
                          'Anticlockwise',
                          style: TextStyle(fontSize: 14, color: Colors.black, fontWeight: FontWeight.normal),

                        ),
                        child: Text('Anticlockwise',
                          style: TextStyle(fontSize: .02 * MediaQuery.of(context).size.width),
                        ),
                        data: 'Anticlockwise',
                        onDraggableCanceled: (velocity, offset) {},
                      ),
                    ),

                    Container(
                      margin: EdgeInsets.only(top:.01 * MediaQuery.of(context).size.width),
                      child: Draggable<String>(
                        feedback: Text(
                          'Up',
                          style: TextStyle(fontSize: 14, color: Colors.black, fontWeight: FontWeight.normal),

                        ),
                        child: Text('Up',
                          style: TextStyle(fontSize: .02 * MediaQuery.of(context).size.width),
                        ),
                        data: 'Up',
                        onDraggableCanceled: (velocity, offset) {},
                      ),
                    ),

                    Container(
                      margin: EdgeInsets.only(top:.01 * MediaQuery.of(context).size.width),
                      child: Draggable<String>(
                        feedback: Text(
                          'Down',
                          style: TextStyle(fontSize: 14, color: Colors.black, fontWeight: FontWeight.normal),

                        ),
                        child: Text('Down',
                          style: TextStyle(fontSize: .02 * MediaQuery.of(context).size.width),
                        ),
                        data: 'Down',
                        onDraggableCanceled: (velocity, offset) {},
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          ElevatedButton(
              onPressed: () {
                setState(() {
                  widgets.clear();
                });
              },
              child: const Text("Clear command")),
          ElevatedButton(
              onPressed: () {

              },
              child: const Text("Send command")),
          ElevatedButton(
              onPressed: () async {
                download_file();
              },
              child: const Text("Download File")),
        ],
      ),
    );
  }

  static void download_file() {
    download('I am a test file'.codeUnits, 'test.txt');
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
