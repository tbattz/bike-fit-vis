import math
import numpy as np
import matplotlib.pyplot as plt


class Bike:
    """
    Contains methods for calculating positions of the bike frame, wheels, crank and pedals.
    """
    def __init__(self, bc):
        """
        :param bc: The bike configuration dictionary.
        """
        self.bc = bc
        self.color = 'gray'

        self.rearWheelLoc = None
        self.xrw = None
        self.yrw = None

        self.frontWheelLoc = None
        self.xfw = None
        self.yfw = None

        self.chainStayAngle = None
        self.seatTube2ChainStayAngle = None
        self.seatTube2HoriAngle = None
        self.xst = None
        self.yst = None

        self.downTubeHorzAngle = None
        self.xfork = None
        self.yfork = None

        self.xfb = None
        self.yfb = None

        self.handleBarPostPosX = None
        self.handleBarPostPosY = None
        self.handleBarEndPosX = None
        self.handleBarEndPosY = None

        self.handsPosX = None
        self.handsPosY = None
        self.leverX = None
        self.leverY = None

        self.c1x = None
        self.c1y = None
        self.c2x = None
        self.c2y = None

        self.crankLine = None



    def calcBikePositions(self):
        """
        Calculate all the positions required to draw the bike.
        Excludes the seat, seat post, cranks and pedals.
        """
        self.calcChainStayLine()
        self.calcRearWheelLoc()
        self.calcFrontWheelLoc()
        self.calcSeatTubeLine()
        self.calcTopForkLoc()
        self.calcFrontBarLoc()
        self.calcHandleBarLoc()
        self.calcLeverPos()


    def drawBikePositions(self):
        """
        Draws the bike, without the seat, seat post, cranks or pedals.
        """
        self.drawChainStayLine()
        self.drawRearWheel()
        self.drawFrontWheel()
        self.drawSeatTubeLine()
        self.drawSeatStay()
        self.drawDownTube()
        self.drawFrontFork()
        self.drawFrontBar()
        self.drawHeadTube()
        self.drawHandleBar()
        self.drawLevers()


    def calcChainStayLine(self):
        """
        Calculate the chain stay line positions.
        """
        # Chain Stay line
        xcs = math.sqrt(self.bc['chainStay']**2 - self.bc['bottomBracketDrop']**2)
        ycs = self.bc['bottomBracketDrop']
        self.rearWheelLoc = [-xcs, ycs]

    def drawChainStayLine(self):
        """
        Draw the chain stay line.
        """
        plt.plot([0, self.rearWheelLoc[0]], [0, self.rearWheelLoc[1]], c=self.color)

    def calcRearWheelLoc(self):
        """
        Calculate the points for the rear wheel circle.
        """
        theta = np.linspace(0, 2 * np.pi, 100)
        self.xrw = ((self.bc['wheelDiameter'] / 2.0) * np.cos(theta)) + self.rearWheelLoc[0]
        self.yrw = ((self.bc['wheelDiameter'] / 2.0) * np.sin(theta)) + self.rearWheelLoc[1]

    def drawRearWheel(self):
        """
        Draw the rear wheel circle.
        """
        # Plot Rear Wheel
        plt.plot(self.xrw, self.yrw, 'r')

    def calcFrontWheelLoc(self):
        """
        Calculate the points for the front wheel circle.
        """
        self.frontWheelLoc = [self.rearWheelLoc[0] + self.bc['wheelBase'], self.rearWheelLoc[1]]
        self.xfw = self.xrw + self.bc['wheelBase']
        self.yfw = self.yrw

    def drawFrontWheel(self):
        """
        Draw the front wheel circle.
        """
        # Plot Front Wheel
        plt.plot(self.xfw, self.yfw, 'r')

    def calcSeatTubeLine(self):
        """
        Calculate the positions for the seat tube.
        """
        # Calculate seat tube point
        self.chainStayAngle = math.sin(self.bc['bottomBracketDrop'] / self.bc['chainStay'])  # Radians
        self.seatTube2ChainStayAngle = math.acos((self.bc['chainStay']**2 + self.bc['seatTube']**2 - self.bc['seatStay']**2)/(2*self.bc['chainStay']*self.bc['seatTube']))
        self.seatTube2HoriAngle = self.chainStayAngle + self.seatTube2ChainStayAngle
        self.xst = -self.bc['seatTube'] * math.cos(self.seatTube2HoriAngle)
        self.yst = self.bc['seatTube'] * math.sin(self.seatTube2HoriAngle)

    def drawSeatTubeLine(self):
        """
        Draw the seat tube line.
        """
        plt.plot([0, self.xst], [0, self.yst], c=self.color)

    def drawSeatStay(self):
        """
        Draw the seat stay.
        """
        # Plot Seat Stay
        plt.plot([self.rearWheelLoc[0], self.xst], [self.rearWheelLoc[1], self.yst], c=self.color)

    def calcTopForkLoc(self):
        """
        Calculate the position at the top of the fork.
        """
        # Calculate hub to front wheel distance
        xcs = -self.rearWheelLoc[0]
        horzHub2FrontWheelDist = self.bc['wheelBase'] - xcs
        hub2FrontWheel = math.sqrt(self.bc['bottomBracketDrop']**2 + horzHub2FrontWheelDist**2)

        # Calculate down tube horz angle
        downTubeAngle = math.acos((self.bc['downTube']**2 + hub2FrontWheel**2 - self.bc['forkLength']**2)/(2*self.bc['downTube']*hub2FrontWheel))
        self.downTubeHorzAngle = downTubeAngle + (math.asin(self.bc['bottomBracketDrop']/hub2FrontWheel))

        # Calculate top of fork position
        self.xfork = self.bc['downTube'] * math.cos(self.downTubeHorzAngle)
        self.yfork = self.bc['downTube'] * math.sin(self.downTubeHorzAngle)

    def drawDownTube(self):
        """
        Draw the down tube.
        """
        plt.plot([0, self.xfork], [0, self.yfork], c=self.color)

    def drawFrontFork(self):
        """
        Draw the front fork.
        """
        # Plot front fork
        plt.plot([self.frontWheelLoc[0], self.xfork], [self.frontWheelLoc[1], self.yfork], c=self.color)

    def calcFrontBarLoc(self):
        """
        Calculate the positions for the front bar.
        """
        # Calculate angle between seat tube and down tube
        seatTube2DownTubeAngle = math.pi - self.seatTube2HoriAngle - self.downTubeHorzAngle
        seatTube2FrontForkDist = math.sqrt(self.bc['seatTube']**2 + self.bc['downTube']**2 - (2*self.bc['seatTube']*self.bc['downTube']*math.cos(seatTube2DownTubeAngle)))

        # Calculate seat tube to fork horz angle
        seatTube2FrontForkAngle = math.sin((self.yfork - self.yst) / seatTube2FrontForkDist)

        # Calculate top tube horizontal angle
        topTubeHorzAngle = math.acos((self.bc['topTube']**2 + seatTube2FrontForkDist**2 - self.bc['headTube']**2)/(2*self.bc['topTube']*seatTube2FrontForkDist)) + seatTube2FrontForkAngle

        # Calculate front bar position
        self.xfb = self.xst + (self.bc['topTube'] * math.cos(topTubeHorzAngle))
        self.yfb = self.yst + (self.bc['topTube'] * math.sin(topTubeHorzAngle))

    def drawFrontBar(self):
        """
        Draw the front bar line.
        """
        plt.plot([self.xst, self.xfb], [self.yst, self.yfb], c=self.color)

    def drawHeadTube(self):
        """
        Draw the head tube.
        """
        # Plot head tube
        plt.plot([self.xfb, self.xfork], [self.yfb, self.yfork], c=self.color)

    def calcHandleBarLoc(self):
        """
        Calculate the handle bar positions.
        """
        # Plot handle bar post
        headTubeAngle = math.atan((self.yfork - self.yfb) / (self.xfork - self.xfb)) + math.pi
        self.handleBarPostPosX = self.xfb + (self.bc['handleBarPost'] * math.cos(headTubeAngle))
        self.handleBarPostPosY = self.yfb + (self.bc['handleBarPost'] * math.sin(headTubeAngle))

        # Calculate distance from front wheel to handle bar post
        frontWheel2HandleBarPost = math.sqrt((self.frontWheelLoc[0] - self.handleBarPostPosX)**2 + (self.frontWheelLoc[1] - self.handleBarPostPosY)**2)
        frontWheel2HandleBarHorzAngle = -math.atan((self.frontWheelLoc[1] - self.handleBarPostPosY)/(self.frontWheelLoc[0] - self.handleBarPostPosX))
        hands2WheelForkAngle = math.acos((self.bc['handleBar2FrontWheel']**2 + frontWheel2HandleBarPost**2 - self.bc['handleBarLength']**2) / (2*self.bc['handleBar2FrontWheel'] * frontWheel2HandleBarPost))
        hands2WheelForkHorzAngle = frontWheel2HandleBarHorzAngle + hands2WheelForkAngle
        self.handleBarEndPosX = self.frontWheelLoc[0] + (self.bc['handleBar2FrontWheel'] * math.cos(math.pi - hands2WheelForkHorzAngle))
        self.handleBarEndPosY = self.frontWheelLoc[1] + (self.bc['handleBar2FrontWheel'] * math.sin(math.pi - hands2WheelForkHorzAngle))

    def drawHandleBar(self):
        """
        Draw the handle bar.
        """
        plt.plot([self.xfb, self.handleBarPostPosX], [self.yfb, self.handleBarPostPosY], c=self.color)
        plt.plot([self.handleBarPostPosX, self.handleBarEndPosX], [self.handleBarPostPosY, self.handleBarEndPosY], c=self.color)

    def calcLeverPos(self):
        """
        Calculate the position of the brake levels, assuming they're 90 deg offset from the handle bar.
        """
        handleBarAngle = math.atan((self.handleBarEndPosY - self.handleBarPostPosY) / (self.handleBarEndPosX - self.handleBarPostPosX))
        leverAngle = handleBarAngle - (math.pi/2.0)
        self.handsPosX = self.handleBarEndPosX + (self.bc['leverLength']*math.cos(leverAngle)/2.0)
        self.handsPosY = self.handleBarEndPosY + (self.bc['leverLength']*math.sin(leverAngle)/2.0)
        self.leverX = self.handleBarEndPosX + (self.bc['leverLength'] * math.cos(leverAngle))
        self.leverY = self.handleBarEndPosY + (self.bc['leverLength'] * math.sin(leverAngle))

    def drawLevers(self):
        """
        Draw the levers.
        """
        plt.plot([self.handleBarEndPosX, self.leverX], [self.handleBarEndPosY, self.leverY], c=self.color)

    def calcCrankLoc(self, theta):
        """
        Calculate the crank locations, given an angle theta.

        :param theta: The angle, in degrees, of the first crank to the horizontal.
        :param phi1: The angle of pedal 1 in radians.
        :param phi2: The angle of pedal 2 in radians.
        """
        thetaRad = math.radians(theta)
        # Calculate crank location
        self.c1x = (self.bc['crankLength'] * math.cos(thetaRad))
        self.c1y = (self.bc['crankLength'] * math.sin(thetaRad))
        self.c2x = (self.bc['crankLength'] * math.cos(thetaRad + math.pi))
        self.c2y = (self.bc['crankLength'] * math.sin(thetaRad + math.pi))

    def drawCrank(self):
        """
        Draw the cranks.
        """
        if self.crankLine is None:
            self.crankLine, = plt.plot([], [], 'b')

        self.crankLine.set_data([self.c1x, self.c2x], [self.c1y, self.c2y])


