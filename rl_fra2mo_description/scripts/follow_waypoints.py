#! /usr/bin/env python3
# Copyright 2021 Samsung Research America
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

from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy
import os
from rclpy.duration import Duration
from ament_index_python.packages import get_package_share_directory
import yaml


waypoints = yaml.safe_load(
    open(os.path.join(get_package_share_directory('rl_fra2mo_description'), "config", "goal.yaml"))
)
initial_pose = yaml.safe_load(
    open(os.path.join(get_package_share_directory('rl_fra2mo_description'), "config", "initial_pose.yaml"))
)
def main():
    rclpy.init()
    navigator = BasicNavigator()
    
    #  # Set our demo's initial pose
    # init_pose = PoseStamped()
    # init_pose.header.frame_id = 'map'
    # init_pose.header.stamp = navigator.get_clock().now().to_msg()
    # init_pose.pose.position.x = initial_pose["initial_pose"]["position"]["x"]
    # init_pose.pose.position.y = initial_pose["initial_pose"]["position"]["y"]
    # init_pose.pose.position.z = initial_pose["initial_pose"]["position"]["z"]
    
    # init_pose.pose.orientation.x = initial_pose["initial_pose"]["orientation"]["x"]
    # init_pose.pose.orientation.y = initial_pose["initial_pose"]["orientation"]["y"]
    # init_pose.pose.orientation.z = initial_pose["initial_pose"]["orientation"]["z"]
    # init_pose.pose.orientation.w = initial_pose["initial_pose"]["orientation"]["w"]
    # navigator.setInitialPose(init_pose)


    def create_pose(transform):
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = navigator.get_clock().now().to_msg()
        pose.pose.position.x = transform["position"]["x"]+3
        pose.pose.position.y = transform["position"]["y"]-3.5
        pose.pose.position.z = transform["position"]["z"]
        pose.pose.orientation.x = transform["orientation"]["x"]
        pose.pose.orientation.y = transform["orientation"]["y"]
        pose.pose.orientation.z = transform["orientation"]["z"]+0.707
        pose.pose.orientation.w = transform["orientation"]["w"]-0.707
        return pose

    # Create all poses from YAML file
    all_goal_poses = list(map(create_pose, waypoints["waypoints"]))

    # Reorder the goals: Goal 3 → Goal 4 → Goal 2 → Goal 1
    reordered_goal_indices = [2, 3, 1, 0]  # Python indexing starts at 0
    goal_poses = [all_goal_poses[i] for i in reordered_goal_indices]

    # Wait for navigation to fully activate, since autostarting nav2
    navigator.waitUntilNav2Active(localizer="smoother_server")

    # Start following the waypoints
    nav_start = navigator.get_clock().now()
    navigator.followWaypoints(goal_poses)
    

    i = 0
    while not navigator.isTaskComplete():
        ################################################
        #
        # Implement some code here for your application!
        #
        ################################################

        # Do something with the feedback
        i += 1
        feedback = navigator.getFeedback()

        if feedback and i % 5 == 0:
            print('Executing current waypoint: ' +
                  str(feedback.current_waypoint + 1) + '/' + str(len(goal_poses)))
            now = navigator.get_clock().now()

            # Some navigation timeout to demo cancellation
            if now - nav_start > Duration(seconds=600):
                navigator.cancelTask()

    # Do something depending on the return code
    result = navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        print('Goal succeeded!')
    elif result == TaskResult.CANCELED:
        print('Goal was canceled!')
    elif result == TaskResult.FAILED:
        print('Goal failed!')
    else:
        print('Goal has an invalid return status!')

    # navigator.lifecycleShutdown()

    exit(0)


if __name__ == '__main__':
    main()