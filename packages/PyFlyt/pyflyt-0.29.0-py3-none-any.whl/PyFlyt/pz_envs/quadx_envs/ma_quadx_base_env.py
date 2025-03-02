"""Base Multiagent QuadX Environment."""

from __future__ import annotations

from typing import Any, Sequence

import numpy as np
import pybullet as p
from gymnasium import Space, spaces
from pettingzoo import ParallelEnv

from PyFlyt.core import Aviary


class MAQuadXBaseEnv(ParallelEnv):
    """MAQuadXBaseEnv."""

    metadata = dict(render_modes="human")

    def __init__(
        self,
        start_pos: np.ndarray = np.array(
            [[-1.0, -1.0, 1.0], [1.0, -1.0, 1.0], [-1.0, 1.0, 1.0], [1.0, 1.0, 1.0]]
        ),
        start_orn: np.ndarray = np.array(
            [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
        ),
        flight_mode: int = 0,
        flight_dome_size: float = 10.0,
        max_duration_seconds: float = 10.0,
        angle_representation: str = "euler",
        agent_hz: int = 40,
        render_mode: None | str = None,
    ):
        """__init__.

        Args:
            start_pos (np.ndarray): start_pos
            start_orn (np.ndarray): start_orn
            flight_mode (int): flight_mode
            flight_dome_size (float): flight_dome_size
            max_duration_seconds (float): max_duration_seconds
            angle_representation (str): angle_representation
            agent_hz (int): agent_hz
            render_mode (None | str): render_mode

        """
        if 120 % agent_hz != 0:
            lowest = int(120 / (int(120 / agent_hz) + 1))
            highest = int(120 / int(120 / agent_hz))
            raise AssertionError(
                f"`agent_hz` must be round denominator of 120, try {lowest} or {highest}."
            )

        if render_mode is not None:
            assert (
                render_mode in self.metadata["render_modes"]
            ), f"Invalid render mode {render_mode}, only {self.metadata['render_modes']} allowed."
        self.render_mode = render_mode is not None

        """SPACES"""
        # attitude size increases by 1 for quaternion
        if angle_representation == "euler":
            attitude_shape = 12
        elif angle_representation == "quaternion":
            attitude_shape = 13
        else:
            raise AssertionError(
                f"angle_representation must be either `euler` or `quaternion`, not {angle_representation}"
            )

        # action space
        angular_rate_limit = np.pi
        thrust_limit = 0.8
        high = np.array(
            [
                angular_rate_limit,
                angular_rate_limit,
                angular_rate_limit,
                thrust_limit,
            ]
        )
        low = np.array(
            [
                -angular_rate_limit,
                -angular_rate_limit,
                -angular_rate_limit,
                0.0,
            ]
        )
        self._action_space = spaces.Box(low=low, high=high, dtype=np.float64)

        # observation space
        self.auxiliary_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(4,), dtype=np.float64
        )
        self.combined_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(
                attitude_shape
                + self.auxiliary_space.shape[0]
                + self.action_space(None).shape[0],  # pyright: ignore
            ),
            dtype=np.float64,
        )

        """ENVIRONMENT CONSTANTS"""
        # check the start_pos shapes
        assert (
            len(start_pos.shape) == 2
        ), f"Expected `start_pos` to be of shape [num_agents, 3], got {start_pos.shape}."
        assert (
            start_pos.shape[-1] == 3
        ), f"Expected `start_pos` to be of shape [num_agents, 3], got {start_pos.shape}."
        assert (
            start_pos.shape == start_orn.shape
        ), f"Expected `start_pos` to be of shape [num_agents, 3], got {start_pos.shape}."
        self.start_pos = start_pos
        self.start_orn = start_orn

        self.flight_mode = flight_mode
        self.flight_dome_size = flight_dome_size
        self.max_steps = int(agent_hz * max_duration_seconds)
        self.env_step_ratio = int(120 / agent_hz)
        if angle_representation == "euler":
            self.angle_representation = 0
        elif angle_representation == "quaternion":
            self.angle_representation = 1

        # select agents
        self.num_possible_agents = len(start_pos)
        self.possible_agents = [
            "uav_" + str(r) for r in range(self.num_possible_agents)
        ]
        self.agent_name_mapping = dict(
            zip(self.possible_agents, list(range(len(self.possible_agents))))
        )

        """RUNTIME PARAMETERS"""
        self.current_actions = np.zeros(
            (
                self.num_possible_agents,
                *self.action_space(None).shape,
            )
        )
        self.past_actions = np.zeros(
            (
                self.num_possible_agents,
                *self.action_space(None).shape,
            )
        )

    def observation_space(self, agent: Any = None) -> Space:
        """observation_space.

        Args:
            agent (Any): agent

        Returns:
            Space:

        """
        raise NotImplementedError

    def action_space(self, agent: Any = None) -> spaces.Box:
        """action_space.

        Args:
            agent (Any): agent

        Returns:
            spaces.Box:

        """
        return self._action_space

    def close(self) -> None:
        """Close."""
        if hasattr(self, "aviary"):
            self.aviary.disconnect()

    def reset(
        self, seed: None | int = None, options: None | dict[str, Any] = dict()
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """reset.

        Args:
            seed (None | int): seed
            options (None | dict[str, Any]): options

        Returns:
            tuple[dict[str, Any], dict[str, Any]]:

        """
        raise NotImplementedError

    def begin_reset(
        self,
        seed: None | int = None,
        options: None | dict[str, Any] = dict(),
        drone_options: None | dict[str, Any] | Sequence[dict[str, Any]] = dict(),
    ) -> None:
        """The first half of the reset function.

        Args:
            seed (None | int): seed
            options (None | dict[str, Any]): options
            drone_options (None | dict[str, Any] | Sequence[dict[str, Any]]): drone_options

        Returns:
            None:

        """
        # if we already have an env, disconnect from it
        if hasattr(self, "aviary"):
            self.aviary.disconnect()
        self.step_count = 0
        self.agents = self.possible_agents[:]

        # rebuild the environment
        self.aviary = Aviary(
            start_pos=self.start_pos,
            start_orn=self.start_orn,
            drone_type="quadx",
            render=bool(self.render_mode),
            drone_options=drone_options,
            seed=seed,
        )

    def end_reset(
        self, seed: None | int = None, options: None | dict[str, Any] = dict()
    ) -> None:
        """The tailing half of the reset function."""
        # register all new collision bodies
        self.aviary.register_all_new_bodies()

        # set flight mode
        self.aviary.set_mode(self.flight_mode)

        # wait for env to stabilize
        for _ in range(10):
            self.aviary.step()
        self.update_states()

    def update_states(self) -> None:
        """Helper method to be called once after the internal aviary has stepped.

        Args:
            agent_id (int): agent_id

        Returns:
            Any:

        """
        pass

    def compute_attitude_by_id(
        self, agent_id: int
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """state.

        This returns the base attitude for the drone.
        - ang_vel (vector of 3 values)
        - ang_pos (vector of 3 values)
        - lin_vel (vector of 3 values)
        - lin_pos (vector of 3 values)
        - quaternion (vector of 4 values)
        """
        raw_state = self.aviary.state(agent_id)

        # state breakdown
        ang_vel = raw_state[0]
        ang_pos = raw_state[1]
        lin_vel = raw_state[2]
        lin_pos = raw_state[3]

        # quaternion angles
        quaternion = p.getQuaternionFromEuler(ang_pos)

        return ang_vel, ang_pos, lin_vel, lin_pos, quaternion

    def compute_observation_by_id(self, agent_id: int) -> Any:
        """compute_observation_by_id.

        Args:
            agent_id (int): agent_id

        Returns:
            Any:

        """
        raise NotImplementedError

    def compute_term_trunc_reward_info_by_id(
        self, agent_id: int
    ) -> tuple[bool, bool, float, dict[str, Any]]:
        """compute_term_trunc_reward_info_by_id.

        Args:
            agent_id (int): agent_id

        Returns:
            Tuple[bool, bool, float, dict[str, Any]]:

        """
        raise NotImplementedError

    def step(self, actions: dict[str, np.ndarray]) -> tuple[
        dict[str, Any],
        dict[str, float],
        dict[str, bool],
        dict[str, bool],
        dict[str, dict[str, Any]],
    ]:
        """step.

        Args:
            actions (dict[str, np.ndarray]): actions

        Returns:
            tuple[dict[str, Any], dict[str, float], dict[str, bool], dict[str, bool], dict[str, dict[str, Any]]]:

        """
        # copy over the past actions
        self.past_actions = self.current_actions.copy()

        # set the new actions and send to aviary
        self.current_actions *= 0.0
        for k, v in actions.items():
            self.current_actions[self.agent_name_mapping[k]] = v
        self.aviary.set_all_setpoints(self.current_actions)

        # observation and rewards dictionary
        observations = dict()
        terminations = {k: False for k in self.agents}
        truncations = {k: False for k in self.agents}
        rewards = {k: 0.0 for k in self.agents}
        infos = {k: dict() for k in self.agents}

        # step enough times for one RL step
        for _ in range(self.env_step_ratio):
            self.aviary.step()
            self.update_states()

            # update reward, term, trunc, for each agent
            # TODO: make it so this doesn't have to be computed every aviary step
            for ag in self.agents:
                ag_id = self.agent_name_mapping[ag]

                # compute term trunc reward
                term, trunc, rew, info = self.compute_term_trunc_reward_info_by_id(
                    ag_id
                )
                terminations[ag] |= term
                truncations[ag] |= trunc
                rewards[ag] += rew
                infos[ag].update(info)

                # compute observations
                observations[ag] = self.compute_observation_by_id(ag_id)

        # increment step count and cull dead agents for the next round
        self.step_count += 1
        self.agents = [
            agent
            for agent in self.agents
            if not (terminations[agent] or truncations[agent])
        ]

        return observations, rewards, terminations, truncations, infos
