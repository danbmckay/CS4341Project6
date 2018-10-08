import random
import sys


class Node():

    def __init__(self, node_name, some_parents, some_conditions):

        self.node_name = node_name
        self.node_place = int(''.join(i for i in node_name if i.isdigit())) - 1
        self.weight = 0
        self.weight_added = False
        if len(some_conditions) > 1:
            self.has_parents = True
        else:
            self.has_parents = False
        self.parent_names = some_parents
        self.parent_nodes = []
        self.children = []
        self.num_children = 0
        self.status = False
        self.been_checked = False
        self.conditions = []
        for a_condition in some_conditions:
            self.conditions.append(float(a_condition))

        self.num_parents = len(some_parents)

    # do after all nodes have been created to find their parent nodes
    # links all the nodes to their parents
    # nodes all of the nodes in the network
    def find_parents(self, nodes):

        if self.has_parents:
            for a_node in nodes:
                for a_parent in self.parent_names:
                    if a_node.node_name == a_parent:
                        self.parent_nodes.append(a_node)
                        a_node.children.append(self)
                        a_node.num_children += 1

    # input either 0 or 1. 1 means true 0 means false and get the correct probability according to weight
    def get_weight(self, input):
        if input == 1:
            return self.weight
        else:
            return 1 - self.weight

    # sets the weight for all of the nodes
    def make_weight(self):
        # don't redo work, checks if it has been done
        if not self.weight_added:
            # if the node is just a parent node the weight is equal to the value of the probability its true
            if not self.has_parents:
                self.weight_added = True
                self.weight = self.conditions[0]

            else:
                # make sure parent weights are set first other wise there will be problems
                for a_parent in self.parent_nodes:
                    a_parent.make_weight()

                # get the number of layers that are going to be in the table
                num_true = 1
                for i in range(0, len(self.parent_nodes)):
                    num_true *= 2

                # get rows of probabilities to multiply and add together
                indiv_weights = []
                for i in range(0, num_true):
                    temp_string = []  # check the string being looked at
                    temp_nums = [self.conditions[i]] # the string of probabilities to be multiplied together
                    temp_counter = 1
                    # get the all the correct probabilities from parents for all permutations
                    for a_parent in self.parent_nodes:
                        trulse = int(i/temp_counter) % 2  # gets a 0 1 in the correct spot
                        temp_string.append(trulse)
                        temp_nums.append(a_parent.get_weight(trulse))
                        temp_counter *= 2
                    indiv_weights.append(temp_nums)

                the_weight = 0
                for a_weight in indiv_weights:
                    temp_weight = 1
                    for a_num in a_weight:
                        temp_weight *= a_num
                    the_weight += temp_weight

                self.weight_added = True
                self.weight = the_weight


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

    # calculates a random outcome of something happening
    def happened(self):

        if self.has_parents:
            # again don't duplicate answers
            if not self.been_checked:
                parents_happened = []
                for a_parent in self.parent_nodes:
                    # make sure that the parents have some result already
                    parents_happened.append(a_parent.happend())

                    # get some random number
                    choice = random.uniform(0, 1)
                    temp_place = 0
                    counter = 1
                    # find the correct location in the truth table to compare later
                    for some_parent in parents_happened:
                        if some_parent:
                            temp_place += counter

                        counter *= 2

                    # determine if it happened or not
                    a_prob = self.conditions[temp_place]
                    if a_prob > choice:
                        self.status = True
                        return True
                    else:
                        self.status = False
                        return False
            # if its already been done, return whats already there
            else:
                return self.status

        # check nodes that are just parents
        else:
            # don't get multiple answers, just do it once
            if not self.been_checked:
                # get a random number and make a choice based on the likely hood of being right
                choice = random.uniform(0, 1)
                if self.conditions[0] > choice:
                    self.status = True
                    return True
                else:
                    self.status = False
                    return False
            else:
                return self.status


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
            # Now add node to graph
            # G.add_node(n)
    for node in node_list:
        print(node.node_place)
        node.find_parents(node_list)
        node.make_weight()
        print(node.weight)


if __name__ == "__main__":
    main()
