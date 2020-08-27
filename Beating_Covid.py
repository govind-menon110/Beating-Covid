import random
import networkx as nx 
import matplotlib.pyplot as plt 
import copy
import time

class Node(object):
    def __init__(self, node_id, weight, covid_infected = False, vaccinated = False):
        self.id = node_id
        self.weight = weight
        self.covid_infected = covid_infected
        self.vaccinated = vaccinated
        self.neighbors = set()

    def get_weight(self):
        return self.weight

    def add_neighbor(self, node_id):
        self.neighbors.add(node_id)

    def is_infected(self):
        return self.covid_infected

    def is_vaccinated(self):
        return self.vaccinated

    def make_infected(self):
        if self.covid_infected : 
            print("node already infected")
        elif self.vaccinated :
            print("node already vaccinated")
        else:
            self.covid_infected = True

    def get_neighbor_node_ids(self):
        return self.neighbors

    def vaccinate_node(self):
        if self.vaccinated:
            print("node already vaccinated")
        elif self.covid_infected:
            print("node already infected")
        else:
            self.vaccinated = True


class Graph(object):
    def __init__(self, node_ids, weights, game_over = 0):
        # structure of graph {node_id: node_object, ...}
        self.graph = {}
        self.vaccinated_node_ids = []
        self.add_nodes(node_ids, weights)
        #first_infected_node_id = random.choice(self.graph.keys())
        first_infected_node_id = 34
        self.graph[first_infected_node_id].make_infected()
        self.infected_node_ids = [first_infected_node_id]
        self.propagator_nodes =[first_infected_node_id]

    def add_nodes(self, node_ids, weights):
        for node_id, weight in zip(node_ids, weights):
            self.add_node(node_id, weight)

    def add_node(self, node_id, weight):
        if node_id in self.graph:
            print("node already exists")
        else:
            new_node = Node(node_id, weight)
            self.graph[node_id] = new_node

    def add_connections(self, connections):
        for node_1_id, node_2_id in connections:
            self.add_connection(node_1_id, node_2_id)

    def add_connection(self, node_1_id, node_2_id):
        if node_1_id not in self.graph or node_2_id not in self.graph:
            print("one of the nodes does not exist")
        else:
            self.graph[node_1_id].add_neighbor(node_2_id)
            self.graph[node_2_id].add_neighbor(node_1_id)

    def get_infected_nodes(self):
        return self.infected_node_ids

    def get_sum_of_weights_of_all_infected_nodes(self):
        infected_sum = 0
        for infected_node_id in self.infected_node_ids:
            infected_sum = infected_sum + self.graph[infected_node_id].get_weight()

        return infected_sum
    def get_sum_of_weights_of_all_healthy_nodes(self):
        healthy_sum =0 
        for id in self.graph.keys():
            if  not self.graph[id].is_infected():
                healthy_sum = healthy_sum + self.graph[id].get_weight()
        return healthy_sum      

    def get_sum_of_weights_of_neighbouring_neutral_nodes(self, node_1_id):
        neutral_neighbor_ids = self.get_neutral_neighbor_ids_of_a_node(node_1_id)
        weighted_sum = 0
        for neighbor_node_id in neutral_neighbor_ids:
            weighted_sum = weighted_sum + self.graph[neighbor_node_id].get_weight()
        return weighted_sum

    def get_neutral_neighbor_ids_of_a_node(self, node_id):
        neutral_neighbor_ids = []
        if node_id not in self.graph:
            print("node does not exist")
        else:
            for neighbor_node_id in self.graph[node_id].get_neighbor_node_ids():
                if not self.graph[neighbor_node_id].is_infected() and not self.graph[neighbor_node_id].is_vaccinated():
                    neutral_neighbor_ids.append(neighbor_node_id)
        
        return neutral_neighbor_ids

    def vaccinate_node(self, node_id):
        if node_id not in self.graph:
            print("node does not exist")
        else:
            self.vaccinated_node_ids.append(node_id)
            self.graph[node_id].vaccinate_node()
    
    def get_nodes_that_will_be_infected_in_next_step(self):
        """Gets the node objects to which the infection will spread in the next
        round. We have to select one node out of these to vaccinate."""

        nodes_that_will_be_infected = {}
        for infected_node_id in self.infected_node_ids:
            neighbor_ids_of_infected_node = self.get_neutral_neighbor_ids_of_a_node(infected_node_id)
            for neighbor_id in neighbor_ids_of_infected_node:
                if neighbor_id not in nodes_that_will_be_infected:
                    nodes_that_will_be_infected[neighbor_id] = self.graph[neighbor_id]
        if(len(nodes_that_will_be_infected) == 0):
            self.game_over = 1
        return nodes_that_will_be_infected

    def play_one_step(self, vaccinate_node_id = None):
        """One step of the game proceeds. The node id given is vaccinated
        and the infection spreads to all the neighboring nodes."""

        nodes_about_to_be_infected = []
        if vaccinate_node_id:
            self.vaccinate_node(vaccinate_node_id)
            for infected_node_id in self.infected_node_ids:
                neutral_neighbor_ids = self.get_neutral_neighbor_ids_of_a_node(infected_node_id)
                for neutral_neighbor_node_id in neutral_neighbor_ids:
                    if neutral_neighbor_node_id not in nodes_about_to_be_infected:
                        nodes_about_to_be_infected.append(neutral_neighbor_node_id)
            self.propagator_nodes = nodes_about_to_be_infected

            for node_id in nodes_about_to_be_infected:
                if node_id not in self.infected_node_ids and node_id not in self.vaccinated_node_ids:
                    self.infected_node_ids.append(node_id)
                    self.graph[node_id].make_infected()

    def node_to_vaccinate_alternate_alpha(self):
        temporary_graph = copy.deepcopy(self)
        values = {}
        nodes_that_will_be_infected = temporary_graph.get_nodes_that_will_be_infected_in_next_step()
        if len(nodes_that_will_be_infected) == 0:
            return None, temporary_graph.get_sum_of_weights_of_all_healthy_nodes()
        else:
            for node_id in nodes_that_will_be_infected:
                temporary_graph.play_one_step(node_id)
                if temporary_graph.get_sum_of_weights_of_all_healthy_nodes()<12000:
                    values[node_id] = 0
                    next_node_to_save = None
                else:
                    next_node_to_save, values[node_id] = temporary_graph.node_to_vaccinate_alternate_alpha()
                temporary_graph = copy.deepcopy(self)

            max_value_key = max(values, key=values.get)
            return max_value_key, values[max_value_key]

    def node_to_vaccinate_alternate(self):
        temporary_graph = copy.deepcopy(self)
        values = {}
        nodes_that_will_be_infected = temporary_graph.get_nodes_that_will_be_infected_in_next_step()
        if len(nodes_that_will_be_infected) == 0:
            return None, temporary_graph.get_sum_of_weights_of_all_healthy_nodes()
        else:
            for node_id in nodes_that_will_be_infected:
                temporary_graph.play_one_step(node_id)
                next_node_to_save, values[node_id] = temporary_graph.node_to_vaccinate_alternate()
                temporary_graph = copy.deepcopy(self)

            max_value_key = max(values, key=values.get)
            return max_value_key, values[max_value_key]
    
    def node_to_vaccinate(self):
        max_sum_weight = 0
        node_vaccinate = -1
        for node_id in self.propagator_nodes:
            node_l1 = self.get_neutral_neighbor_ids_of_a_node(node_id)
            for node_id_l1 in node_l1:
                if (max_sum_weight< self.get_sum_of_weights_of_neighbouring_neutral_nodes(node_id_l1)) + self.graph[node_id_l1].get_weight():
                    max_sum_weight = self.get_sum_of_weights_of_neighbouring_neutral_nodes(node_id_l1) +self.graph[node_id_l1].get_weight()
                    node_vaccinate = node_id_l1

        return node_vaccinate

# assigning node ids, weights and start of game play.
node_ids = [i for i in range(1,101)]
weights = [i for i in range(10,1010,10)]

# initialize a graph - the first infected node is randomly chosen.
graph = Graph(node_ids, weights)

# get the id of the first infected node.
first_infected_node = graph.get_infected_nodes()[0]
# print the id of the first infected node.
print("First infected node: "), first_infected_node

# connections between nodes
connections = [(61, 66), (3, 83), (48, 99), (49, 56), (57, 86), (75, 99), (5, 46), (37, 49), (19, 35), (50, 88), (21, 43), (69, 93), (15, 42), (57, 70), (21, 93), (48, 90), (26, 48), (5, 67), (67, 86), (23, 76), (42, 88), (67, 93), (23, 51), (17, 58), (35, 86), (61, 68), (38, 40), (47, 68), (34, 40), (86, 92), (5, 77), (34, 56), (11, 80), (18, 80), (67, 73), (16, 78), (51, 98), (8, 68), (3, 21), (8, 13), (36, 38), (14, 58), (45, 66), (5, 86), (23, 46), (36, 65), (67, 89), (9, 90), (28, 94), (4, 57), (36, 48), (40, 99), (88, 100), (34, 69), (81, 90), (83, 96), (11, 40), (14, 42), (18, 30), (45, 58), (47, 86), (15, 26), (45, 59), (3, 29), (39, 41), (16, 83), (39, 73), (3, 6), (33, 93), (18, 40), (30, 98), (35, 90), (55, 71), (20, 65), (10, 77), (37, 58), (41, 65), (45, 100), (55, 84), (23, 85), (77, 89), (8, 34), (5, 35), (19, 77), (7, 61), (23, 80), (69, 82), (4, 59), (39, 94), (17, 79), (16, 17), (1, 59), (90, 91), (2, 28), (31, 51), (23, 40), (43, 72), (31, 85), (76, 92), (31, 63)]

# create connections
graph.add_connections(connections)

#initializing the graph to draw, add the nodes and connections.
g = nx.Graph()
g.add_nodes_from(node_ids)
g.add_edges_from(connections)

# Specify appearance of node.
graph_pos = nx.shell_layout(g)

# Creating the graph to draw, adding edges and nodes (all blue) with initial edge conditions.
nx.draw(g,graph_pos,with_labels=True,node_color='green',node_size=50)
plt.show()

print("Close images to proceed.")
print('\n')


# Start game play.
while (len(graph.get_nodes_that_will_be_infected_in_next_step())):
    # id = graph.node_to_vaccinate()
    start_time = time.time() 
    id = graph.node_to_vaccinate_alternate()[0]
    print("Time elapsed : " + str(time.time()-start_time))
    #color_map = []                     #updating color map at each step of the loop
    #for x in graph.graph.keys():
    #    if graph.graph[x].is_infected():
    #        color_map.append('red')
    #    elif graph.graph[x].is_vaccinated():
    #        color_map.append('blue')
    #    else:
    #        color_map.append('green')    
    #print "node to vaccinate :", id
    
    # Update graph conditions.
    #nx.draw(g,graph_pos,node_color=color_map,with_labels=True, node_size=500, ax=ax)
    #plt.show()
    graph.play_one_step(id)

graph.play_one_step()
color_map = []
for x in graph.graph.keys():
    if graph.graph[x].is_infected():
       color_map.append('red')
    elif graph.graph[x].is_vaccinated():
        color_map.append('blue')
    else:
        color_map.append('green') 
nx.draw(g,graph_pos,node_color=color_map,with_labels=True, node_size=50)
plt.show()
print("Sum of weights of healthy nodes saved:", graph.get_sum_of_weights_of_all_healthy_nodes())