import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class Settings extends StatefulWidget{
  const Settings({super.key});

  @override
  State<Settings> createState() => _SettingsState();

}

class _SettingsState extends State<Settings>{
  String url = '';
  String data = '';
  String result = '0';
  double _leftTrimming = 20;
  double _rightTrimming = 20;
  double _exposure = 20;
  TextEditingController _leftTrimController = TextEditingController();
  TextEditingController _rightTrimController = TextEditingController();
  TextEditingController _exposureController = TextEditingController();


  Future<void> send_Data(String url) async {
    await http.get(Uri.parse(url));
  }

  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    _leftTrimController = TextEditingController(text:((_leftTrimming*100).round()/100).toString());
    _rightTrimController = TextEditingController(text:((_rightTrimming*100).round()/100).toString());
    _exposureController = TextEditingController(text:((_exposure*100).round()/100).toString());
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: <Widget>[
          Row(
            children: [
              Expanded(
                flex:1,
                child: Text("Left leg trim"),
              ),
              Expanded(
                flex: 1,
                child: TextField(controller:_leftTrimController,
                onSubmitted: (value) {
                  setState(() {
                    _leftTrimming = double.parse(value);
                  });
                  send_Data("http://robot.local:5000/settings?leftTrim="+_leftTrimming.toString());
                },
                ),
              ),
              Expanded(
                flex: 3,
                child: Slider(
                  value: _leftTrimming,
                  max: 360,
                  divisions: 3600,
                  label: ((_leftTrimming*100).round()/100).toString(),
                  onChanged: (double value) {
                    setState(() {
                      _leftTrimming = value;
                    });
                    send_Data("http://robot.local:5000/settings?leftTrim="+_leftTrimming.toString());
                  },
                ),
              ),
            ],
          ),
          Row(
            children: [
              Expanded(
                flex:1,
                child: Text("Right leg trim"),
              ),
              Expanded(
                flex: 1,
                child: TextField(
                  controller: _rightTrimController,
                  onSubmitted: (value) {
                    setState(() {
                      _rightTrimming = double.parse(value);
                    });
                    send_Data("http://robot.local:5000/settings?rightTrim="+_rightTrimming.toString());
                  },
                ),
              ),
              Expanded(
                flex: 3,
                child: Slider(
                  value: _rightTrimming,
                  max: 360,
                  divisions: 3600,
                  label: ((_rightTrimming*100).round()/100).toString(),
                  onChanged: (double value) {
                    setState(() {
                      _rightTrimming = value;
                    });
                    send_Data("http://robot.local:5000/settings?rightTrim="+_rightTrimming.toString());
                  },
                ),
              ),
            ],
          ),
          Row(
            children: [
              Expanded(
                flex:1,
                child: Text("Exposure time"),
              ),
              Expanded(
                flex: 1,
                child: TextField(
                  controller: _exposureController,
                  onSubmitted: (value) {
                    setState(() {
                      _exposure = double.parse(value);
                    });
                    send_Data("http://robot.local:5000/settings?exposure="+_exposure.toString());
                  },
                ),
              ),
              Expanded(
                flex: 3,
                child: Slider(
                  value: _exposure,
                  max: 360,
                  divisions: 3600,
                  label: ((_exposure*100).round()/100).toString(),
                  onChanged: (double value) {
                    setState(() {
                      _exposure = value;
                    });
                    send_Data("http://robot.local:5000/settings?rightTrim="+_exposure.toString());
                  },
                ),
              ),
            ],
          )

        ],
      ),
    );
  }
}


