#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import paho.mqtt.client as mqtt
import json
import time

from mindset.MindSet import *

MQTT_SERVER = '127.0.0.1'
MQTT_PORT = 1883
MQTT_TOPIC = "rcr/demo/mindset"

class TestMQTT():
    def __init__( self, mqtt_server, mqtt_port, mqtt_topic ):
        self.mqtt_server = mqtt_server
        self.mqtt_port = mqtt_port
        self.mqtt_topic = mqtt_topic

    def mqtt_on_connect( self, client, userdata, flags, rc ):
        pass

    def mqtt_on_message( self, client, userdata, msg ):
        pass

    def run( self ):
        mqtt_client = mqtt.Client()
        mqtt_client.on_connect = self.mqtt_on_connect
        mqtt_client.on_message = self.mqtt_on_message
        mqtt_client.loop_start()
        mqtt_client.connect( self.mqtt_server, self.mqtt_port )
        time.sleep( 2 )

        # Bluetooth version
        #   headSet = MindSet( '/dev/rfcomm4' )
        # RF version: 0x0000=connect any, 0xXXYY=connect with  0xXXY
        #   headSet = MindSet( '/dev/ttyUSB0', 0x0000 )
        msd = MindSetData()
        headSet = MindSet( '/dev/rfcomm4' )
        if( headSet.connect() ):
            while( True  ):
                headSet.getMindSetData( msd )
                data = json.dumps( msd.__dict__ )
                mqtt_client.publish( self.mqtt_topic, data )
                print( data )
                time.sleep( 0.5 )
            headSet.disconnect()


if( __name__ == "__main__" ):
    TestMQTT( MQTT_SERVER, MQTT_PORT, MQTT_TOPIC ).run()
