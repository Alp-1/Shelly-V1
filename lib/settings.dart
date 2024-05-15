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
  double _exposure = 0;
  double _speed = 1;
  double _quality = 75;
  double _brightness = 0;
  TextEditingController _leftTrimController = TextEditingController();
  TextEditingController _rightTrimController = TextEditingController();
  TextEditingController _exposureController = TextEditingController();
  TextEditingController _speedController = TextEditingController();
  TextEditingController _qualityController = TextEditingController();
  TextEditingController _brightnessController = TextEditingController();


  Future<void> send_Data(String url) async {
    await http.get(Uri.parse(url));
  }

  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    _leftTrimController = TextEditingController(text:((_leftTrimming*100).round()/100).toString());
    _rightTrimController = TextEditingController(text:((_rightTrimming*100).round()/100).toString());
    _exposureController = TextEditingController(text:((_exposure*100).round()/100).toString());
    _brightnessController = TextEditingController(text:((_brightness*100).round()/100).toString());
    _qualityController = TextEditingController(text:_quality.toString());
    _speedController = TextEditingController(text:_speed.toString());
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
                  },
                ),
              ),
              Expanded(
                flex: 3,
                child: Slider(
                  value: _exposure,
                  max: 8,
                  min:-8,
                  divisions: 1600,
                  label: ((_exposure*100).round()/100).toString(),
                  onChanged: (double value) {
                    setState(() {
                      _exposure = value;
                    });
                  },
                ),
              ),
            ],
          ),
          Row(
            children: [
              Expanded(
                flex:1,
                child: Text("Brightness"),
              ),
              Expanded(
                flex: 1,
                child: TextField(
                  controller: _brightnessController,
                  onSubmitted: (value) {
                    setState(() {
                      _brightness = double.parse(value);
                    });
                  },
                ),
              ),
              Expanded(
                flex: 3,
                child: Slider(
                  value: _brightness,
                  max: 1,
                  min: -1,
                  divisions: 200,
                  label: ((_brightness*100).round()/100).toString(),
                  onChanged: (double value) {
                    setState(() {
                      _brightness = value;
                    });
                  },
                ),
              ),
            ],
          ),
          Row(
            children: [
              Expanded(
                flex:1,
                child: Text("Quality"),
              ),
              Expanded(
                flex: 1,
                child: TextField(
                  controller: _qualityController,
                  onSubmitted: (value) {
                    setState(() {
                      _quality = double.parse(value);
                    });
                  },
                ),
              ),
              Expanded(
                flex: 3,
                child: Slider(
                  value: _quality,
                  max: 100,
                  divisions: 100,
                  label: _quality.toString(),
                  onChanged: (double value) {
                    setState(() {
                      _quality = value;
                    });
                  },
                ),
              ),
            ],
          ),
          Row(
            children: [
              Expanded(
                flex:1,
                child: Text("Speed"),
              ),
              Expanded(
                flex: 1,
                child: TextField(
                  controller: _speedController,
                  onSubmitted: (value) {
                    setState(() {
                      _speed = double.parse(value);
                    });
                  },
                ),
              ),
              Expanded(
                flex: 3,
                child: Slider(
                  value: _speed,
                  max: 3,
                  divisions: 3,
                  label: _speed.toString(),
                  onChanged: (double value) {
                    setState(() {
                      _speed = value;
                    });
                  },
                ),
              ),
            ],
          ),
          Padding(
            padding: EdgeInsets.fromLTRB(0, 100, 0, 0),
            child: ElevatedButton(
              child:Text("Save settings"),
              onPressed: (){
                send_Data("http://robot.local:5000/settings?rightTrim="+_exposure.toString()+"&leftTrim="+_leftTrimming.toString()+"&exposure="+_exposure.toString()+"&brightness="+_brightness.toString()+"&quality="+_quality.toString()+"&speed="+_speed.toString());
              },
            ),
          ),


        ],
      ),
    );
  }
}


