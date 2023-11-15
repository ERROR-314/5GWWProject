#! /usr/bin/env python3
# Import ROS.
import rospy
# Import the API.
from iq_gnc.py_gnc_functions import *
# To print colours (optional).
from iq_gnc.PrintColours import *


def main():
    # Initializing ROS node.
    rospy.init_node("drone_controller", anonymous=True)

    # Create an object for the API.
    drone = gnc_api()
    # Wait for FCU connection.
    drone.wait4connect()
    # Wait for the mode to be switched.
    drone.wait4start()

    # Create local reference frame.
    drone.initialize_local_frame()

    # Create local reference frame.
    drone.start_stream()

    # Request takeoff with an altitude of 3m
    #drone.takeoff(3)

    rate = rospy.Rate(1)

    # Specify some waypoints
    goals = [[0, 0, 0, 0], [5, 0, 0, -90], [5, 5, 0, 0],
             [0, 5, 0, 90], [0, 0, 0, 180], [0, 0, 0, 0]]
    i = 0

    while i < len(goals):
        x=goals[i][0]
        y=goals[i][1]
        z=goals[i][2]
        psi=goals[i][3]
        rospy.loginfo(CYELLOW2 + "Current waypoints x: {} y: {} z: {} psi: {}".format(x,y,z,psi) + CEND)
        drone.print_coords()
        rate.sleep()

        if drone.edited1_check_waypoint_reached(x,y,z,psi):
            i += 1
            rospy.loginfo(CYELLOW2 + "##############Changing waypoints now##################" + CEND)


    # Land after all waypoints is reached.
    rospy.loginfo(CGREEN2 + "All waypoints reached." + CEND)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()


