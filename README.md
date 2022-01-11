# Instrumentations

Project repository for the Instrumentations Studio 2021/22 

Design & Computation - University of the Arts, Berlin

## Setup

### Hardware
1. fix motor 1 to the left and motor 2 to the right
2. connect motors to fabscan shield sockets 1 and 2
3. measure 'MOTOR_DIST': horizontal distance between motors
4. hang cables
5. add weights to pen and both ends
6. position pen at zero position
7. measure 'HOME_LEN': length of cables from pen to motor at zero position 
1. power to fabscan shield (12V)
2. connect arduino to laptop

### Scripts

1. Upload and run *Arduino/PolargraphCalibration* to measure 'LEN_PER_STEP': the change in cable length in mm per motor step
2. Set 'MOTOR_DIST', 'HOME_LEN' and 'LEN_PER_STEP' in *Arduino/Polargraph*
3. Set limits and maxSpeed
4. Upload *Arduino/Polargraph* to arduino
5. Start python script to control polargraph
