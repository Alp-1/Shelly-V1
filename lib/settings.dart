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
                  max: 360,
                  divisions: 3600,
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
          Padding(
            padding: EdgeInsets.fromLTRB(0, 100, 0, 0),
            child: ElevatedButton(
              child:Text("Save settings"),
              onPressed: (){
                send_Data("http://robot.local:5000/settings?rightTrim="+_exposure.toString()+"&leftTrim="+_leftTrimming.toString()+"&exposure="+_exposure.toString());
              },
            ),
          ),


        ],
      ),
    );
  }
}


