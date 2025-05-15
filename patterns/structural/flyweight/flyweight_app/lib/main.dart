import 'package:flutter/material.dart';
import 'package:flyweight_app/flyweight.dart';
import 'package:flutter/cupertino.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
      ),
      home: const MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      backgroundColor: Colors.white,
      body: Center(
        child: GridView.count(
          crossAxisCount: 2,
          children: <Widget>[
            ImageWidget(assetPath: 'assets/avatar.png'),
            ImageWidget(
              assetPath: 'assets/avatar.png',
              height: 50,
              width: 128,
            ), // cache
            ImageWidget(assetPath: 'assets/avatar-gray.png'),
            ImageWidget(assetPath: 'assets/avatar-gray.png'), // cache
            CircleAvatar(
              radius: 56,
              backgroundColor: Colors.transparent,
              child: Padding(
                padding: const EdgeInsets.all(8), // Border radius
                child: ClipOval(
                  child: ImageWidget(assetPath: 'assets/avatar-gray.png'),
                ),
              ),
            ),
            CupertinoButton(
              child: const Text('Open route'),
              onPressed: () {
                Navigator.push(
                  context,
                  CupertinoPageRoute(builder: (context) => const SecondRoute()),
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}

class SecondRoute extends StatelessWidget {
  const SecondRoute({super.key});

  @override
  Widget build(BuildContext context) {
    return CupertinoPageScaffold(
      navigationBar: const CupertinoNavigationBar(middle: Text('Second Route')),
      child: Center(
        child: GridView.count(
          crossAxisCount: 1,
          children: [
            CupertinoButton(
              onPressed: () {
                Navigator.pop(context);
              },
              child: const Text('Go back!'),
            ),
            ImageWidget(assetPath: 'assets/avatar-edge.png'),
          ],
        ),
      ),
    );
  }
}
