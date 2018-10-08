import networkx as nx
import sys


class Node():

    def __init__(self, node_name, some_parents, some_conditions):

        self.node_name = node_name
        if len(some_conditions > 2):
            self.has_parents = True
        else:
            self.has_parents = False
        self.parent_names = some_parents
        self.parent_nodes = []
        self.conditions = some_conditions
        self.num_parents = len(some_parents)

    # do after all nodes have been created to find their parent nodes
    def find_parents(self, nodes):

        if self.has_parents:
            for a_node in nodes:
                for a_parent in self.parent_names:
                    if a_node.node_name == a_parent:
                        self.parent_nodes.append(a_node)

    

def main():
    network_file = sys.argv[1]
    query_file = sys.argv[2]
    num_samples = sys.argv[3]

    with open(network_file, 'r') as f:
        for line in f:
            for word in line.split():
                print(word)

if __name__ == "__main__":
    main()
