#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import numpy as np
#import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import time
import random
import sys
import threading
import paho.mqtt.client as mqtt
import json
import queue

from mindset.MindSet import *

MQTT_SERVER = '127.0.0.1'
MQTT_PORT = 1883
MQTT_TOPIC = "rcr/demo/mindset"

class TestGraphicsMQTT():
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
        #sys.setcheckinterval( 100 )

        attentionESense = [0]*10
        meditationESense = [0]*10
        rawWave16Bit = [0]*64
        delta = [0]*10
        theta = [0]*10

        fig = plt.figure( figsize=( 9, 6 ) )
        fig.subplots_adjust( wspace=0.3, hspace=0.3 )
        plt.show( block=False )

        plt.subplot( 2, 3, 1 )
        plt.ylim( 0, 101 )
        plt.grid( True )
        plt.title( "Attention ESense", { "fontsize": 8 } )
        plt.tick_params(axis='both', which='major', labelsize=8)
        liAtt, = plt.plot( attentionESense, "r.-"  )

        plt.subplot( 2, 3, 2 )
        plt.ylim( 0, 101 )
        plt.grid( True )
        plt.title( "Meditation ESense", { "fontsize": 8 } )
        plt.tick_params(axis='both', which='major', labelsize=8)
        liMed, = plt.plot( meditationESense, "b.-" )

        plt.subplot( 2, 3, 3 )
        plt.ylim( -2048, 2048 )
        plt.grid( True )
        plt.title( "Raw Wave 16Bit", { "fontsize": 8 } )
        plt.tick_params(axis='both', which='major', labelsize=8)
        liRaw, = plt.plot( rawWave16Bit, "b-" )

        plt.subplot( 2, 3, 4 )
        plt.ylim( 0, 16777215 )
        plt.grid( True )
        plt.title( "Delta", { "fontsize": 8 } )
        plt.tick_params(axis='both', which='major', labelsize=8)
        liDelta, = plt.plot( delta, "b.-" )

        plt.subplot( 2, 3, 5 )
        plt.ylim( 0, 16777215 )
        plt.grid( True )
        plt.title( "Theta", { "fontsize": 8 } )
        plt.tick_params(axis='both', which='major', labelsize=8)
        liTheta, = plt.plot( theta, "b.-" )

        fig.canvas.flush_events()

        mqtt_client = mqtt.Client()
        mqtt_client.on_connect = self.mqtt_on_connect
        mqtt_client.on_message = self.mqtt_on_message
        mqtt_client.loop_start()
        mqtt_client.connect( self.mqtt_server, self.mqtt_port )
        time.sleep( 2 )

        while( True ):
            msg = self.messages.get()
            msd = json.loads( msg.payload )

            attentionESense.pop( 0 )
            meditationESense.pop( 0 )
            delta.pop(0)
            theta.pop(0)
            rawWave16Bit.pop( 0 )

            attentionESense.append( msd['attentionESense'] );
            meditationESense.append( msd['meditationESense'] );
            delta.append( msd['delta'] )
            theta.append( msd['theta'] )
            rawWave16Bit.append( msd['rawWave16Bit'] );

            liAtt.set_ydata( attentionESense )
            liMed.set_ydata( meditationESense )
            liDelta.set_ydata( delta )
            liTheta.set_ydata( theta )
            liRaw.set_ydata( rawWave16Bit )

            time.sleep( 0.0001 )
            fig.canvas.draw()
            fig.canvas.flush_events()
            time.sleep( 0.0001 )


if( __name__ == "__main__" ):
    TestGraphicsMQTT( MQTT_SERVER, MQTT_PORT, MQTT_TOPIC ).run()
