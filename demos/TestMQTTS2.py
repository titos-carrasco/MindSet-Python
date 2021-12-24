#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import rtmidi
import paho.mqtt.client as mqtt
import json
import time
import queue

from mindset.MindSet import *

MQTT_SERVER = '127.0.0.1'
MQTT_PORT = 1883
MQTT_TOPIC = "rcr/demo/mindset"

MQTT_S2_TOPIC = "rcr/S2"

class TestS2MQTT():
    def __init__( self, mqtt_server, mqtt_port, mqtt_topic, mqtt_s2_topic ):
        self.mqtt_server = mqtt_server
        self.mqtt_port = mqtt_port
        self.mqtt_topic = mqtt_topic
        self.mqtt_s2_topic = mqtt_s2_topic
        self.messages = queue.Queue( 1 )

    def mqtt_on_connect( self, client, userdata, flags, rc ):
        client.subscribe( self.mqtt_topic )

    def mqtt_on_message( self, client, userdata, message ):
        try:
            self.messages.get_nowait()
        except:
            pass
        self.messages.put_nowait( message )

    def run( self ):
        mqtt_client = mqtt.Client()
        mqtt_client.on_connect = self.mqtt_on_connect
        mqtt_client.on_message = self.mqtt_on_message
        mqtt_client.loop_start()
        mqtt_client.connect( self.mqtt_server, self.mqtt_port )
        time.sleep( 2 )

        moving = False
        while( True ):
            msg = self.messages.get()
            msd = json.loads( msg.payload )
            print( msd )

            value = msd['attentionESense']
            if( not moving and value > 80 ):
                mqtt_client.publish( self.mqtt_s2_topic, 'izquierda' )
                moving = True
            elif( moving and value <= 80 ):
                mqtt_client.publish( self.mqtt_s2_topic, 'detente' )
                moving = False

if( __name__ == "__main__" ):
    TestS2MQTT( MQTT_SERVER, MQTT_PORT, MQTT_TOPIC, MQTT_S2_TOPIC ).run()
