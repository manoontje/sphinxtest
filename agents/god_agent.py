import numpy as np
from agents.agent_brain import AgentBrain

from environment.actions.object_actions import RemoveObject
from environment.actions.object_actions import GrabAction
from environment.actions.door_actions import *


class God_agent(AgentBrain):

    def __init__(self):
        super().__init__()
        print("Hello, I am God")

        # duration of the current gust of wind, decreases over time
        self.wind_duration = 0
        # chance for a gust of wind
        self.wind_probability = 0.6
        # minimum and maximum possible duration for a gust of wind
        self.wind_gust_length = [1,3]


    def decide_on_action(self, state, possible_actions):
        action = None

        if self.wind_duration <= 0:
            # randomly determine if there is a new gust of wind
             p = np.random.random_sample()
             if p <= self.wind_probability:

                # randomly determine the length of the gust of wind within certain bounds
                b = self.wind_gust_length[1]
                a = self.wind_gust_length[0]
                self.wind_duration = int((b - a) * np.random.random_sample() + a)

        else:
            self.wind_duration -= 1
            action = "StirWater"

        action_kwargs = {}
        return action, action_kwargs
