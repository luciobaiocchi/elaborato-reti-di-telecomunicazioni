# node.py

class Node:
    def __init__(self, name):
        self.name = name
        self.routing_table = {name: (0, name)}  # Se stesso come destinazione
        self.neighbors = {}

    def add_neighbor(self, neighbor, cost):
        self.neighbors[neighbor] = cost

    def remove_neighbor(self, neighbor):
        if neighbor in self.neighbors:
            del self.neighbors[neighbor]

    def update_routing_table(self):
        updated = False
        for neighbor, cost_to_neighbor in self.neighbors.items():
            for dest, (cost_to_dest, next_hop) in neighbor.routing_table.items():
                new_cost = cost_to_neighbor + cost_to_dest
                if dest not in self.routing_table or new_cost < self.routing_table[dest][0]:
                    self.routing_table[dest] = (new_cost, neighbor.name)
                    updated = True
        return updated

    def get_routing_table_str(self):
        return "\n".join(
            [f"{dest}: cost={cost}, next_hop={next_hop}" for dest, (cost, next_hop) in self.routing_table.items()]
        )