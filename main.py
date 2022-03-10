import matplotlib.pyplot as plt
import numpy as np
import math
import json

from bike import Bike



if __name__ == '__main__':
    # Measurements in mm
    seatPersonOffsetX = 25.0
    seatPersonOffsetY = 110.0
    hip2ShoulderLength = 430.0
    hip2KneeLength = 440.0
    knee2FootLength = 410.0
    footLength = 210.0
    footContactProportion = 0.75
    shoulder2ElbowLength = 290.0
    elbow2WristContactLength = 230.0
    wrist2FingerHoldPoint = 135.0


    # Read bike configuration
    with open('bike.json') as f:
        bc = json.load(f)
        print('Read bike configuration file:')
        for key, val in bc.items():
            print(key+":", val)

    # Create bike
    bike = Bike(bc)
    bike.calcBikePositions()


    fig = plt.figure()

    bike.drawBikePositions()

    bike.calcCrankAndPedalLoc(theta=-30)
    bike.drawCrankAndPedals()



    plt.axis('equal')
    plt.show()


