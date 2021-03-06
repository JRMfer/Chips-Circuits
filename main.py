import matplotlib.pyplot as plt
from code.function import plot_grid as pg
from code.classes import gate
from code.classes import grid
from code.classes import net
from code.algorithms import random_solve as rs
from code.algorithms import greedy as gr
from code.algorithms import astar as ast
from code.algorithms import simannealing as siman
import csv
import random

if __name__ == "__main__":
    # Declare global variables
    chip_number = float('inf')
    netlist_number = float('inf')
    algorithm = float('inf')
    annealing = float('inf')
    size = 17

    # Request user input: chip number
    while chip_number != "0" and chip_number != "1" and chip_number != "2":
        chip_number = input("Welk chipnumber wilt u testen? 0, 1 of 2?    ")

    # Request user input: netlist number
    if chip_number == "0":
        while netlist_number != "1" and netlist_number != "2" and netlist_number != "3": 
            netlist_number = input("Welke netlist wilt u gebruiken? 1, 2 of 3?   ")
            size = 7
    elif chip_number == "1":
        while netlist_number != "4" and netlist_number != "5" and netlist_number != "6": 
            netlist_number = input("Welke netlist wilt u gebruiken? 4, 5 of 6?   ")  
    elif chip_number == "2":
        while netlist_number != "7" and netlist_number != "8" and netlist_number != "9": 
            netlist_number = input("Welke netlist wilt u gebruiken? 7, 8 of 9?   ")

    # Request user input: algorithm
    while algorithm != "1" and algorithm != "2" and algorithm != "3":
        algorithm = input("Welk algoritme wilt u gebruiken? 1:Random 2:Greedy 3:A*   ")

    # Perform desired algorithm: Random
    if int(algorithm) == 1:
        print(f"U hebt gekozen voor:") 
        print(f"Algoritme: Random Chip: {chip_number} Netlist: {netlist_number}")
        generated_grid = grid.Grid(f"data/chip_{chip_number}/print_{chip_number}.csv", f"data/chip_{chip_number}/netlist_{netlist_number}.csv", size)
        rs.random_solve3D(generated_grid)
        
        # Print results and plot graph  
        cost = generated_grid.cost_of_route()
        print(f"De totale kost is: {cost}")
        pg.plot_grid(generated_grid, chip_number, netlist_number, cost, "Random")

    # Perform desired algorithm : Greedy    
    elif int(algorithm) == 2:
        print(f"U hebt gekozen voor:") 
        print(f"Algoritme: Greedy Chip: {chip_number} Netlist: {netlist_number}")
        reset = False
        while not reset:
            generated_grid = grid.Grid(f"data/chip_{chip_number}/print_{chip_number}.csv", f"data/chip_{chip_number}/netlist_{netlist_number}.csv", size)
            greedy = gr.LengthGreedy(generated_grid)
            reset = greedy.run()
        
        # Print results and plot graph
        cost = generated_grid.cost_of_route()  
        print(f"De totale kost is: {cost}")
        pg.plot_grid(generated_grid, chip_number, netlist_number, cost, "Greedy")

    # Perform desired algorithm: A*       
    elif int(algorithm) == 3:
        while annealing != "ja" and annealing != "nee":
            annealing = input("Wil je dat er simulated annealing wordt toegepast na het algoritme? ja of nee  ")
        
        # Perform without simulated annealing
        if annealing == "nee":
            print(f"U hebt gekozen voor:") 
            print(f"Algoritme: A* Chip: {chip_number} Netlist: {netlist_number} Simulated Annealing: Nee")
            reset = False
            while not reset:
                generated_grid = grid.Grid(f"data/chip_{chip_number}/print_{chip_number}.csv", f"data/chip_{chip_number}/netlist_{netlist_number}.csv", size)
                astar = ast.PopAstar(generated_grid)
                reset = astar.run()
            cost = generated_grid.cost_of_route()
        
        # Perform with simulated annealing
        if annealing == "ja":
            print(f"U hebt gekozen voor:") 
            print(f"Algoritme: A* Chip: {chip_number} Netlist: {netlist_number} Simulated Annealing: Nee")
            while True:
                try:
                    iterations = int(input("Hoeveel iteraties wilt u gebruiken? (standaard is 100, maar bij hogere netlists kan dit voor zeer hoge verwerkingstijden zorgen. Netlist 9 met 100 iteraties kan ongeveer 10 uur duren.)    "))
                except ValueError:
                    print("Dit is geen Integer")
                    continue
                else:
                    break
            reset = False
            while not reset:
                generated_grid = grid.Grid(f"data/chip_{chip_number}/print_{chip_number}.csv", f"data/chip_{chip_number}/netlist_{netlist_number}.csv", size)
                astar = ast.PopAstar(generated_grid)
                reset = astar.run()

            cost = generated_grid.cost_of_route()
            print(f"Kosten voor Simulated Annealing: {cost}")
            simA = siman.SimulatedAnnealing(generated_grid)
            result = simA.run(cost, iterations)
            cost = result[0]

            # Plots difference in costs before and after simulated annealing
            plt.plot(result[1], color = "r", label="Newly calculated cost")
            plt.plot(result[2], color= "b", label="Current cost")
            plt.style.use('ggplot')
            plt.legend()
            plt.show()

        # Print results and plot graph  
        print(f"De totale kost is: {cost}")
        pg.plot_grid(generated_grid, chip_number, netlist_number, cost, "Astar")