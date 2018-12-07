__author__ = 'gkour'

from creatures.creature import Creature
from creature_actions import Actions
from config import ConfigBiology, ConfigBrain
from brains.brain_dqn import BrainDQN
import utils
from evolution import DNA


class Human(Creature):
    _master_brain = None
    Fitrah = [0, 0, 0, 0, 0, 0, 0]

    def __init__(self, universe, id, dna, age=0, energy=ConfigBiology.INITIAL_ENERGY, parents=None):
        super(Human, self).__init__(universe, id, dna, age, energy, parents)
        self._brain = self.get_master_brain()
        # self.new_born()

    def get_master_brain(self):
        if Human._master_brain is None:
            Human._master_brain = BrainDQN(lr=ConfigBrain.BASE_LEARNING_RATE,
                                           observation_shape=self.observation_shape(),
                                           num_actions=self.num_actions(),
                                           h_size=ConfigBrain.BASE_HIDDEN_LAYER_SIZE,
                                           gamma=ConfigBrain.BASE_GAMMA,
                                           scope='master' + self.race_name())
            return Human._master_brain
        return Human._master_brain

    @staticmethod
    def race_basic_dna():
        return DNA(ConfigBiology.BASE_MEMORY_SIZE,
                   ConfigBrain.BASE_LEARNING_RATE,
                   ConfigBrain.BASE_HIDDEN_LAYER_SIZE,
                   ConfigBiology.BASE_LEARN_FREQ,
                   ConfigBiology.BASE_LIFE_EXPECTANCY,
                   ConfigBrain.BASE_GAMMA,
                   Human.race_fitrah())

    @staticmethod
    def get_actions():
        return [Actions.LEFT, Actions.RIGHT, Actions.UP, Actions.DOWN, Actions.EAT, Actions.MATE, Actions.FIGHT]

    @staticmethod
    def get_race():
        return Human

    @staticmethod
    def race_name():
        return 'Human'

    @staticmethod
    def race_fitrah():
        return utils.softmax(Human.Fitrah, len(Human.get_actions()))

    @staticmethod
    def self_race_enemy():
        return False

    def decide(self, state):
        eps = max(ConfigBrain.BASE_EPSILON,
                 1 - (self._age / (self.learning_frequency() * ConfigBiology.MATURITY_AGE)))
        brain_actions_prob = self._brain.think(state)
        action_prob = utils.softmax(brain_actions_prob, temprature=len(self.fitrah()))
        decision = utils.epsilon_greedy(eps, action_prob)
        return decision

    def new_born(self):
        if self.get_parent() is None:
            return
        self._memory = self.get_parent().get_memory()
