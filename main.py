import matplotlib.pyplot as plt
import numpy as np
import math
import json



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


    fig = plt.figure()
    # Chain Stay line
    xcs = math.sqrt(bc['chainStay']**2 - bc['bottomBracketDrop']**2)
    ycs = bc['bottomBracketDrop']
    rearWheelLoc = [-xcs, ycs]
    plt.plot([0, rearWheelLoc[0]], [0, rearWheelLoc[1]])

    # Plot Rear Wheel
    theta = np.linspace(0, 2*np.pi, 100)
    xrw = ((bc['wheelDiameter']/2.0)*np.cos(theta)) + rearWheelLoc[0]
    yrw = ((bc['wheelDiameter']/2.0)*np.sin(theta)) + rearWheelLoc[1]
    plt.plot(xrw, yrw)

    # Plot Front Wheel
    frontWheelLoc = [rearWheelLoc[0] + bc['wheelBase'], rearWheelLoc[1]]
    xfw = xrw + bc['wheelBase']
    yfw = yrw
    plt.plot(xfw, yfw)

    # Calculate seat tube point
    chainStayAngle = math.sin(bc['bottomBracketDrop']/bc['chainStay'])  # Radians
    seatTube2ChainStayAngle = math.acos((bc['chainStay']**2 + bc['seatTube']**2 - bc['seatStay']**2)/(2*bc['chainStay']*bc['seatTube']))
    seatTube2HoriAngle = chainStayAngle + seatTube2ChainStayAngle
    xst = -bc['seatTube']*math.cos(seatTube2HoriAngle)
    yst = bc['seatTube']*math.sin(seatTube2HoriAngle)
    plt.plot([0, xst], [0, yst])

    # Plot Seat Stay
    plt.plot([rearWheelLoc[0], xst], [rearWheelLoc[1], yst])

    # Calculate hub to front wheel distance
    horzHub2FrontWheelDist = bc['wheelBase'] - xcs
    hub2FrontWheel = math.sqrt(bc['bottomBracketDrop']**2 + horzHub2FrontWheelDist**2)

    # Calculate down tube horz angle
    downTubeAngle = math.acos((bc['downTube']**2 + hub2FrontWheel**2 - bc['forkLength']**2)/(2*bc['downTube']*hub2FrontWheel))
    downTubeHorzAngle = downTubeAngle + (math.asin(bc['bottomBracketDrop']/hub2FrontWheel))

    # Calculate top of fork position
    xfork = bc['downTube']*math.cos(downTubeHorzAngle)
    yfork = bc['downTube']*math.sin(downTubeHorzAngle)
    plt.plot([0, xfork], [0, yfork])

    # Plot front fork
    plt.plot([frontWheelLoc[0], xfork], [frontWheelLoc[1], yfork])

    # Calculate angle between seat tube and down tube
    seatTube2DownTubeAngle = math.pi - seatTube2HoriAngle - downTubeHorzAngle
    seatTube2FrontForkDist = math.sqrt(bc['seatTube']**2 + bc['downTube']**2 - (2*bc['seatTube']*bc['downTube']*math.cos(seatTube2DownTubeAngle)))

    # Calculate seat tube to fork horz angle
    seatTube2FrontForkAngle = math.sin((yfork - yst)/seatTube2FrontForkDist)

    # Calculate top tube horizontal angle
    topTubeHorzAngle = math.acos((bc['topTube']**2 + seatTube2FrontForkDist**2 - bc['headTube']**2)/(2*bc['topTube']*seatTube2FrontForkDist)) + seatTube2FrontForkAngle

    # Calculate front bar position
    xfb = xst + (bc['topTube']*math.cos(topTubeHorzAngle))
    yfb = yst + (bc['topTube']*math.sin(topTubeHorzAngle))
    plt.plot([xst, xfb], [yst, yfb])

    # Plot head tube
    plt.plot([xfb, xfork], [yfb, yfork])

    # Plot seat extension
    seatExtX = bc['seatHeight'] * math.cos(seatTube2HoriAngle)
    seatExtY = bc['seatHeight'] * math.sin(seatTube2HoriAngle)
    seatPosX = xst - seatExtX
    seatPosY = yst + seatExtY
    plt.plot([xst, seatPosX], [yst, seatPosY])

    # Plot handle bar post
    headTubeAngle = math.atan((yfork - yfb)/(xfork - xfb)) + math.pi
    handleBarPostPosX = xfb + (bc['handleBarPost'] * math.cos(headTubeAngle))
    handleBarPostPosY = yfb + (bc['handleBarPost'] * math.sin(headTubeAngle))
    plt.plot([xfb, handleBarPostPosX], [yfb, handleBarPostPosY])

    # Calculate distance from front wheel to handle bar post
    frontWheel2HandleBarPost = math.sqrt((frontWheelLoc[0] - handleBarPostPosX)**2 + (frontWheelLoc[1] - handleBarPostPosY)**2)
    frontWheel2HandleBarHorzAngle = -math.atan((frontWheelLoc[1] - handleBarPostPosY) / (frontWheelLoc[0] - handleBarPostPosX))
    hands2WheelForkAngle = math.acos((bc['hands2FrontWheel']**2 + frontWheel2HandleBarPost**2 - bc['handleBarLength']**2) / (2 * bc['hands2FrontWheel'] * frontWheel2HandleBarPost))
    hands2WheelForkHorzAngle = frontWheel2HandleBarHorzAngle + hands2WheelForkAngle
    handsPosX = frontWheelLoc[0] + (bc['hands2FrontWheel'] * math.cos(math.pi - hands2WheelForkHorzAngle))
    handsPosY = frontWheelLoc[1] + (bc['hands2FrontWheel'] * math.sin(math.pi - hands2WheelForkHorzAngle))
    plt.plot([handleBarPostPosX, handsPosX], [handleBarPostPosY, handsPosY])

    # Plot Seat (Assumes flat seat)
    plt.plot([seatPosX - bc['seatLengthAft'], seatPosX + bc['seatLengthFwd']], [seatPosY, seatPosY])


    # Crank and pedals
    theta = -40 # degrees
    thetaRad = math.radians(theta)
    c1x = (bc['crankLength']*math.cos(thetaRad))
    c1y = (bc['crankLength']*math.sin(thetaRad))
    c2x = (bc['crankLength']*math.cos(thetaRad + math.pi))
    c2y = (bc['crankLength']*math.sin(thetaRad + math.pi))
    plt.plot([c1x, c2x], [c1y, c2y])
    plt.plot([c1x-(bc['pedalLength']/2.0), c1x+(bc['pedalLength']/2.0)], [c1y, c1y])
    plt.plot([c2x-(bc['pedalLength']/2.0), c2x+(bc['pedalLength']/2.0)], [c2y, c2y])




    plt.axis('equal')
    plt.show()


