import numpy as np
import voluptuous as vol

from time import time
from enum import Enum
from random import randint
from ledfx.effects.chromance_ripple import Ripple, RippleState, fmap
from ledfx.effects.chromance_config import segmentConnections, ledAssignments
from ledfx.effects.audio import AudioReactiveEffect
from random import uniform








nodeConnections = [
    [-1, -1, -1, -1, 0, -1],
    [-1, -1, 3, -1, 2, -1],
    [-1, -1, 5, -1, -1, -1],
    [-1, 0, 6, 12, -1, -1],
    [-1, 2, 8, 14, 7, 1],
    [-1, 4, 10, 16, 9, 3],
    [-1, -1, -1, 18, 11, 5],
    [-1, 7, -1, 13, -1, 6],
    [-1, 9, -1, 15, -1, 8],
    [-1, 11, -1, 17, -1, 10],
    [12, -1, 19, -1, -1, -1],
    [14, -1, 21, -1, 20, -1],
    [16, -1, 23, -1, 22, -1],
    [18, -1, -1, -1, 24, -1],
    [13, 20, 25, 29, -1, -1],
    [15, 22, -1, -1, -1, 21],
    [17, 24, -1, 33, 28, 23],
    [-1, 26, -1, 30, -1, 25],
    [-1, 28, -1, 32, -1, 27],
    [29, -1, 34, -1, -1, -1],
    [31, -1, -1, -1, -1, -1],
    [33, -1, -1, -1, 37, -1],
    [30, 35, 38, -1, -1, 34],
    [32, 37, -1, -1, 39, 36],
    [-1, 39, -1, -1, -1, 38]
]


class ChromanceRippleEffect(AudioReactiveEffect):
    NAME = "Chromance-Erdtree"
    CATEGORY = "2D"

    CONFIG_SCHEMA = vol.Schema(
        {
            vol.Optional(
                "align",
                description="Alignment of bands",
                default="left",
            ): vol.In(list(["left", "right", "invert", "center"])),
            vol.Optional(
                "gradient_repeat",
                description="Repeat the gradient into segments",
                default=6,
            ): vol.All(vol.Coerce(int), vol.Range(min=1, max=16)),
            vol.Optional(
                "mirror",
                description="Mirror the effect",
                default=False,
            ): bool,
        }
    )

    def on_activate(self, pixel_count):
        self.r = np.zeros((40, 14, 3))
        self.ripples = [Ripple(i) for i in range(0, 40)]


    def render(self):
        for i in range(0, len(self.ripples)):
            r = self.ripples[i]
            if r.state == RippleState.dead:
                if (randint(0, 30) == 5):
                    r.start(15 if randint(0,1) == 0 else 20, 0, (randint(190,255), randint(160,220), randint(0,50)), uniform(0.6, 3), uniform(2000, 8000), randint(2,4), nodeConnections, segmentConnections)
            else:
                r.advance(self.r)
        for i in range (0, 40):
            for j in range (0, 14):
                self.r[i][j] = self.r[i][j] * 0.9
                if np.average(self.r[i][j]) < 10:
                    self.r[i][j] = [0,0,0] # too dark to show well
        pixels = np.zeros((560, 3))
        for segment in range(0, 40):
            for fromBottom in range(0, 14):
                led = round(fmap(fromBottom, 0, 13, ledAssignments[segment][1], ledAssignments[segment][0]))
                pixels[led][0] = self.r[segment][fromBottom][0]
                pixels[led][1] = self.r[segment][fromBottom][1]
                pixels[led][2] = self.r[segment][fromBottom][2]
        self.pixels = pixels
