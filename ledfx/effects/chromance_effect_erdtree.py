import numpy as np
import voluptuous as vol

from time import time
from enum import Enum
from random import randint
from ledfx.effects.chromance_ripple import Ripple, RippleState, fmap
from ledfx.effects.chromance_config import segmentConnections, ledAssignments
from ledfx.effects.temporal import TemporalEffect
from random import uniform
import requests
import audioop
import asyncio
import math

# IP Webcam server URL
url = 'http://192.168.50.142:8080/audio.wav'









nodeConnections = [
    [-1, -1, -1, -1, 0, -1],
    [-1, -1, 3, -1, 2, -1],
    [-1, -1, 5, -1, -1, -1],
    [-1, 0, -1, 12, -1, -1],
    [-1, 2, -1, 14, 7, 1],
    [-1, 4, 10, 16, -1, 3],
    [-1, -1, -1, 18, 11, 5],
    [-1, 7, -1, 13, -1, 6],
    [-1, 9, -1, 15, -1, 8],
    [-1, 11, -1, 17, -1, 10],
    [12, -1, 19, -1, -1, -1],
    [14, -1, 21, -1, 20, -1],
    [16, -1, 23, -1, 22, -1],
    [18, -1, -1, -1, 24, -1],
    [13, 20, 25, 29, -1, -1],
    [15, 22, 27, 31, 26, 21],
    [17, 24, -1, 33, 28, 23],
    [-1, 26, -1, 30, -1, 25],
    [-1, 28, -1, 32, -1, 27],
    [29, -1, 34, -1, -1, -1],
    [31, -1, 36, -1, 35, -1],
    [33, -1, -1, -1, 37, -1],
    [30, 35, 38, -1, -1, 34],
    [32, 37, -1, -1, 39, 36],
    [-1, 39, -1, -1, -1, 38]
]


rippleColors = [
    [150, 110, 80],
    [150, 90, 50],
    [150, 110, 20],
    [150, 100, 30],
    [150, 80, 30],
    [150, 90, 0],
]

intenseRippleColors = [
    [255, 0, 0],
    [255, 40, 20],
    [255, 30, 0]
]

class ChromanceRippleEffect(TemporalEffect):
    NAME = "Chromance-Erdtree"
    CATEGORY = "2D"
    phase = 0
    volume = 0
    task = None
    future = None
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop) # Here

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
        self.ripples = [Ripple(i) for i in range(0, 20)]
        asyncio.create_task(self.run_forever())

    async def run_forever(self):
        while True:
            await self.get_audio_sync()
            await asyncio.sleep(0.02)

    def lightSegment(self, pixels, segment, color):
        leds = ledAssignments[segment]
        m, M = min(leds), max(leds)
        pixels[m:M + 1] = np.maximum(pixels[m:M + 1], color)

    async def get_audio(self, future):
        # Open a streaming session
        session = requests.Session()
        response = session.get(url, stream=True)
        try:
            # Read a 50ms audio chunk from the stream
            chunk = response.raw.read(int(16000 / 20))
            if not chunk:
                return
            # Calculate volume using audioop
            volume = audioop.rms(chunk, 2) - 3294
            # print(f"Volume: {volume}")
            future.set_result(volume)
            return volume
        except:
            return

    async def get_audio_sync(self):
        try:
            if self.task is None:
                self.future = self.loop.create_future()
                # self.loop.run_until_complete(self.get_audio(self.future))
                # def handle_future(future):
                #     print("I HANDLING")
                #     response = future.result()
                #     self.volume = response
                #     print("VOL", response)
                #     self.task = None

                # self.future.add_done_callback(handle_future)
                self.task = asyncio.create_task(self.get_audio(self.future))


        except Exception as err:
            print(err)
        if self.future.done():
            self.volume = self.future.result()
            self.task = None
        else:
            return

    def render(self):
        self.phase += 0.1

        spawnChance = 800
        useCol = rippleColors
        if self.volume > 10:
            spawnChance = 200
        if self.volume > 30:
            spawnChance = 20
            useCol = intenseRippleColors
        if self.volume > 100:
            spawnChance = 2
            useCol = intenseRippleColors

        for i in range(0, len(self.ripples)):
            ripple = self.ripples[i]
            if ripple.state == RippleState.dead:
                if randint(0, spawnChance) == 0:
                    color = useCol[randint(0, len(useCol) - 1)]
                    ripple.start(20 if randint(0,1) == 1 else 15, 0, color, uniform(0.6, 2), uniform(1000, 6000), 1,
                                 nodeConnections, segmentConnections)
            else:
                ripple.advance(self.r)

        self.r *= 0.95
        self.r[np.average(self.r, axis=2) < 10] = [0, 0, 0]
        # for i in range (0, 40):
        #     for j in range (0, 14):
        #         self.r[i][j] = self.r[i][j] * 0.94
        #         if np.average(self.r[i][j]) < 10:
        #             self.r[i][j] = [0,0,0] # too dark to show well

        pixels = np.zeros((560, 3))
        for segment in range(0, 40):
            for fromBottom in range(0, 14):
                led = round(fmap(fromBottom, 0, 13, ledAssignments[segment][1], ledAssignments[segment][0]))
                pixels[led][0] = self.r[segment][fromBottom][0]
                pixels[led][1] = self.r[segment][fromBottom][1]
                pixels[led][2] = self.r[segment][fromBottom][2]

        glowVal = 10
        glowAdd = self.phase % (glowVal * 2)
        if glowAdd > glowVal:
            glowAdd = glowVal - (glowAdd % glowVal)
        baseCol = (35 + glowAdd, 15, glowVal/2 - glowAdd/2)
        self.lightSegment(pixels, 31, baseCol)
        self.lightSegment(pixels, 15, baseCol)
        self.lightSegment(pixels, 26, baseCol)
        self.lightSegment(pixels, 25, baseCol)
        self.lightSegment(pixels, 13, baseCol)
        self.lightSegment(pixels, 6, baseCol)
        self.lightSegment(pixels, 27, baseCol)
        self.lightSegment(pixels, 28, baseCol)
        self.lightSegment(pixels, 19, baseCol)
        self.lightSegment(pixels, 24, baseCol)
        self.lightSegment(pixels, 17, baseCol)
        self.lightSegment(pixels, 11, baseCol)
        self.lightSegment(pixels, 22, baseCol)
        self.lightSegment(pixels, 21, baseCol)
        self.lightSegment(pixels, 14, baseCol)
        self.lightSegment(pixels, 16, baseCol)
        self.lightSegment(pixels, 1, baseCol)
        self.lightSegment(pixels, 4, baseCol)
        self.lightSegment(pixels, 35, baseCol)
        self.lightSegment(pixels, 36, baseCol)

        multiplier = math.log10(self.volume+1)+1

        self.pixels = pixels * multiplier
        self.volume = 0
