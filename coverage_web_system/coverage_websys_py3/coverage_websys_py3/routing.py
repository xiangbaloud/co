# channels 2.1.2
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

import coverage_websys_func.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            coverage_websys_func.routing.urlpatterns
        )
    ),
    'http': URLRouter(coverage_websys_func.routing.urlpatterns),
})

# channels 1.1.5
# from channels import route
# from coverage_websys_func.consumers import ws_connect, ws_disconnect, message_handler

# channel_routing = [
#     route('websocket.connect', ws_connect),
#     route('websocket.disconnect', ws_disconnect),
#     route("websocket.receive", message_handler)
# ]