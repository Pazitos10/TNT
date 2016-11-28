from channels import include, routing
from tntapp.consumers import ws_connect, ws_receive, ws_disconnect

ws_routing = [
    routing.route("websocket.connect", ws_connect),
    routing.route("websocket.receive", ws_receive),
    routing.route("websocket.disconnect", ws_disconnect),
]

channel_routing = [
    include(ws_routing, path=r"^/sync"),
]
