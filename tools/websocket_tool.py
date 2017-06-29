#!/usr/bin/python
# Be responsible... 

import binascii
import uuid

from websocket import *
ws = create_connection("ws://localhost:19870/general")

#{"SEQ":"12345","CMD":""} - Get command list on any service. 
#{"SEQ":"12345","CMD":"get_info"} - Serial Number & User Token
#{"SEQ":"12345","CMD":"read","INDEX":"fly_limit_height"} - Read fly_limit_height
#{"SEQ":"12345","CMD":"write","INDEX":"fly_limit_height", "VALUE":111} - Set fly_limit_height ( limited by Max value )

ws.settimeout(2)
try:
    appstatus =  ws.recv()
    appversion =  ws.recv()
    appflags =  ws.recv()
    configstatus =  ws.recv()
    devicestatus =  ws.recv()
    pcstatus =  ws.recv()

    deviceHash = devicestatus.split(",")[3].strip().split(":")[1].split('"')[1] # Extract Hash_ServiceID
    print "Connecting to " + deviceHash
    print "------------------"
    devConfigURL = "ws://localhost:19870/controller/config/user/" + deviceHash
    ws.close

    if devicestatus.find(devConfigURL):
        print "Connecting to " + devConfigURL
        ws = create_connection(devConfigURL)
        commands = ws.recv()
        # print commands
        if commands.find("read"):
            print "Reading fly_limit_height over the websocket"
            ws.send('{"SEQ":"' + str(uuid.uuid4().get_hex().upper()[0:6]) + '","CMD":"read","INDEX":"fly_limit_height"}')
            result = ws.recv()
            print result
        else:
            print "No read command available in the Websocket API for this service"
        if commands.find("write"):
            print "Writing to fly_limit_height value over the websocket"
            ws.send('{"SEQ":"' + str(uuid.uuid4().get_hex().upper()[0:6]) + '","CMD":"write","INDEX":"fly_limit_height", "VALUE":111}')
            result = ws.recv()
            print result
        else:
            print "No read command available in the Websocket API for this service"
    else:
        print "Necessary Service is not present"


except WebSocketTimeoutException as e:
    print e

ws.close()

