from jie.controller import Blueprint, HTTPMethodView, ViewRoute

from services import ServiceInfo

registry_bp = Blueprint('registry')


@ViewRoute(registry_bp, '/_services')
class ServicesView(HTTPMethodView):

    async def post(self, request):
        data = request.json
        routes = data['routes']
        service_info = data['service_info']
        service = ServiceInfo(**service_info, routes=routes)
        service.add_routes(request.app)
