import rtmidi  # pip install python-rtmidi
import paho.mqtt.client as mqtt  # pip install paho-mqtt
import json
import time
import queue

from mindset.MindSet import *


class TestMusicaMQTT:
    def __init__(self, midi_port, mqtt_server, mqtt_port, mqtt_topic):
        self.messages = queue.Queue(1)

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

        self.midiOut = rtmidi.MidiOut()
        idx = [
            i
            for i, name in enumerate(self.midiOut.get_ports())
            if name.startswith(midi_port)
        ][0]
        self.midiOut.open_port(idx)

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
        nota1 = [0] * 4
        nota2 = [0] * 4

        self.mqtt_client.loop_start()
        self.mqtt_client.connect(self.mqtt_server, self.mqtt_port)
        time.sleep(2)
        print("Esperando datos de MQTT en el topico: " + self.mqtt_topic)
        t = time.time()
        while True:
            try:
                try:
                    msg = self.messages.get_nowait()
                except queue.Empty:
                    time.sleep(0.001)
                    continue
                except KeyboardInterrupt:
                    break
                msd = json.loads(msg.payload)
                if time.time() - t < 1:
                    continue
                t = time.time()

                nota = msd["attentionESense"]
                print("AttentionESense:", nota)
                self.midiOut.send_message(
                    [0x90, nota, 8]
                )  # on channel 0, nota, velocidad
                nota1.append(nota)
                nota = nota1.pop(0)
                self.midiOut.send_message(
                    [0x80, nota, 8]
                )  # off channel 0, nota, velocidad

                nota = msd["meditationESense"]
                print("MeditationESense:", nota)
                self.midiOut.send_message(
                    [0x91, nota, 8]
                )  # on channel 1, nota, velocidad
                nota2.append(nota)
                nota = nota2.pop(0)
                self.midiOut.send_message(
                    [0x81, nota, 8]
                )  # off channel 1, nota, velocidad
            except KeyboardInterrupt:
                break
        self.mqtt_client.disconnect()
        for nota in nota1:
            self.midiOut.send_message([0x80, nota, 0])
        for nota in nota2:
            self.midiOut.send_message([0x81, nota, 0])


# -- show time
app = TestMusicaMQTT("Vital", "127.0.0.1", 1883, "rcr/demo/mindset")
app.run()
