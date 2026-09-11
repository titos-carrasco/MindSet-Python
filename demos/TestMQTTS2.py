import paho.mqtt.client as mqtt  # pip install paho-mqtt
import json
import time
import queue

from mindset.MindSet import *


class TestS2MQTT:
    def __init__(self, mqtt_server, mqtt_port, mqtt_topic, mqtt_s2_topic):
        self.messages = queue.Queue(1)

        self.mqtt_server = mqtt_server
        self.mqtt_port = mqtt_port
        self.mqtt_topic = mqtt_topic
        self.mqtt_s2_topic = mqtt_s2_topic
        self.mqtt_s2_topic = mqtt_s2_topic
        self.mqtt_client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2
        )
        self.mqtt_client.on_connect = self.mqtt_on_connect
        self.mqtt_client.on_message = self.mqtt_on_message

    def mqtt_on_connect(self, client, userdata, flags, reasonCode, properties):
        client.subscribe(self.mqtt_topic)

    def mqtt_on_message(self, client, userdata, message):
        try:
            self.messages.get_nowait()
        except:
            pass
        self.messages.put_nowait(message)

    def run(self):
        self.mqtt_client.loop_start()
        self.mqtt_client.connect(self.mqtt_server, self.mqtt_port)
        time.sleep(2)
        print("Esperando datos de MQTT en el topico: " + self.mqtt_topic)

        moving = 0
        while True:
            try:
                msg = self.messages.get()
                msd = json.loads(msg.payload)

                value = msd["attentionESense"]
                print(
                    f"Poor Signal Quality: {msd['poorSignalQuality']:03d} - Attention ESense: {value:03d}"
                )
                if value < 20 and moving > 0:
                    self.mqtt_client.publish(self.mqtt_s2_topic, "detente")
                    moving = 0
                elif value >= 20 and value != moving:
                    self.mqtt_client.publish(self.mqtt_s2_topic, f"MOVE {value}")
                    moving = value
            except queue.Empty:
                time.sleep(0.001)
            except KeyboardInterrupt:
                break
        self.mqtt_client.disconnect()


# -- show time
app = TestS2MQTT("127.0.0.1", 1883, "rcr/demo/mindset", "rcr/s2")
app.run()
