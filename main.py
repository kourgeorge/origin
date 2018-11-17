from universe import Universe
from creature import Creature
from config import Config
import numpy as np
import log


def main():
    universe = Universe()

    while universe.pass_time():

        if universe.num_creatures() == 0:
            return

        current_time = universe.get_time()
        universe.give_food(Config.ConfigPhysics.NUM_FATHERS)

        print(str(current_time) + ' - Population: ' + str(universe.num_creatures()), end='\t - ')
        print('IDs:' + str(Creature.counter), end='\t - ')
        print('Mean age: ' + str(np.round(np.mean([creature.age() for creature in universe.get_all_creatures()]))),
              end='\t - ')
        print('Mean Max age: ' + str(
            np.round(np.mean([creature.max_age() for creature in universe.get_all_creatures()]))), end='\t - ')
        print('Mean Hidden Layer: ' + str(
            np.round(np.mean([creature.brain_hidden_layer() for creature in universe.get_all_creatures()]))), end='\t - ')
        print('Mean Learn Freq: ' + str(
            np.round(np.mean([creature.learning_frequency() for creature in universe.get_all_creatures()]))),
              end='\t - ')
        print('Mean Vision range: ' + str(
            np.round(np.mean([creature.vision_range() for creature in universe.get_all_creatures()]))),
              end='\t - ')
        print('Death Cause [Fa Fi E]: ' + str(log.death_cause))
        log.death_cause = np.zeros_like(log.death_cause)

        if current_time % 10 == 0:
            # print(universe.space(), end='\t')
            print('Food Supply: ' + str(universe.get_food_distribution()))
            print('Action Dist [LREMF]: ' + str(np.round(np.array(log.action_log) / sum(log.action_log), 2)))
            # energy = [creature.energy() for creature in universe.get_all_creatures()]
            # print(np.histogram(energy))

            log.action_log = np.zeros_like(log.action_log)

        # if (len(universe.get_all_creatures())) == 1:
        #    print(universe.get_all_creatures()[0].dna())


if __name__ == '__main__':
    main()
