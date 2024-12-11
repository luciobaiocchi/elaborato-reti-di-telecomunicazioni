# routing_table.py
from node import Node

class RoutingTableManager:
    def __init__(self, nodes):
        self.nodes = nodes

    def update_routing_tables(self):
        updated = False
        for node in self.nodes:
            if node.update_routing_table():
                updated = True

        # Se almeno una tabella è stata aggiornata, ridisegnare tutto
        return updated