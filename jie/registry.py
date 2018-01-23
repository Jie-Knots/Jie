import aiohttp


class ServiceRegistry:

    def __init__(self, app, loop, uri, host, port=None):
        self._app = app
        self._loop = loop
        self._uri = uri
        self._host = host
        self._port = port

    @property
    def app(self):
        return self._app

    @property
    def loop(self):
        return self._loop

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, host):
        self._uri = uri

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, host):
        self._host = host

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        self._port = port

    @property
    def register_url(self):
        url = 'http://{host}{port}{uri}'.format(host=self.host, 
                                                port=':{}'.format(self.port) if self.port else '', 
                                                uri=self.uri if self.uri.startswith('/') else '/{}'.format(self.uri))
        return url

    async def register_service(self, env):
        async with aiohttp.ClientSession() as session:  
            routes = list(self.app.router.routes_all.keys())
            app_host = env.host
            app_port = env.port
            app_name = self.app.name
            registry_data = {'routes': routes, 
                             'service_info': {'host': app_host, 'port': app_port, 'name': app_name}}
            url = self.register_url
            async with session.post(url=url, json=registry_data) as resp:
                pass

    async def unregister_service(self, env):
        async with aiohttp.ClientSession() as session:  
            app_host = env.host
            app_port = env.port
            app_name = self.app.name
            registry_data = {'service_info': {'host': app_host, 'port': app_port, 'name': app_name}}
            url = self.register_url
            async with session.delete(url=url, json=registry_data) as resp:
                pass
