import numpy as np
import matplotlib.pyplot as plt
import time

from mindset.MindSet import *


class TestGraphics:
    def __init__(self, port):
        # Bluetooth version
        #   headSet = MindSet( '/dev/rfcomm4' )
        # RF version: 0x0000=connect any, 0xXXYY=connect with  0xXXY
        #   headSet = MindSet( '/dev/ttyUSB0', 0x0000 )
        self.headSet = MindSet(port)
        self.running = False

    def run(self):
        attentionESense = np.zeros(100)
        meditationESense = np.zeros(100)
        rawWave16Bit = np.zeros(100)
        delta = np.zeros(100)
        theta = np.zeros(100)
        signal = np.zeros(100)

        fig = plt.figure()
        dpi = fig.dpi
        width = 1024.0
        height = 768.0
        fig.set_size_inches(width / dpi, height / dpi)
        fig.subplots_adjust(
            left=0.10, right=0.95, top=0.90, bottom=0.10, wspace=0.3, hspace=0.3
        )
        fig.canvas.manager.set_window_title("MindSet Data")

        axes = []

        ax1 = plt.subplot(2, 3, 1)
        plt.ylim(0, 110)
        plt.grid(True)
        plt.title("Attention ESense", {"fontsize": 8})
        plt.tick_params(axis="both", which="major", labelsize=8)
        (liAtt,) = plt.plot(attentionESense, "r-", animated=True)
        axes.append(ax1)

        ax2 = plt.subplot(2, 3, 2)
        plt.ylim(0, 110)
        plt.grid(True)
        plt.title("Meditation ESense", {"fontsize": 8})
        plt.tick_params(axis="both", which="major", labelsize=8)
        (liMed,) = plt.plot(meditationESense, "b-", animated=True)
        axes.append(ax2)

        ax3 = plt.subplot(2, 3, 3)
        plt.ylim(-2100, 2100)
        plt.grid(True)
        plt.title("Raw Wave 16Bit", {"fontsize": 8})
        plt.tick_params(axis="both", which="major", labelsize=8)
        (liRaw,) = plt.plot(rawWave16Bit, "b-", animated=True)
        axes.append(ax3)

        ax4 = plt.subplot(2, 3, 4)
        plt.ylim(0, 16777215)
        plt.grid(True)
        plt.title("Delta", {"fontsize": 8})
        plt.tick_params(axis="both", which="major", labelsize=8)
        (liDelta,) = plt.plot(delta, "b-", animated=True)
        axes.append(ax4)

        ax5 = plt.subplot(2, 3, 5)
        plt.ylim(0, 16777215)
        plt.grid(True)
        plt.title("Theta", {"fontsize": 8})
        plt.tick_params(axis="both", which="major", labelsize=8)
        (liTheta,) = plt.plot(theta, "b-", animated=True)
        axes.append(ax5)

        ax6 = plt.subplot(2, 3, 6)
        plt.ylim(0, 210)
        plt.grid(True)
        plt.title("Poor Signal Quality", {"fontsize": 8})
        plt.tick_params(axis="both", which="major", labelsize=8)
        (liSIgnal,) = plt.plot(signal, "b-", animated=True)
        axes.append(ax6)

        plt.show(block=False)
        plt.pause(0.1)

        backgrounds = [fig.canvas.copy_from_bbox(ax.bbox) for ax in axes]

        msd = MindSetData()
        if self.headSet.connect():
            self.running = True
            fig.canvas.mpl_connect(
                "close_event", lambda event: setattr(self, "running", False)
            )
            while self.running:
                try:
                    self.headSet.getMindSetData(msd)

                    attentionESense[:-1] = attentionESense[1:]
                    attentionESense[-1] = msd.attentionESense

                    meditationESense[:-1] = meditationESense[1:]
                    meditationESense[-1] = msd.meditationESense

                    delta[:-1] = delta[1:]
                    delta[-1] = msd.delta

                    theta[:-1] = theta[1:]
                    theta[-1] = msd.theta

                    rawWave16Bit[:-1] = rawWave16Bit[1:]
                    rawWave16Bit[-1] = msd.rawWave16Bit

                    signal[:-1] = signal[1:]
                    signal[-1] = msd.poorSignalQuality

                    for bg, ax in zip(backgrounds, axes):
                        fig.canvas.restore_region(bg)

                    liAtt.set_ydata(attentionESense)
                    liMed.set_ydata(meditationESense)
                    liDelta.set_ydata(delta)
                    liTheta.set_ydata(theta)
                    liRaw.set_ydata(rawWave16Bit)
                    liSIgnal.set_ydata(signal)

                    ax1.draw_artist(liAtt)
                    ax2.draw_artist(liMed)
                    ax3.draw_artist(liRaw)
                    ax4.draw_artist(liDelta)
                    ax5.draw_artist(liTheta)
                    ax6.draw_artist(liSIgnal)

                    fig.canvas.blit(fig.bbox)
                    fig.canvas.flush_events()
                    time.sleep(0.001)
                except KeyboardInterrupt:
                    self.running = False
            plt.close("all")
            self.headSet.disconnect()


# -- show time
app = TestGraphics("COM21")
app.run()
