"""Launch ADAS2019 actuators and sensors."""

import launch
from launch_ros.actions import Node
from launch.actions import LogInfo, Shutdown

# Written by ChatGPT. Ugly but works.
shutdown_initiated = False
def shutdown(context):
    global shutdown_initiated
    if not shutdown_initiated:
        shutdown_initiated = True
        return [
            LogInfo(msg = ["A node has died. Stopping everything..."]),
            Shutdown(reason='Shutting down because of node termination.')
        ]

def generate_launch_description():

    Actuator = Node(
        name = 'Actuator',
        namespace = 'adas2019',
        package = 'ros_adas2019',
        executable = 'Actuator',
        output = 'screen'
    )
    Battery = Node(
        name = 'Battery',
        namespace = 'adas2019',
        package = 'ros_adas2019',
        executable = 'Battery',
        output = 'screen'
    )
    Odometry = Node(
        name = 'Odometry',
        namespace = 'adas2019',
        package = 'ros_adas2019',
        executable = 'Odometry',
        output = 'screen',
        parameters = [{'poll_rate_hz': 80}]
    )
    Ultrasonic = Node(
        name = 'Ultrasonic',
        namespace = 'adas2019',
        package = 'ros_adas2019',
        executable = 'Ultrasonic',
        output = 'screen'
    )

    uss_side_left_tf = Node(
        name = 'uss_side_left_tf',
        namespace = 'adas2019',
        package = 'tf2_ros', 
        executable = "static_transform_publisher",
        arguments = "--x 0.255 --y 0.15 --z 0 --qx 0 --qy 0 --qz 0.7071068 --qw 0.7071068 --frame-id base_link --child-frame-id uss_side_left".split()
    )
    uss_rear_left_tf = Node(
        name = 'uss_rear_left_tf',
        namespace = 'adas2019',
        package = 'tf2_ros', 
        executable = "static_transform_publisher",
        arguments = "--x -0.08 --y 0.11 --z 0 --qx 0 --qy 0 --qz 0.9659258 --qw 0.258819 --frame-id base_link --child-frame-id uss_rear_left".split()
    )
    uss_rear_center_tf = Node(
        name = 'uss_rear_center_tf',
        namespace = 'adas2019',
        package = 'tf2_ros', 
        executable = "static_transform_publisher",
        arguments = "--x -0.1 --y 0 --z 0 --qx 0 --qy 0 --qz 1 --qw 0 --frame-id base_link --child-frame-id uss_rear_center".split()
    )
    uss_rear_right_tf = Node(
        name = 'uss_rear_right_tf',
        namespace = 'adas2019',
        package = 'tf2_ros', 
        executable = "static_transform_publisher",
        arguments = "--x -0.08 --y -0.11 --z 0 --qx 0 --qy 0 --qz 0.9659258 --qw -0.258819 --frame-id base_link --child-frame-id uss_rear_right".split()
    )
    uss_side_right_tf = Node(
        name = 'uss_side_right_tf',
        namespace = 'adas2019',
        package = 'tf2_ros',
        executable = "static_transform_publisher",
        arguments = "--x 0.255 --y -0.15 --z 0 --qx 0 --qy 0 --qz -0.7071068 --qw 0.7071068 --frame-id base_link --child-frame-id uss_side_right".split()
    )

    ld = launch.LaunchDescription([
        Actuator, Battery, Odometry, Ultrasonic,
        uss_side_left_tf, uss_rear_left_tf, uss_rear_center_tf, uss_rear_right_tf, uss_side_right_tf
        ])

    # Stop everything if one node crashes
    # also relevant: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Using-Event-Handlers.html
    ld.add_action(launch.actions.RegisterEventHandler(
        event_handler = launch.event_handlers.OnProcessExit(
            on_exit = [
                launch.actions.OpaqueFunction(function=shutdown)
            ]
        )
    ))
    return ld
