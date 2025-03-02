"""Base PyFlyt Environment for the Rocket model using the Gymnasim API."""

from __future__ import annotations

from typing import Any, Literal

import gymnasium
import numpy as np
import pybullet as p
from gymnasium import spaces

from PyFlyt.core.aviary import Aviary
from PyFlyt.core.utils.compile_helpers import check_numpy


class RocketBaseEnv(gymnasium.Env):
    """Base PyFlyt Environment for the Rocket model using the Gymnasim API."""

    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 30}

    def __init__(
        self,
        start_pos: np.ndarray = np.array([[0.0, 0.0, 10.0]]),
        start_orn: np.ndarray = np.array([[0.0, 0.0, 0.0]]),
        ceiling: float = np.inf,
        max_displacement: float = np.inf,
        max_duration_seconds: float = 60.0,
        angle_representation: Literal["euler", "quaternion"] = "quaternion",
        agent_hz: int = 30,
        render_mode: None | Literal["human", "rgb_array"] = None,
        render_resolution: tuple[int, int] = (480, 480),
    ):
        """__init__.

        Args:
            start_pos (np.ndarray): start_pos
            start_orn (np.ndarray): start_orn
            drone_type (str): drone_type
            drone_model (str): drone_model
            ceiling (float): ceiling
            max_displacement (float): max_displacement
            max_duration_seconds (float): max_duration_seconds
            angle_representation (Literal["euler", "quaternion"]): angle_representation
            agent_hz (int): agent_hz
            render_mode (None | Literal["human", "rgb_array"]): render_mode
            render_resolution (tuple[int, int]): render_resolution

        """
        if 120 % agent_hz != 0:
            lowest = int(120 / (int(120 / agent_hz) + 1))
            highest = int(120 / int(120 / agent_hz))
            raise ValueError(
                f"`agent_hz` must be round denominator of 120, try {lowest} or {highest}."
            )

        if render_mode and render_mode not in self.metadata["render_modes"]:
            raise ValueError(
                f"Invalid render mode {render_mode}, only {self.metadata['render_modes']} allowed."
            )
        self.render_mode = render_mode
        self.render_resolution = render_resolution

        """GYMNASIUM STUFF"""
        # attitude size increases by 1 for quaternion
        if angle_representation == "euler":
            attitude_shape = 12
        elif angle_representation == "quaternion":
            attitude_shape = 13
        else:
            raise ValueError(
                f"angle_representation must be either `euler` or `quaternion`, not {angle_representation}"
            )

        self.attitude_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(attitude_shape,), dtype=np.float64
        )
        self.auxiliary_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(9,), dtype=np.float64
        )

        # force_x, force_y, roll, ignition, throttle, booster_gimbal_1, booster_gimbal_2
        finlet_setpoint_limit = 1.0
        throttle_limit = 1.0
        booster_gimbal_limit = 1.0
        high = np.array(
            [
                finlet_setpoint_limit,
                finlet_setpoint_limit,
                finlet_setpoint_limit,
                1.0,
                throttle_limit,
                booster_gimbal_limit,
                booster_gimbal_limit,
            ]
        )
        low = np.array(
            [
                -finlet_setpoint_limit,
                -finlet_setpoint_limit,
                -finlet_setpoint_limit,
                0.0,
                0.0,
                -booster_gimbal_limit,
                -booster_gimbal_limit,
            ]
        )
        self.action_space = spaces.Box(low=low, high=high, dtype=np.float64)

        # the whole implicit state space = attitude + previous action + auxiliary information
        self.combined_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(
                attitude_shape
                + self.action_space.shape[0]
                + self.auxiliary_space.shape[0],
            ),
            dtype=np.float64,
        )

        """ ENVIRONMENT CONSTANTS """
        self.start_pos = start_pos
        self.start_orn = start_orn
        self.ceiling = ceiling
        self.max_displacement = max_displacement
        self.max_steps = int(agent_hz * max_duration_seconds)
        self.env_step_ratio = int(120 / agent_hz)
        if angle_representation == "euler":
            self.angle_representation = 0
        elif angle_representation == "quaternion":
            self.angle_representation = 1

    def reset(
        self, *, seed: None | int = None, options: None | dict[str, Any] = dict()
    ):
        """Resets the environment.

        Args:
            seed: int
            options: None

        """
        raise NotImplementedError

    def close(self):
        """Disconnects the internal Aviary."""
        # if we already have an env, disconnect from it
        if hasattr(self, "env"):
            self.env.disconnect()

    def begin_reset(
        self,
        seed: None | int = None,
        options: None | dict[str, Any] = dict(),
        drone_options: None | dict[str, Any] = dict(),
    ):
        """The first half of the reset function."""
        super().reset(seed=seed)

        # if we already have an env, disconnect from it
        if hasattr(self, "env"):
            self.env.disconnect()

        self.step_count = 0
        self.termination = False
        self.truncation = False
        self.state = None
        self.action = np.zeros((7,))
        self.reward = 0.0
        self.info = {}
        self.info["out_of_bounds"] = False
        self.info["fatal_collision"] = False
        self.info["env_complete"] = False

        # some tracking variables
        self.throttle_state = False
        self.ignition_state = False
        self.previous_throttle_state = False
        self.previous_ignition_state = False

        # for rendering
        self.previous_render_ignition_state = False
        self.ignition_color = np.array([1.0, 0.3, 0.3, 0.8])

        # need to handle Nones
        if options is None:
            options = dict()
        if drone_options is None:
            drone_options = dict()

        # override the spawn location if needed
        if "randomize_drop" in options and options["randomize_drop"]:
            spawn_range = self.max_displacement * 0.1
            start_xy = self.np_random.uniform(-spawn_range, spawn_range, size=(2,))
            start_z = self.np_random.uniform(self.ceiling * 0.8, self.ceiling * 0.9)
            self.start_pos = np.array([*start_xy, start_z])[None, ...]

            # random rotation + make kind of upright
            self.start_orn = self.np_random.uniform(-0.3, 0.3, size=(3,))[None, ...]

        # camera handling
        drone_options["use_camera"] = drone_options.get("use_camera", False) or bool(
            self.render_mode
        )
        drone_options["camera_fps"] = int(120 / self.env_step_ratio)

        # init env
        self.env = Aviary(
            start_pos=self.start_pos,
            start_orn=self.start_orn,
            drone_type="rocket",
            render=self.render_mode == "human",
            drone_options=drone_options,
            np_random=self.np_random,
        )

        # add the random velocities to our base
        start_ang_vel = np.array([0.0, 0.0, 0.0])
        start_lin_vel = np.array([0.0, 0.0, 0.0])
        if options.get("randoimize_drop", False):
            start_lin_vel += self.np_random.uniform(-5.0, 5.0, size=(3,))
            start_ang_vel += self.np_random.uniform(-0.5, 0.5, size=(3,))

        # speed up the drop if required
        if options.get("accelerate_drop", False):
            start_lin_vel += np.array([0.0, 0.0, -100.0])

        self.env.resetBaseVelocity(self.env.drones[0].Id, start_lin_vel, start_ang_vel)

        if self.render_mode == "human":
            self.camera_parameters = self.env.getDebugVisualizerCamera()

    def end_reset(
        self, seed: None | int = None, options: None | dict[str, Any] = dict()
    ):
        """The tailing half of the reset function."""
        # register all new collision bodies
        self.env.register_all_new_bodies()

        # set flight mode
        self.env.set_mode(0)

        # wait for env to stabilize
        for _ in range(10):
            self.env.step()

        self.compute_state()

    def compute_state(self):
        """Computes the state of the Rocket."""
        raise NotImplementedError

    def compute_auxiliary(self):
        """This returns the auxiliary state form the drone."""
        # rollover tracked values
        self.previous_throttle_state = self.throttle_state
        self.previous_ignition_state = self.ignition_state

        # get auxiliary info
        aux = self.env.aux_state(0)

        # update tracked values
        self.throttle_state = aux[-4]
        self.ignition_state = aux[-5]

        return aux

    def compute_attitude(self):
        """state.

        This returns the base attitude for the drone.
        - ang_vel (vector of 3 values)
        - ang_pos (vector of 3/4 values)
        - lin_vel (vector of 3 values)
        - lin_pos (vector of 3 values)
        - previous_action (vector of 4 values)
        """
        raw_state = self.env.state(0)

        # state breakdown
        ang_vel = raw_state[0]
        ang_pos = raw_state[1]
        lin_vel = raw_state[2]
        lin_pos = raw_state[3]

        # quaternion angles
        quaternion = p.getQuaternionFromEuler(ang_pos)

        return ang_vel, ang_pos, lin_vel, lin_pos, quaternion

    def compute_term_trunc_reward(self):
        """compute_term_trunc_reward."""
        raise NotImplementedError

    def compute_base_term_trunc_reward(
        self, collision_ignore_mask: np.ndarray | list[int] = []
    ):
        """compute_base_term_trunc_reward.

        Args:
            collision_ignore_mask (np.ndarray | list[int]): list of ids to ignore collisions between

        """
        # exceed step count
        if self.step_count > self.max_steps:
            self.truncation = self.truncation or True

        # mask collisions if any
        collision_array = self.env.contact_array.copy()
        for i, j in zip(collision_ignore_mask[1:], collision_ignore_mask[:-1]):
            collision_array[i, j] = False
            collision_array[j, i] = False

        # fatal collision or below ground
        if np.any(collision_array) or self.env.state(0)[-1, -1] < 0.0:
            self.info["fatal_collision"] = True
            self.termination |= True

        # exceed flight dome
        if (
            np.linalg.norm(self.env.state(0)[-1, :2]) > self.max_displacement
            or self.env.state(0)[-1, 2] > self.ceiling
        ):
            self.info["out_of_bounds"] = True
            self.termination |= True

    def step(self, action: np.ndarray):
        """Steps the environment.

        Args:
            action (np.ndarray): action

        Returns:
            state, reward, termination, truncation, info

        """
        # unsqueeze the action to be usable in aviary
        self.action = action.copy()

        # reset the reward and set the action
        self.reward = 0.0
        self.env.set_setpoint(0, action)

        # step through env, the internal env updates a few steps before the outer env
        for _ in range(self.env_step_ratio):
            # if we've already ended, don't continue
            if self.termination or self.truncation:
                break

            self.env.step()

            # compute state and done
            self.compute_state()
            self.compute_term_trunc_reward()

        # increment step count
        self.step_count += 1

        # render the booster ignition
        if self.render_mode and (
            self.ignition_state != self.previous_render_ignition_state
        ):
            self.previous_render_ignition_state = self.ignition_state
            self.env.changeVisualShape(
                self.env.drones[0].Id,
                9,
                rgbaColor=self.ignition_color,
            )

        return self.state, self.reward, self.termination, self.truncation, self.info

    def render(self):
        """Render."""
        check_numpy()
        if self.render_mode is None:
            raise ValueError(
                "Please set `render_mode='human'` or `render_mode='rgb_array'` in init to use this function."
            )

        _, _, rgbaImg, _, _ = self.env.getCameraImage(
            width=self.render_resolution[1],
            height=self.render_resolution[0],
            viewMatrix=self.env.drones[0].camera.view_mat,
            projectionMatrix=self.env.drones[0].camera.proj_mat,
        )

        rgbaImg = np.asarray(rgbaImg, dtype=np.uint8).reshape(
            self.render_resolution[0], self.render_resolution[1], -1
        )

        return rgbaImg
