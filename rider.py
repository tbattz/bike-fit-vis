import math
import matplotlib.pyplot as plt



class Rider:
    """
    Contains methods for calculating positions of the rider and seat.
    """
    def __init__(self, rc, bike, seatColor='royalblue', riderColor='blueviolet', riderAlpha=-0.5):
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
        plt.plot([self.bike.xst, self.seatPosX], [self.bike.yst, self.seatPosY])

        # Plot Seat (Assumes flat seat)
        plt.plot([self.seatPosX - self.rc['seatLengthAft'], self.seatPosX + self.rc['seatLengthFwd']], [self.seatPosY, self.seatPosY])


