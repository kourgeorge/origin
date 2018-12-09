__author__ = 'gkour'

from simulator import Simulator, SimState
from visualization.dashboard import Dashboard
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, Scale
import matplotlib.pyplot as plt
from config import ConfigPhysics
import sys
from queue import Queue


plt.style.use('seaborn-paper')
LARGE_FONT = ("Verdana", 12)


class OriginGUI:

    def __init__(self, master, *args, **kwargs):
        tk.Tk.wm_title(master, "Project Origin")
        # tk.Tk.iconbitmap(self,default="")

        self.master = master
        self.msg_queue = Queue()

        container = tk.Frame(master)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self._simulation_page = SimulationPage(container, master, self.msg_queue)
        self._simulation_page.grid(row=0, column=0, sticky="nsew")
        self._simulation_page.tkraise()

    def refresh_data(self, msg):
        self._simulation_page.refresh_data(msg)

    def process_incoming_msg(self):
        """Handle all messages currently in the queue, if any."""
        while self.msg_queue.qsize():
            try:
                self.refresh_data(self.msg_queue.get(0))
            except Exception as exp:
                print(str(exp))
                pass


class SimulationPage(tk.Frame):

    def __init__(self, parent, controller, queue):
        self._dashboard = Dashboard()
        self.controller = controller
        self.simulator = Simulator(queue)

        tk.Frame.__init__(self, parent, bg='white')
        title_label = tk.Label(self, text="Project Origin Dashboard", font=LARGE_FONT, foreground='blue', bg='white')
        title_label.pack(pady=10, padx=10)

        self.s = ttk.Style()
        self.s.theme_use('vista')

        self.status_label = tk.Label(self, text="Simulator ready", bg='white')
        self.status_label.pack(pady=10, padx=10)

        self.start_sim_btn = ttk.Button(self, text="Start Simulation",
                                        command=lambda: self.start_simulation())

        self.start_sim_btn.pack()
        self.food_creature_scale = Scale(self, from_=0, to=1, orient=tk.HORIZONTAL, resolution=0.1, bg='white',
                                         command=lambda x: self.set_food_creature_ratio(x))
        self.food_creature_scale.set(ConfigPhysics.FOOD_CREATURE_RATIO)
        self.food_creature_scale.pack()

        dash_fig = self._dashboard.get_figure()

        canvas = FigureCanvasTkAgg(dash_fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        controller.protocol("WM_DELETE_WINDOW", self.close_window)

    def close_window(self):
        self.simulator.stop()
        self.status_label['text'] = "Simulation Stopping!"
        self.controller.destroy()
        sys.exit()

    def refresh_data(self, msg):
        if type(msg) == SimState:
            print(msg.value)
            if msg == SimState.INITIALIZING:
                self.start_sim_btn['state'] = tk.DISABLED
            if msg == SimState.STOPPED:
                self.start_sim_btn['state'] = tk.ACTIVE
            self.status_label['text'] = str(msg.value)
        else:
            self._dashboard.update_step_dash(msg.step_stats_df)
            self._dashboard.update_epoch_dash(msg.epoch_stats_df)

    def start_simulation(self):
        self.simulator.run_in_thread()

    @staticmethod
    def set_food_creature_ratio(new):
        ConfigPhysics.FOOD_CREATURE_RATIO = float(new)
