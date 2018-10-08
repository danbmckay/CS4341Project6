import sys
import random

class Node():

    def __init__(self, node_name, some_parents, some_conditions):

        self.node_name = node_name
        if len(some_conditions) > 1:
            self.has_parents = True
        else:
            self.has_parents = False
        self.parent_names = some_parents
        self.parent_nodes = []
        self.children = []
        self.num_children = 0
        self.conditions = some_conditions
        self.num_parents = len(some_parents)

    # do after all nodes have been created to find their parent nodes
    def find_parents(self, nodes):

        if self.has_parents:
            for a_node in nodes:
                for a_parent in self.parent_names:
                    if a_node.node_name == a_parent:
                        self.parent_nodes.append(a_node)
                        a_node.children.append(self)
                        a_node.num_children += 1

    def create_init_status(self, status):
        self.status = status

    # def change_status(self):
    #
    #     if self.has_parents:
    #         probabilities = []
    #         place_in_table = []
    #         for a_parent in self.parent_nodes:
    #             temp_result = a_parent.change_status()
    #             place_in_table.append(temp_result[1])
    #             probabilities.append(temp_result[0])
    #
    #         temp_place = 0
    #         counter = 1
    #         for a_place in place_in_table:
    #             if a_place:
    #                 temp_place += counter
    #
    #             counter *= 2
    #
    #         self.status = self.conditions[temp_place]
    #
    #     else:
    #         if self.status == 1:
    #             return [self.conditions[0], True]
    #         elif self.status == 0:
    #             return [1 - self.conditions[0], False]

    def happened(self, a_prob):

        if self.has_parents:
            for a_parent in self.parent_nodes:

                if self.status > a_prob:
                    return True

        else:
            choice = random.uniform(0, 1)
            if choice > self.conditions[0]:
                return True
            else:
                return False

    

def main():
    network_file = sys.argv[1]
    query_file = sys.argv[2]
    num_samples = sys.argv[3]
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

    for node in node_list:
        node.find_parents(node_list)
    #rejection sampling

    #likelihood weighting sampling




if __name__ == "__main__":
    main()
