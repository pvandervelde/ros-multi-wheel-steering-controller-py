import math
import pytest
from typing import Mapping, List, Tuple

# locals
from .control_model import BodyState, DriveModuleState, Motion, SimpleFourWheelSteeringControlModel
from .drive_module import DriveModule
from .geometry import Point

def create_drive_modules(
    length: float = 1.0,
    width: float = 1.0,
    wheel_radius: float = 0.1,
    steering_max_velocity: float = 1.0,
    steering_min_acceleration: float = 0.1,
    steering_max_acceleration: float = 1.0,
    drive_max_velocity: float = 1.0,
    drive_min_acceleration: float = 0.1,
    drive_max_acceleration: float = 1.0) -> List[DriveModule]:
    result: List[DriveModule] = []

    right_front_drive = DriveModule(
        name="module_1",
        steering_link="steering_link_1",
        drive_link="drive_link_1",
        steering_axis_xy_position=Point(0.5 * length, -0.5 * width, 0.0),
        wheel_radius=wheel_radius,
        steering_motor_maximum_velocity=steering_max_velocity,
        steering_motor_minimum_acceleration=steering_min_acceleration,
        steering_motor_maximum_acceleration=steering_max_acceleration,
        drive_motor_maximum_velocity=drive_max_velocity,
        drive_motor_minimum_acceleration=drive_min_acceleration,
        drive_motor_maximum_acceleration=drive_max_acceleration
    )
    result.append(right_front_drive)

    left_front_drive = DriveModule(
        name="module_2",
        steering_link="steering_link_2",
        drive_link="drive_link_2",
        steering_axis_xy_position=Point(0.5 * length, 0.5 * width, 0.0),
        wheel_radius=wheel_radius,
        steering_motor_maximum_velocity=steering_max_velocity,
        steering_motor_minimum_acceleration=steering_min_acceleration,
        steering_motor_maximum_acceleration=steering_max_acceleration,
        drive_motor_maximum_velocity=drive_max_velocity,
        drive_motor_minimum_acceleration=drive_min_acceleration,
        drive_motor_maximum_acceleration=drive_max_acceleration
    )
    result.append(left_front_drive)

    left_rear_drive = DriveModule(
        name="module_3",
        steering_link="steering_link_3",
        drive_link="drive_link_3",
        steering_axis_xy_position=Point(-0.5 * length, 0.5 * width, 0.0),
        wheel_radius=wheel_radius,
        steering_motor_maximum_velocity=steering_max_velocity,
        steering_motor_minimum_acceleration=steering_min_acceleration,
        steering_motor_maximum_acceleration=steering_max_acceleration,
        drive_motor_maximum_velocity=drive_max_velocity,
        drive_motor_minimum_acceleration=drive_min_acceleration,
        drive_motor_maximum_acceleration=drive_max_acceleration
    )
    result.append(left_rear_drive)

    right_rear_drive = DriveModule(
        name="module_4",
        steering_link="steering_link_4",
        drive_link="drive_link_4",
        steering_axis_xy_position=Point(-0.5 * length, -0.5 * width, 0.0),
        wheel_radius=wheel_radius,
        steering_motor_maximum_velocity=steering_max_velocity,
        steering_motor_minimum_acceleration=steering_min_acceleration,
        steering_motor_maximum_acceleration=steering_max_acceleration,
        drive_motor_maximum_velocity=drive_max_velocity,
        drive_motor_minimum_acceleration=drive_min_acceleration,
        drive_motor_maximum_acceleration=drive_max_acceleration
    )
    result.append(right_rear_drive)

    return result

# body_motion_from_wheel_module_states

def test_should_show_forward_movement_when_modules_are_pointing_forward_with_velocity():
    drive_modules = create_drive_modules()
    controller = SimpleFourWheelSteeringControlModel(drive_modules)

    states: List[DriveModuleState] = []
    for i in range(len(drive_modules)):
        module_state = DriveModuleState(
            drive_modules[i].name,
            drive_modules[i].steering_axis_xy_position.x,
            drive_modules[i].steering_axis_xy_position.y,
            math.radians(0),
            0.0,
            1.0,
            0.0
        )
        states.append(module_state)

    motion = controller.body_motion_from_wheel_module_states(states)

    assert math.isclose(motion.linear_velocity.x, 1.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.linear_velocity.y, 0.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.linear_velocity.z, 0.0, rel_tol=1e-6, abs_tol=1e-15)

    assert math.isclose(motion.angular_velocity.x, 0.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.angular_velocity.y, 0.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.angular_velocity.z, 0.0, rel_tol=1e-6, abs_tol=1e-15)

def test_should_show_no_movement_when_modules_are_pointing_forward_without_velocity():
    drive_modules = create_drive_modules()
    controller = SimpleFourWheelSteeringControlModel(drive_modules)

    states: List[DriveModuleState] = []
    for i in range(len(drive_modules)):
        module_state = DriveModuleState(
            drive_modules[i].name,
            drive_modules[i].steering_axis_xy_position.x,
            drive_modules[i].steering_axis_xy_position.y,
            math.radians(0),
            0.0,
            0.0,
            0.0
        )
        states.append(module_state)

    motion = controller.body_motion_from_wheel_module_states(states)

    assert math.isclose(motion.linear_velocity.x, 0.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.linear_velocity.y, 0.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.linear_velocity.z, 0.0, rel_tol=1e-6, abs_tol=1e-15)

    assert math.isclose(motion.angular_velocity.x, 0.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.angular_velocity.y, 0.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.angular_velocity.z, 0.0, rel_tol=1e-6, abs_tol=1e-15)

def test_should_show_reverse_movement_when_modules_are_pointing_forward_with_negative_velocity():
    drive_modules = create_drive_modules()
    controller = SimpleFourWheelSteeringControlModel(drive_modules)

    states: List[DriveModuleState] = []
    for i in range(len(drive_modules)):
        module_state = DriveModuleState(
            drive_modules[i].name,
            drive_modules[i].steering_axis_xy_position.x,
            drive_modules[i].steering_axis_xy_position.y,
            math.radians(0),
            0.0,
            -1.0,
            0.0
        )
        states.append(module_state)

    motion = controller.body_motion_from_wheel_module_states(states)

    assert math.isclose(motion.linear_velocity.x, -1.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.linear_velocity.y, 0.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.linear_velocity.z, 0.0, rel_tol=1e-6, abs_tol=1e-15)

    assert math.isclose(motion.angular_velocity.x, 0.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.angular_velocity.y, 0.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.angular_velocity.z, 0.0, rel_tol=1e-6, abs_tol=1e-15)

def test_should_show_reverse_movement_when_modules_are_pointing_backwards_with_velocity():
    drive_modules = create_drive_modules()
    controller = SimpleFourWheelSteeringControlModel(drive_modules)

    states: List[DriveModuleState] = []
    for i in range(len(drive_modules)):
        module_state = DriveModuleState(
            drive_modules[i].name,
            drive_modules[i].steering_axis_xy_position.x,
            drive_modules[i].steering_axis_xy_position.y,
            math.radians(180),
            0.0,
            1.0,
            0.0
        )
        states.append(module_state)

    motion = controller.body_motion_from_wheel_module_states(states)

    assert math.isclose(motion.linear_velocity.x, -1.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.linear_velocity.y, 0.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.linear_velocity.z, 0.0, rel_tol=1e-6, abs_tol=1e-15)

    assert math.isclose(motion.angular_velocity.x, 0.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.angular_velocity.y, 0.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.angular_velocity.z, 0.0, rel_tol=1e-6, abs_tol=1e-15)

def test_should_show_left_sideways_movement_when_modules_are_pointing_left_with_velocity():
    drive_modules = create_drive_modules()
    controller = SimpleFourWheelSteeringControlModel(drive_modules)

    states: List[DriveModuleState] = []
    for i in range(len(drive_modules)):
        module_state = DriveModuleState(
            drive_modules[i].name,
            drive_modules[i].steering_axis_xy_position.x,
            drive_modules[i].steering_axis_xy_position.y,
            math.radians(90),
            0.0,
            1.0,
            0.0
        )
        states.append(module_state)

    motion = controller.body_motion_from_wheel_module_states(states)

    assert math.isclose(motion.linear_velocity.x, 0.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.linear_velocity.y, 1.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.linear_velocity.z, 0.0, rel_tol=1e-6, abs_tol=1e-15)

    assert math.isclose(motion.angular_velocity.x, 0.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.angular_velocity.y, 0.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.angular_velocity.z, 0.0, rel_tol=1e-6, abs_tol=1e-15)

def test_should_show_right_sideways_movement_when_modules_are_pointing_left_with_velocity():
    drive_modules = create_drive_modules()
    controller = SimpleFourWheelSteeringControlModel(drive_modules)

    states: List[DriveModuleState] = []
    for i in range(len(drive_modules)):
        module_state = DriveModuleState(
            drive_modules[i].name,
            drive_modules[i].steering_axis_xy_position.x,
            drive_modules[i].steering_axis_xy_position.y,
            math.radians(270),
            0.0,
            1.0,
            0.0
        )
        states.append(module_state)

    motion = controller.body_motion_from_wheel_module_states(states)

    assert math.isclose(motion.linear_velocity.x, 0.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.linear_velocity.y, -1.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.linear_velocity.z, 0.0, rel_tol=1e-6, abs_tol=1e-15)

    assert math.isclose(motion.angular_velocity.x, 0.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.angular_velocity.y, 0.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.angular_velocity.z, 0.0, rel_tol=1e-6, abs_tol=1e-15)

def test_should_show_left_diagonal_movement_when_modules_are_pointing_left_diagonal_with_velocity():
    drive_modules = create_drive_modules()
    controller = SimpleFourWheelSteeringControlModel(drive_modules)

    states: List[DriveModuleState] = []
    for i in range(len(drive_modules)):
        module_state = DriveModuleState(
            drive_modules[i].name,
            drive_modules[i].steering_axis_xy_position.x,
            drive_modules[i].steering_axis_xy_position.y,
            math.radians(45),
            0.0,
            1.0,
            0.0
        )
        states.append(module_state)

    motion = controller.body_motion_from_wheel_module_states(states)

    assert math.isclose(motion.linear_velocity.x, math.sqrt(0.5), rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.linear_velocity.y, math.sqrt(0.5), rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.linear_velocity.z, 0.0, rel_tol=1e-6, abs_tol=1e-15)

    assert math.isclose(motion.angular_velocity.x, 0.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.angular_velocity.y, 0.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.angular_velocity.z, 0.0, rel_tol=1e-6, abs_tol=1e-15)

def test_should_show_right_diagonal_movement_when_modules_are_pointing_angled_with_velocity():
    drive_modules = create_drive_modules()
    controller = SimpleFourWheelSteeringControlModel(drive_modules)

    states: List[DriveModuleState] = []
    for i in range(len(drive_modules)):
        module_state = DriveModuleState(
            drive_modules[i].name,
            drive_modules[i].steering_axis_xy_position.x,
            drive_modules[i].steering_axis_xy_position.y,
            math.radians(315),
            0.0,
            1.0,
            0.0
        )
        states.append(module_state)

    motion = controller.body_motion_from_wheel_module_states(states)

    assert math.isclose(motion.linear_velocity.x, math.sqrt(0.5), rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.linear_velocity.y, -math.sqrt(0.5), rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.linear_velocity.z, 0.0, rel_tol=1e-6, abs_tol=1e-15)

    assert math.isclose(motion.angular_velocity.x, 0.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.angular_velocity.y, 0.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.angular_velocity.z, 0.0, rel_tol=1e-6, abs_tol=1e-15)

def test_should_show_pure_rotation_movement_when_modules_are_pointing_left_diagonal_with_velocity():
    drive_modules = create_drive_modules(1.0, 1.0)
    controller = SimpleFourWheelSteeringControlModel(drive_modules)

    states: List[DriveModuleState] = []
    for i in range(len(drive_modules)):
        module_state = DriveModuleState(
            drive_modules[i].name,
            drive_modules[i].steering_axis_xy_position.x,
            drive_modules[i].steering_axis_xy_position.y,
            math.radians(45 + i * 90),
            0.0,
            math.sqrt(0.5),
            0.0
        )
        states.append(module_state)

    motion = controller.body_motion_from_wheel_module_states(states)

    assert math.isclose(motion.linear_velocity.x, 0.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.linear_velocity.y, 0.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.linear_velocity.z, 0.0, rel_tol=1e-6, abs_tol=1e-15)

    assert math.isclose(motion.angular_velocity.x, 0.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.angular_velocity.y, 0.0, rel_tol=1e-6, abs_tol=1e-15)
    assert math.isclose(motion.angular_velocity.z, 1.0, rel_tol=1e-6, abs_tol=1e-15)

def test_should_show_translation_and_rotation_movement_when_modules_are_angled_with_velocity():
    pytest.fail("not implemented yet")

def test_should_show_translation_movement_when__one_module_is_slightly_offset():
    pytest.fail("not implemented yet")

# state_of_wheel_modules_from_body_motion

def test_should_have_parallel_forward_wheels_with_forward_velocity_when_forward_motion():
    drive_modules = create_drive_modules()
    controller = SimpleFourWheelSteeringControlModel(drive_modules)

    motion = Motion(1.0, 0.0, 0.0)

    states: List[DriveModuleState] = []
    for i in range(len(drive_modules)):
        module_state = DriveModuleState(
            drive_modules[i].name,
            drive_modules[i].steering_axis_xy_position.x,
            drive_modules[i].steering_axis_xy_position.y,
            math.radians(45),
            0.0,
            0.0,
            0.0
        )
        states.append(module_state)

    proposed_states = controller.state_of_wheel_modules_from_body_motion(states, motion)

    assert len(proposed_states) == len(drive_modules)

    for i in range(len(proposed_states)):
        module_state = proposed_states[i]

        assert math.isclose(module_state.forward_steering_angle, 0.0, rel_tol=1e-6, abs_tol=1e-15)
        assert math.isclose(module_state.forward_drive_velocity, 1.0, rel_tol=1e-6, abs_tol=1e-15)

        assert math.isclose(module_state.reverse_steering_angle, math.pi, rel_tol=1e-6, abs_tol=1e-15)
        assert math.isclose(module_state.reverse_drive_velocity, -1.0, rel_tol=1e-6, abs_tol=1e-15)

def test_should_have_parallel_forward_wheels_with_legal_forward_velocity_when_excessive_forward_motion():
    drive_modules = create_drive_modules(drive_max_velocity=1.0)
    controller = SimpleFourWheelSteeringControlModel(drive_modules)

    motion = Motion(2.0, 0.0, 0.0)

    states: List[DriveModuleState] = []
    for i in range(len(drive_modules)):
        module_state = DriveModuleState(
            drive_modules[i].name,
            drive_modules[i].steering_axis_xy_position.x,
            drive_modules[i].steering_axis_xy_position.y,
            math.radians(45),
            0.0,
            0.0,
            0.0
        )
        states.append(module_state)

    proposed_states = controller.state_of_wheel_modules_from_body_motion(states, motion)

    assert len(proposed_states) == len(drive_modules)

    for i in range(len(proposed_states)):
        module_state = proposed_states[i]

        assert math.isclose(module_state.forward_steering_angle, 0.0, rel_tol=1e-6, abs_tol=1e-15)
        assert math.isclose(module_state.forward_drive_velocity, 1.0, rel_tol=1e-6, abs_tol=1e-15)

        assert math.isclose(module_state.reverse_steering_angle, math.pi, rel_tol=1e-6, abs_tol=1e-15)
        assert math.isclose(module_state.reverse_drive_velocity, -1.0, rel_tol=1e-6, abs_tol=1e-15)

def test_should_have_parallel_forward_wheels_with_reverse_velocity_when_backward_motion():
    drive_modules = create_drive_modules(1.0, 1.0)
    controller = SimpleFourWheelSteeringControlModel(drive_modules)

    motion = Motion(-1.0, 0.0, 0.0)

    states: List[DriveModuleState] = []
    for i in range(len(drive_modules)):
        module_state = DriveModuleState(
            drive_modules[i].name,
            drive_modules[i].steering_axis_xy_position.x,
            drive_modules[i].steering_axis_xy_position.y,
            math.radians(45),
            0.0,
            0.0,
            0.0
        )
        states.append(module_state)

    proposed_states = controller.state_of_wheel_modules_from_body_motion(states, motion)

    assert len(proposed_states) == len(drive_modules)

    for i in range(len(proposed_states)):
        module_state = proposed_states[i]

        assert math.isclose(module_state.forward_steering_angle, math.pi, rel_tol=1e-6, abs_tol=1e-15)
        assert math.isclose(module_state.forward_drive_velocity, 1.0, rel_tol=1e-6, abs_tol=1e-15)

        assert math.isclose(module_state.reverse_steering_angle, 0.0, rel_tol=1e-6, abs_tol=1e-15)
        assert math.isclose(module_state.reverse_drive_velocity, -1.0, rel_tol=1e-6, abs_tol=1e-15)

def test_should_have_parallel_left_sideways_wheels_with_forward_velocity_when_sideways_motion():
    drive_modules = create_drive_modules(1.0, 1.0)
    controller = SimpleFourWheelSteeringControlModel(drive_modules)

    motion = Motion(0.0, 1.0, 0.0)

    states: List[DriveModuleState] = []
    for i in range(len(drive_modules)):
        module_state = DriveModuleState(
            drive_modules[i].name,
            drive_modules[i].steering_axis_xy_position.x,
            drive_modules[i].steering_axis_xy_position.y,
            math.radians(45),
            0.0,
            0.0,
            0.0
        )
        states.append(module_state)

    proposed_states = controller.state_of_wheel_modules_from_body_motion(states, motion)

    assert len(proposed_states) == len(drive_modules)

    for i in range(len(proposed_states)):
        module_state = proposed_states[i]

        assert math.isclose(module_state.forward_steering_angle, math.radians(90), rel_tol=1e-6, abs_tol=1e-15)
        assert math.isclose(module_state.forward_drive_velocity, 1.0, rel_tol=1e-6, abs_tol=1e-15)

        assert math.isclose(module_state.reverse_steering_angle, math.radians(270), rel_tol=1e-6, abs_tol=1e-15)
        assert math.isclose(module_state.reverse_drive_velocity, -1.0, rel_tol=1e-6, abs_tol=1e-15)

def test_should_have_parallel_right_sideways_wheels_with_forward_velocity_when_sideways_motion():
    drive_modules = create_drive_modules(1.0, 1.0)
    controller = SimpleFourWheelSteeringControlModel(drive_modules)

    motion = Motion(0.0, -1.0, 0.0)

    states: List[DriveModuleState] = []
    for i in range(len(drive_modules)):
        module_state = DriveModuleState(
            drive_modules[i].name,
            drive_modules[i].steering_axis_xy_position.x,
            drive_modules[i].steering_axis_xy_position.y,
            math.radians(45),
            0.0,
            0.0,
            0.0
        )
        states.append(module_state)

    proposed_states = controller.state_of_wheel_modules_from_body_motion(states, motion)

    assert len(proposed_states) == len(drive_modules)

    for i in range(len(proposed_states)):
        module_state = proposed_states[i]

        assert math.isclose(module_state.forward_steering_angle, math.radians(270), rel_tol=1e-6, abs_tol=1e-15)
        assert math.isclose(module_state.forward_drive_velocity, 1.0, rel_tol=1e-6, abs_tol=1e-15)

        assert math.isclose(module_state.reverse_steering_angle, math.radians(90), rel_tol=1e-6, abs_tol=1e-15)
        assert math.isclose(module_state.reverse_drive_velocity, -1.0, rel_tol=1e-6, abs_tol=1e-15)

def test_should_have_parallel_diagonal_wheels_with_forward_velocity_when_diagonal_motion():
    drive_modules = create_drive_modules(1.0, 1.0)
    controller = SimpleFourWheelSteeringControlModel(drive_modules)

    motion = Motion(1.0, 1.0, 0.0)

    states: List[DriveModuleState] = []
    for i in range(len(drive_modules)):
        module_state = DriveModuleState(
            drive_modules[i].name,
            drive_modules[i].steering_axis_xy_position.x,
            drive_modules[i].steering_axis_xy_position.y,
            math.radians(90),
            0.0,
            0.0,
            0.0
        )
        states.append(module_state)

    proposed_states = controller.state_of_wheel_modules_from_body_motion(states, motion)

    assert len(proposed_states) == len(drive_modules)

    for i in range(len(proposed_states)):
        module_state = proposed_states[i]

        assert math.isclose(module_state.forward_steering_angle, math.radians(45), rel_tol=1e-6, abs_tol=1e-15)
        assert math.isclose(module_state.forward_drive_velocity, 1.0, rel_tol=1e-6, abs_tol=1e-15)

        assert math.isclose(module_state.reverse_steering_angle, math.radians(225), rel_tol=1e-6, abs_tol=1e-15)
        assert math.isclose(module_state.reverse_drive_velocity, -1.0, rel_tol=1e-6, abs_tol=1e-15)

def test_should_have_angled_wheels_with_forward_velocity_when_pure_rotation():
    drive_modules = create_drive_modules(1.0, 1.0)
    controller = SimpleFourWheelSteeringControlModel(drive_modules)

    motion = Motion(0.0, 0.0, 1.0)

    states: List[DriveModuleState] = []
    for i in range(len(drive_modules)):
        module_state = DriveModuleState(
            drive_modules[i].name,
            drive_modules[i].steering_axis_xy_position.x,
            drive_modules[i].steering_axis_xy_position.y,
            math.radians(0),
            0.0,
            0.0,
            0.0
        )
        states.append(module_state)

    proposed_states = controller.state_of_wheel_modules_from_body_motion(states, motion)

    assert len(proposed_states) == len(drive_modules)

    for i in range(len(proposed_states)):
        module_state = proposed_states[i]

        assert math.isclose(module_state.forward_steering_angle, math.radians(45 + i * 90), rel_tol=1e-6, abs_tol=1e-15)
        assert math.isclose(module_state.forward_drive_velocity, math.sqrt(0.5), rel_tol=1e-6, abs_tol=1e-15)

        reversing_angle = 45 + i * 90 + 180
        if reversing_angle >= 360:
            reversing_angle -= 360
        assert math.isclose(module_state.reverse_steering_angle, math.radians(reversing_angle), rel_tol=1e-6, abs_tol=1e-15)
        assert math.isclose(module_state.reverse_drive_velocity, -math.sqrt(0.5), rel_tol=1e-6, abs_tol=1e-15)

def test_should_have_angled_wheels_with_individual_velocities_when_rotation_and_translation():
    pytest.fail("not implemented yet")

def test_should_not_move_wheels_when_zero_motion():
    drive_modules = create_drive_modules()
    controller = SimpleFourWheelSteeringControlModel(drive_modules)

    motion = Motion(0.0, 0.0, 0.0)

    states: List[DriveModuleState] = []
    for i in range(len(drive_modules)):
        module_state = DriveModuleState(
            drive_modules[i].name,
            drive_modules[i].steering_axis_xy_position.x,
            drive_modules[i].steering_axis_xy_position.y,
            math.radians(45),
            0.0,
            0.0,
            0.0
        )
        states.append(module_state)

    proposed_states = controller.state_of_wheel_modules_from_body_motion(states, motion)

    assert len(proposed_states) == len(drive_modules)

    for i in range(len(proposed_states)):
        module_state = proposed_states[i]

        assert math.isclose(module_state.forward_steering_angle, math.radians(45), rel_tol=1e-6, abs_tol=1e-15)
        assert math.isclose(module_state.forward_drive_velocity, 0.0, rel_tol=1e-6, abs_tol=1e-15)

        assert math.isclose(module_state.reverse_steering_angle, math.radians(225), rel_tol=1e-6, abs_tol=1e-15)
        assert math.isclose(module_state.reverse_drive_velocity, 0.0, rel_tol=1e-6, abs_tol=1e-15)

def test_should_not_move_wheels_when_stopping():
    drive_modules = create_drive_modules()
    controller = SimpleFourWheelSteeringControlModel(drive_modules)

    motion = Motion(0.0, 0.0, 0.0)

    states: List[DriveModuleState] = []
    for i in range(len(drive_modules)):
        module_state = DriveModuleState(
            drive_modules[i].name,
            drive_modules[i].steering_axis_xy_position.x,
            drive_modules[i].steering_axis_xy_position.y,
            math.radians(45 + i * 90),
            0.0,
            math.sqrt(0.5),
            0.0
        )
        states.append(module_state)

    proposed_states = controller.state_of_wheel_modules_from_body_motion(states, motion)

    assert len(proposed_states) == len(drive_modules)

    for i in range(len(proposed_states)):
        module_state = proposed_states[i]

        assert math.isclose(module_state.forward_steering_angle, math.radians(45 + i * 90), rel_tol=1e-6, abs_tol=1e-15)
        assert math.isclose(module_state.forward_drive_velocity, 0.0, rel_tol=1e-6, abs_tol=1e-15)

        reversing_angle = 45 + i * 90 + 180
        if reversing_angle >= 360:
            reversing_angle -= 360
        assert math.isclose(module_state.reverse_steering_angle, math.radians(reversing_angle), rel_tol=1e-6, abs_tol=1e-15)
        assert math.isclose(module_state.reverse_drive_velocity, 0.0, rel_tol=1e-6, abs_tol=1e-15)