import matplotlib.pyplot as plt
import random
from code.classes import grid
from matplotlib.font_manager import FontProperties
import time
import os

def plot_grid(grid_file, chip_number, netlist_number, cost, algorithm):
    """ 
    Plots the 3d graph 
    """
    
    list_of_nets = grid_file.get_list_of_routes()
    size = grid_file.get_size()

    x = []
    y = []

    coordinates_gates = grid_file.get_coordinates_gates()

    # Put all x and y coordinates in list
    for item in coordinates_gates:
        x_coordinate = int(item[0])
        y_coordinate = int(item[1])

        x.append(x_coordinate)
        y.append(y_coordinate)

    # Set all the variables up
    ax = plt.axes(projection="3d")
    ax.set_xlim3d(0, size)
    ax.set_ylim3d(0, size)
    ax.set_zlim3d(0, 7)
    x_points = x
    y_points = y
    z_points = 0

    # Initiate the graph with gates
    ax.scatter3D(x_points, y_points, z_points, cmap='hsv', color="r")

    # Get every line in the graph
    for count in range(len(list_of_nets)):
        nets = list_of_nets[count]
        
        # Get random color
        r = random.random()
        b = random.random()
        g = random.random()
        color = (r, g, b)
        
        x = []
        y = []
        z = [] 
        
        # Form the lines
        for item in nets:
            a = item.get_coordinates_from()
            b = item.get_coordinates_to()

            x.extend([a[0], b[0]])
            y.extend([a[1], b[1]])
            z.extend([a[2], b[2]])

        nets = list(nets)
        coordinates_gate_a = nets[0].get_coordinates_from()
        coordinates_gate_b = nets[-1].get_coordinates_to()
        gate_a = grid_file.get_current_gate_number(coordinates_gate_a[0], coordinates_gate_a[1])
        gate_b = grid_file.get_current_gate_number(coordinates_gate_b[0], coordinates_gate_b[1])

        # Plot the line
        ax.plot3D(x, y, z, color=color, label=f"{gate_a} to {gate_b}")

    # Set labels
    ax.set_xlabel('X', fontsize = 10)
    ax.set_ylabel('Y', fontsize = 10)
    ax.set_zlabel('Z', fontsize = 10)

    # Set up legend and title
    fontP = FontProperties()
    fontP.set_size('small')
    plt.legend(bbox_to_anchor=(1.0,0.5), loc="center left", ncol=1, prop=fontP)
    plt.title(f"Chip {chip_number}  | Netlist: {netlist_number}  | Cost: {cost}")
    plt.show()