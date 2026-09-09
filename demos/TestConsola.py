import time
from mindset.MindSet import *


class TestConsola:
    def __init__(self, port):
        # Bluetooth version
        #   headSet = MindSet( '/dev/rfcomm4' )
        # RF version: 0x0000=connect any, 0xXXYY=connect with  0xXXYY
        #   headSet = MindSet( '/dev/ttyUSB0', 0x0000 )
        self.headSet = MindSet(port)

    def run(self):
        msd = MindSetData()
        if self.headSet.connect():
            while True:
                try:
                    self.headSet.getMindSetData(msd)
                    print(
                        "%d %d %d %d %d %u %u %u %u %u %u %u %u"
                        % (
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
                            msd.midGamma,
                        ),
                        flush=True,
                    )
                    time.sleep(0.001)
                except KeyboardInterrupt:
                    break
            self.headSet.disconnect()


# -- show time
app = TestConsola("COM21")
app.run()
