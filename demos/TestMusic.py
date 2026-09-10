import rtmidi  # pip install python-rtmidi
import time

from mindset.MindSet import *


class TestMusica:
    def __init__(self, port, midi_port):
        # Bluetooth version
        #   headSet = MindSet( '/dev/rfcomm4' )
        # RF version: 0x0000=connect any, 0xXXYY=connect with  0xXXY
        #   headSet = MindSet( '/dev/ttyUSB0', 0x0000 )
        self.headSet = MindSet(port)

        self.keys_chan1 = [None] * 4
        self.keys_chan2 = [None] * 4

        self.midiOut = rtmidi.MidiOut()
        idx = [
            i
            for i, name in enumerate(self.midiOut.get_ports())
            if name.startswith(midi_port)
        ][0]
        self.midiOut.open_port(idx)

    def map(self, x, in_min, in_max, out_min, out_max):
        return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    def play_note(self, channel, note, velocity):
        if channel == 1:
            keys = self.keys_chan1
        elif channel == 2:
            keys = self.keys_chan2
        else:
            return

        # note off
        k = keys.pop(0)
        if k:
            self.midiOut.send_message([0x80 + k[0] - 1, k[1], 0])

        # C1 a C6
        k = [channel, note]

        # note on
        keys.append(k)
        self.midiOut.send_message([0x90 + channel - 1, note, velocity])

        return note

    def stop_notes(self, channel):
        if channel == 1:
            keys = self.keys_chan1
        elif channel == 2:
            keys = self.keys_chan2
        else:
            return

        for k in keys:
            if k:
                self.midiOut.send_message([0x80 + k[0] - 1, k[1], 0])

    def run(self):
        msd = MindSetData()
        if self.headSet.connect():
            while True:
                try:
                    self.headSet.getMindSetData(msd)

                    sense = msd.attentionESense
                    nota = self.map(sense, 0, 100, 36, 96)
                    print(
                        f"{time.time():14.3f} AttentionESense : {sense:03d} - {nota:03d}"
                    )
                    self.play_note(1, nota, 127)

                    sense = msd.meditationESense
                    nota = self.map(sense, 0, 100, 36, 96)
                    print(
                        f"{time.time():14.3f} MeditationESense: {sense:03d} - {nota:03d}"
                    )
                    self.play_note(2, nota, 127)

                    time.sleep(1)
                except KeyboardInterrupt:
                    break
            self.headSet.disconnect()

            self.stop_notes(1)
            self.stop_notes(2)


# -- show time
app = TestMusica("COM21", "MindLink")
app.run()
