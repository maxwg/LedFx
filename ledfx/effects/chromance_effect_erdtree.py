import numpy as np
import voluptuous as vol

from time import time
from enum import Enum
from random import randint
from ledfx.effects.chromance_ripple import Ripple, RippleState, fmap
from ledfx.effects.chromance_config import segmentConnections, ledAssignments, led_order
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
    [150, 120, 80],
    [150, 90, 50],
    [150, 120, 20],
    [150, 100, 30],
    [150, 80, 30],
    [150, 90, 0],
]

intenseRippleColors = [
    [255, 0, 0],
    [255, 40, 20],
    [255, 30, 0]
]

segsToLight = [70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335]

class ChromanceRippleEffect(TemporalEffect):
    NAME = "Chromance-Erdtree"
    CATEGORY = "2D"
    phase = 0
    volume = np.zeros(60)
    vIdx = 0
    wroteVol = False
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

    def lightSegment(self, pixels, segment, color ,arr):
        leds = ledAssignments[segment]
        m = min(leds[0], leds[1])
        M = max(leds[0], leds[1])
        for i in range(m, M + 1):
            arr.append(i)
            pixels[i][0] = max(color[0], pixels[i][0])
            pixels[i][1] = max(color[1], pixels[i][1])
            pixels[i][2] = max(color[2], pixels[i][2])
        # leds = ledAssignments[segment]
        # m, M = min(leds), max(leds)
        # pixels[m:M + 1] = np.maximum(pixels[m:M + 1], color)

    def lightPixels(self, pixels, indexes, color):
        for i in indexes:
            pixels[i][0] = max(color[0], pixels[i][0])
            pixels[i][1] = max(color[1], pixels[i][1])
            pixels[i][2] = max(color[2], pixels[i][2])

    async def get_audio(self, future):
        # Open a streaming session
        session = requests.Session()
        response = session.get(url, stream=True)
        try:
            # Read a 25ms audio chunk from the stream
            chunk = response.raw.read(int(16000 / 40))
            if not chunk:
                return
            # Calculate volume using audioop
            volume = audioop.rms(chunk, 2) - 4659
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
            self.wroteVol = True
            self.volume[self.vIdx] = self.future.result()
            self.task = None
        else:
            return

    def render(self):
        a = time()
        self.phase += 0.1

        spawnChance = 800
        useCol = rippleColors
        vol = self.volume[self.vIdx]
        if self.wroteVol:
            if vol > 10:
                spawnChance = 200
            if vol > 20:
                spawnChance = 80
            if vol > 60:
                spawnChance = 20
                useCol = intenseRippleColors
            if vol > 140:
                spawnChance = 5
                useCol = intenseRippleColors
        else:
            self.volume[self.vIdx] = 0

        for i in range(0, len(self.ripples)):
            ripple = self.ripples[i]
            if ripple.state == RippleState.dead:
                if randint(0, spawnChance) == 0:
                    color = useCol[randint(0, len(useCol) - 1)]
                    ripple.start(20 if randint(0,1) == 1 else 15, 0, color, uniform(0.6, 2), uniform(1000, 6000), 1,
                                 nodeConnections, segmentConnections)
            else:
                ripple.advance(self.r)

        b = time()
        # print("AB", (b - a)*1000)

        self.r *= 0.94
        self.r[np.average(self.r, axis=2) < 10] = [0, 0, 0]
        # for i in range (0, 40):
        #     for j in range (0, 14):
        #         self.r[i][j] = self.r[i][j] * 0.94
        #         if np.average(self.r[i][j]) < 10:
        #             self.r[i][j] = [0,0,0] # too dark to show well

        pixels = np.zeros((560, 3))
        i = 0
        for segment in range(0, 40):
            for fromBottom in range(0, 14):
                # led = round(fmap(fromBottom, 0, 13, ledAssignments[segment][1], ledAssignments[segment][0]))
                pixels[led_order[i]] = self.r[segment][fromBottom]
                i += 1
                # pixels[led][0] = self.r[segment][fromBottom][0]
                # pixels[led][1] = self.r[segment][fromBottom][1]
                # pixels[led][2] = self.r[segment][fromBottom][2]

        c = time()
        # print("BC", (c - b)*1000)

        glowVal = 10
        glowAdd = self.phase % (glowVal * 2)
        if glowAdd > glowVal:
            glowAdd = glowVal - (glowAdd % glowVal)
        baseCol = (35 + glowAdd, 15, glowVal/2 - glowAdd/2)
        # arr = []
        # self.lightSegment(pixels, 31, baseCol, arr)
        # self.lightSegment(pixels, 15, baseCol, arr)
        # self.lightSegment(pixels, 26, baseCol, arr)
        # self.lightSegment(pixels, 25, baseCol, arr)
        # self.lightSegment(pixels, 13, baseCol, arr)
        # self.lightSegment(pixels, 6, baseCol, arr)
        # self.lightSegment(pixels, 27, baseCol, arr)
        # self.lightSegment(pixels, 28, baseCol, arr)
        # self.lightSegment(pixels, 19, baseCol, arr)
        # self.lightSegment(pixels, 24, baseCol, arr)
        # self.lightSegment(pixels, 17, baseCol, arr)
        # self.lightSegment(pixels, 11, baseCol, arr)
        # self.lightSegment(pixels, 22, baseCol, arr)
        # self.lightSegment(pixels, 21, baseCol, arr)
        # self.lightSegment(pixels, 14, baseCol, arr)
        # self.lightSegment(pixels, 16, baseCol, arr)
        # self.lightSegment(pixels, 1, baseCol, arr)
        # self.lightSegment(pixels, 4, baseCol, arr)
        # self.lightSegment(pixels, 35, baseCol, arr)
        # self.lightSegment(pixels, 36, baseCol, arr)
        # print(arr)

        self.lightPixels(pixels, segsToLight, baseCol)
        d = time()
        # print("CD", (d - c)*1000)

        # smoothly transition volume

        multiplier = (math.log10(moving_window_sum(self.volume, self.vIdx, 0.8)+1)+2)/2
        # print(multiplier)
        self.pixels = pixels * multiplier
        self.vIdx = (self.vIdx + 1) % len(self.volume)
        self.wroteVol = False

def moving_window_sum(volume, index, decay):
    window_sum = volume[index]
    i = 1
    while (index - i) >= 0 or (index + i) < len(volume):
        left_value = volume[index - i] if (index - i) >= 0 else 0
        right_value = volume[index + i] if (index + i) < len(volume) else 0
        window_sum += (decay ** i) * (left_value + right_value)
        i += 1
    return window_sum