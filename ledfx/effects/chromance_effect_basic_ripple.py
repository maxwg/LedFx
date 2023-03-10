import numpy as np
import voluptuous as vol

from time import time
from enum import Enum
from random import randint
from ledfx.effects.gradient import GradientEffect
from ledfx.effects.chromance_ripple import Ripple, RippleState, fmap
from ledfx.effects.chromance_config import ledAssignments

class ChromanceRippleEffect(GradientEffect):
    NAME = "Chromance-Basic-Ripple"
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
        self.ripples = [Ripple(i) for i in range(0, 4)]


    def render(self):
        for i in range(0, len(self.ripples)):
            r = self.ripples[i]
            if r.state == RippleState.dead:
                # if (randint(0, 200) == 50):
                r.start(15, 0, (randint(0,255), randint(0,255), randint(0,255)), 0.8, 500000, 2)
            else:
                r.advance(self.r)
        self.r = self.r * 0.9
        pixels = np.zeros((560, 3))
        for segment in range(0, 40):
            for fromBottom in range(0, 14):
                led = round(fmap(fromBottom, 0, 13, ledAssignments[segment][1], ledAssignments[segment][0]))
                pixels[led][0] = self.r[segment][fromBottom][0]
                pixels[led][1] = self.r[segment][fromBottom][1]
                pixels[led][2] = self.r[segment][fromBottom][2]
        self.pixels = pixels
