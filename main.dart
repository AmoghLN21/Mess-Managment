import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  String cmd;
  var r ="hi";
  request ()async 
  {
    var response = await http.get("http://192.168.43.66/cgi-bin/web.py?x=$cmd");
    print(response.body);
    setState(() {
      r=response.body;
    });

  }
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        appBar: AppBar(
          title: Text("Docker App"),
          centerTitle: true,
          leading: Icon(Icons.menu),
        ),
        body: Column(
          children: <Widget>[
            Container(
              margin: EdgeInsets.symmetric(horizontal: 150, vertical: 30),
              height: 100,
              width: 100,
              child: Image(
                image: AssetImage("assets/docker.png"),
              ),
            ),
            Container(
              margin: EdgeInsets.symmetric(horizontal: 5),
              width: 400,
              child: TextField(
                style: TextStyle(fontSize: 20),
                onChanged: (text) {
                  cmd = text;
                },
                decoration: InputDecoration(
                    enabledBorder: const OutlineInputBorder(
                      borderRadius: BorderRadius.all(Radius.circular(20.0)),
                      borderSide: const BorderSide(
                        color: Colors.grey,
                      ),
                    ),
                    focusedBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.all(Radius.circular(20.0)),
                      borderSide: BorderSide(
                          color: Colors.blueGrey, style: BorderStyle.solid),
                    ),
                    prefix: Text(
                      "\$  ",
                      style: TextStyle(color: Colors.black, fontSize: 20),
                    ),
                    hintText: "             Enter Docker Command"),
              ),
            ),
            Container(
              child: MaterialButton(
                onPressed: () {
                  request();
                },
                color: Colors.blue,
                child: Text("SUBMIT"),
              ),
            ),
            Container(
              decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(20),
                  color: Colors.blueGrey),
              width: 400,
              height: 330,
              child: Text("\n$r", style: TextStyle(color: Colors.white,fontSize: 15),),
            )
          ],
        ),
      ),
    );
  }
}
