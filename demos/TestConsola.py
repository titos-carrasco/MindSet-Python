#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import time

from mindset.MindSet import *

class TestConsola():
    def __init__( self ):
        pass

    def run( self ):
        # Bluetooth version
        #   headSet = MindSet( '/dev/rfcomm4' )
        # RF version: 0x0000=connect any, 0xXXYY=connect with  0xXXY
        #   headSet = MindSet( '/dev/ttyUSB0', 0x0000 )
        msd = MindSetData()
        headSet = MindSet( '/dev/rfcomm4' )
        if( headSet.connect() ):
            t = time.time()
            while( time.time() - t < 20  ):
                headSet.getMindSetData( msd )
                print( '%d %d %d %d %d %u %u %u %u %u %u %u %u' % (
                            msd.poorSignalQuality,
                            msd.attentionESense,
                            msd.meditationESense,
                            msd.blinkStrength,
                            msd.rawWave16Bit,
                            msd.delta,
                            msd.theta,
                            msd.lowAlpha,
                            msd.highAlpha,
                            msd.lowBeta,
                            msd.highBeta,
                            msd.lowGamma,
                            msd.midGamma
                        ), flush=True )
                time.sleep( 0.001 )
            headSet.disconnect()


if( __name__ == "__main__" ):
    TestConsola().run()
