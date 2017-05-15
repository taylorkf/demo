# -*- coding: utf-8 -*-
"""
Created on Mon May 15 14:48:09 2017

@author: Taylor
"""
import sys
import yaml
from move_base_msgs.msg import MoveBaseActionGoal, MoveBaseActionResult
from hsrb_interface import Robot
import rospy
import actionlib


def reachedGoal(state):
    return state == 3
    


def inGripper():
    #check if something in gripper
    print("Checking my gripper")
    return True

def speak():
    #command to speak
    print("I am speaking")

def toTable(pose, client):
    #send command to navigate
    print("I am navigating to the table")
    msg = MoveBaseActionGoal()
    msg.goal.target_pose.header.frame_od = 'odom'
    msg.goal.target_pose.header.stamp = rospy.Time.now()
    msg.goal.target_pose.pose.position.x = pose[0]
    msg.goal.target_pose.pose.position.y = pose[1]
    msg.goal.target_pose.pose.position.z = pose[2]
    msg.goal.target_pose.pose.orientation.x = pose[3]
    msg.goal.target_pose.pose.orientation.y = pose[4]
    msg.goal.target_pose.pose.orientation.z = pose[5]
    msg.goal.target_pose.pose.orientation.w = pose[6]
    client.send_goal(msg)
    client.wait_for_result()
    return client.get_state()
    
def toTrash(pose, client):
    #send command to navigate
    print("I am navigating to the trash can")
    msg = MoveBaseActionGoal()
    msg.goal.target_pose.header.frame_od = 'odom'
    msg.goal.target_pose.header.stamp = rospy.Time.now()
    msg.goal.target_pose.pose.position.x = pose[0]
    msg.goal.target_pose.pose.position.y = pose[1]
    msg.goal.target_pose.pose.position.z = pose[2]
    msg.goal.target_pose.pose.orientation.x = pose[3]
    msg.goal.target_pose.pose.orientation.y = pose[4]
    msg.goal.target_pose.pose.orientation.z = pose[5]
    msg.goal.target_pose.pose.orientation.w = pose[6]
    client.send_goal(msg)
    client.wait_for_result()
    return client.get_state()


    
def pickUp():
    #send command to pick up
    print("I am picking up an object")
    
def putDown():
    #send command to drop object
    print("I am dropping an object")
    
def main():
    table_pos = None
    trash_pos = None
    #get file with pose data
    file_name = sys.argv[1]
    with open(file_name, 'r') as f:
        pos_file = yaml.load(f)
        trash_pos = pos_file["trash"]
        table_pos = pos_file["table"]

    client = actionlib.SimpleActionClient('move_base', MoveBaseActionGoal)

    client.wait_for_server()
    
    speak()
    try:
        while True:
            state = toTable(table_pos, client)
            while not succeeded(state):
                state = toTable(table_pos, client)
                
            pickUp()
            while(not inGripper()):
                pickUp()
                
            state = toTrash(trash_pos, client)
            while not succeeded(state):
                state = toTrash(trash_pos, client)
                
            putDown()
            
    except KeyboardInterrupt:
        pass
    
    
if __name__ == "__main__":
    main()