DISCLAIMER: This is to be used as an aid only, and does not replace a professional bike fit. The author will not be held accountable for anything that results from the use of this tool. Use at your own risk.

# bike-fit-vis
A simple tool that uses bike frame and person length measurements to visualise the user on a bike, and calculate current angles as the crank moves through a revolution. This allows multiple riders to be overlaid and plotted in different positions, to compare the effect of adjusting seat height and position.

<img src="https://github.com/tbattz/bike-fit-vis/raw/main/images/sample-plot.png" width="1000" height="426">

# Setup
There are two main configuration files, one for the bike, and one for the rider. The rider file allows multiple rider configurations to be set.
## bike.json
This defines the dimensions of the bike. "Required for rider" determines whether the length has an effect on the rider angles.

| Parameter Name | Required for Rider | Description                                                                                                |
| -------------- | ------------------ |------------------------------------------------------------------------------------------------------------|
| chainStay      | No                 | The length from the bottom bracket to the center of the rear wheel.                                        |
| wheelBase      | No                 | The length between the centers of the two wheels.                                                          |
| wheelDiameter  | No                 | The diameter of the wheel.                                                                                 |
| seatTube       | Yes                | The length from the bottom bracket to the point where the seat tube meets the rest of the frame.           |
| seatStay       | No                 | The length from the center of the rear wheel to the point where the seat tube meets the rest of the frame. |
| bototmBracketDrop | Yes             | The vertical distance between the center of the rear wheel and the bottom bracket.                         |
| forkLength     | No                 | The distance from the center of the front wheel to the point where the fork meets the rest of the frame.   |
| downTube       | Yes                | The distance from the bottom bracket to the point where the fork meets the frame.                          |
| topTube        | Yes                | The distance from the seat post frame point to the front post frame point.                                 |
| headTube       | No                 | The distance from where the fork meets the frame to where the top tube meets the frame.                    |
| handleBarPost  | Yes                | The distance from the point where the top tube meets the frame to the top of the handle bar tube.          |
| handleBarLength | Yes               | The distance fro the top of the handle bar post to the front levers. |
| handleBar2FrontWheel | No           | The distance from the front levers to the center of the front wheel. |
| crankLength | Yes                   | The length of the cranks. |
| leverLength | Yes                   | The length of the brake/gear levers. |


## rider.json
This can define multiple riders. Each rider must have the following defined.

| Parameter Name        | Required for Rider | Description                                                                   |
|-----------------------| ------------------ |-------------------------------------------------------------------------------|
| seatLengthFwd         | Yes                | The length of the seat forward of the seatpost.                               |
| seatLengthAft         | Yes                | The length of the seat behind the seatpost.                                   |
| seatRiderOffsetX      | Yes              | The horizontal offset of the rider hip joint from the seat/seatpost position. |
| seatRiderOffsetY      | Yes              | The vertical offset of the rider hip joint from the seat/seatpost position.   |
| hip2ShoulderLength    | Yes            | The distance between the hip joint point and the shoulder joint point.        |
| hip2KneeLength        | Yes                | The distance from the hip joint to the knee joint. |
| knee2AnkleLength      | Yes              | The distance between the knee joint point to the ankle joint point. |
| footLength            | Yes                | The length from the ankle joint to the toe. |
| footContactProportion | Yes         | The proportion from the rear of the foot that the foot contacts the middle of the pedal. |
| pedalLength           | Yes         | The Length of the pedal. |
| shoulder2ElbowLength  | Yes         | The length from the shoulder joint to the elbow joint. |
| elbowWristContactLength | Yes       | The length from the elbow joint to the wrist joint. |
| wrist2FingerHoldPoint | Yes         | The length from the wrist joint to the point on the fingers that wrap around the levers. |
| hip2HorizontalAngleDeg | Yes        | The angle, in degrees of the riders torso, to the horizontal. |

# Use
Update both bike.json and rider.json with your configurations, then run

```
python main.py
```

This allows the user to visualise the position through the crank cycle, and compare the maximum and minimum knee and hip angles for each configuration.


