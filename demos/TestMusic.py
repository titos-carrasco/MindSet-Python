#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import rtmidi
import time

from mindset.MindSet import *

class TestMusica():
    def __init__( self ):
        pass

    def run( self ):
        midiOut = rtmidi.MidiOut()
        midiOut.open_virtual_port( 'MindSet Port' )

        # Bluetooth version
        #   headSet = MindSet( '/dev/rfcomm4' )
        # RF version: 0x0000=connect any, 0xXXYY=connect with  0xXXY
        #   headSet = MindSet( '/dev/ttyUSB0', 0x0000 )
        msd = MindSetData()
        headSet = MindSet( '/dev/rfcomm4' )
        if( headSet.connect() ):
            nota1 = [ 0 ]*4
            nota2 = [ 0 ]*4

            while( True ):
                headSet.getMindSetData( msd )
                nota = msd.attentionESense
                midiOut.send_message( [ 0x90, nota,32 ] )  # on channel 0, nota, velocidad
                nota1.append( nota )
                nota = nota1.pop(0)
                midiOut.send_message( [ 0x80, nota, 8 ] )  # off channel 0, nota, velocidad
                nota = msd.meditationESense
                midiOut.send_message( [ 0x91, nota, 32 ] )  # on channel 1, nota, velocidad
                nota2.append( nota )
                nota = nota2.pop(0)
                midiOut.send_message( [ 0x81, nota, 8 ] )  # off channel 1, nota, velocidad

                time.sleep( 2 )
            headSet.disconnect()

if( __name__ == "__main__" ):
    TestMusica().run()
