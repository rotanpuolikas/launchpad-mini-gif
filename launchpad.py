import mido
from colours import COLOURS

class Launchpad:
    def __init__(self):
        self.inport_name, self.outport_name = self._find_ports()
        self.inport = mido.open_input(self.inport_name)
        self.outport = mido.open_output(self.outport_name)

    def _find_ports(self):
        inputs = mido.get_input_names()
        outputs = mido.get_output_names()

        lp_input = next((n for n in inputs if "launchpad" in n.lower()), None)
        lp_output = next((n for n in outputs if "launchpad" in n.lower()), None)

        if not lp_input or not lp_output:
            raise RuntimeErro("launchpad not found")

        return lp_input, lp_output

    def set_top_led(self, col, colour_name):
        velocity = COLOURS.get(colour_name, 0)
        cc = 104 + col
        msg = mido.Message("control_change", control=cc, value=velocity)
        self.outport.send(msg)

    def set_right_led(self, row, colour_name):
        velocity = COLOURS.get(colour_name, 0)
        note = row * 16 + 8
        msg = mido.Message("note_on", note=note, velocity=velocity)
        self.outport.send(msg)

    def set_grid_led(self, row, col, colour_name):
        velocity = COLOURS.get(colour_name, 0)
        note = row * 16 + col
        msg = mido.Message("note_on", note=note, velocity=velocity)
        self.outport.send(msg)
