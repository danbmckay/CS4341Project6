import networkx as nx
import sys


class Node():

    def __init__(self, node_name, some_parents, some_conditions):

        self.node_name = node_name
        if len(some_conditions) > 1:
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
    G = nx.Graph()
    node_list = []

    with open(network_file, 'r') as f:
        for line in f:
            # list_bool is True when we are looking at the node parent list, false when looking at probability list
            name, parent_list, prob_list, list_bool = "", [], [], True
            for word in line.split():
                if ":" in word:
                    name = word[:-1]
                else:
                    add_node = True
                    if "[" in word and "]" not in word and list_bool and add_node:
                        parent_list.append(word[1:])
                        add_node = False
                    if "]" in word and list_bool and add_node:
                        if len(word) != 2:
                            if "[" in word:
                                parent_list.append(word[1:-1])
                            else:
                                parent_list.append(word[:-1])
                        list_bool = False
                        add_node = False
                    if "[" in word and "]" not in word and not list_bool and add_node:
                        # add to probability list
                        prob_list.append(word[1:])
                        add_node = False
                    if "]" in word and not list_bool and add_node:
                        # dont have to check for empty prob list because it will never be empty
                        if "[" in word:
                            prob_list.append(word[1:-1])
                        else:
                            prob_list.append(word[:-1])
                        add_node = False
                    if list_bool and add_node:
                        parent_list.append(word)
                        add_node = False
                    if not list_bool and add_node:
                        prob_list.append(word)

            # Now create the node
            node_list.append(Node(name, parent_list, prob_list))
            # Now add node to graph
            # G.add_node(n)
    for node in node_list:
        node.find_parents(node_list)




if __name__ == "__main__":
    main()
