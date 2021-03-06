from code.classes import net
from code.classes import node
from code.function import check_constraints
import random

class Astar():
    def __init__(self, grid_file):
        """
        Astar looks for the best route between 2 gates
        """
        self.grid_file = grid_file
    
    def get_netlists(self, gridfile):
        """
        Returns the netlist in random order
        """
        netlists = self.grid_file.get_netlists()

        return netlists
    
    def run(self):
        """
        Seeks the best path between 2 gates
        """
        netlists = self.get_netlists(self.grid_file)
        counter = 0

        while len(netlists) != 0:
            """
            As long as there are paths left in netlists it needs to run
            Define begin point and end point
            """
            netlist = self.grid_file.get_coordinates_netlist(netlists[0])
            netlists.pop(0)
            crosses = []

            open_list = []
            closed_list = []

            directions = [(0,0,1), (0,0,-1), (0,-1,0), (1,0,0), (0,1,0), (-1,0,0)]

            origin_x = netlist[0]
            origin_y = netlist[1]
            destination_x = netlist[2]
            destination_y = netlist[3]

            coordinates_origin = (origin_x, origin_y, 0)
            coordinates_destination = (destination_x, destination_y,0)

            # Create start and end node
            start_node = node.Node(None, coordinates_origin)
            start_node.g = start_node.h = start_node.f = 0
            end_node = node.Node(None, coordinates_destination)
            end_node.g = end_node.h = end_node.f = 0

            open_list.append(start_node)

            while len(open_list) != 0:
                # Set a current node and then get new "best" node from open list
                current_node = open_list[0]
                current_index = 0
                nets = []

                for index, item in enumerate(open_list, 0):
                    if item.f <= current_node.f:
                        current_node = item
                        current_index = index
                
                # Pop current off open list, add to closed list
                open_list.pop(current_index)
                closed_list.append(current_node)

                # If current node equals end node then start making the path
                if current_node == end_node:
                    paths = []
                    
                    current = current_node
                    while current is not None:
                        paths.append(current.position)
                        current = current.parent

                    # Return path
                    for i in range(len(paths)-1):
                        cross = check_constraints.check_constraints(self.grid_file, paths[i], paths[i+1], coordinates_destination, nets)[1]
                        if cross is not None:
                            crosses.append(cross)
                        new_netlist = net.Net(paths[i], paths[i+1])
                        nets.append(new_netlist)
                    
                    self.grid_file.add_route(nets, crosses)
                    counter += 1
                    if counter % 10 == 0:
                        print(f"Route connected: {coordinates_origin}, {coordinates_destination}, Crosses: {len(crosses)}, Nummer: {counter}")
                    break
                
                # Generate children
                children = []

                for direction in directions:
                    node_position = (current_node.position[0] + direction[0], current_node.position[1] + direction[1], current_node.position[2] + direction[2])

                    # Check if node is within the constraints
                    check = check_constraints.check_constraints(self.grid_file, current_node.position, node_position, coordinates_destination, nets)
                    if check[0]:
                        if check[1] is not None:
                            new_node = node.Node(current_node, node_position)
                            new_node.cross = True
                            children.append(new_node)
                        else:  
                            new_node = node.Node(current_node, node_position)
                            children.append(new_node)
                
                # Check if children are new or if a "better" route has been found
                for child in children:
                    check = False

                    for closed_node in closed_list:
                        if child == closed_node:
                            check = True
                            continue
                        
                    child.g = current_node.g + 1
                    child.h = abs(destination_x - child.position[0]) + abs(destination_y - child.position[1]) + abs(0 - child.position[2])
                    
                    # Check if node crosses a different node
                    if child.cross :
                        child.h += 300

                    child.f = child.g + child.h

                    # Check if position has already been generated and compare the cost
                    for open_node in open_list:
                        if child == open_node and child.f >= open_node.f:
                            check = True
                            continue
                    
                    if not check:
                        open_list.append(child)
                
                # Abort if length equals 0 but end not found
                if len(open_list) == 0:
                    return False
        return True

class PopAstar(Astar):
    """
    The PopAstar Class sorts the gates by amount of connections
    The gates with the most connections come first
    """
    def get_netlists(self, grid_file):
        """
        Counts how many connections each chip has and returns the order from high to low.
        """
        netlists = grid_file.get_netlists()
        counting = {}

        # Count the connections each gate has
        for item in netlists:
            counting[int(item[0])] = 0
            counting[int(item[1])] = 0
        for item in netlists:
            counting[int(item[0])] += 1
            counting[int(item[1])] += 1

        populated_netlists = []

        # Sort the gates by connections, most connections first
        while len(counting) != 0:
            gate_max = max(counting, key=lambda key: counting[key])
            del counting[gate_max]

            current_connections = []

            # Add route to netlist, if current gate_max is the destination, change it to origin
            for item in netlists:
                if int(item[0]) == gate_max:
                    populated_netlists.append(item)
                    current_connections.append(item)
                elif int(item[1]) == gate_max:
                    new_item = (item[1], item[0])
                    populated_netlists.append(new_item)
                    current_connections.append(item)

            for item in current_connections:
                netlists.remove(item)

        return populated_netlists

class LengthAstar(Astar):
    """
    Returns netlists ordered by length
    """
    def get_netlists(self, grid_file):
        netlists = grid_file.get_netlists()

        netlist_distance = {}

        # Calculate distance of all netlists
        for item in netlists:
            coordinates_gates = grid_file.get_coordinates_netlist(item)
            distance = abs(coordinates_gates[0] - coordinates_gates[2]) + abs(coordinates_gates[1] - coordinates_gates[3])
            netlist_distance[item] = distance

        length_netlists = []

        # Sort netlists from shortest to longest
        while len(netlist_distance) != 0:
            min_distance = min(netlist_distance, key=lambda key: netlist_distance[key])
            length_netlists.append(min_distance)
            del netlist_distance[min_distance]

        # Reverses netlists, ordered from longest to shortest
        length_netlists.reverse()
        
        return length_netlists
