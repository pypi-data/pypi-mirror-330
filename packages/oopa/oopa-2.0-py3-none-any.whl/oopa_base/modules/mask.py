"""
Generate Hashcat masks
"""

from collections import defaultdict

from ..analysis import Analysis
from ..table import FrequencyTable


class MaskAnalysis(Analysis):

    def __init__(self):
        self.mask_counts = defaultdict(lambda: 0)

        super(MaskAnalysis, self).__init__()

    def analyze(self, word):
        """
        Determines appropriate mask and records it.
        """
        mask = ""
        for c in word:
            if c.isdigit():
                mask += "?d"
            elif c in "abcdefghijklmnopqrstuvwxyz":
                mask += "?l"
            elif c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                mask += "?u"
            elif c in " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~":
                mask += "?s"
            elif ord(c) >= 0xC0 and ord(c) <= 0xFF:
                mask += "?h"
            else:
                mask = None
                break

        if mask is not None:
            self.mask_counts[mask] += 1

    def report(self):
        """
        Reports mask frequency
        """
        table = FrequencyTable("Hashcat Mask")

        table.add_counts(self.word_count, self.mask_counts)

        return table
