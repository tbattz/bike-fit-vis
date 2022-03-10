import matplotlib.pyplot as plt
import numpy as np
import math
import json

from bike import Bike
from rider import Rider



if __name__ == '__main__':
    # Read bike configuration
    with open('bike.json') as f:
        bc = json.load(f)
        print('Read bike configuration file:')
        for key, val in bc.items():
            print(key+":", val)
        print()

    # Read rider configurations
    with open('rider.json') as f:
        rcs = json.load(f)
        print('Read rider configuration file:')
        for riderName, rc in rcs.items():
            print("Rider: %s" % riderName)
            for key, val in rc.items():
                print(key+":", val)
            print()


    # Create bike
    bike = Bike(bc)
    bike.calcBikePositions()

    # Create rider 1
    rider1 = Rider(rcs['rider1'], bike, seatColor='royalblue', riderColor='blueviolet', riderAlpha=-0.5)


    fig = plt.figure()

    bike.drawBikePositions()

    bike.calcCrankAndPedalLoc(theta=-30)
    bike.drawCrankAndPedals()

    rider1.drawSeat()


    plt.axis('equal')
    plt.show()

