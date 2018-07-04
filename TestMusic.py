#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import rtmidi
import time

from rcr.mindset.MindSet import *

def main():
    midiOut = rtmidi.RtMidiOut()
    midiOut.openVirtualPort("MindSet Port")

    # Bluetooth version
    #headSet = MindSet( "/dev/rfcomm4" )

    # RF version: 0x0000=connect any, 0xXXYY=connect with  0xXXYY
    headSet = MindSet( "/dev/ttyUSB0", 0x0000 )

    if( headSet.connect() ):
        msd = MindSetData()
        while( True ):
            headSet.getMindSetData( msd )
            nota1 = msd.attentionESense
            nota2 = msd.meditationESense

            midiOut.sendMessage( rtmidi.MidiMessage.noteOn( 0, nota1, 127 ) ) # channel, note, velocity
            midiOut.sendMessage( rtmidi.MidiMessage.noteOn( 1, nota2, 127 ) ) # channel, note, velocity
            time.sleep( (msd.rawWave16Bit & 0x0F )/10 )
            midiOut.sendMessage( rtmidi.MidiMessage.noteOff( 0, nota1 ) )     # channel, note
            midiOut.sendMessage( rtmidi.MidiMessage.noteOff( 1, nota2 ) )     # channel, note

            time.sleep( 0.0001 )
        headSet.disconnect()

if( __name__ == "__main__" ):
    main()
