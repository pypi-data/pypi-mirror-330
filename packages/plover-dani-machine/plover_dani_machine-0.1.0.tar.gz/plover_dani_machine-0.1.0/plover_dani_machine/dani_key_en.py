# dani_key_en.py

from plover.machine.base import StenotypeBase, register_machine
from plover.misc import boolean
from plover.oslayer.keyboardcontrol import KeyboardCapture

@register_machine
class dani_key_En(StenotypeBase):
    NAME = "Dani Key (English Alphabet)"
    KEYS = (
        "A-", "B-", "C-", "D-", "E-", "F-", "G-",
        "H-", "I-", "J-", "K-", "L-", "M-",
        "N-", "O-", "P-", "Q-", "R-", "S-",
        "T-", "U-", "V-", "W-", "X-", "Y-", "Z-",
    )

    KEYS_LAYOUT = '''
    ... (unchanged keyboard layout text) ...
    '''
    ACTIONS = ('arpeggiate',)

    def __init__(self, params):
        # (your existing constructor code)
        ...

    def start_capture(self):
        # (your existing method code)
        ...

    def stop_capture(self):
        # (your existing method code)
        ...

    # plus the rest of your existing code, unchanged
    ...

    @classmethod
    def get_option_info(cls):
        return {
            'arpeggiate': (False, boolean),
            'first_up_chord_send': (False, boolean),
        }
