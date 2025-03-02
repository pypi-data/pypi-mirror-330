"""Multiagent QuadX Hover Environment."""

from __future__ import annotations

from typing import Any, Literal

import numpy as np
from gymnasium import spaces

from PyFlyt.pz_envs.quadx_envs.ma_quadx_base_env import MAQuadXBaseEnv


class MAQuadXHoverEnv(MAQuadXBaseEnv):
    """Simple Multiagent Hover Environment.

    Actions are vp, vq, vr, T, ie: angular rates and thrust.
    The target is for each agent to not crash for the longest time possible.

    Args:
        start_pos (np.ndarray): an (num_drones x 3) numpy array specifying the starting positions of each agent.
        start_orn (np.ndarray): an (num_drones x 3) numpy array specifying the starting orientations of each agent.
        sparse_reward (bool): whether to use sparse rewards or not.
        flight_mode (int): the flight mode of all UAVs.
        flight_dome_size (float): size of the allowable flying area.
        max_duration_seconds (float): maximum simulation time of the environment.
        angle_representation (Literal["euler", "quaternion"]): can be "euler" or "quaternion".
        agent_hz (int): looprate of the agent to environment interaction.
        render_mode (None | str): can be "human" or None.

    """

    metadata = {
        "render_modes": ["human"],
        "name": "ma_quadx_hover",
    }

    def __init__(
        self,
        start_pos: np.ndarray = np.array(
            [[-1.0, -1.0, 1.0], [1.0, -1.0, 1.0], [-1.0, 1.0, 1.0], [1.0, 1.0, 1.0]]
        ),
        start_orn: np.ndarray = np.array(
            [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
        ),
        sparse_reward: bool = False,
        flight_mode: int = 0,
        flight_dome_size: float = 10.0,
        max_duration_seconds: float = 30.0,
        angle_representation: Literal["euler", "quaternion"] = "quaternion",
        agent_hz: int = 40,
        render_mode: None | str = None,
    ):
        """__init__.

        Args:
            start_pos (np.ndarray): an (num_drones x 3) numpy array specifying the starting positions of each agent.
            start_orn (np.ndarray): an (num_drones x 3) numpy array specifying the starting orientations of each agent.
            sparse_reward (bool): whether to use sparse rewards or not.
            flight_mode (int): the flight mode of all UAVs.
            flight_dome_size (float): size of the allowable flying area.
            max_duration_seconds (float): maximum simulation time of the environment.
            angle_representation (Literal["euler", "quaternion"]): can be "euler" or "quaternion".
            agent_hz (int): looprate of the agent to environment interaction.
            render_mode (None | str): can be "human" or None.

        """
        super().__init__(
            start_pos=start_pos,
            start_orn=start_orn,
            flight_mode=flight_mode,
            flight_dome_size=flight_dome_size,
            max_duration_seconds=max_duration_seconds,
            angle_representation=angle_representation,
            agent_hz=agent_hz,
            render_mode=render_mode,
        )
        self.sparse_reward = sparse_reward

        # observation space
        self._observation_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(self.combined_space.shape[0] + 3,),
            dtype=np.float64,
        )

    def observation_space(self, agent: Any = None) -> spaces.Space:
        """observation_space.

        Args:
            agent (Any): agent

        Returns:
            spaces.Space:

        """
        return self._observation_space

    def reset(
        self, seed=None, options=dict()
    ) -> tuple[dict[str, np.ndarray], dict[str, Any]]:
        """reset.

        Args:
            seed: seed to pass to the base environment.
            options: None

        """
        super().begin_reset(seed, options)
        super().end_reset(seed, options)

        observations = {
            ag: self.compute_observation_by_id(self.agent_name_mapping[ag])
            for ag in self.agents
        }
        infos = {ag: dict() for ag in self.agents}
        return observations, infos

    def compute_observation_by_id(self, agent_id: int) -> np.ndarray:
        """compute_observation_by_id.

        Args:
            agent_id (int): agent_id

        Returns:
            np.ndarray:

        """
        # get all the relevant things
        raw_state = self.compute_attitude_by_id(agent_id)
        aux_state = self.aviary.aux_state(agent_id)

        # state breakdown
        ang_vel = raw_state[0]
        ang_pos = raw_state[1]
        lin_vel = raw_state[2]
        lin_pos = raw_state[3]
        ang_vel, ang_pos, lin_vel, lin_pos, quaternion = raw_state

        # depending on angle representation, return the relevant thing
        if self.angle_representation == 0:
            return np.concatenate(
                [
                    ang_vel,
                    ang_pos,
                    lin_vel,
                    lin_pos,
                    aux_state,
                    self.past_actions[agent_id],
                    self.start_pos[agent_id],
                ],
                axis=-1,
            )
        elif self.angle_representation == 1:
            return np.concatenate(
                [
                    ang_vel,
                    quaternion,
                    lin_vel,
                    lin_pos,
                    aux_state,
                    self.past_actions[agent_id],
                    self.start_pos[agent_id],
                ],
                axis=-1,
            )
        else:
            raise AssertionError("Not supposed to end up here!")

    def compute_term_trunc_reward_info_by_id(
        self, agent_id: int
    ) -> tuple[bool, bool, float, dict[str, Any]]:
        """Computes the termination, truncation, and reward of the current timestep."""
        # initialize
        reward = 0.0
        term = False
        trunc = self.step_count > self.max_steps
        info = dict()

        # collision
        if np.any(self.aviary.contact_array[self.aviary.drones[agent_id].Id]):
            reward -= 100.0
            info["collision"] = True
            term |= True

        # exceed flight dome
        if np.linalg.norm(self.aviary.state(agent_id)[-1]) > self.flight_dome_size:
            reward -= 100.0
            info["out_of_bounds"] = True
            term |= True

        # reward
        if not self.sparse_reward:
            # distance from 0, 0, 1 hover point
            linear_distance = np.linalg.norm(
                self.aviary.state(agent_id)[-1] - self.start_pos[agent_id]
            )

            # how far are we from 0 roll pitch
            angular_distance = np.linalg.norm(self.aviary.state(agent_id)[1][:2])

            reward -= float(linear_distance + angular_distance * 0.1)
            reward += 1.0

        return term, trunc, reward, info
