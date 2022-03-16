import math
import numpy as np

from fourBarLink import FourBarLink



class Rider:
    """
    Contains methods for calculating positions of the rider and seat.
    """
    def __init__(self, rc, bike, seatColor='royalblue', riderColor='blueviolet', riderAlpha=0.5, ax=None):
        """
        :param rc: The rider config dictionary.
        :param bike: An existing bike class containing frame, seat and crank positions.
        :param seatColor: The named color to use for drawing the seat.
        :param riderColor: The named color to use for drawing the rider.
        :param Alpha: The alpha transparency value for the rider, from 0 to 1.
        :param ax: The axes object to plot on.
        """
        self.rc = rc
        self.bike = bike
        self.seatColor = seatColor
        self.riderColor = riderColor
        self.riderAlpha = riderAlpha
        self.ax = ax

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

        self.fourBarLegs = None
        self.fourBarUpper = None

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
        self.upperLine1 = None

        self.crankAngle = []
        self.kneeAngle = []
        self.hipAngle = []

        self.kneeAngleLine = None
        self.hipAngleLine = None

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
        self.ax.plot([self.bike.xst, self.seatPosX], [self.bike.yst, self.seatPosY], c=self.seatColor)

        # Plot Seat (Assumes flat seat)
        self.ax.plot([self.seatPosX - self.rc['seatLengthAft'], self.seatPosX + self.rc['seatLengthFwd']], [self.seatPosY, self.seatPosY], c=self.seatColor)

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

    def calcKneeAngle(self):
        """
        Calculate the knee angle in degrees.
        """
        # Find the distance from A to O4
        AO4Len = math.sqrt((self.fourBarLegs.Ann[0] - self.fourBarLegs.O4n[0])**2 + (self.fourBarLegs.Ann[1] - self.fourBarLegs.O4n[1])**2)
        # Using the cosine rule
        kneeAngle = math.degrees(math.acos((AO4Len**2 - self.fourBarLegs.ABLen**2 - self.fourBarLegs.BO4Len**2)/(2*self.fourBarLegs.ABLen*self.fourBarLegs.BO4Len)))

        return kneeAngle

    def calcHipAngle(self):
        """
        Calculate the hip angle in degrees.
        """
        # Find the distance from A to O4
        AO4Len = math.sqrt((self.fourBarLegs.Ann[0] - self.fourBarLegs.O4n[0]) ** 2 + (
                    self.fourBarLegs.Ann[1] - self.fourBarLegs.O4n[1]) ** 2)
        # Using the cosine rule
        oppAngle = math.degrees(math.acos((self.fourBarLegs.ABLen**2 - AO4Len**2 - self.fourBarLegs.BO4Len**2)/(2*AO4Len*self.fourBarLegs.BO4Len)))
        hipAngle = (90 - oppAngle) + self.rc['hip2HorizontalAngleDeg']

        return hipAngle

    def calcRiderLowerBody(self, crankAngleDeg):
        """
        Calculate all points of the rider.
        """
        self.calcRiderHipPos()
        self.calculatePedalAndFoot(crankAngleDeg)

        # Setup four bar
        # O2 is the foot-pedal contact point
        # A is the ankle joint
        # B is the knee joint
        # O4 is the hip joint
        O2 = np.array([self.bike.c1x, self.bike.c1y])
        O4 = np.array([self.hipX, self.hipY])
        O2ALen = self.rc['footContactProportion']*self.rc['footLength']
        ABLen = self.rc['knee2AnkleLength']
        BO4Len = self.rc['hip2KneeLength']

        # Create/setup four bar link
        adjustedFootAngle = math.pi - self.footAngleRad1
        if self.fourBarLegs is None:
            self.fourBarLegs = FourBarLink(O2, O4, O2ALen, ABLen, BO4Len, adjustedFootAngle)
        else:
            self.fourBarLegs.setO2O4Pt(O2, O4, adjustedFootAngle)

        # Store values
        if crankAngleDeg < 360.1 and crankAngleDeg > -1:
            # Calculate Knee angle
            kneeAngle = self.calcKneeAngle()
            hipAngle = self.calcHipAngle()

            # Store values
            self.crankAngle.append(crankAngleDeg)
            self.kneeAngle.append(abs(kneeAngle))
            self.hipAngle.append(abs(hipAngle))


    def drawAngleLines(self, axKnee, axHip):
        """
        Draw the angle lines for the knee and hip.

        :param axKnee: The axes to draw the knee line on.
        :param axHip: The axes to draw the hip on.
        """
        if self.kneeAngleLine is None:
            self.kneeAngleLine, = axKnee.plot([], [])
        if self.hipAngleLine is None:
            self.hipAngleLine, = axHip.plot([], [])

        self.kneeAngleLine.set_data(self.crankAngle, self.kneeAngle)
        self.hipAngleLine.set_data(self.crankAngle, self.hipAngle)


    def drawPedalAndFoot(self):
        """
        Draw the stationary top half of the rider.
        """
        if self.pedalLine1 is None:
            self.pedalLine1, = self.ax.plot([], [])
        if self.pedalLine2 is None:
            self.pedalLine2, = self.ax.plot([], [])
        if self.footLine1 is None:
            self.footLine1, = self.ax.plot([], [], 'k-')
        if self.footLine2 is None:
            self.footLine2, = self.ax.plot([], [], 'k-')

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
            self.legLine1, = self.ax.plot([], [], 'k-')


        self.legLine1.set_data([self.fourBarLegs.O2n[0], self.fourBarLegs.Ann[0], self.fourBarLegs.Bnn[0], self.fourBarLegs.O4n[0]],
                               [self.fourBarLegs.O2n[1], self.fourBarLegs.Ann[1], self.fourBarLegs.Bnn[1], self.fourBarLegs.O4n[1]])


    def drawRiderLowerBody(self):
        """
        Draw the lower body of the rider.
        """
        self.drawPedalAndFoot()
        self.drawRiderLegs()


    def calcUpperBody(self):
        """
        Calculate the positions of the rider upper body using a Four Bar Link.
        """
        # Setup four bar
        # O2 is the hip joint
        # A is the shoulder joint
        # B is the elbow joint
        # O4 is the hand joint
        O2 = np.array([self.hipX, self.hipY])
        O4 = np.array([self.bike.handsPosX, self.bike.handsPosY])
        O2ALen = self.rc['hip2ShoulderLength']
        ABLen = self.rc['shoulder2ElbowLength']
        BO4Len = self.rc['elbow2WristContactLength']

        # Create/setup four bar link
        adjustedHipAngle = math.radians(self.rc['hip2HorizontalAngleDeg'])
        if self.fourBarUpper is None:
            self.fourBarUpper = FourBarLink(O2, O4, O2ALen, ABLen, BO4Len, adjustedHipAngle)
        else:
            self.fourBarUpper.setO2O4Pt(O2, O4, adjustedHipAngle)


    def drawUpperBody(self):
        """
        Draw the riders upper body.
        """
        if self.upperLine1 is None:
            self.upperLine1, = self.ax.plot([], [], 'k-')


        self.upperLine1.set_data([self.fourBarUpper.O2n[0], self.fourBarUpper.Ann[0], self.fourBarUpper.Bnn[0], self.fourBarUpper.O4n[0]],
                                [self.fourBarUpper.O2n[1], self.fourBarUpper.Ann[1], self.fourBarUpper.Bnn[1], self.fourBarUpper.O4n[1]])



    def calcAndDrawAll(self, crankAngleDeg):
        """
        Calculate and draw the entire rider.

        :param crankAngleDeg: The crank angle to draw at.
        """
        # Draw rider lower body
        self.calcRiderLowerBody(crankAngleDeg)
        self.drawRiderLowerBody()

        # Draw rider upper body
        self.calcUpperBody()
        self.drawUpperBody()


