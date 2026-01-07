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

if __name__ == '__main__':

    s = sonar.Sonar()

    while True:
        
        print('Assignment [] for Group []')
        
        time.sleep(0.1)
        print(s.getDistance())
        
        time.sleep(1) 
        
        board.bus_servo_set_position(1, [[1, 500], [2, 500]])
        time.sleep(1)
        board.bus_servo_set_position(2, [[1, 0], [2, 0]])
        time.sleep(1)
        board.bus_servo_stop([1, 2])
        time.sleep(1)

    
