import math
import numpy as np
import matplotlib.pyplot as plt

from fourBarLink import FourBarLink



class Rider:
    """
    Contains methods for calculating positions of the rider and seat.
    """
    def __init__(self, rc, bike, seatColor='royalblue', riderColor='blueviolet', riderAlpha=0.5):
        """
        :param rc: The rider config dictionary.
        :param bike: An existing bike class containing frame, seat and crank positions.
        :param seatColor: The named color to use for drawing the seat.
        :param riderColor: The named color to use for drawing the rider.
        :paramAlpha: The alpha transparency value for the rider, from 0 to 1.
        """
        self.rc = rc
        self.bike = bike
        self.seatColor = seatColor
        self.riderColor = riderColor
        self.riderAlpha = riderAlpha

        self.seatExtX = None
        self.seatExtY = None
        self.seatPosX = None
        self.seatPosY = None

        self.hipX = None
        self.hipY = None

        self.ped1x1 = None
        self.ped1y1 = None
        self.ped1x2 = None
        self.ped1y2 = None
        self.ped2x1 = None
        self.ped2y1 = None
        self.ped2x2 = None
        self.ped2y2 = None

        self.anklePos1 = None
        self.endOfFoot1 = None
        self.anklePos2 = None
        self.endOfFoot2 = None

        self.pedalLine1 = None
        self.pedalLine2 = None
        self.footLine1 = None
        self.footLine2 = None
        self.footAngleRad1 = None
        self.footAngleRad1 = None

        self.fourBar1 = None
        self.fourBar2 = None

        self.ankle1 = None
        self.knee1 = None

        self.O2s = None
        self.O4s = None
        self.O2n = None
        self.Ann = None
        self.Bnn = None
        self.O4n = None

        self.legLine1 = None
        self.legLine2 = None

        self.calcSeatExtensionPos()

    def calcSeatExtensionPos(self):
        """
        Calculate the position for the seat post and seat.
        """
        # Plot seat extension
        self.seatExtX = self.rc['seatHeight'] * math.cos(self.bike.seatTube2HoriAngle)
        self.seatExtY = self.rc['seatHeight'] * math.sin(self.bike.seatTube2HoriAngle)
        self.seatPosX = self.bike.xst - self.seatExtX
        self.seatPosY = self.bike.yst + self.seatExtY

    def drawSeat(self):
        """
        Draw the seat and seat post.
        """
        # Plot Seat post
        plt.plot([self.bike.xst, self.seatPosX], [self.bike.yst, self.seatPosY], c=self.seatColor)

        # Plot Seat (Assumes flat seat)
        plt.plot([self.seatPosX - self.rc['seatLengthAft'], self.seatPosX + self.rc['seatLengthFwd']], [self.seatPosY, self.seatPosY], c=self.seatColor)

    def calculatePedalAndFoot(self, crankAngleDeg):
        """
        Calculate the positions of the pedals and feet.

        :param crankAngleDeg: The angle of the main crank.
        """
        # Calculate foot angle using experimental relationship
        # footAngleDeg = 22*math.sin(math.radians(crankAngleDeg + 190)) + 20.76
        footAngleDeg1 = 22 * math.sin(math.radians(-(crankAngleDeg) + 190 + 90)) + 20.76
        self.footAngleRad1 = math.radians(footAngleDeg1)
        footAngleDeg2 = 22 * math.sin(math.radians(-(crankAngleDeg + 180) + 190 + 90)) + 20.76
        self.footAngleRad2 = math.radians(footAngleDeg2)

        # Calculate pedal locations
        # Pedal 1
        self.ped1x1 = self.bike.c1x - ((self.rc['pedalLength'] / 2.0) * math.cos(self.footAngleRad1))
        self.ped1x2 = self.bike.c1x + ((self.rc['pedalLength'] / 2.0) * math.cos(self.footAngleRad1))
        self.ped1y1 = self.bike.c1y + ((self.rc['pedalLength'] / 2.0) * math.sin(self.footAngleRad1))
        self.ped1y2 = self.bike.c1y - ((self.rc['pedalLength'] / 2.0) * math.sin(self.footAngleRad1))
        # Pedal 2
        self.ped2x1 = self.bike.c2x - ((self.rc['pedalLength'] / 2.0) * math.cos(self.footAngleRad2 + math.pi))
        self.ped2x2 = self.bike.c2x + ((self.rc['pedalLength'] / 2.0) * math.cos(self.footAngleRad2 + math.pi))
        self.ped2y1 = self.bike.c2y + ((self.rc['pedalLength'] / 2.0) * math.sin(self.footAngleRad2 + math.pi))
        self.ped2y2 = self.bike.c2y - ((self.rc['pedalLength'] / 2.0) * math.sin(self.footAngleRad2 + math.pi))

        # Calculate ankle positions
        # Ankle 1
        footLeverLength = self.rc['footContactProportion'] * self.rc['footLength']
        anklePosX = self.bike.c1x - (footLeverLength * math.cos(self.footAngleRad1))
        anklePosY = self.bike.c1y + (footLeverLength * math.sin(self.footAngleRad1))
        self.anklePos1 = [anklePosX, anklePosY]
        endOfFootX = self.anklePos1[0] + (self.rc['footLength'] * math.cos(self.footAngleRad1))
        endOfFootY = self.anklePos1[1] - (self.rc['footLength'] * math.sin(self.footAngleRad1))
        self.endOfFoot1 = [endOfFootX, endOfFootY]
        # Ankle 2
        footLeverLength = self.rc['footContactProportion'] * self.rc['footLength']
        anklePosX = self.bike.c2x - (footLeverLength * math.cos(self.footAngleRad2))
        anklePosY = self.bike.c2y + (footLeverLength * math.sin(self.footAngleRad2))
        self.anklePos2 = [anklePosX, anklePosY]
        endOfFootX = self.anklePos2[0] + (self.rc['footLength'] * math.cos(self.footAngleRad2))
        endOfFootY = self.anklePos2[1] - (self.rc['footLength'] * math.sin(self.footAngleRad2))
        self.endOfFoot2 = [endOfFootX, endOfFootY]



    def calcAllRiderPos(self, crankAngleDeg):
        """
        Calculate all points of the rider.
        """
        self.calcRiderHipPos()
        self.calculatePedalAndFoot(crankAngleDeg)

        # Setup four bar
        # O2 is the foot-pedal contact point
        # A is the ankle joint
        # B is the knee join
        # O4 is the hip join
        O2 = np.array([self.bike.c1x, self.bike.c1y])
        O4 = np.array([self.hipX, self.hipY])
        O2ALen = self.rc['footContactProportion']*self.rc['footLength']
        ABLen = self.rc['knee2AnkleLength']
        BO4Len = self.rc['hip2KneeLength']

        # Shift O2 point to the origin
        self.O2s = O2 - O2
        self.O4s = O4 - O2

        # Rotate points to lie on the x axes
        adjustedFootAngle = math.pi - self.footAngleRad1
        adjustedO2O4Angle = math.pi - math.atan2(self.O2s[1] - self.O4s[1], self.O2s[0] - self.O4s[0])
        rotMatrix = np.array([[math.cos(adjustedO2O4Angle), -math.sin(adjustedO2O4Angle)],
                              [math.sin(adjustedO2O4Angle), math.cos(adjustedO2O4Angle)]])
        self.O2s = np.dot(rotMatrix, self.O2s)
        self.O4s = np.dot(rotMatrix, self.O4s)

        # Create/setup four bar link
        if self.fourBar1 is None:
            self.fourBar1 = FourBarLink(self.O2s.tolist(), self.O4s.tolist(), O2ALen, ABLen, BO4Len, adjustedFootAngle + adjustedO2O4Angle)
        else:
            self.fourBar1.setO4Pt(self.O4s.tolist(), adjustedFootAngle + adjustedO2O4Angle)
        self.fourBar1.calcAngles(adjustedFootAngle + adjustedO2O4Angle)

        # Counter rotate resultant points
        rotMatrix = np.array([[math.cos(-adjustedO2O4Angle), -math.sin(-adjustedO2O4Angle)],
                              [math.sin(-adjustedO2O4Angle), math.cos(-adjustedO2O4Angle)]])
        self.O2n = np.dot(rotMatrix, np.array([[self.fourBar1.O2[0]], [self.fourBar1.O2[1]]])).flatten() + O2
        self.O4n = np.dot(rotMatrix, np.array([[self.fourBar1.O4[0]], [self.fourBar1.O4[1]]])).flatten() + O2
        self.Ann = np.dot(rotMatrix, np.array([[self.fourBar1.An[0]], [self.fourBar1.An[1]]])).flatten() + O2
        self.Bnn = np.dot(rotMatrix, np.array([[self.fourBar1.Bn1[0]], [self.fourBar1.Bn1[1]]])).flatten() + O2



    def drawPedalAndFoot(self):
        """
        Draw the stationary top half of the rider.
        """
        if self.pedalLine1 is None:
            self.pedalLine1, = plt.plot([], [])
        if self.pedalLine2 is None:
            self.pedalLine2, = plt.plot([], [])
        if self.footLine1 is None:
            self.footLine1, = plt.plot([], [], 'k-')
        if self.footLine2 is None:
            self.footLine2, = plt.plot([], [], 'k-')

        # Draw foot
        self.footLine1.set_data([self.anklePos1[0], self.endOfFoot1[0]], [self.anklePos1[1], self.endOfFoot1[1]])
        #self.footLine2.set_data([self.anklePos2[0], self.endOfFoot2[0]], [self.anklePos2[1], self.endOfFoot2[1]])

        # Draw Pedal
        self.pedalLine1.set_data([self.ped1x1, self.ped1x2], [self.ped1y1, self.ped1y2])
        self.pedalLine2.set_data([self.ped2x1, self.ped2x2], [self.ped2y1, self.ped2y2])



    def calcRiderHipPos(self):
        """
        Calculate the position of the rider's hip joint.
        """
        self.hipX = self.seatPosX + self.rc['seatRiderOffsetX']
        self.hipY = self.seatPosY + self.rc['seatRiderOffsetY']


    def drawRiderLegs(self):
        """
        Draw the riders legs using positions from the 4-bar link.
        """
        if self.legLine1 is None:
            self.legLine1, = plt.plot([], [], 'k-')

        self.legLine1.set_data([self.O2n[0], self.Ann[0], self.Bnn[0], self.O4n[0]],
                               [self.O2n[1], self.Ann[1], self.Bnn[1], self.O4n[1]])






