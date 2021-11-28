# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 12:22:03 2021

@author: Kit

Eyerok Code for Senior Design Project (Threading Method-Not going to work U2D2 cannot process 2 signals at the same time)
"""

import os
import time
import threading
import concurrent.futures
import keyboard
if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode() 
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import *                    # Uses Dynamixel SDK library

# Control table address                        # Control table address is different in Dynamixel model
ADDR_MX_TORQUE_ENABLE      = 24               
ADDR_MX_GOAL_POSITION      = 30
ADDR_MX_PRESENT_POSITION   = 36
ADDR_MX_MOVE_SPEED         = 32
ADDR_MX_CCW_ANG_LMT        = 8
ADDR_MX_PRESENT_SPEED      = 38
ADDR_MX_TORQUE_LIMIT       = 34
ADDR_MX_PRESSENT_LOAD      = 40
# Protocol version
PROTOCOL_VERSION            = 1.0               # See which protocol version is used in the Dynamixel

# Default setting
DXL_0                       =  0                # Dynamixel ID : 0
DXL_1                       =  1                # Dynamixel ID : 1
BAUDRATE                    = 1000000           # Dynamixel default baudrate : 57600, Increased to 2m, maybe better latency
DEVICENAME                  = 'COM4'            # Windows    #'/dev/tty.usbserial-FT62AGHG' # Macbook    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL_0_MINIMUM_POSITION_VALUE  = 704
DXL_0_MAXIMUM_POSITION_VALUE  = 849 
DXL_1_MINIMUM_POSITION_VALUE  = 530                 # Dynamixel will rotate between this value
DXL_1_MAXIMUM_POSITION_VALUE  = 799
            # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_MOVING_STATUS_THRESHOLD = 10                # Dynamixel moving status threshold

DXL_HOME                    = 799               # Home Value for O degree of motors

def run(portHandler,packetHandler):
    dxl_comm_result0, dxl_error0 = packetHandler.write2ByteTxRx(portHandler, DXL_0, ADDR_MX_CCW_ANG_LMT, 0)
    dxl_comm_result1, dxl_error1 = packetHandler.write2ByteTxRx(portHandler, DXL_1, ADDR_MX_CCW_ANG_LMT, 0)
    dxl_0_present_speed, dxl_comm_result0, dxl_error0 = packetHandler.read2ByteTxRx(portHandler, DXL_0, ADDR_MX_PRESENT_SPEED)
    dxl_1_present_speed, dxl_comm_result0, dxl_error0 = packetHandler.read2ByteTxRx(portHandler, DXL_1, ADDR_MX_PRESENT_SPEED)
    dxl_0_present_position, dxl_comm_result0, dxl_error0 = packetHandler.read2ByteTxRx(portHandler, DXL_0, ADDR_MX_PRESENT_POSITION)
    dxl_1_present_position, dxl_comm_result0, dxl_error0 = packetHandler.read2ByteTxRx(portHandler, DXL_1, ADDR_MX_PRESENT_POSITION)
    dxl_0_present_position_range = (dxl_0_present_position-DXL_0_MINIMUM_POSITION_VALUE)/(DXL_0_MAXIMUM_POSITION_VALUE-DXL_0_MINIMUM_POSITION_VALUE)
    dxl_1_present_position_range = (dxl_1_present_position-DXL_1_MINIMUM_POSITION_VALUE)/(DXL_1_MAXIMUM_POSITION_VALUE-DXL_1_MINIMUM_POSITION_VALUE)
    
    i=0
    getdelay = True
    while True:
        if keyboard.is_pressed("q"):
            shut_down(portHandler,packetHandler)         # Calls Shutdown Function
            break
        last_dxl_1_present_speed = dxl_1_present_speed
        dxl_0_present_speed, dxl_comm_result0, dxl_error0 = packetHandler.read2ByteTxRx(portHandler, DXL_0, ADDR_MX_PRESENT_SPEED)
        dxl_1_present_speed, dxl_comm_result0, dxl_error0 = packetHandler.read2ByteTxRx(portHandler, DXL_1, ADDR_MX_PRESENT_SPEED)
        
        


    
        


        


        
       
        dxl_0_present_position, dxl_comm_result0, dxl_error0 = packetHandler.read2ByteTxRx(portHandler, DXL_0, ADDR_MX_PRESENT_POSITION)
        dxl_1_present_position, dxl_comm_result0, dxl_error0 = packetHandler.read2ByteTxRx(portHandler, DXL_1, ADDR_MX_PRESENT_POSITION)

        last_dxl_0_present_position_range=dxl_0_present_position_range
        last_dxl_1_present_position_range=dxl_1_present_position_range  
        dxl_0_present_position_range = (dxl_0_present_position-DXL_0_MINIMUM_POSITION_VALUE)/(DXL_0_MAXIMUM_POSITION_VALUE-DXL_0_MINIMUM_POSITION_VALUE)
        dxl_1_present_position_range = (dxl_1_present_position-DXL_1_MINIMUM_POSITION_VALUE)/(DXL_1_MAXIMUM_POSITION_VALUE-DXL_1_MINIMUM_POSITION_VALUE)

        S
        dirMove0 = dxl_0_present_position_range-last_dxl_0_present_position_range<0
        dirMove1 = dxl_1_present_position_range-last_dxl_1_present_position_range<0
        # print(dxl_0_present_speed)
        if dirMove0:
            dxl_0_present_speed -= 1023
        if dirMove1:
            dxl_1_present_speed -= 1023
        
        
        sendspeed = abs(int(1000*(dxl_0_present_position_range-last_dxl_0_present_position_range)))
        a = dxl_0_present_position_range>dxl_1_present_position_range-.15
        b = not dirMove0
        dxl_comm_result0, dxl_error0 = packetHandler.write2ByteTxRx(portHandler, DXL_1, ADDR_MX_TORQUE_LIMIT,1023)
        if(a):
            dxl_comm_result0, dxl_error0 = packetHandler.write2ByteTxRx(portHandler, DXL_1, ADDR_MX_MOVE_SPEED,1023)
            if abs(dxl_1_present_speed-dxl_1_present_speed)<50:
                dxl_comm_result0, dxl_error0 = packetHandler.write2ByteTxRx(portHandler, DXL_0, ADDR_MX_MOVE_SPEED,2047)
        else:
            dxl_comm_result0, dxl_error0 = packetHandler.write2ByteTxRx(portHandler, DXL_0, ADDR_MX_MOVE_SPEED,0)
            if abs(dxl_0_present_position-dxl_1_present_position)<5:
                pass
            elif (a and (not b)) or ((not a) and b):
             sendspeed = int(sendspeed-sendspeed*sendspeed/1000)
            else:
                sendspeed = int(sendspeed+sendspeed*sendspeed/100)   
            dxl_comm_result0, dxl_error0 = packetHandler.write2ByteTxRx(portHandler, DXL_1, ADDR_MX_MOVE_SPEED,int(dirMove0)*1023 + sendspeed)
     
    
        #print(str(int(a and b)) + " Speed0:"+str(1000*(dxl_0_present_position_range-last_dxl_0_present_position_range))+"\tSpeed1:"+str(dxl_1_present_speed)+"\tPos0:"+str(dxl_0_present_position_range)+"\tPos1:"+str(dxl_1_present_position_range)+"\tsendspeed:"+str(sendspeed))
   



def start_up():                                 # Initilizes connection to motors and sets starting parmeters.
    
    portHandler = PortHandler(DEVICENAME)       # Initialize PortHandler and set port path
    packetHandler = PacketHandler(PROTOCOL_VERSION) # Initialize PacketHandler and set protocol version
    
    if portHandler.openPort():                  # Open port
        print("Succeeded to open the port")
    else:
        print("Failed to open the port")
        print("Press any key to terminate...")
        getch()
        quit()
    
    if portHandler.setBaudRate(BAUDRATE):       # Set port baudrate
        print("Succeeded to change the baudrate")
    else:
        print("Failed to change the baudrate")
        print("Press any key to terminate...")
        getch()
        quit()
    
    dxl_comm_result0, dxl_error0 = packetHandler.write1ByteTxRx(portHandler, DXL_0, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)   #Enables Torque for Motor 0
    if dxl_comm_result0 != COMM_SUCCESS:        # Checks if Motor 0 connected correctly
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result0))
    elif dxl_error0 != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error0))
    else:
        print("Dynamixel#%d has been successfully connected" % DXL_0)
              
    dxl_comm_result1, dxl_error1 = packetHandler.write1ByteTxRx(portHandler, DXL_1, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)   #Enables Torque for Motor 1
    if dxl_comm_result1 != COMM_SUCCESS:        # Checks if Motor 1 connected correctly
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result1))
    elif dxl_error1 != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error1))
    else:
        print("Dynamixel#%d has been successfully connected" % DXL_1)
    
    dxl_comm_result0, dxl_error0 = packetHandler.write2ByteTxRx(portHandler,DXL_0,ADDR_MX_TORQUE_LIMIT,1000) # Sets Torque of Motor 0 to Max
    torquelimit0, dxl_comm_result0, dxl_error0 = packetHandler.read2ByteTxRx(portHandler,DXL_0,ADDR_MX_TORQUE_LIMIT) # Reads Torque of Motor 0 
    print("Dynamixel#%d Torque Limit is:" % DXL_0, torquelimit0)
          
    dxl_comm_result1, dxl_error1 = packetHandler.write2ByteTxRx(portHandler,DXL_1,ADDR_MX_TORQUE_LIMIT,1000) # Sets Torque of Motor 0 to Max
    torquelimit1, dxl_comm_result1, dxl_error1 = packetHandler.read2ByteTxRx(portHandler,DXL_1,ADDR_MX_TORQUE_LIMIT) # Reads Torque of Motor 1
    print("Dynamixel#%d Torque Limit is:" % DXL_1, torquelimit1)
    
    dxl_comm_result0, dxl_error0 = packetHandler.write2ByteTxRx(portHandler, DXL_0, ADDR_MX_MOVE_SPEED, 0)
    dxl_comm_result1, dxl_error1 = packetHandler.write2ByteTxRx(portHandler, DXL_1, ADDR_MX_MOVE_SPEED, 0)      
    dxl_comm_result0, dxl_error0 = packetHandler.write2ByteTxRx(portHandler, DXL_0, ADDR_MX_CCW_ANG_LMT, 1023) # Writes Motor 0 to Joint Mode
    dxl_comm_result0, dxl_error0 = packetHandler.write2ByteTxRx(portHandler, DXL_0, ADDR_MX_GOAL_POSITION, int((DXL_0_MAXIMUM_POSITION_VALUE+DXL_0_MINIMUM_POSITION_VALUE)/2)) # Writes Motor 0 to DXL_HOME value
    dxl_comm_result1, dxl_error1 = packetHandler.write2ByteTxRx(portHandler, DXL_1, ADDR_MX_CCW_ANG_LMT, 1023) # Writes Motor 1 to Joint Mode
    dxl_comm_result1, dxl_error1 = packetHandler.write2ByteTxRx(portHandler, DXL_1, ADDR_MX_GOAL_POSITION, int((DXL_1_MAXIMUM_POSITION_VALUE+DXL_1_MINIMUM_POSITION_VALUE)/2)) # Writes Motor 1 to DXL_HOME value

    while True:                                 # Waits until Motors are home before proceeding
        dxl_0_present_position, dxl_comm_result0, dxl_error0 = packetHandler.read2ByteTxRx(portHandler, DXL_0, ADDR_MX_PRESENT_POSITION)
        dxl_1_present_position, dxl_comm_result1, dxl_error1 = packetHandler.read2ByteTxRx(portHandler, DXL_1, ADDR_MX_PRESENT_POSITION)
        tol = (dxl_0_present_position + dxl_1_present_position)/2
        time.sleep(1)
        if abs(dxl_0_present_position - int((DXL_0_MAXIMUM_POSITION_VALUE+DXL_0_MINIMUM_POSITION_VALUE)/2)) < 5 and abs(dxl_0_present_position - int((DXL_0_MAXIMUM_POSITION_VALUE+DXL_0_MINIMUM_POSITION_VALUE)/2)) < 5:
            break
    print('Motors have successfully started')
    print("Press any key to continue! (or press ESC to quit!)")
    if getch() == chr(0x1b):
        shut_down(portHandler,packetHandler)
    else:
        run(portHandler,packetHandler)

    
    
    
def shut_down(portHandler,packetHandler):                                # Terminates connection to motors.
    
    dxl_comm_result0, dxl_error0 = packetHandler.write2ByteTxRx(portHandler, DXL_0, ADDR_MX_MOVE_SPEED, 0)
    dxl_comm_result1, dxl_error1 = packetHandler.write2ByteTxRx(portHandler, DXL_1, ADDR_MX_MOVE_SPEED, 0)
    
    dxl_comm_result0, dxl_error0 = packetHandler.write1ByteTxRx(portHandler, DXL_0, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE) # Disable Dynamixel Torque Motor 0
    if dxl_comm_result0 != COMM_SUCCESS:        # Checks if Motor 0 disconnected properly
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result0))
    elif dxl_error0 != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error0))
        
    dxl_comm_result1, dxl_error1 = packetHandler.write1ByteTxRx(portHandler, DXL_1, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE) # Disable Dynamixel Torque Motor 1
    if dxl_comm_result1 != COMM_SUCCESS:        # Checks if Motor 1 disconnected properly
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result1))
    elif dxl_error1 != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error1))
    
    portHandler.closePort()                     # Close port
    print("Successfully closed the port")
    

    
start_up()          # Calls Startup Function 



