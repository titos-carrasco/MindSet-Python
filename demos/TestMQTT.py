import paho.mqtt.client as mqtt  # pip install paho-mqtt
import json
import time

from mindset.MindSet import *


class TestMQTT:
    def __init__(self, port, mqtt_server, mqtt_port, mqtt_topic):
        # Bluetooth version
        #   headSet = MindSet( '/dev/rfcomm4' )
        # RF version: 0x0000=connect any, 0xXXYY=connect with  0xXXY
        #   headSet = MindSet( '/dev/ttyUSB0', 0x0000 )
        self.headSet = MindSet(port)

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
        pass

    def mqtt_on_subscribe(self, client, userdata, mid, reason_codes, properties):
        pass

    def mqtt_on_message(self, client, userdata, message):
        pass

    def mqtt_on_disconnect(self, client, userdata, flags, reason_code, properties):
        pass

    def run(self):
        self.mqtt_client.loop_start()
        self.mqtt_client.connect(self.mqtt_server, self.mqtt_port)
        time.sleep(2)

        msd = MindSetData()
        if self.headSet.connect():
            while True:
                try:
                    self.headSet.getMindSetData(msd)
                    data = json.dumps(msd.__dict__)
                    self.mqtt_client.publish(self.mqtt_topic, data)
                    print(data)
                    time.sleep(0.5)
                except KeyboardInterrupt:
                    break
            self.headSet.disconnect()
            self.mqtt_client.disconnect()


# -- show time
app = TestMQTT("COM21", "127.0.0.1", 1883, "rcr/demo/mindset")
app.run()
