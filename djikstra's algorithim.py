import copy

class Node:
    def __init__(self, number, cost = 99):
        self.number = number
        self.previous = copy.deepcopy(self.number)
        self.cost = cost
        self.edges = []
        self.first_hop = "N/A"

    def get_number(self):
        return (self.number)

    def get_cost(self):
        return (self.cost)

    def set_cost(self, value):
        self.cost = value

    def get_edges(self):
        return (self.edges)

    def get_previous(self):
        return (self.previous)

    def set_previous(self, value):
        self.previous = value

    def get_first_hop(self):
        return (self.first_hop)

    def set_first_hop(self, value):
        self.first_hop = value

    #if the node contains no identical edges, then add the edge to the list
    def add_edge(self, new_edge):
        connecting_node = new_edge.get_other_node(self.number)
        same = False
        for edge in self.edges:
            if (edge.get_other_node(self.number) == connecting_node):
                same = True
        if (not same):
            self.edges.append(new_edge)

    #returns a list of nodes this node is connected to
    def get_connected_nodes(self):
        connected_nodes = []
        for edge in self.edges:
            connected_nodes.append(edge.get_other_node(self.number))
        return (connected_nodes)

    #returns the edge that connects with the node number
    def get_edge_with(self, number):
        for edge in self.edges:
            if (edge.connects_to_node(number)):
                return (edge)

class Edge:
    def __init__(self, node1, node2, cost):
        self.node1 = node1
        self.node2 = node2
        self.cost = cost

    def get_other_node(self, number):
        if (self.node1 == number):
            return (self.node2)
        else:
            return (self.node1)

    def connects_to_node(self, number):
        return (self.node1 == number or self.node2 == number)

    def get_cost(self):
        return (self.cost)

#handles the output of the program
class Output:
    def __init__(self):
        self.lines_to_print = []
        self.order = []
        self.input_file_name = ""

    def set_input_filename(self, name):
        self.input_file_name = name

    def add_output(self, list):
        # find the starting node
        for node in list:
            if (node.get_cost() == 0):
                starting_node = node
        # print out the results
        for node in list:
            #set the cost 0 node to have a hop cost of N/A
            if (node.get_cost() == 0):
                node.set_cost("N/A")
            self.lines_to_print.append("start: " + str(starting_node.get_number()) + " destination: " + str(
                node.get_number()) + " next hop: " + str(node.get_first_hop()) + " cost: " + str(node.get_cost()))
            self.order.append(starting_node.get_number() * len(list) + node.get_number())

    def print_output(self):
        print ("file name: " + self.input_file_name)
        #format output to be in right order
        lines = []
        for line in self.lines_to_print:
            lines.append(line)
        for i in range(0, len(self.order)):
            lines[self.order[i]] = self.lines_to_print[i]
        #output each line
        for line in lines:
            print (line)

#checks to see whether or not a node with that value has been added to the list of nodes
def exists_node(number):
    for node in node_list:
        if (node.get_number() == number):
            return (True)
    return (False)

def find_node(number, list):
    for node in list:
        if (node.get_number() == number):
            return (node)
    print ("fail")
    print (number)

#get the input and put it in the data structures
def handle_input():
    file_name = input("What is the name of the input file? ")
    try:
        input_file = open(file_name, "r")
    except:
        print("Error opening input file. Make sure you entered the correct filename and make sure the file is in the same directory as the source code.")
    output.set_input_filename(file_name)
    for line in input_file:
        entry = line.split(" ")
        # if the next entry refers to nodes that haven't been created, create them and add them to the list of nodes
        if (not exists_node(int(entry[0]))):
            node_list.append(Node(int(entry[0])))
        if (not exists_node(int(entry[1]))):
            node_list.append(Node(int(entry[1])))
        new_edge = Edge(int(entry[0]), int(entry[1]), int(entry[2]))
        # add the new edge to the appropriate nodes
        for node in node_list:
            if (new_edge.connects_to_node(node.get_number())):
                node.add_edge(new_edge)

def dijkstra():
    #create the initial list of visited and unvisited nodes
    unvisited_nodes = copy.deepcopy(node_list)
    visited_nodes = []

    while (len(unvisited_nodes) > 0):
        #find the node with the lowest cost as the next current node
        current_node = unvisited_nodes[0]
        for node in unvisited_nodes:
            if (node.get_cost() < current_node.get_cost()):
                current_node = node
        #travel along the edges and update the costs of nodes as necessary
        edges = []
        edges = current_node.get_edges()
        for edge in edges:
            #find the node the edge connects to
            for node in unvisited_nodes:
                if (node.get_number() == edge.get_other_node(current_node.get_number())):
                    connecting_node = node
            for node in visited_nodes:
                if (node.get_number() == edge.get_other_node(current_node.get_number())):
                    connecting_node = node
            #update the cost of the node the edge connects to if necessary
            if ((current_node.get_cost() + edge.get_cost()) < connecting_node.get_cost()):
                connecting_node.set_cost(current_node.get_cost() + edge.get_cost())
                connecting_node.set_previous(current_node.get_number())
        unvisited_nodes.remove(current_node)
        visited_nodes.append(current_node)

    #go backwards to find the next hops
    for node in visited_nodes:
        #set the starting node cost to N/A
        backtracker = node
        while (not backtracker.get_previous() == backtracker.get_number()):
            node.set_first_hop(backtracker.get_number())
            backtracker = find_node(backtracker.get_previous(), visited_nodes)

    output.add_output(visited_nodes)

def main():
    handle_input()
    for node in node_list:
        #set the cost to 0 so that the algorithim will use it as the starting node then change it back afterwards
        node.set_cost(0)
        dijkstra()
        node.set_cost(99)
    output.print_output()

node_list = []
output = Output()
main()