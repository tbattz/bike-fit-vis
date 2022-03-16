import math
import numpy as np
import matplotlib.pyplot as plt


class FourBarLink:
    """
    Assumes O2 and O4 line on the same horizontal line, with O4 to the right of O2.
    """
    def __init__(self, O2, O4, O2ALen, ABLen, BO4Len, theta2=0.0):
        # Pinned Points
        self.O2 = O2
        self.O4 = O4

        # Link Lengths
        self.O2ALen = O2ALen
        self.ABLen = ABLen
        self.BO4Len = BO4Len

        self.theta2 = theta2

        self.checkDists = False

        self.a = None
        self.b = None
        self.c = None
        self.d = None

        self.k1 = None
        self.k2 = None
        self.k3 = None
        self.k4 = None
        self.k5 = None

        self.A = None
        self.B = None
        self.C = None
        self.D = None
        self.E = None
        self.F = None

        self.theta31 = None
        self.theta32 = None
        self.theta41 = None
        self.theta42 = None

        self.An = None
        self.Bn1 = None
        self.Bn2 = None

        self.fig = None
        self.l1 = None
        self.l2 = None
        self.p1 = None

        self.calcVectorLengths()
        self.calcKCoeffs()
        self.calcLetterCoeffs()

    def setO4Pt(self, O4, theta2):
        """
        Update the O4 point.

        :param O4: The [x,y] coordinates for the new point.
        :param theta2: The angle between the r2 line and the r1 line
        """
        self.O4 = O4
        self.theta2 = theta2

        # Recalculate positions
        self.calcVectorLengths()
        self.calcKCoeffs()
        self.calcLetterCoeffs()

    def calcVectorLengths(self):
        # Calculate lengths
        # O2O4
        self.a = self.O2ALen
        # O2A
        self.b = self.ABLen
        # AB
        self.c = self.BO4Len
        # B04
        self.d = math.sqrt((self.O4[0] - self.O2[0])**2 + (self.O4[1] - self.O2[1])**2)

    def calcKCoeffs(self):
        # Calculate k Coefficients
        self.k1 = self.d / self.a
        self.k2 = self.d / self.c
        self.k3 = (self.a**2 + self.c**2 + self.d**2 - self.b**2) / (2*self.a*self.c)
        self.k4 = self.d / self.b
        self.k5 = (self.c**2 - self.d**2 - self.a**2 - self.b**2) / (2*self.a*self.b)

    def calcLetterCoeffs(self):
        # Calculate A-F Coefficients
        self.A = math.cos(self.theta2) - self.k1 - (self.k2 * math.cos(self.theta2)) + self.k3
        self.B = -2 * math.sin(self.theta2)
        self.C = self.k1 - ((self.k2 + 1) * math.cos(self.theta2)) + self.k3
        self.D = math.cos(self.theta2) - self.k1 + (self.k4 * math.cos(self.theta2)) + self.k5
        self.E = -2 * math.sin(self.theta2)
        self.F = self.k1 + ((self.k4 - 1) * math.cos(self.theta2)) + self.k5

    def calcAngles(self, theta2):
        self.theta2 = theta2
        self.calcLetterCoeffs()
        # Calculate bar angles
        #self.theta31 = 2 * math.atan2(-self.E + math.sqrt(self.E**2 - (4 * self.D * self.F)), 2 * self.D)
        #self.theta32 = 2 * math.atan2(-self.E - math.sqrt(self.E**2 - (4 * self.D * self.F)), 2 * self.D)
        if self.B**2 > 4 * self.A * self.C:
            self.theta41 = 2 * math.atan2(-self.B + math.sqrt(self.B**2 - 4 * self.A * self.C), 2 * self.A)
            self.theta42 = 2 * math.atan2(-self.B - math.sqrt(self.B**2 - 4 * self.A * self.C), 2 * self.A)

            # Calculate new positions for the points
            self.An =  [self.O2[0] + (self.a*math.cos(self.theta2)), self.O2[1] + (self.a*math.sin(self.theta2))]
            self.Bn1 = [self.O4[0] + (self.c*math.cos(self.theta41)), self.O4[1] + (self.c*math.sin(self.theta41))]
            self.Bn2 = [self.O4[0] + (self.c*math.cos(self.theta42)), self.O4[1] + (self.c*math.sin(self.theta42))]

            if self.checkDists:
                r2 = math.sqrt((self.O2[0] - self.An[0]) ** 2 + (self.O2[1] - self.An[1]) ** 2)
                r3a = math.sqrt((self.An[0] - self.Bn1[0]) ** 2 + (self.An[1] - self.Bn1[1]) ** 2)
                # r3b = math.sqrt((self.An[0] - self.Bn2[0]) ** 2 + (self.An[1] - self.Bn2[1]) ** 2)
                r4 = math.sqrt((self.Bn1[0] - self.O4[0]) ** 2 + (self.Bn1[1] - self.O4[1]) ** 2)
                # print('%.1f' % r2, '%.1f' % r3a, '%.1f' % r3b, '%.1f' % r4)
                print('%.1f' % r2, '%.1f' % r3a, '%.1f' % r4)
        else:
            self.An = [0.0, 0.0]
            self.Bn1 = [0.0, 0.0]
            self.Bn2 = [0.0, 0.0]


    def setupFig(self, fig=None):
        if fig is None:
            self.fig = plt.figure()
        else:
            self.fig = fig

        plt.ion()

        self.l1, = plt.plot([], [], 'r-')
        self.l2, = plt.plot([], [], 'b-')
        self.p1, = plt.plot([], [], 'ko')


    def plotLinks(self):
        self.l1.set_data([self.O2[0], self.An[0], self.Bn1[0], self.O4[0]], [self.O2[1], self.An[1], self.Bn1[1], self.O4[1]])
        self.l2.set_data([self.O2[0], self.An[0], self.Bn2[0], self.O4[0]], [self.O2[1], self.An[1], self.Bn2[1], self.O4[1]])
        self.p1.set_data([self.O2[0], self.O4[0]], [self.O2[1], self.O4[1]])
        #plt.gca().relim()
        #plt.autoscale()
        plt.show()



if __name__ == '__main__':
    # Define points
    O2 = [0.0, 0.0]
    #A = [3.0, 0.0]
    #B = [5.5510033, 4.2645471]
    O4 = [6.0, 0.0]
    O2ALen = 3.0
    ABLen = 4.969303754524299
    BO4Len = 4.288118469064177

    # Define driving angle
    theta2 = math.pi/2.0

    # Create a 4 bar
    fourBar = FourBarLink(O2, O4, O2ALen, ABLen, BO4Len, 0.0)
    fourBar.setupFig()
    plt.xlim([-10, 10])
    plt.ylim([-10, 10])
    # Plotting
    for theta2 in np.linspace(0.0, 5*2*math.pi, 5*100):
        fourBar.calcAngles(theta2)
        fourBar.plotLinks()

        plt.pause(0.1)



