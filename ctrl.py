import time
import rtmidi

from rtmidi.midiutil import open_midioutput, open_midiinput, list_available_ports, list_output_ports, list_input_ports

DEFAULT_IN_PORT = 4
DEFAULT_OUT_PORT = 5


def select_port(port_type="input"):
    if port_type=="input":
        list_input_ports()
    elif port_type=="output":
        list_output_ports()
    print("Select Port by number: ", end="")
    return int(input())


class Device(object):
    def __init__(self, name="unnamed", channel=7, interactive=False):
        self.name = name
        self.channel = channel 
        if interactive:
            self.output, self.outname = open_midioutput(select_port("output"))
            self.input,  self.inname  = open_midiinput (select_port("input"))
            self.init_callback()
        else:
            self.output = self.input = None
            self.outname = self.inname = "Uninitialized"

    def init_callback(self):
        self.input.set_callback(self.input_callback) 

    def input_callback(self, event, date=None):
        message, deltatime = event
        print("[%s] %r" % (self.name, message))

    def send(self, cc, value):
        channel_byte = 0xB0 + self.channel - 1
        self.output.send_message([channel_byte, cc, value])


class MidiLoop(Device):

    def __init__(self):
        super().__init__("MidiLoop", 7)
        self.output, self.outname = open_midioutput(1)
        self.input,  self.inname  = open_midiinput (0)
        self.init_callback()


class BCR2k(Device):
       
    def __init__(self):
        super().__init__("BCR2k", 7)
        self.output, self.outname = open_midioutput(DEFAULT_OUT_PORT)
        self.input,  self.inname  = open_midiinput (DEFAULT_IN_PORT)
        self.init_callback()

bcr = BCR2k()
loop = MidiLoop()

cc_1 = [182, 2, 127]
bcr.send(3, 0)
bcr.send(4, 0)
bcr.send(5, 0)


try:
    while True:
        pass
except KeyboardInterrupt:
    print("Exiting...")

def fun(bcr):
    x = 0
    import math
    import time
    while True:
        time.sleep(0.05)
        v = min(math.sin(x) * 64 + 64, 127)
        bcr.send(3, v)
        x += 0.2
