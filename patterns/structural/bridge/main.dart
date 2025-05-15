abstract class CloudProvider {
  String bucket;

  CloudProvider(this.bucket);

  void save(String file);

  @override
  String toString() {
    return 'CloudProvider(bucket: $bucket)';
  }
}

class CloudFlareR2 extends CloudProvider {
  CloudFlareR2(String bucket) : super(bucket);

  @override
  void save(String file) {
    print('Saving $file to CloudFlare R2');
  }

  @override
  String toString() {
    return 'CloudFlareR2(bucket: $bucket)';
  }
}

class AWSS3 extends CloudProvider {
  AWSS3(String bucket) : super(bucket);

  @override
  void save(String file) {
    print('Saving $file to AWS S3');
  }

  @override
  String toString() {
    return 'AWSS3(bucket: $bucket)';
  }
}

abstract class FileStorage {
  CloudProvider provider;
  FileStorage(this.provider);

  void upload_file(String file);
}

class CloudStorage extends FileStorage {
  CloudStorage(CloudProvider provider) : super(provider);

  @override
  void upload_file(String file) {
    print('Saving $file to CloudStorage');
    provider.save(file);
    print('File $file saved to ${provider.bucket}');
  }
}

void client() {
  final cloudFlareR2 = CloudFlareR2('book-images');
  final awsS3 = AWSS3('profile-images');

  print(cloudFlareR2);
  print(awsS3);

  final cloudStorageCloudFlareR2 = CloudStorage(cloudFlareR2);
  cloudStorageCloudFlareR2.upload_file('file1.png');

  final cloudStorageAWSS3 = CloudStorage(awsS3);
  cloudStorageAWSS3.upload_file('file2.jpg');
}

void main() {
  client();
}
