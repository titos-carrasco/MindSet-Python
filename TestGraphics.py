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

from rcr.mindset.MindSet import *

def main():
    #sys.setcheckinterval( 100 )

    # Bluetooth version
    #headSet = MindSet( "/dev/rfcomm4" )

    # RF version: 0x0000=connect any, 0xXXYY=connect with  0xXXYY
    headSet = MindSet( "/dev/ttyUSB0", 0x0000 )

    if( headSet.connect() ):
        msd = MindSetData()

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

        while( True ):
            try:
                attentionESense.pop( 0 )
                meditationESense.pop( 0 )
                rawWave16Bit.pop( 0 )
                delta.pop(0)
                theta.pop(0)

                headSet.getMindSetData( msd )
                attentionESense.append( msd.attentionESense );
                meditationESense.append( msd.meditationESense );
                rawWave16Bit.append( msd.rawWave16Bit );
                delta.append( msd.delta )
                theta.append( msd.theta )

                liAtt.set_ydata( attentionESense )
                liMed.set_ydata( meditationESense )
                liRaw.set_ydata( rawWave16Bit )
                liDelta.set_ydata( delta )
                #liDelta.axes.relim()
                #liDelta.axes.autoscale_view()
                liTheta.set_ydata( theta )

                time.sleep( 0.0001 )
                fig.canvas.draw()
                time.sleep( 0.0001 )

            except Exception as e:
                print( e )
                break
        headSet.disconnect()


if( __name__ == "__main__" ):
    main()
