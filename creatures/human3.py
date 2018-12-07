__author__ = 'gkour'

from config import ConfigBiology, ConfigBrain
from brains.brain_dqn_pytorch import BrainDQN
import utils
from creatures.human import Human
from evolution import DNA


class Human3(Human):
    _master_brain = None
    Fitrah = [0, 0, 0, 0, 0, 0, 0]

    def __init__(self, universe, id, dna, age=0, energy=ConfigBiology.INITIAL_ENERGY, parents=None):
        super(Human3, self).__init__(universe, id, dna, age, energy, parents)
        self._brain = self.get_master_brain()
        # self.new_born()

    def get_master_brain(self):
        if Human3._master_brain is None:
            Human3._master_brain = BrainDQN(observation_shape=tuple(self.observation_shape()),
                                            num_actions=self.num_actions(), gamma=ConfigBrain.BASE_GAMMA)
            Human3._master_brain.load_model(self.model_path())
            return Human3._master_brain
        return Human3._master_brain

    @staticmethod
    def get_race():
        return Human3

    @staticmethod
    def race_name():
        return 'Human3'

    @staticmethod
    def race_basic_dna():
        return DNA(ConfigBiology.BASE_MEMORY_SIZE,
                   ConfigBrain.BASE_LEARNING_RATE,
                   ConfigBrain.BASE_HIDDEN_LAYER_SIZE,
                   ConfigBiology.BASE_LEARN_FREQ,
                   ConfigBiology.BASE_LIFE_EXPECTANCY,
                   ConfigBrain.BASE_GAMMA,
                   Human3.race_fitrah())

    @staticmethod
    def race_fitrah():
        return utils.softmax(Human3.Fitrah, len(Human3.get_actions()))

    @staticmethod
    def self_race_enemy():
        return False

    def model_path(self):
        return './models/'+self.race_name()