import random
from code.classes import net

def random_solve3D(origin_x, origin_y, destination_x,  destination_y, size, list_of_nets, counter, list_of_coordinates, restart):
    tries = 0
    directions = [(0,1,0), (1,0,0), (0,-1,0), (-1,0,0), (0,0,1), (0,0,-1)]
    nets = set()

    coordinates_from = (origin_x, origin_y, 0)
    coordinates_destination = (destination_x, destination_y, 0)

    current_x = origin_x
    current_y = origin_y
    destination_z = 0
    current_z = 0
    
    moves = 0
    max_moves = 8
    restart += 1

    while current_x != destination_x or current_y != destination_y or current_z != destination_z:
        tries += 1
        if tries == 2000 or moves > max_moves:
            return random_solve3D(origin_x, origin_y, destination_x,  destination_y, size, list_of_nets, counter, list_of_coordinates, restart)
        count = 0
        check = True
        direction = random.choice(directions)
        coordinates_to = (coordinates_from[0] + direction[0], coordinates_from[1] + direction[1], coordinates_from[2] + direction[2])
        
        if coordinates_to[0] > size  or coordinates_to[1] > size or coordinates_to[2] > size or coordinates_to[0] < 0 or coordinates_to[1] < 0 or coordinates_to[2] < 0:
            check = False

        for i in range(len(list_of_nets)):
            for x in list_of_nets[i]:
                net_from = x.get_coordinates_from()
                net_to = x.get_coordinates_to()

                if coordinates_to == net_from or coordinates_to == net_to:
                    count += 1
                if coordinates_from == net_from and coordinates_to == net_to:
                    check = False
                    break
                if coordinates_from == net_to and coordinates_to == net_from:
                    check = False
                    break
                if coordinates_to in list_of_coordinates and coordinates_to != coordinates_destination:
                    check = False
                    break

        for i in nets:
            net_from = i.get_coordinates_from()
            net_to = i.get_coordinates_to()

            if coordinates_to == net_from or coordinates_to == net_to:
                    count += 1
            if coordinates_from == net_from and coordinates_to == net_to:
                check = False
                break
            if coordinates_from == net_to and coordinates_to == net_from:
                check = False
                break
            if coordinates_to in list_of_coordinates and coordinates_to != coordinates_destination:
                check = False
                break

        if count == 2:
            check = False
        
        if check:
            moves += 1
            new_netlist = net.Net(coordinates_from, coordinates_to)
            nets.add(new_netlist)
            coordinates_from = coordinates_to 
            current_x = coordinates_to[0]
            current_y = coordinates_to[1]
            current_z = coordinates_to[2]

    print(f"route {counter} needed {restart} restarts")
    return nets, moves

def random_solve(origin_x, origin_y, destination_x,  destination_y, size, list_of_nets, counter, list_of_coordinates):
    tries = 0
    directions = [(0,1), (1,0), (0,-1), (-1,0)]
    nets = set()
    coordinates_from = (origin_x, origin_y)

    current_x = origin_x
    current_y = origin_y

    while current_x != destination_x or current_y != destination_y:
        tries += 1
        if tries == 2000:
            return nets, tries
        count = 0
        check = True
        direction = random.choice(directions)
        coordinates_to = (coordinates_from[0] + direction[0], coordinates_from[1] + direction[1])
        
        if coordinates_to[0] > size  or coordinates_to[1] > size  or coordinates_to[0] <= 0 or coordinates_to[1] <= 0:
            check = False

        for i in range(len(list_of_nets)):
            for x in list_of_nets[i]:
                net_from = x.get_coordinates_from()
                net_to = x.get_coordinates_to()

                # if (coordinates_to[0] == net_from[0] and coordinates_to[1] == net_from[1]) or (coordinates_to[0] == net_to[0] and coordinates_to[1] == net_to[1]):
                if coordinates_to == net_from or coordinates_to == net_to:
                    count += 1
                if coordinates_from == net_from and coordinates_to == net_to:
                    check = False
                    break
                if coordinates_from == net_to and coordinates_to == net_from:
                    check = False
                    break
                if coordinates_to in list_of_coordinates and coordinates_to[0] != destination_x and coordinates_to[1] != destination_y:
                    check = False
                    break
                # f.write(str(coordinates_from) + str(net_from) + str(check) + str(counter) + str(coordinates_to) + str(net_to) + "\n")
                # print(coordinates_from,net_from, check, coordinates_to, net_to)

        for i in nets:
            net_from = i.get_coordinates_from()
            net_to = i.get_coordinates_to()

            if coordinates_to == net_from or coordinates_to == net_to:
                    count += 1
            if coordinates_from == net_from and coordinates_to == net_to:
                check = False
                break
            if coordinates_from == net_to and coordinates_to == net_from:
                check = False
                break
            if coordinates_to in list_of_coordinates and coordinates_to[0] != destination_x and coordinates_to[1] != destination_y:
                check = False
                break

        if count == 2:
            check = False
        
        if check:
            new_netlist = net.Net(coordinates_from, coordinates_to)
            nets.add(new_netlist)
            coordinates_from = coordinates_to 
            current_x = coordinates_to[0]
            current_y = coordinates_to[1]

    return nets