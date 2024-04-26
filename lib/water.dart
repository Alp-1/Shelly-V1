import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:permission_handler/permission_handler.dart';
import 'download.dart';
import 'package:file_picker/file_picker.dart';
import 'dart:convert';

class SubmergedView extends StatefulWidget {
  const SubmergedView({super.key});

  @override
  State<SubmergedView> createState() => _SubmergedState();
}

class _SubmergedState extends State<SubmergedView> {
  String url = '';
  String data = '';
  String result = '0';
  List<Widget> widgets = [];
  List<List<String>> commands = [];
  List<TextEditingController> controllers = [];

  Future<String> get_Data(String url) async {
    http.Response response = await http.get(Uri.parse(url));
    return response.body;
  }

  Future<void> send_Data(String url) async {
    await http.get(Uri.parse(url));
  }

  @override
  Widget build(BuildContext context) {
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
                    TextEditingController _controller = TextEditingController(text: '0');
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
                                  child: TextField(
                                    controller:_controller,
                                  )))
                        ]));
                    controllers.add(_controller);
                    commands.add([details.data]);
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

                    Container(
                      margin: EdgeInsets.only(top:.01 * MediaQuery.of(context).size.width),
                      child: Draggable<String>(
                        feedback: Text(
                          'Start record',
                          style: TextStyle(fontSize: 14, color: Colors.black, fontWeight: FontWeight.normal),

                        ),
                        child: Text('Start record',
                          style: TextStyle(fontSize: .02 * MediaQuery.of(context).size.width),
                        ),
                        data: 'Start record',
                        onDraggableCanceled: (velocity, offset) {},
                      ),
                    ),

                    Container(
                      margin: EdgeInsets.only(top:.01 * MediaQuery.of(context).size.width),
                      child: Draggable<String>(
                        feedback: Text(
                          'Stop record',
                          style: TextStyle(fontSize: 14, color: Colors.black, fontWeight: FontWeight.normal),

                        ),
                        child: Text('Stop record',
                          style: TextStyle(fontSize: .02 * MediaQuery.of(context).size.width),
                        ),
                        data: 'Stop record',
                        onDraggableCanceled: (velocity, offset) {},
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          Row(
              mainAxisAlignment: MainAxisAlignment.center,
            children:[
              ElevatedButton(
                  onPressed: () async {
                    var picked = await FilePicker.platform.pickFiles();
                    String value = "";
                    if (picked != null) {
                      var bytes = picked.files.first.bytes;
                      if (bytes != null){
                         value = utf8.decode(bytes);
                      }
                    }
                    setState(() {
                      widgets.clear();
                      commands.clear();
                      controllers.clear();
                    });
                    for (String val in value.split("\n")){
                      List<String> parts = val.split(":");
                      setState(() {
                        switch (parts[0]) {
                          case "Forward":
                            add_command(parts);
                            break;
                          case "Backward":
                            add_command(parts);
                            break;
                          case "Right":
                            add_command(parts);
                            break;
                          case "Left":
                            add_command(parts);
                            break;
                          case "Up":
                            add_command(parts);
                            break;
                          case "Down":
                            add_command(parts);
                            break;
                          default:
                            print('invalid command');
                        }
                      });
                    }
                  },
                  child: const Text("Import commands")),
          ElevatedButton(
              onPressed: () {
                setState(() {
                  widgets.clear();
                  controllers.clear();
                  commands.clear();
                });
              },
              child: const Text("Clear command")),
          ElevatedButton(
              onPressed: () {
                String string = "http://robot.local:5000/water?commands=[";
                for (int index = 0; index < widgets.length; index++){
                  commands[index].add(controllers[index].text);
                  string += '['+commands[index][0]+','+controllers[index].text+']';
                  print(controllers[index].text);
                }
                send_Data(string+']');
              },
              child: const Text("Send command")),
          ElevatedButton(
              onPressed: () async {
                download_file();
              },
              child: const Text("Download File")),
            ]
          )
        ],
      ),
    );
  }
  void add_command(List<String> parts){
    TextEditingController _controller = TextEditingController(text: parts[1]);
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
                    parts[0],
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
                  child: TextField(
                    controller:_controller,
                  )))
        ]));
    controllers.add(_controller);
    commands.add([parts[0]]);
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
