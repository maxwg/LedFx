import numpy as np
import voluptuous as vol

from time import time
from enum import Enum
from random import randint
# from chromance_base import nodeConnections, segmentConnections, ledAssignments
from ledfx.effects.chromance_config import nodeConnections, segmentConnections, ledAssignments
from ledfx.effects.audio import AudioReactiveEffect
from ledfx.effects.gradient import GradientEffect

"""
   A dot animation that travels along rails
   (C) Voidstar Lab LLC 2021
"""

class RippleState(Enum):
    dead = 0
    withinNode = 1  # Ripple isn't drawn as it passes through a node to keep the speed consistent
    travelingUpwards = 2
    travelingDownwards = 3

class RippleBehavior(Enum):
    weaksauce = 0
    feisty = 1
    angry = 2
    alwaysTurnsRight = 3
    alwaysTurnsLeft = 4

def fmap(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class Ripple:
    def __init__(self, ripple_id):
        self.ripple_id = ripple_id
        print(f"Instanced ripple #{self.ripple_id}")


    state = RippleState.dead
    color = (255, 255, 255)
    position = [0, 0]
    speed = 0.0  # Each loop, ripples move this many LED's.
    lifespan = 0  # The ripple stops after this many milliseconds
    behavior = 0  # 0: Always goes straight ahead if possible, 1: Can take 60-degree turns, 2: Can take 120-degree turns
    justStarted = False
    pressure = 0.0  # When Pressure reaches 1, ripple will move
    birthday = 0  # Used to track age of ripple
    rippleCount = 0  # Used to give them unique ID's

    # Place the Ripple in a node
    def start(self, node, direction, color, speed, lifespan, behavior):
        self.color = color
        self.speed = speed
        self.lifespan = lifespan
        self.behavior = behavior

        self.birthday = time()
        self.pressure = 0
        self.state = RippleState.withinNode

        self.position = [node, direction]

        self.justStarted = True

        print(f"Ripple {self.ripple_id} starting at node {self.position[0]} direction {self.position[1]}")

    def advance(self, ledColors):
        age = (time() - self.birthday) * 1000
        if self.state == RippleState.dead:
            return

        self.pressure += fmap(float(age), 0.0, float(self.lifespan), self.speed, 0.0)

        if self.pressure < 1 and (self.state == RippleState.travelingUpwards or self.state == RippleState.travelingDownwards):
            self.renderLed(ledColors, age)

        while self.pressure >= 1:
            if self.state == RippleState.withinNode:
                if self.justStarted:
                    self.justStarted = False
                else:
                    newDirection = -1

                    sharpLeft = (self.position[1] + 1) % 6
                    wideLeft = (self.position[1] + 2) % 6
                    forward = (self.position[1] + 3) % 6
                    wideRight = (self.position[1] + 4) % 6
                    sharpRight = (self.position[1] + 5) % 6

                    if self.behavior <= 2:
                        anger = self.behavior

                        while newDirection < 0:
                            if anger == 0:
                                forwardConnection = nodeConnections[self.position[0]][forward]

                                if forwardConnection < 0:
                                    anger += 1
                                else:
                                    newDirection = forward

                            if anger == 1:
                                leftConnection = nodeConnections[self.position[0]][wideLeft]
                                rightConnection = nodeConnections[self.position[0]][wideRight]

                                if leftConnection >= 0 and rightConnection >= 0:
                                    newDirection = wideLeft if randint(0,1) == 1 else wideRight
                                elif leftConnection >= 0:
                                    newDirection = wideLeft
                                elif rightConnection >= 0:
                                    newDirection = wideRight
                                else:
                                    anger += 1

                            if anger == 2:
                                leftConnection = nodeConnections[self.position[0]][sharpLeft]
                                rightConnection = nodeConnections[self.position[0]][sharpRight]

                                if leftConnection >= 0 and rightConnection >= 0:
                                    newDirection = sharpLeft if randint(0,1) == 1 else sharpRight
                                elif leftConnection >= 0:
                                    newDirection = sharpLeft
                                elif rightConnection >= 0:
                                    newDirection = sharpRight
                                else:
                                    anger -= 1
                    elif self.behavior == RippleBehavior.alwaysTurnsRight:
                        for i in range(1, 6):
                            possibleDirection = (self.position[1] + i) % 6

                            if nodeConnections[self.position[0]][possibleDirection] >= 0:
                                newDirection = possibleDirection
                                break

                    elif self.behavior == RippleBehavior.alwaysTurnsLeft:
                        for i in range(5, 0, -1):
                            possibleDirection = (self.position[1] + i) % 6

                            if nodeConnections[self.position[0]][possibleDirection] >= 0:
                                newDirection = possibleDirection
                                break
                    self.position[1] = newDirection

                self.position[0] = nodeConnections[self.position[0]][self.position[1]]
                # Look up which segment we're on

                if self.position[1] == 5 or self.position[1] == 0 or self.position[1] == 1:
                    # Top half of the node
                    self.state = RippleState.travelingUpwards
                    self.position[1] = 0  # Starting at bottom of segment
                else:
                    self.state = RippleState.travelingDownwards
                    self.position[1] = 13  # Starting at top of 14-LED-long strip

            if self.state == RippleState.travelingUpwards:
                self.position[1] += 1
                if self.position[1] >= 14:
                    # We've reached the top!
                    segment = self.position[0]
                    self.position[0] = segmentConnections[self.position[0]][0]
                    for i in range(6):
                        # Figure out from which direction the ripple is entering the node.
                        # Allows us to exit in an appropriately aggressive direction.
                        incomingConnection = nodeConnections[self.position[0]][i]
                        if incomingConnection == segment:
                            self.position[1] = i
                    self.state = RippleState.withinNode
                else:
                    pass

            if self.state == RippleState.travelingDownwards:
                self.position[1] -= 1
                if self.position[1] < 0:
                    # We've reached the bottom!
                    segment = self.position[0]
                    self.position[0] = segmentConnections[self.position[0]][1]
                    for i in range(6):
                        # Figure out from which direction the ripple is entering the node.
                        # Allows us to exit in an appropriately aggressive direction.
                        incomingConnection = nodeConnections[self.position[0]][i]
                        if incomingConnection == segment:
                            self.position[1] = i
                    self.state = RippleState.withinNode
                else:
                    pass

            self.pressure -= 1
            if self.state == RippleState.travelingUpwards or self.state == RippleState.travelingDownwards:
                # Ripple is visible - render it
                self.renderLed(ledColors, age)

        if self.lifespan and age >= self.lifespan:
            # We dead
            self.state = RippleState.dead
            self.position[0] = self.position[1] = pressure = age = 0

    def renderLed(self, ledColors, age):
        # strip = ledAssignments[position[0]][0]
        # led = ledAssignments[position[0]][2] + position[1]
        red = ledColors[self.position[0]][self.position[1]][0]
        green = ledColors[self.position[0]][self.position[1]][1]
        blue = ledColors[self.position[0]][self.position[1]][2]

        ledColors[self.position[0]][self.position[1]][0] = min(255, max(0, int(fmap(float(age), 0.0, float(self.lifespan),
                                                                          (self.color[0]) & 0xFF, 0.0)) + red))
        ledColors[self.position[0]][self.position[1]][1] = min(255, max(0, int(fmap(float(age), 0.0, float(self.lifespan),
                                                                          (self.color[1]) & 0xFF, 0.0)) + green))
        ledColors[self.position[0]][self.position[1]][2] = min(255, max(0,
                                                              int(fmap(float(age), 0.0, float(self.lifespan), self.color[2],
                                                                       0.0)) + blue))