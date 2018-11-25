__author__ = 'gkour'

from universe import Universe
from statistics import Stats
import printing
from config import Config


def run(msg_queue=None):
    stats = Stats()
    universe = Universe(stats)

    while universe.pass_time():
        stats.initialize_inter_epoch_stats()
        stats.accumulate_step_stats(universe)
        printing.print_step_stats(stats)
        msg_queue.put(stats)

        if universe.get_time() % Config.Batch_SIZE == 0:
            stats.accumulate_epoch_stats(universe)
            printing.print_epoch_stats(stats)



if __name__ == '__main__':
    run()