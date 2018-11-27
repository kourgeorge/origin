__author__ = 'gkour'

import matplotlib.pyplot as plt
import numpy as np
from creature_actions import Actions
from config import Config


class Dashboard:
    def __init__(self):

        self._fig = plt.figure(figsize=(9, 5), dpi=120, facecolor='w')
        self._fig.canvas.set_window_title('Origin Dashboard')
        self._fig_pop = self._fig.add_subplot(221)
        self._fig_pop.set_ylabel('Population Size')
        self._fig_age = self._fig.add_subplot(222)
        self._fig_age.set_ylabel('Avg Population Age')
        self._line_pop, = self._fig_pop.plot([], [], '-')
        self._line_age, = self._fig_age.plot([], [], '-')

        self._fig_creatures_loc = self._fig.add_axes([0.1, 0.1, 0.2, 0.3])
        self._fig_creatures_loc.yaxis.set_major_locator(plt.NullLocator())
        self._fig_creatures_loc.xaxis.set_major_locator(plt.NullLocator())
        self._fig_food_loc = self._fig.add_axes([0.31, 0.1, 0.2, 0.3])
        self._fig_food_loc.yaxis.set_major_locator(plt.NullLocator())
        self._fig_food_loc.xaxis.set_major_locator(plt.NullLocator())
        self._fig_action = self._fig.add_subplot(224)

    def update_epoch_dash(self, epoch_stats_df):
        if epoch_stats_df is None or epoch_stats_df.empty:
            return

    def update_step_dash(self, step_stats_df):
        if step_stats_df is None or step_stats_df.empty:
            return
        self._line_pop.set_xdata(step_stats_df['Time'])
        self._line_pop.set_ydata(step_stats_df['Population'])

        self._line_age.set_xdata(step_stats_df['Time'])
        self._line_age.set_ydata(step_stats_df['Age'])

        self._fig.canvas.draw()
        self._fig.canvas.flush_events()
        self._fig_pop.relim()
        self._fig_pop.autoscale_view()
        self._fig_age.relim()
        self._fig_age.autoscale_view()

        ## Creatures Dist
        creatures_dist = np.asarray(step_stats_df['CreaturesDist'].iloc[-1])
        self._fig_creatures_loc.clear()
        self._fig_creatures_loc.imshow(creatures_dist, cmap="Purples", aspect="auto", vmin=0, vmax=50)
        self._fig_creatures_loc.set_title('Creatures Location')
        self._fig_creatures_loc.yaxis.set_major_locator(plt.NullLocator())
        self._fig_creatures_loc.xaxis.set_major_locator(plt.NullLocator())


        ## Food Supply
        food_supply = np.asarray(step_stats_df['FoodDist'].iloc[-1])
        self._fig_food_loc.clear()
        self._fig_food_loc.imshow(food_supply, cmap="Greens", aspect="auto", vmin=0, vmax=100)
        self._fig_food_loc.set_title('Food Dist')
        self._fig_food_loc.yaxis.set_major_locator(plt.NullLocator())
        self._fig_food_loc.xaxis.set_major_locator(plt.NullLocator())

        ## Action Dist Pie
        actions_dist = np.mean(step_stats_df['ActionDist'].tail(Config.Batch_SIZE).values, axis=0)
        self._fig_action.clear()
        self._fig_action.pie(actions_dist, labels=Actions.get_available_action_str(),
                             startangle=90, autopct='%1.1f%%')

    def get_figure(self):
        return self._fig
