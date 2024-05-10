import 'package:bio_robotics/water.dart';
import 'package:bio_robotics/land.dart';
import 'package:bio_robotics/settings.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "Shelly's Control Terminal",
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: "Shelly's Control Terminal"),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

Future<String> get_Data(String url) async {
  http.Response response = await http.get(Uri.parse(url));
  return response.body;
}

class _MyHomePageState extends State<MyHomePage> {
  int previous = -1;
  LandView lv = LandView();
  String ip = "robot.local";
  String port = "5000";
  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      initialIndex: 1,
      length: 3,
      child: Scaffold(
        appBar: AppBar(
          backgroundColor: Theme.of(context).colorScheme.inversePrimary,
          title: Text(widget.title),
          bottom: TabBar(
            isScrollable: false,
            onTap: (index){
              if(previous != index && index == 0){
                var length = MediaQuery.of(context).size.width > MediaQuery.of(context).size.height ? MediaQuery.of(context).size.height : MediaQuery.of(context).size.width;
                get_Data('http://'+ip+':'+port+'/land?size='+(0.75 * length).round().toString()+','+(0.75 * length).round().toString());
              }
              else if (previous != index && index == 1){
                get_Data('http://'+ip+':'+port+'/water');
              }
              else if (previous != index && index == 2){
                get_Data('http://'+ip+':'+port+'/settings');
              }
              previous = index;
              print(previous);
            },
            tabs: <Widget>[
              Tab(
                icon: Icon(
                  Icons.directions_walk_outlined,
                ),
              ),
              Tab(
                icon: Icon(
                  Icons.waves_outlined,
                ),
              ),
              Tab(
                icon: Icon(Icons.brightness_5_sharp),
              ),
            ],
          ),
        ),
        body: TabBarView(
          physics: NeverScrollableScrollPhysics(),
          children: <Widget>[
            lv,
            SubmergedView(),
            Settings(
            ),
          ],
        ),
      ),
    );
  }

}
