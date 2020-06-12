import matplotlib.pyplot as plt
from code.function import plot_grid as pg
from code.classes import gate
from code.classes import grid
from code.classes import net
from code.algorithms import random_solve
from code.algorithms import greedy as gr
import csv
import random
from mpl_toolkits import mplot3d

if __name__ == '__main__':
    # Read multiple files
    chip_number = "0"
    netlistfile = "netlist_3.csv"
    size = 7
    test_grid = grid.Grid(f"data/chip_{chip_number}/print_{chip_number}.csv", f"data/chip_{chip_number}/{netlistfile}", size)

    output = open("chip2netlist9.csv", "a")
    output.write("versie,cost,counter\n")

    # --------------------------------------------Perform the desired algoritm--------------------------------------------------------------
    
    # random_solve.random_solve3D(test_grid)

    # greedy = gr.Greedy(test_grid)
    # greedy.run(output)

    # pop_greedy = gr.PopulationGreedy(test_grid)
    # pop_greedy.run(output)

    # len_greedy = gr.LengthGreedy(test_grid)
    # len_greedy.run(output)

    # cost = test_grid.cost_of_route()

    # output.write(f"chip_{0}_net_{1},{cost},{counter}")
    # output.close()

    # Plot the graph
    # pg.plot_grid(test_grid)

    # --------------------------While loops to run till solution
    
    
    reset = False
    counter = 0

    while counter != 1:
        
        while not reset:
            test_grid = grid.Grid(f"data/chip_{chip_number}/print_{chip_number}.csv", f"data/chip_{chip_number}/{netlistfile}", size)
            greedy = gr.Greedy(test_grid)
            reset = greedy.run(output)

        cost = test_grid.cost_of_route()
        output.write(f"Greedy,{cost},{counter}\n")
        counter += 1
        reset = False
        
    output.write("\n\n")
    print("normal greedy done")
    pg.plot_grid(test_grid)



    reset = False
    counter = 0
    
    while counter != 50:

        while not reset:
            test_grid = grid.Grid(f"data/chip_{chip_number}/print_{chip_number}.csv", f"data/chip_{chip_number}/{netlistfile}", size)
            pop_greedy = gr.PopulationGreedy(test_grid)
            reset = pop_greedy.run(output)

        cost = test_grid.cost_of_route()
        output.write(f"GreedyPopulation,{cost},{counter}\n")
        counter += 1
        reset = False

    output.write("\n\n")
    print("population klaar")


    reset = False
    counter = 0

    while counter != 50:

        while not reset:
            test_grid = grid.Grid(f"data/chip_{chip_number}/print_{chip_number}.csv", f"data/chip_{chip_number}/{netlistfile}", size)
            len_greedy = gr.LengthGreedy(test_grid)
            reset = len_greedy.run(output)

        cost = test_grid.cost_of_route()
        output.write(f"GreedyLength,{cost},{counter}\n")
        counter += 1
        reset = False

    print("korste lengte eerst klaar")

    output.close()

    