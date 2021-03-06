#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# Copyright 2017 ROBOTIS CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

# Author: Ryu Woon Jung (Leon)

#
# *********     Read and Write Example      *********
#
#
# Available DXL model on this example : All models using Protocol 1.0
# This example is tested with a DXL MX-28, and an USB2DYNAMIXEL
# Be sure that DXL MX properties are already set as %% ID : 1 / Baudnum : 34 (Baudrate : 57600)
#

import os
import threading

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

# Control table address
ADDR_MX_TORQUE_ENABLE      = 24               # Control table address is different in Dynamixel model
ADDR_MX_GOAL_POSITION      = 30
ADDR_MX_PRESENT_POSITION   = 36
ADDR_MX_MOVE_SPEED = 32
ADDR_MX_CCW_ANG_LMT = 8
ADDR_MX_PRESENT_SPEED = 38
ADDR_MX_TORQUE_LIMIT = 34



# Protocol version
PROTOCOL_VERSION            = 1.0               # See which protocol version is used in the Dynamixel

# Default setting
DXL_1                       =  1     # Dynamixel ID : 1
DXL_0                       =  0
BAUDRATE                    = 2000000            # Dynamixel default baudrate : 57600
DEVICENAME                  = '/dev/tty.usbserial-FT62AGHG'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL_MINIMUM_POSITION_VALUE  = 0           # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE  = 1023            # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_MOVING_STATUS_THRESHOLD = 20                # Dynamixel moving status threshold

index = 0
dxl_goal_position = [DXL_MINIMUM_POSITION_VALUE, DXL_MAXIMUM_POSITION_VALUE]         # Goal position

def TEMPmoveDXL0((portHandler,packetHandler)):

    while True:
        try:
            pos1, dxl_comm_result0, dxl_error0 = packetHandler.read2ByteTxRx(portHandler, DXL_1, ADDR_MX_PRESENT_POSITION)
        except Exception:
            print("Position out of measureable range")
            dxl_comm_result0, dxl_error0 = packetHandler.write2ByteTxRx(portHandler, DXL_1, ADDR_MX_CCW_ANG_LMT, 1023)
            dxl_comm_result0, dxl_error0 = packetHandler.write2ByteTxRx(portHandler, DXL_0, ADDR_MX_GOAL_POSITION, 0)
            dxl_comm_result0, dxl_error0 = packetHandler.write2ByteTxRx(portHandler, DXL_1, ADDR_MX_CCW_ANG_LMT, 0)
            pos1 = 0
        if abs(pos1-0)<5:
            dxl_comm_result0, dxl_error0 = packetHandler.write2ByteTxRx(portHandler, DXL_1, ADDR_MX_GOAL_POSITION, 1023)
        else:
            dxl_comm_result0, dxl_error0 = packetHandler.write2ByteTxRx(portHandler, DXL_1, ADDR_MX_GOAL_POSITION, 0)


def start_up():
    portHandler = PortHandler(DEVICENAME)

    # Initialize PacketHandler instance
    # Set the protocol version
    # Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
    packetHandler = PacketHandler(PROTOCOL_VERSION)

    # Open port
    if portHandler.openPort():
        print("Succeeded to open the port")
    else:
        print("Failed to open the port")
        print("Press any key to terminate...")
        getch()
        quit()

    # Set port baudrate
    if portHandler.setBaudRate(BAUDRATE):
        print("Succeeded to change the baudrate")
    else:
        print("Failed to change the baudrate")
        print("Press any key to terminate...")
        getch()
        quit()

    dxl_comm_result1, dxl_error1 = packetHandler.write1ByteTxRx(portHandler, DXL_1, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
    dxl_comm_result0, dxl_error0 = packetHandler.write1ByteTxRx(portHandler, DXL_0, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)

    if dxl_comm_result1 != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result0))
    elif dxl_error1 != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error0))
    else:
        print("Dynamixel has been successfully connected 00??")

    dxl_comm_result0, dxl_error0 = packetHandler.write2ByteTxRx(portHandler,DXL_0,ADDR_MX_TORQUE_LIMIT,1023)
    dxl_comm_result0, dxl_error0 = packetHandler.write2ByteTxRx(portHandler,DXL_1,ADDR_MX_TORQUE_LIMIT,1023)
    torquelimit, dxl_comm_result0, dxl_error0 = packetHandler.read2ByteTxRx(portHandler,DXL_0,ADDR_MX_TORQUE_LIMIT)
    dxl_comm_result0, dxl_error0 = packetHandler.write2ByteTxRx(portHandler, DXL_0, ADDR_MX_CCW_ANG_LMT, 1023)
    print("torquelimt: ", torquelimit)
    return portHandler,packetHandler

portHandler,packetHandler = start_up()
x = threading.Thread(target=TEMPmoveDXL0(), args=(portHandler,packetHandler))


# while 1:
#     dxl_comm_result0, dxl_error0 = packetHandler.write2ByteTxRx(portHandler, DXL_0, ADDR_MX_CCW_ANG_LMT, 1023)
#     dxl_comm_result0, dxl_error0 = packetHandler.write2ByteTxRx(portHandler, DXL_1, ADDR_MX_CCW_ANG_LMT, 1023)
#     dxl_comm_result0, dxl_error0 = packetHandler.write2ByteTxRx(portHandler, DXL_0, ADDR_MX_GOAL_POSITION, 0)
#     dxl_comm_result0, dxl_error0 = packetHandler.write2ByteTxRx(portHandler, DXL_1, ADDR_MX_GOAL_POSITION, 0)
#
#     speed = 0
#     print("Press any key to continue! (or press ESC to quit!)")
#     if getch() == chr(0x1b):
#         break
#     dxl_comm_result0, dxl_error0 = packetHandler.write2ByteTxRx(portHandler, DXL_1, ADDR_MX_CCW_ANG_LMT,0)
#     dxl_comm_result0, dxl_error0 = packetHandler.write2ByteTxRx(portHandler, DXL_0, ADDR_MX_GOAL_POSITION, 1023)
#     try:
#         pos1, dxl_comm_result0, dxl_error0 = packetHandler.read2ByteTxRx(portHandler, DXL_1, ADDR_MX_PRESENT_POSITION)
#     except Exception:
#         print("Position out of measureable range")
#         dxl_comm_result0, dxl_error0 = packetHandler.write2ByteTxRx(portHandler, DXL_1, ADDR_MX_CCW_ANG_LMT, 1023)
#         dxl_comm_result0, dxl_error0 = packetHandler.write2ByteTxRx(portHandler, DXL_0, ADDR_MX_GOAL_POSITION, 0)
#         dxl_comm_result0, dxl_error0 = packetHandler.write2ByteTxRx(portHandler, DXL_1, ADDR_MX_CCW_ANG_LMT, 0)
#         pos1 = 0



    # while abs(pos1-1023)>5:
    #     currentSpeed0,dxl_comm_result0, dxl_error0 = packetHandler.read2ByteTxRx(portHandler,DXL_0,ADDR_MX_PRESENT_SPEED)
    #     currentSpeed1, dxl_comm_result0, dxl_error0 = packetHandler.read2ByteTxRx(portHandler, DXL_1, ADDR_MX_PRESENT_SPEED)
    #     pos0, dxl_comm_result0, dxl_error0 = packetHandler.read2ByteTxRx(portHandler, DXL_0, ADDR_MX_PRESENT_POSITION)
    #     pos1, dxl_comm_result0, dxl_error0 = packetHandler.read2ByteTxRx(portHandler, DXL_1, ADDR_MX_PRESENT_POSITION)
    #     dx = pos0-pos1
    #     ds = int(.6*(currentSpeed0-currentSpeed1))
    #     speed = ds + dx + currentSpeed0
    #     if(speed>1023):
    #         speed=1023
    #     dxl_comm_result0, dxl_error0 = packetHandler.write2ByteTxRx(portHandler, DXL_1, ADDR_MX_MOVE_SPEED,speed)
    #     print('Motor 0 speed: ', currentSpeed0)
    #     print('Motor 1 speed: ', currentSpeed1)
    #     print(pos1)
    #     try:
    #         pos1, dxl_comm_result0, dxl_error0 = packetHandler.read2ByteTxRx(portHandler, DXL_1, ADDR_MX_PRESENT_POSITION)
    #     except Exception:
    #         print("Position out of measureable range")

    # dxl_comm_result0, dxl_error0 = packetHandler.write2ByteTxRx(portHandler, DXL_1, ADDR_MX_MOVE_SPEED, 0)
    # print("Any key to resart esc to exit")
    # if getch() == chr(0x1b):
    #     break
    # else:
    #     pass






# Disable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_1, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

# Close port
portHandler.closePort()
