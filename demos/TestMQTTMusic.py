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

class TestMusicaMQTT():
    def __init__( self, mqtt_server, mqtt_port, mqtt_topic ):
        self.mqtt_server = mqtt_server
        self.mqtt_port = mqtt_port
        self.mqtt_topic = mqtt_topic
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
        midiOut = rtmidi.MidiOut()
        midiOut.open_virtual_port( 'MindSet Port' )

        nota1 = [ 0 ]*4
        nota2 = [ 0 ]*4

        mqtt_client = mqtt.Client()
        mqtt_client.on_connect = self.mqtt_on_connect
        mqtt_client.on_message = self.mqtt_on_message
        mqtt_client.loop_start()
        mqtt_client.connect( self.mqtt_server, self.mqtt_port )
        time.sleep( 2 )

        while( True ):
            msg = self.messages.get()
            msd = json.loads( msg.payload )

            nota = msd['attentionESense']
            midiOut.send_message( [ 0x90, nota,8 ] )  # on channel 0, nota, velocidad
            nota1.append( nota )
            nota = nota1.pop(0)
            midiOut.send_message( [ 0x80, nota, 8 ] )  # off channel 0, nota, velocidad
            nota = msd['meditationESense']
            midiOut.send_message( [ 0x91, nota, 8 ] )  # on channel 1, nota, velocidad
            nota2.append( nota )
            nota = nota2.pop(0)
            midiOut.send_message( [ 0x81, nota, 8 ] )  # off channel 1, nota, velocidad

if( __name__ == "__main__" ):
    TestMusicaMQTT( MQTT_SERVER, MQTT_PORT, MQTT_TOPIC ).run()
