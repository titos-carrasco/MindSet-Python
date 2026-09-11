import numpy as np

import matplotlib.pyplot as plt
import time
import paho.mqtt.client as mqtt  # pip install paho-mqtt
import json
import queue

from mindset.MindSet import *


class TestGraphicsMQTT:
    def __init__(self, mqtt_server, mqtt_port, mqtt_topic):
        self.messages = queue.Queue(1)
        self.running = False

        self.mqtt_server = mqtt_server
        self.mqtt_port = mqtt_port
        self.mqtt_topic = mqtt_topic
        self.mqtt_client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2
        )
        self.mqtt_client.on_connect = self.mqtt_on_connect
        self.mqtt_client.on_subscribe = self.mqtt_on_subscribe
        self.mqtt_client.on_message = self.mqtt_on_message
        self.mqtt_client.on_disconnect = self.mqtt_on_disconnect

    def mqtt_on_connect(self, client, userdata, flags, reasonCode, properties):
        client.subscribe(self.mqtt_topic)

    def mqtt_on_subscribe(self, client, userdata, mid, reason_codes, properties):
        pass

    def mqtt_on_message(self, client, userdata, message):
        try:
            self.messages.get_nowait()
        except:
            pass
        self.messages.put_nowait(message)

    def mqtt_on_disconnect(self, client, userdata, flags, reason_code, properties):
        pass

    def run(self):
        # sys.setcheckinterval( 100 )

        attentionESense = [0] * 10
        meditationESense = [0] * 10
        rawWave16Bit = [0] * 64
        delta = [0] * 10
        theta = [0] * 10
        signal = [0] * 10

        fig = plt.figure(figsize=(9, 6))
        fig.subplots_adjust(wspace=0.3, hspace=0.3)
        plt.show(block=False)

        plt.subplot(2, 3, 1)
        plt.ylim(0, 101)
        plt.grid(True)
        plt.title("Attention ESense", {"fontsize": 8})
        plt.tick_params(axis="both", which="major", labelsize=8)
        (liAtt,) = plt.plot(attentionESense, "r.-")

        plt.subplot(2, 3, 2)
        plt.ylim(0, 101)
        plt.grid(True)
        plt.title("Meditation ESense", {"fontsize": 8})
        plt.tick_params(axis="both", which="major", labelsize=8)
        (liMed,) = plt.plot(meditationESense, "b.-")

        plt.subplot(2, 3, 3)
        plt.ylim(-2048, 2048)
        plt.grid(True)
        plt.title("Raw Wave 16Bit", {"fontsize": 8})
        plt.tick_params(axis="both", which="major", labelsize=8)
        (liRaw,) = plt.plot(rawWave16Bit, "b-")

        plt.subplot(2, 3, 4)
        plt.ylim(0, 16777215)
        plt.grid(True)
        plt.title("Delta", {"fontsize": 8})
        plt.tick_params(axis="both", which="major", labelsize=8)
        (liDelta,) = plt.plot(delta, "b.-")

        plt.subplot(2, 3, 5)
        plt.ylim(0, 16777215)
        plt.grid(True)
        plt.title("Theta", {"fontsize": 8})
        plt.tick_params(axis="both", which="major", labelsize=8)
        (liTheta,) = plt.plot(theta, "b.-")

        plt.subplot(2, 3, 6)
        plt.ylim(0, 200)
        plt.grid(True)
        plt.title("Poor Signal Quality", {"fontsize": 8})
        plt.tick_params(axis="both", which="major", labelsize=8)
        (liSIgnal,) = plt.plot(signal, "b.-")

        fig.canvas.flush_events()

        self.mqtt_client.loop_start()
        self.mqtt_client.connect(self.mqtt_server, self.mqtt_port)
        time.sleep(2)

        self.running = True
        fig.canvas.mpl_connect(
            "close_event", lambda event: setattr(self, "running", False)
        )
        while self.running:
            try:
                try:
                    msg = self.messages.get_nowait()
                    msd = json.loads(msg.payload)

                    attentionESense.pop(0)
                    meditationESense.pop(0)
                    delta.pop(0)
                    theta.pop(0)
                    rawWave16Bit.pop(0)
                    signal.pop(0)

                    attentionESense.append(msd["attentionESense"])
                    meditationESense.append(msd["meditationESense"])
                    delta.append(msd["delta"])
                    theta.append(msd["theta"])
                    rawWave16Bit.append(msd["rawWave16Bit"])
                    signal.append(msd["poorSignalQuality"])

                    liAtt.set_ydata(attentionESense)
                    liMed.set_ydata(meditationESense)
                    liDelta.set_ydata(delta)
                    liTheta.set_ydata(theta)
                    liRaw.set_ydata(rawWave16Bit)
                    liSIgnal.set_ydata(signal)
                except queue.Empty:
                    pass
                time.sleep(0.0001)
                fig.canvas.draw()
                fig.canvas.flush_events()
                time.sleep(0.0001)
            except KeyboardInterrupt:
                break
        plt.close("all")
        self.mqtt_client.disconnect()


# -- show time
app = TestGraphicsMQTT("127.0.0.1", 1883, "rcr/demo/mindset")
app.run()
