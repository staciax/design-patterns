abstract class IServer {
  void handle_request(String request);
}

class Server implements IServer {
  final String name;

  Server(this.name);

  @override
  void handle_request(String request) {
    print('Server $name handling request: $request');
  }
}

class LoadBalancerProxy implements IServer {
  final List<Server> servers;
  int _current = 0;

  LoadBalancerProxy(this.servers);

  @override
  void handle_request(String request) {
    final server = servers[_current];
    _current = (_current + 1) % servers.length;
    server.handle_request(request);
  }
}

void client() {
  final servers = [
    Server('Server 1'),
    Server('Server 2'),
    Server('Server 3'),
  ];

  final loadBalancer = LoadBalancerProxy(servers);

  loadBalancer.handle_request('Request 1');
  loadBalancer.handle_request('Request 2');
  loadBalancer.handle_request('Request 3');

  loadBalancer.handle_request('Request 4');
  loadBalancer.handle_request('Request 5');
  loadBalancer.handle_request('Request 6');
}

void main() {
  client();
}
