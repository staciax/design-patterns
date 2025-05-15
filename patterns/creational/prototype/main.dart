abstract class FileSystemProtoype {
  String name;

  FileSystemProtoype(this.name);

  FileSystemProtoype rename(String name) {
    this.name = name;
    return this;
  }

  FileSystemProtoype clone();
}

class File extends FileSystemProtoype {
  int size;

  File(String name, this.size) : super(name);

  @override
  File clone() {
    return File(name, size);
  }

  @override
  String toString() {
    return 'File: $name, size: $size';
  }
}

class Directory extends FileSystemProtoype {
  List<FileSystemProtoype> children;

  Directory(String name, [this.children = const []]) : super(name);

  void add(FileSystemProtoype child) {
    children.add(child);
  }

  @override
  Directory clone() {
    return Directory(name, children.map((child) => child.clone()).toList());
  }

  @override
  String toString() {
    return 'Directory: $name, children: $children';
  }
}

void client() {
  final file1 = File('main.py', 150);
  final file2 = File('diagram.drawio', 300);

  print(file1);
  print(file2);

  print('-' * 90);

  final directory = Directory('d1', [file1, file2]);
  print(directory);

  print('-' * 90);

  final directory2 = Directory('d2', [directory]);
  print(directory2);

  directory2.add(file1.clone().rename('main copy.py'));
  directory2.add(file2.clone().rename('diagram copy.drawio'));
  print(directory2);

  print('-' * 90);

  final directory3 = directory.clone().rename('d3');
  print(directory3);
}

void main() {
  client();
}
