from hand_shaker.msg import ShakeHandAction, ShakeHandGoal, ShakeHandActionGoal

import rsb
import logging
import time
import rospy
import sys
import signal


class RsbServer():

    #cleanup after SIGINT
    def signal_handler(self, signal, frame):
        print("\nkilling rsbserver")
        self.listener.deactivate
        print("killing node")
        rospy.signal_shutdown("hs_bridge done")
        sys.exit(0)

    def handle(self, event):
        goal = ShakeHandActionGoal()

        print("------------- received data -------------")
        print("Received event: \n %s \n" % event)

        #add correct group_name
        if event.data == 'left':
            goal.goal.group_name = '\'left_arm\''
        if event.data == 'right':
            goal.goal.group_name = '\'right_arm\''


        print("Publishing goal: \n %s \n" % goal)

        #publish goal
        pub.publish(goal)

        print("------------- published successfully -------------")


    def __init__(self, pub, scope):
        logging.basicConfig()

        #configure listener and handler
        self.listener = rsb.createListener(scope)
        self.listener.addHandler(self.handle)

        #setup signalhandler
        signal.signal(signal.SIGINT, self.signal_handler)

        try:
            while True:
                time.sleep(1)
        finally:
            print("\nkilling rsbserver")
            self.listener.deactivate
            print("killing node")
            rospy.signal_shutdown("hs_bridge done")


if __name__ == '__main__':
    #publisher for hand_shaker goal
    pub = rospy.Publisher('/hand_shaker/goal', ShakeHandActionGoal, queue_size=10)

    #init node
    rospy.init_node('hs_bridge')

    #specify rsb scope
    scope = "/hand_shaker"

    #create rsbserver with hand_shaker publisher and given scope
    rsb = RsbServer(pub, scope)

    #keep script alive until node is killed
    rospy.spin()
