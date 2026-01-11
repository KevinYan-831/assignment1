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
#front leg second servo pushing downward to lift the robot body up
def front_lifting():
        board.bus_servo_set_position(1, [[8, 600], [17, 400]])

#front leg second servo pushing downward to lift the robot body up with faster speed
def front_lifting2():
        board.bus_servo_set_position(0.5, [[8, 600], [17, 400]])

#restore front leg second servo's default position
def front_lifting_default():
      board.bus_servo_set_position(1, [[8, 400], [17, 600]])

#restore front leg second servo's default position with faster speed
def front_lifting_default2():
      board.bus_servo_set_position(0.5, [[8, 400], [17, 600]])

#front leg first servo moving forward
def front_forwarding():
      board.bus_servo_set_position(1, [[7, 300], [16, 700]])

#front leg first servo moving forward with faster spped
def front_forwarding2():
      board.bus_servo_set_position(0.5, [[7, 300], [16, 700]])

#restore front leg first servo's default position
def front_forwarding_default():
      board.bus_servo_set_position(1, [[7, 500], [16, 500]])

#restore front leg first servo's default position with faster speed
def front_forwarding_default2():
      board.bus_servo_set_position(0.5, [[7, 700], [16, 300]])

#front leg end servo crawling inward
def front_crawling():
      board.bus_servo_set_position(1, [[9, 100], [18, 900]])

#restore front leg end servo's default position
def front_crawling_default():
      board.bus_servo_set_position(1, [[9, 300], [18, 700]])

#middle leg     
#middle leg second servo pushing downward to lift the robot body up
def middle_lifting():
        board.bus_servo_set_position(1, [[5, 600], [14, 400]])

#middle leg second servo pushing downward to lift the robot body up with faster speed
def middle_lifting2():
        board.bus_servo_set_position(0.5, [[5, 600], [14, 400]])

#middle leg second servo pushing downward to lift the robot body up with less extent
def middle_lifting_little():
        board.bus_servo_set_position(0.5, [[5, 350], [14, 650]])
        
#restore middle leg second servo's default position
def middle_lifting_default():
      board.bus_servo_set_position(0.5, [[5, 400], [14, 600]])

#middle leg first servo moving backward
def middle_forwarding():
      board.bus_servo_set_position(1, [[4, 700], [13, 300]])

#middle leg first servo moving forward
def middle_forwarding2():
      board.bus_servo_set_position(1, [[4, 300], [13, 700]])

#middle leg first servo moving forward with faster speed
def middle_forwarding3():
      board.bus_servo_set_position(0.5, [[4, 300], [13, 700]])

#restore middle leg first servo's default position
def middle_forwarding_default():
      board.bus_servo_set_position(1, [[4, 500], [13, 500]])

#restore middle leg first servo's default position with faster speed
def middle_forwarding_default2():
      board.bus_servo_set_position(0.5, [[4, 700], [13, 300]])

#middle leg end servo crawling inward
def middle_crawling():
      board.bus_servo_set_position(1, [[6, 500], [15, 500]])

#restore middle leg end servo's default position
def middle_crawling_default():
      board.bus_servo_set_position(1, [[6, 300], [15, 700]])

#back leg 
#back leg second servo pushing downward to lift the robot body up
def back_lifting():
        board.bus_servo_set_position(1, [[2, 600], [11, 400]])

#back leg second servo pushing downward to lift the robot body up with faster speed
def back_lifting2():
       board.bus_servo_set_position(0.5, [[2, 700], [11, 300]])
       
#restore back leg second servo's default position
def back_lifting_default():
      board.bus_servo_set_position(1, [[2, 400], [11, 600]])

#restore back leg second servo's default position with faster speed
def back_lifting_default2():
      board.bus_servo_set_position(0.5, [[2, 400], [11, 600]])

#back leg first servo moving backward
def back_forwarding():
      board.bus_servo_set_position(1, [[1, 700], [10, 300]])

#back leg first servo moving backward with faster speed
def back_forwarding3():
      board.bus_servo_set_position(0.5, [[1, 700], [10, 300]])

#back leg first servo moving forward
def back_forwarding2():
      board.bus_servo_set_position(1, [[1, 300], [10, 700]])

#restore back leg first servo's default position
def back_forwarding_default():
      board.bus_servo_set_position(1, [[1, 500], [10, 500]])

#restore back leg first servo's default position with faster speed
def back_forwarding_default2():
      board.bus_servo_set_position(0.5, [[1, 500], [10, 500]])

#back leg end servo crawling inward
def back_crawling():
      board.bus_servo_set_position(1, [[3, 500], [12, 500]])

#restore back leg end servo's default position
def back_crawling_default():
      board.bus_servo_set_position(1, [[3, 300], [12, 700]])

#restore back leg end servo's default position with faster speed
def back_crawling_default2():
      board.bus_servo_set_position(0.5, [[3, 300], [12, 700]])



def ripple_slow():
            front_forwarding()
            middle_lifting_little()   
            time.sleep(0.5)
            middle_forwarding2()
            time.sleep(0.5)
            middle_lifting_default()
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
            back_crawling()
            time.sleep(0.5)
            back_lifting_default()
            time.sleep(0.5)
            back_crawling_default()
            time.sleep(0.5)
            back_forwarding_default()

#with faster time gap and greater range of movement
def ripple_fast():
            front_forwarding2()
            middle_lifting_little()   
            time.sleep(0.2)
            middle_forwarding3()
            time.sleep(0.2)
            middle_lifting_default()
            time.sleep(0.2)
            back_forwarding3()
            time.sleep(0.2)

            front_lifting2()
            time.sleep(0.2)
            front_forwarding_default2()
            time.sleep(0.2)
            front_lifting_default2()
            time.sleep(0.2)


            middle_lifting2()
            time.sleep(0.2)
            middle_forwarding_default2()
            time.sleep(0.2)
            middle_lifting_default()
            time.sleep(0.2)


            back_lifting2()
            time.sleep(0.2)
            board.bus_servo_set_position(0.5, [[3, 250], [12, 750]])
            back_crawling()
            time.sleep(0.2)
            back_lifting_default2()
            time.sleep(0.2)
            back_crawling_default2()
            time.sleep(0.2)
            back_forwarding_default2()
      
      

def set_all_default():
      front_lifting_default()
      front_forwarding_default()
      front_crawling_default()
      middle_lifting_default()
      middle_forwarding_default()
      middle_crawling_default()
      back_lifting_default()
      back_forwarding_default()
      back_crawling_default()

     


def lift_push():
        back_forwarding()
        time.sleep(1)
        back_lifting()
        time.sleep(1)
        back_crawling()
        time.sleep(1)
        back_forwarding_default()
        time.sleep(1)
        back_lifting_default()
        time.sleep(1)
        back_crawling_default()

        time.sleep(1)
        middle_forwarding()
        time.sleep(1)
        middle_lifting()
        time.sleep(1)
        middle_crawling()
        time.sleep(1)
        middle_forwarding_default()
        time.sleep(1)
        middle_lifting_default()
        time.sleep(1)
        middle_crawling_default()
        time.sleep(1)

        front_forwarding()
        time.sleep(1)
        front_lifting()
        time.sleep(1)
        front_crawling()
        time.sleep(1)
        front_forwarding_default()
        time.sleep(1)
        front_lifting_default()
        time.sleep(1)
        front_crawling_default()
        time.sleep(1)    




if __name__ == '__main__':

    s = sonar.Sonar()

        
    print('Assignment [0] for Group [k]')
    set_all_default()
    if True:
          ripple_slow()



          












        
        

                                     


        



    
