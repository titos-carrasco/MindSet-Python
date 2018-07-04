#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import time

from rcr.mindset.MindSet import *

def main():
    # Bluetooth version
    #headSet = MindSet( "/dev/rfcomm4" )

    # RF version: 0x0000=connect any, 0xXXYY=connect with  0xXXY
    headSet = MindSet( "/dev/ttyUSB0", 0x0000 )

    if( headSet.connect() ):
        msd = MindSetData()
        t = time.time()
        while( time.time() - t < 20  ):
            headSet.getMindSetData( msd )
            print( "%d %d %d %d %d %u %u %u %u %u %u %u %u\n" % (
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
                    ), end= '' )
            time.sleep( 1.0 )
        headSet.disconnect()


if( __name__ == "__main__" ):
    main()
