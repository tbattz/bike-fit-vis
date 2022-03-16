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

    # Create riders
    rider1 = Rider(rcs['rider1'], bike, seatColor='royalblue', riderColor='blueviolet', riderAlpha=0.5)
    rider2 = Rider(rcs['rider2'], bike, seatColor='lime', riderColor='blueviolet', riderAlpha=0.5)

    # Create figure
    fig = plt.figure()
    plt.axis('equal')
    plt.xlim([-1000, 1800])
    plt.ion()

    # Draw bike
    bike.drawBikePositions()

    # Draw Seat
    rider1.drawSeat()
    rider2.drawSeat()

    # Draw pedal and feet
    for crankAngleDeg in np.linspace(45, 360*40, 360*20):
        # Draw cranks
        bike.calcCrankLoc(theta=-crankAngleDeg)
        bike.drawCrank()

        # Draw rider lower body
        rider1.calcAllRiderPos(crankAngleDeg)
        rider1.drawPedalAndFoot()
        rider1.drawRiderLegs()

        # Draw rider upper body
        rider1.calcUpperBody()
        rider1.drawUpperBody()



        plt.pause(0.01)




    plt.axis('equal')
    plt.show()

