import 'package:flutter/material.dart';

class ImageFlyweight {
  String assetPath;
  Image image;

  ImageFlyweight(this.assetPath) : image = Image.asset(assetPath);

  Image resize(int width, int height) {
    return Image(image: ResizeImage(image.image, width: width, height: height));
  }
}

class ImageCacheFactory {
  static final Map<String, ImageFlyweight> imageCache = {};

  static ImageFlyweight getImage(String assetPath) {
    if (!imageCache.containsKey(assetPath)) {
      print('add to cache: $assetPath');
      imageCache[assetPath] = ImageFlyweight(assetPath);
    }
    print('use cache: $assetPath');
    return imageCache[assetPath]!;
  }

  static List<ImageFlyweight> getImages() {
    return imageCache.values.toList();
  }
}

// ignore: must_be_immutable
class ImageWidget extends StatelessWidget {
  String assetPath;
  late ImageFlyweight image;
  final int width;
  final int height;

  ImageWidget({
    super.key,
    required this.assetPath,
    this.width = 100,
    this.height = 100,
  }) {
    image = ImageCacheFactory.getImage(assetPath);
  }

  @override
  Widget build(BuildContext context) {
    return image.resize(width, height);
  }
}
