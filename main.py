import matplotlib.pyplot as plt
from code.function import plot_grid
from code.classes import chip
from code.classes import grid
from code.classes import net
import csv

if __name__ == '__main__':
    test_grid = grid.Grid("data/chip_0/print_0.csv", "data/chip_0/netlist_1.csv")
    
    x = []
    y = []

    chips = test_grid.get_chips()

    for i in chips:
        coordinates = chips[i].get_coordinates()
        x_coordinate = int(coordinates[0])
        y_coordinate = int(coordinates[1])

        x.append(x_coordinate)
        y.append(y_coordinate)

    plot_grid.plot_grid(x,y,6,6)

    netlists = test_grid.get_netlists()
    net_needed = 0
    line_from = []
    line_to = []
    list_of_nets = []

    for netlist in netlists:
        origin = int(netlist[0])
        destination = int(netlist[1])

        chip_origin = chips[origin]
        chip_destination = chips[destination]

        coordinates_origin = chip_origin.get_coordinates()
        coordinates_destination = chip_destination.get_coordinates()

        origin_x = int(coordinates_origin[0])
        origin_y = int(coordinates_origin[1])

        destination_x = int(coordinates_destination[0])
        destination_y = int(coordinates_destination[1])

        delta_x = destination_x - origin_x
        delta_y = destination_y - origin_y


        coordinates_from = coordinates_origin
        current_x = origin_x
        

        if delta_x > 0:
            for i in range(delta_x):
                coordinates_to = [current_x + 1, origin_y]
                current_x += 1

                new_netlist = net.Net(coordinates_from, coordinates_to)
                coordinates_from = coordinates_to
                list_of_nets.append(new_netlist)
        else:
            for i in range(abs(delta_x)):
                coordinates_to = [current_x - 1, origin_y]
                current_x -= 1

                new_netlist = net.Net(coordinates_from, coordinates_to)
                coordinates_from = coordinates_to
                list_of_nets.append(new_netlist)

        print(list_of_nets)
        net_needed += (abs(destination_x - origin_x))
        net_needed += (abs(destination_y - origin_y))

        line_from.append([origin_x, origin_y])
        line_to.append([destination_x, origin_y])



        line_from.append([destination_x, origin_y])
        line_to.append([destination_x, destination_y])

        for count, x in enumerate(list_of_nets):
            print(x)
            print(x.get_coordinates_from)
        print(count)
        for i in range(len(line_from)):
            a = []
            b = []

            a.append(int(line_from[i][0]))
            a.append(int(line_to[i][0]))

            b.append(int(line_from[i][1]))
            b.append(int(line_to[i][1]))

            plt.plot(a, b, color='b')

    print("hoi", net_needed)
    plt.show()