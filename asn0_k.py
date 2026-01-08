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

#front leg:7,8,9; 16,17,18
#middle leg:4,5,6; 13,14,15
#back leg: 1,2,3;10,11,12
#default values: (2,5,8)=400,(11,14,17)=600
#default values: (1,4,7)=500,(10,13,16)=500
#default values: (3,6,9)=300,(12,15,18)=700



board = rrc.Board()
start = True

def Stop(signum, frame):
    global start
    start = False

signal.signal(signal.SIGINT, Stop)

#front leg
def front_lifting():
        #lifting up, after tested, found out the legs in opposite site have opposite axis, 400 is the default location at the right side, and 600 is rhe default position at the left side
        board.bus_servo_set_position(1, [[8, 400], [17, 600]])
        time.sleep(1)
        #lifting the same amount, for right side, lifting up is decreasing, for left side, lifting down is increasing
        board.bus_servo_set_position(1, [[8, 600], [17, 400]])
        
def front_lifting_default():
      board.bus_servo_set_position(1, [[8, 400], [17, 600]])

def front_forwarding():
      board.bus_servo_set_position(1, [[7, 500], [16, 500]])
      time.sleep(1)
      board.bus_servo_set_position(1, [[7, 300], [16, 700]])

def front_forwarding_default():
      board.bus_servo_set_position(1, [[7, 500], [16, 500]])

def front_cramping():
      board.bus_servo_set_position(1, [[9, 300], [18, 700]])
      time.sleep(1)
      board.bus_servo_set_position(1, [[9, 100], [18, 900]])

def front_cramping_default():
      board.bus_servo_set_position(1, [[9, 300], [18, 700]])


#middle leg     
def middle_lifting():
        #lifting up, after tested, found out the legs in opposite site have opposite axis, 400 is the default location at the right side, and 600 is rhe default position at the left side
        board.bus_servo_set_position(1, [[5, 400], [14, 600]])
        time.sleep(1)
        #lifting the same amount, for right side, lifting up is decreasing, for left side, lifting down is increasing
        board.bus_servo_set_position(1, [[5, 600], [14, 400]])

def middle_lifting_little():
        #lifting up, after tested, found out the legs in opposite site have opposite axis, 400 is the default location at the right side, and 600 is rhe default position at the left side
        board.bus_servo_set_position(1, [[5, 400], [14, 600]])
        time.sleep(1)
        #lifting the same amount, for right side, lifting up is decreasing, for left side, lifting down is increasing
        board.bus_servo_set_position(1, [[5, 350], [14, 650]])
        
def middle_lifting_default():
      board.bus_servo_set_position(1, [[5, 400], [14, 600]])

def middle_forwarding():
      board.bus_servo_set_position(1, [[4, 500], [13, 500]])
      time.sleep(1)
      board.bus_servo_set_position(1, [[4, 700], [13, 300]])

def middle_forwarding2():
      board.bus_servo_set_position(1, [[4, 500], [13, 500]])
      time.sleep(1)
      board.bus_servo_set_position(1, [[4, 300], [13, 700]])

def middle_forwarding_default():
      board.bus_servo_set_position(1, [[4, 500], [13, 500]])

def middle_cramping():
      board.bus_servo_set_position(1, [[6, 300], [15, 700]])
      time.sleep(1)
      board.bus_servo_set_position(1, [[6, 500], [15, 500]])

def middle_cramping_default():
      board.bus_servo_set_position(1, [[6, 300], [15, 700]])




#back leg 
def back_lifting():
        #lifting up, after tested, found out the legs in opposite site have opposite axis, 400 is the default location at the right side, and 600 is rhe default position at the left side
        board.bus_servo_set_position(1, [[2, 400], [11, 600]])
        time.sleep(1)
        #lifting the same amount, for right side, lifting up is decreasing, for left side, lifting down is increasing
        board.bus_servo_set_position(1, [[2, 600], [11, 400]])

        
def back_lifting_default():
      board.bus_servo_set_position(1, [[2, 400], [11, 600]])

def back_forwarding():
      board.bus_servo_set_position(1, [[1, 500], [10, 500]])
      time.sleep(1)
      board.bus_servo_set_position(1, [[1, 700], [10, 300]])

def back_forwarding2():
      board.bus_servo_set_position(1, [[1, 500], [10, 500]])
      time.sleep(1)
      board.bus_servo_set_position(1, [[1, 300], [10, 700]])

def back_forwarding_default():
      board.bus_servo_set_position(1, [[1, 500], [10, 500]])

def back_cramping():
      board.bus_servo_set_position(1, [[3, 300], [12, 700]])
      time.sleep(1)
      board.bus_servo_set_position(1, [[3, 500], [12, 500]])

def back_cramping_default():
      board.bus_servo_set_position(1, [[3, 300], [12, 700]])


def lift_push():
        back_forwarding()
        time.sleep(1)
        back_lifting()
        time.sleep(1)
        back_cramping()
        time.sleep(1)
        back_forwarding_default()
        time.sleep(1)
        back_lifting_default()
        time.sleep(1)
        back_cramping_default()

        time.sleep(1)
        middle_forwarding()
        time.sleep(1)
        middle_lifting()
        time.sleep(1)
        middle_cramping()
        time.sleep(1)
        middle_forwarding_default()
        time.sleep(1)
        middle_lifting_default()
        time.sleep(1)
        middle_cramping_default()
        time.sleep(1)

        front_forwarding()
        time.sleep(1)
        front_lifting()
        time.sleep(1)
        front_cramping()
        time.sleep(1)
        front_forwarding_default()
        time.sleep(1)
        front_lifting_default()
        time.sleep(1)
        front_cramping_default()
        time.sleep(1)     


def ripple():
            front_forwarding()
            time.sleep(0.5)
            middle_lifting_little()
            time.sleep(0.5)
            middle_lifting_default()
            time.sleep(0.5)
            middle_forwarding2()
            time.sleep(0.5)
            back_forwarding()
            time.sleep(0.5)

            front_lifting()
            time.sleep(0.5)
            front_forwarding_default()
            time.sleep(0.5)
            front_lifting_default()
            time.sleep(0.5)


            middle_lifting()
            time.sleep(0.5)
            middle_forwarding_default()
            time.sleep(0.5)
            middle_lifting_default()
            time.sleep(0.5)


            back_lifting()
            time.sleep(0.5)
            back_cramping()
            time.sleep(0.5)
            back_lifting_default()
            time.sleep(0.5)
            back_cramping_default()
            time.sleep(0.5)
            back_forwarding_default()
      
      

     
     






if __name__ == '__main__':

    s = sonar.Sonar()

        
    print('Assignment [0] for Group [k]')
    if True:
          ripple()


          












    

        
        


        #moving forward, now the left side's coordinate is not setting correctly
        # board.bus_servo_set_position(1, [[3, 500], [12, 800]])
        # time.sleep(1)
        # board.bus_servo_set_position(1, [[3, 250], [12, 500]])
        # time.sleep(1)
        # board.bus_servo_stop([2, 3, 11, 12])
        # time.sleep(1)

        # # #moving second pair of legs
        # #lifting
        # board.bus_servo_set_position(1, [[5, 400], [14, 600]])
        # time.sleep(1)
        # board.bus_servo_set_position(1, [[5, 250], [14, 750]])
        # time.sleep(1)

        #moving forward
        # board.bus_servo_set_position(1, [[6, 500], [15, 500]])
        # time.sleep(1)
        # board.bus_servo_stop([5, 6, 14, 15])
        # time.sleep(1)

        # #moving third pair of legs
        #lifitng
        # board.bus_servo_set_position(1, [[8, 400], [17, 600]])
        # time.sleep(1)
        # board.bus_servo_set_position(1, [[8, 250], [17, 750]])
        # time.sleep(1)

        #moving forward
        # board.bus_servo_set_position(1, [[9, 500], [18, 500]])
        # time.sleep(1)
        # board.bus_servo_stop([8, 9, 17, 18])
        # time.sleep(1)

        
        

                                     


        



    
