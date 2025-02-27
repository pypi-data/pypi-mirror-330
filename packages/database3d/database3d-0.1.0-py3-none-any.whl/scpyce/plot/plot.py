import matplotlib
import matplotlib.pyplot as plt
import numpy as np


class Plot:

    def __init__(self, model):
        self._model = model
        self.ax = plt.axes(projection='3d')

    def show_model(self):
        bar_list = self._model.get_bars()

        for bar in bar_list:

            # Data for a three-dimensional line
            self.ax.plot3D([bar.node_a.x, bar.node_b.x], 
                    [bar.node_a.y, bar.node_b.y], 
                    [bar.node_a.z, bar.node_b.z], 
                    'gray')

    def show_displacements(self, scale = 1):
        bar_list = self._model.get_bars()

        for bar in bar_list:

            bar_displacemnts = self._model.get_bar_displacements(bar.name)
            node_a_displacemnts_factored = [result * scale for result in bar_displacemnts[0]]
            node_b_displacemnts_factored = [result * scale for result in bar_displacemnts[1]]            
            
            self.ax.plot3D([bar.node_a.x + node_a_displacemnts_factored[0], bar.node_b.x + node_b_displacemnts_factored[0]], 
                    [bar.node_a.y + node_a_displacemnts_factored[1], bar.node_b.y + node_b_displacemnts_factored[1]], 
                    [bar.node_a.z + node_a_displacemnts_factored[2], bar.node_b.z + node_b_displacemnts_factored[2]], 
                    'blue')

    def show_supports(self, /, *, show_text = False):

        supports = self._model.get_supports()

        symbol = 'X'

        for support in supports:

            if support.is_fix():
                symbol = 's'
            
            if support.is_pin():
                symbol = '^'
            
            if support.is_slider():
                symbol = 'o'
                
            self.ax.scatter(support.node.x, support.node.y, support.node.z, marker=symbol, color='black')

            if show_text:
                self.ax.text(support.node.x, support.node.y, support.node.z, str(support), color='black')

    def show_loads(self, /, *, show_text=False):

        point_loads = self._model.get_point_loads()

        for load in point_loads:

            self.ax.scatter(load.node.x, load.node.y, load.node.z, marker='o', color='red')

            if show_text:
                self.ax.text(load.node.x, load.node.y, load.node.z, str(load), color='red')

    def plot(self):

        plt.gca().set_aspect('equal', adjustable='box')
        plt.axis('off')
        plt.show()