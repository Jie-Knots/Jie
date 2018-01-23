class Services(set):

    _instance = {}

    def __new__(cls, name, *args, **kwargs):
        if not cls._instance or name not in cls._instance:
            instance = super().__new__(cls)
            instance.__name__ = name
            instance.routes = set()
            instance.routed = False
            cls._instance[name] = instance
        else:
            instance = cls._instance[name]
        return instance

    def __init__(self, name):
        pass

    def attach(self, service_info, routes):
        """
        
        :param service_info: ServiceInfo object 
        :param routes: Set
        """
        if not self.routes:
            self.routes = routes
        elif self.routes != routes:
            raise
        self.add(service_info)

    def add_routes(self, router):
        if self.routed:
            return True
        if self.routes:
            for uri in self.routes:
                route = router.routes_all.get(uri):
                if route:
                    if route.name != self.__name__:
                        raise
                    continue
                router.add(uri, ('GET',), self, strict_slashes=True)
            self.routed = True
        return True

    async def __call__(self, *args, **kwargs):
        return list(self)


class ServiceInfo:

    def __init__(self, name, host, port, routes):
        self.name = name
        self.host = host
        self.port = port
        self.routes = routes
        self.services = Services(self.name)
        self.update()

    def update(self):
        self.services.attach(self, set(routes))

    def add_routes(self, app):
        router = app.router
        self.services.add_routes(router)
