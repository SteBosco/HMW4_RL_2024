# Homework3_rl2024
Homework 3 for Robotics Lab 2024/2025

First build all the packages by using:

```
colcon build --packages-select aruco aruco_msgs aruco_ros rl_fra2mo_description ros2_opencv
```
In each terminal you open, source the install directory:
```
source install/setup.bash
```
# 1. Launch the Gazebo simulation and spawn the mobile robot in the world leonardo_race_field
Run the following command:
```
ros2 launch rl_fra2mo_description gazebo_fra2mo.launch.py
```

# 2. Autonomous navigation task
In the first terminal run:
```
ros2 launch rl_fra2mo_description gazebo_fra2mo.launch.py
```
In second terminal, run:
```
ros2 launch rl_fra2mo_description display_fra2mo.launch.py
```
In another terminal launch:
```
ros2 launch rl_fra2mo_description fra2mo_explore.launch.py
```
In the last terminal run:
```
ros2 run rl_fra2mo_description follow_waypoints.py 
```

# 4a-4b.  2D navigation task 
In the first terminal run:
```
ros2 launch rl_fra2mo_description gazebo_fra2mo.launch.py
```
In second terminal, run:
```
ros2 launch rl_fra2mo_description display_fra2mo.launch.py
```
In another terminal launch:
```
ros2 launch rl_fra2mo_description nav_aruco.launch.py
```
In another terminal run:
```
ros2 run rl_fra2mo_description vision_based_navigation.py
```
# 4c.  Publish the Aruco pose as TF 
In the first terminal run:
```
ros2 launch rl_fra2mo_description gazebo_fra2mo.launch.py
```
NOTE:once the robot has been spawned in the Gazebo, move it close to obstacle 9 so that it can see the Aruco Marker with the camera.

In second terminal, run:
```
ros2 launch rl_fra2mo_description nav_aruco.launch.py
```
In another terminal, to check whether the robot is actually detecting the marker, run:
```
ros2 run rqt_image_view rqt_image_view 
```
and select as topic: aruco_single/result.

In another terminal run:
```
ros2 run rl_fra2mo_description aruco_tf_publisher
```
In the last terminal, to see the transformation published by the node, run:
```
ros2 topic echo /tf
```

 NOTES:
 After running the command provided above, as soon as Gazebo opens, PRESS THE PLAY BUTTON in the lower left corner!!!


 
