import sys
import time
import signal
import threading
import ros_robot_controller_sdk as rrc
import sonar

print('''
**********************************************************
********CS/ME 301 Assignment Template*******
**********************************************************
----------------------------------------------------------
Usage:
    sudo python3 asn_template.py
----------------------------------------------------------
Tips:
 * Press Ctrl+C to close the program. If it fails,
      please try multiple times！
----------------------------------------------------------
''')

board = rrc.Board()
start = True

def Stop(signum, frame):
    global start
    start = False

signal.signal(signal.SIGINT, Stop)

#Perspective looking from front to back of the robot, and inner are the closest bus servos to the body center

'''
Inner:  Controls forward/backward swing
          Right side: -  forward
          Left side:  +  forward
Middle: Controls up/down lift
          Right side: - lift up
          Left side:  + lift up
Outer:  Controls foot extension (for grip/crawling)
            Right side: + extend foot forward
            Left side:  - extend foot forward
'''

# Right Front Leg
RF_INNER_ID = 7     
RF_MIDDLE_ID = 8     
RF_OUTER_ID = 9      
RF_INNER_DEFAULT = 500
RF_MIDDLE_DEFAULT = 400
RF_OUTER_DEFAULT = 300

# Left Front Leg
LF_INNER_ID = 16
LF_MIDDLE_ID = 17
LF_OUTER_ID = 18
LF_INNER_DEFAULT = 500
LF_MIDDLE_DEFAULT = 600
LF_OUTER_DEFAULT = 700

# Right Middle Leg 
RM_INNER_ID = 4
RM_MIDDLE_ID = 5
RM_OUTER_ID = 6
RM_INNER_DEFAULT = 500
RM_MIDDLE_DEFAULT = 400
RM_OUTER_DEFAULT = 300

# Left Middle Leg
LM_INNER_ID = 13
LM_MIDDLE_ID = 14
LM_OUTER_ID = 15
LM_INNER_DEFAULT = 500
LM_MIDDLE_DEFAULT = 600
LM_OUTER_DEFAULT = 700

# Right Back Leg
RB_INNER_ID = 1
RB_MIDDLE_ID = 2
RB_OUTER_ID = 3
RB_INNER_DEFAULT = 500
RB_MIDDLE_DEFAULT = 400
RB_OUTER_DEFAULT = 300

# Left Back Leg
LB_INNER_ID = 10
LB_MIDDLE_ID = 11
LB_OUTER_ID = 12
LB_INNER_DEFAULT = 500
LB_MIDDLE_DEFAULT = 600
LB_OUTER_DEFAULT = 700

#Set every servo to default position
def set_all_default():
    board.bus_servo_set_position(1, [
        # Right Front
        [RF_INNER_ID, RF_INNER_DEFAULT], 
        [RF_MIDDLE_ID, RF_MIDDLE_DEFAULT], 
        [RF_OUTER_ID, RF_OUTER_DEFAULT],
        # Right Middle
        [RM_INNER_ID, RM_INNER_DEFAULT], 
        [RM_MIDDLE_ID, RM_MIDDLE_DEFAULT], 
        [RM_OUTER_ID, RM_OUTER_DEFAULT],
        # Right Back
        [RB_INNER_ID, RB_INNER_DEFAULT], 
        [RB_MIDDLE_ID, RB_MIDDLE_DEFAULT], 
        [RB_OUTER_ID, RB_OUTER_DEFAULT],
        # Left Front
        [LF_INNER_ID, LF_INNER_DEFAULT], 
        [LF_MIDDLE_ID, LF_MIDDLE_DEFAULT], 
        [LF_OUTER_ID, LF_OUTER_DEFAULT],
        # Left Middle
        [LM_INNER_ID, LM_INNER_DEFAULT], 
        [LM_MIDDLE_ID, LM_MIDDLE_DEFAULT], 
        [LM_OUTER_ID, LM_OUTER_DEFAULT],
        # Left Back
        [LB_INNER_ID, LB_INNER_DEFAULT], 
        [LB_MIDDLE_ID, LB_MIDDLE_DEFAULT], 
        [LB_OUTER_ID, LB_OUTER_DEFAULT],
    ])
    time.sleep(1)


#Front pair leg helper functions
def front_pair_swing_forward(duration, amount):
    board.bus_servo_set_position(duration, [[RF_INNER_ID, RF_INNER_DEFAULT - amount], [LF_INNER_ID, LF_INNER_DEFAULT + amount]])


def front_pair_swing_backward(duration, amount):
    board.bus_servo_set_position(duration, [[RF_INNER_ID, RF_INNER_DEFAULT + amount],  [LF_INNER_ID, LF_INNER_DEFAULT - amount]])


def front_pair_swing_default(duration):
    board.bus_servo_set_position(duration, [[RF_INNER_ID, RF_INNER_DEFAULT],[LF_INNER_ID, LF_INNER_DEFAULT]])


def front_pair_push_down(duration, amount):
    board.bus_servo_set_position(duration, [[RF_MIDDLE_ID, RF_MIDDLE_DEFAULT + amount], [LF_MIDDLE_ID, LF_MIDDLE_DEFAULT - amount]])


def front_pair_lift_leg(duration, amount):
    board.bus_servo_set_position(duration, [[RF_MIDDLE_ID, RF_MIDDLE_DEFAULT - amount], [LF_MIDDLE_ID, LF_MIDDLE_DEFAULT + amount]])


def front_pair_middle_default(duration):
    board.bus_servo_set_position(duration, [[RF_MIDDLE_ID, RF_MIDDLE_DEFAULT],[LF_MIDDLE_ID, LF_MIDDLE_DEFAULT]])


def front_pair_extend_outward(duration, amount):
    board.bus_servo_set_position(duration, [[RF_OUTER_ID, RF_OUTER_DEFAULT + amount],  [LF_OUTER_ID, LF_OUTER_DEFAULT - amount]])


def front_pair_retract_inward(duration, amount):
    board.bus_servo_set_position(duration, [[RF_OUTER_ID, RF_OUTER_DEFAULT - amount],  [LF_OUTER_ID, LF_OUTER_DEFAULT + amount]])


def front_pair_outer_default(duration):
    board.bus_servo_set_position(duration, [[RF_OUTER_ID, RF_OUTER_DEFAULT],[LF_OUTER_ID, LF_OUTER_DEFAULT]])

# Middle pair leg helper functions
def middle_pair_swing_forward(duration, amount):
    board.bus_servo_set_position(duration, [[RM_INNER_ID, RM_INNER_DEFAULT - amount],  [LM_INNER_ID, LM_INNER_DEFAULT + amount]])


def middle_pair_swing_backward(duration, amount):
    board.bus_servo_set_position(duration, [[RM_INNER_ID, RM_INNER_DEFAULT + amount], [LM_INNER_ID, LM_INNER_DEFAULT - amount]])


def middle_pair_swing_default(duration):
    board.bus_servo_set_position(duration, [[RM_INNER_ID, RM_INNER_DEFAULT],[LM_INNER_ID, LM_INNER_DEFAULT]])


def middle_pair_push_down(duration, amount):
    board.bus_servo_set_position(duration, [[RM_MIDDLE_ID, RM_MIDDLE_DEFAULT + amount], [LM_MIDDLE_ID, LM_MIDDLE_DEFAULT - amount]])


def middle_pair_lift_leg(duration, amount):
    board.bus_servo_set_position(duration, [[RM_MIDDLE_ID, RM_MIDDLE_DEFAULT - amount], [LM_MIDDLE_ID, LM_MIDDLE_DEFAULT + amount]])


def middle_pair_middle_default(duration):
    board.bus_servo_set_position(duration, [[RM_MIDDLE_ID, RM_MIDDLE_DEFAULT],[LM_MIDDLE_ID, LM_MIDDLE_DEFAULT]])


def middle_pair_extend_outward(duration, amount):
    board.bus_servo_set_position(duration, [[RM_OUTER_ID, RM_OUTER_DEFAULT + amount], [LM_OUTER_ID, LM_OUTER_DEFAULT - amount]])


def middle_pair_retract_inward(duration, amount):
    board.bus_servo_set_position(duration, [[RM_OUTER_ID, RM_OUTER_DEFAULT - amount],  [LM_OUTER_ID, LM_OUTER_DEFAULT + amount]])


def middle_pair_outer_default(duration):
    board.bus_servo_set_position(duration, [[RM_OUTER_ID, RM_OUTER_DEFAULT],[LM_OUTER_ID, LM_OUTER_DEFAULT]])

#Back pair leg helper functions
def back_pair_swing_forward(duration, amount):
    board.bus_servo_set_position(duration, [[RB_INNER_ID, RB_INNER_DEFAULT - amount],  [LB_INNER_ID, LB_INNER_DEFAULT + amount]])


def back_pair_swing_backward(duration, amount):
    board.bus_servo_set_position(duration, [[RB_INNER_ID, RB_INNER_DEFAULT + amount], [LB_INNER_ID, LB_INNER_DEFAULT - amount]])


def back_pair_swing_default(duration):
    board.bus_servo_set_position(duration, [[RB_INNER_ID, RB_INNER_DEFAULT],[LB_INNER_ID, LB_INNER_DEFAULT]])


def back_pair_push_down(duration, amount):
    board.bus_servo_set_position(duration, [[RB_MIDDLE_ID, RB_MIDDLE_DEFAULT + amount],  [LB_MIDDLE_ID, LB_MIDDLE_DEFAULT - amount]])


def back_pair_lift_leg(duration, amount):
    board.bus_servo_set_position(duration, [[RB_MIDDLE_ID, RB_MIDDLE_DEFAULT - amount], [LB_MIDDLE_ID, LB_MIDDLE_DEFAULT + amount]])


def back_pair_middle_default(duration):
    board.bus_servo_set_position(duration, [[RB_MIDDLE_ID, RB_MIDDLE_DEFAULT],[LB_MIDDLE_ID, LB_MIDDLE_DEFAULT]])


def back_pair_extend_outward(duration, amount):
    board.bus_servo_set_position(duration, [[RB_OUTER_ID, RB_OUTER_DEFAULT + amount],  [LB_OUTER_ID, LB_OUTER_DEFAULT - amount]])


def back_pair_retract_inward(duration, amount):
    board.bus_servo_set_position(duration, [[RB_OUTER_ID, RB_OUTER_DEFAULT - amount],  [LB_OUTER_ID, LB_OUTER_DEFAULT + amount]])


def back_pair_outer_default(duration):
    board.bus_servo_set_position(duration, [[RB_OUTER_ID, RB_OUTER_DEFAULT],[LB_OUTER_ID, LB_OUTER_DEFAULT]])

#last 8.5 seconds
def ripple_slow():
    duration = 1.0
    swing = 200
    push = 200
    crawl = 200
    pause = 0.5
    
    # PHASE 1: Front and middle pair of legs swing forward
    front_pair_swing_forward(duration, swing)
    
    middle_pair_lift_leg(pause, 50)  # Slight lift for stability
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")

    middle_pair_swing_forward(duration, swing)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")

    middle_pair_middle_default(pause)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")

    back_pair_swing_backward(duration, swing)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")

    # PHASE 2: Front pair crawling
    front_pair_push_down(duration, push)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")

    front_pair_swing_default(duration)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")

    front_pair_middle_default(duration)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")

    # PHASE 3: Middle pair crawling
    middle_pair_push_down(duration, push)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")

    middle_pair_swing_default(duration)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")

    middle_pair_middle_default(duration)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")

    # PHASE 4: Back pair push forward and crawl
    back_pair_push_down(duration, push)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")

    back_pair_extend_outward(duration, crawl)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")

    back_pair_middle_default(duration)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")

    back_pair_outer_default(duration)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")
    
    back_pair_swing_default(duration)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")

#lasts 5.5 seconds
def ripple_fast():
    duration = 0.6
    swing = 200
    push = 250
    crawl = 250
    pause = 0.3
    
    #  Front and middle pair of legs swing forward
    front_pair_swing_forward(duration, swing)
    
    middle_pair_lift_leg(pause, 50)  # Slight lift for stability
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")
    middle_pair_swing_forward(duration, swing)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")

    middle_pair_middle_default(pause)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")
    
    back_pair_swing_backward(duration, swing)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")

    # PHASE 2: Front pair crawling
    front_pair_push_down(duration, push)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")

    front_pair_swing_default(duration)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")

    front_pair_middle_default(duration)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")

    # PHASE 3: Middle pair crawling
    middle_pair_push_down(duration, push)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")

    middle_pair_swing_default(duration)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")

    middle_pair_middle_default(duration)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")

    # PHASE 4: Back pair push forward and crawl
    back_pair_push_down(duration, push)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")

    back_pair_extend_outward(duration, crawl)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")

    back_pair_middle_default(duration)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")

    back_pair_outer_default(duration)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")

    back_pair_swing_default(duration)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")





    # Front right 


#Discover the problem that if directly moving the pair of legs, the friction created by that will distort the robot, so lift and moving
def front_pair_step_forward(duration, swing):
    # Lift + swing forward
    board.bus_servo_set_position(duration, [
        [RF_MIDDLE_ID, RF_MIDDLE_DEFAULT - 50],
        [LF_MIDDLE_ID, LF_MIDDLE_DEFAULT + 50],
        [RF_INNER_ID, RF_INNER_DEFAULT - swing],
        [LF_INNER_ID, LF_INNER_DEFAULT + swing]
    ])
    time.sleep(duration)
    
    # Lower 
    board.bus_servo_set_position(0.5, [
        [RF_MIDDLE_ID, RF_MIDDLE_DEFAULT],
        [LF_MIDDLE_ID, LF_MIDDLE_DEFAULT]
    ])

def middle_pair_step_forward(duration, swing):
    board.bus_servo_set_position(duration, [
        [RM_MIDDLE_ID, RM_MIDDLE_DEFAULT - 50],
        [LM_MIDDLE_ID, LM_MIDDLE_DEFAULT + 50],
        [RM_INNER_ID, RM_INNER_DEFAULT - swing],
        [LM_INNER_ID, LM_INNER_DEFAULT + swing]
    ])
    time.sleep(duration)
    
    # Lower
    board.bus_servo_set_position(0.5, [
        [RM_MIDDLE_ID, RM_MIDDLE_DEFAULT],
        [LM_MIDDLE_ID, LM_MIDDLE_DEFAULT]
    ])


    # Lift + swing backward
    board.bus_servo_set_position(duration, [
        [RB_MIDDLE_ID, RB_MIDDLE_DEFAULT - 50],
        [LB_MIDDLE_ID, LB_MIDDLE_DEFAULT + 50],
        [RB_INNER_ID, RB_INNER_DEFAULT + swing],  
        [LB_INNER_ID, LB_INNER_DEFAULT - swing]    
    ])
    time.sleep(duration)
    
    # Lower 
    board.bus_servo_set_position(0.5, [
        [RB_MIDDLE_ID, RB_MIDDLE_DEFAULT],
        [LB_MIDDLE_ID, LB_MIDDLE_DEFAULT]
    ])

def front_pair_push_and_swing_backward(duration, push, swing):
    board.bus_servo_set_position(duration, [
        [RF_MIDDLE_ID, RF_MIDDLE_DEFAULT + push],
        [LF_MIDDLE_ID, LF_MIDDLE_DEFAULT - push],
        [RF_INNER_ID, RF_INNER_DEFAULT + swing],
        [LF_INNER_ID, LF_INNER_DEFAULT - swing]
    ])

def middle_pair_push_and_swing_backward(duration, push, swing):
    board.bus_servo_set_position(duration, [
        [RM_MIDDLE_ID, RM_MIDDLE_DEFAULT + push],
        [LM_MIDDLE_ID, LM_MIDDLE_DEFAULT - push],
        [RM_INNER_ID, RM_INNER_DEFAULT + swing],
        [LM_INNER_ID, LM_INNER_DEFAULT - swing]
    ])

def back_pair_push_and_swing_backward(duration, push, swing):
    board.bus_servo_set_position(duration, [
        [RB_MIDDLE_ID, RB_MIDDLE_DEFAULT + push],   
        [LB_MIDDLE_ID, LB_MIDDLE_DEFAULT - push],
        [RB_INNER_ID, RB_INNER_DEFAULT + swing],   
        [LB_INNER_ID, LB_INNER_DEFAULT - swing]
    ])

def back_pair_default(duration):
    board.bus_servo_set_position(duration, [
        [RB_MIDDLE_ID, RB_MIDDLE_DEFAULT],
        [LB_MIDDLE_ID, LB_MIDDLE_DEFAULT],
        [RB_INNER_ID, RB_INNER_DEFAULT],
        [LB_INNER_ID, LB_INNER_DEFAULT]
    ])

def ripple_slow2():
    duration = 1.0
    pause=0.5
    swing = 200
    push = 200

    #Phase 1: Front and middle pair step forward, back pair step backward
    front_pair_step_forward(duration, swing)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")

    middle_pair_step_forward(duration, swing)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")

    #Phase 2: Front push and swing backward
    front_pair_push_and_swing_backward(duration, push, swing)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")

    #Phase 3: Middle push and swing backward
    middle_pair_push_and_swing_backward(duration, push, swing)
    time.sleep(pause)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")

    #Phase 4: Back push and swing backward
    back_pair_push_and_swing_backward(duration, push, swing)
    time.sleep(pause)
    back_pair_default(duration)
    print(f"[{time.time() - start_time}s] Sonar: {s.getDistance()} mm")










if __name__ == '__main__':

    s = sonar.Sonar()
    start_time = time.time()
    set_all_default()
    
    print('Assignment 0 for Group K')

    while True:

        ripple_slow()
        time.sleep(1)
        # ripple_fast()
        # time.sleep(1)


        



        


    
