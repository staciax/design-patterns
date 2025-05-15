import 'package:toml/toml.dart';
import 'dart:convert';
import 'dart:io';

class JSON {
  Future<Map<String, dynamic>> read(String path) async {
    final configString = await File(path).readAsString();
    final config = json.decode(configString);
    return config;
  }
}

class TOML {
  Future<Map<String, dynamic>> read(String path) async {
    final configDocument = await TomlDocument.load(path);
    final config = configDocument.toMap();
    return config;
  }
}

abstract class Config {
  final String filename = 'config';
  late String projectName;
  late String projectDescription;
  late String projectVersion;

  Future<Map<String, dynamic>> read();

  Future<void> setup() async {
    final config = await read();
    projectName = config['project']['name'];
    projectDescription = config['project']['description'];
    projectVersion = config['project']['version'];
  }

  @override
  String toString() {
    return 'Project Name: $projectName\n'
        'Project Description: $projectDescription\n'
        'Project Version: $projectVersion\n';
  }
}

class JSONAdapter extends Config {
  JSON handler;

  JSONAdapter(this.handler);

  @override
  Future<Map<String, dynamic>> read() async {
    return handler.read(this.filename + '.json');
  }
}

class TOMLAdapter extends Config {
  TOML handler;
  TOMLAdapter(this.handler);

  @override
  Future<Map<String, dynamic>> read() async {
    return handler.read(this.filename + '.toml');
  }
}

class Application {
  String name;
  late Config config;

  Application(this.name);

  Future<void> setConfig(Config config) async {
    await config.setup();
    this.config = config;
  }

  Config getConfig() {
    return config;
  }
}

void main() async {
  final jsonLib = JSON();
  final tomlLib = TOML();

  final jsonAdapter = JSONAdapter(jsonLib);
  final tomlAdapter = TOMLAdapter(tomlLib);

  final app = Application('app');

  await app.setConfig(tomlAdapter);
  await app.setConfig(jsonAdapter);

  print(app.getConfig());
}

// inspired by cloudflare workers configuration
// https://developers.cloudflare.com/workers/configuration
