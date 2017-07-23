#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import rtmidi
import time

from rcr.mindset.MindSet import *

def main():
    midiOut = rtmidi.MidiOut()
    midiOut.open_virtual_port("My virtual output")

    headSet = MindSet( "/dev/rfcomm4" )
    if( headSet.connect() ):
        msd = MindSetData()
        while( True ):
            headSet.getMindSetData( msd )
            nota1 = msd.attentionESense
            nota2 = msd.meditationESense

            midiOut.send_message( [ 0x90, nota1, 127 ] )  # on channel 0, nota, velocidad
            midiOut.send_message( [ 0x91, nota2, 127 ] )  # on channel 1, nota, velocidad
            time.sleep( (msd.rawWave16Bit & 0x0F )/100 )
            midiOut.send_message( [ 0x80, nota1, 16 ] )  # off channel 0, nota, velocidad
            midiOut.send_message( [ 0x81, nota2, 16 ] )  # off channel 1, nota, velocidad

            time.sleep( 0.01 )
        headSet.disconnect()

if( __name__ == "__main__" ):
    main()
