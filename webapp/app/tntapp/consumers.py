from channels import Group
from channels.sessions import enforce_ordering
import json

# Connected to websocket.connect
@enforce_ordering(slight=True)
def ws_connect(message):
    print "Websocket connected: %s" % (message.reply_channel)
    Group("notifications").add(message.reply_channel)

# Connected to websocket.disconnect
@enforce_ordering(slight=True)
def ws_disconnect(message):
    Group("notifications").discard(message.reply_channel)

@enforce_ordering(slight=True)
def ws_receive(message):
    print "Receiving: '%s' from %s" % (message.content['text'], message.content['reply_channel'])
    # To test if the app can send something back to the clients enable the following
    Group("notifications").send({
        "text": json.dumps(message.content['text']),
    })
