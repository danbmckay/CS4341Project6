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
                print(the_weight)
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
                    parents_happened.append(a_parent.happened())

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
                        self.been_checked = True
                        self.status = True
                        return True
                    else:
                        self.been_checked = True
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
                    self.been_checked = True
                    self.status = True
                    return True
                else:
                    self.been_checked = True
                    self.status = False
                    return False
            else:
                return self.status


# num_samples: the number of samples to do
# node_list: the list of the nodes in the network
# query_params: the query to follow
# does rejection sampling on the given node list with the given query and returns
# probability of ? variable being true after rejecting samples
def rejection_sampling(num_samples, node_list, query_params):
    # rejection sampling
    correct_samples, total_samples = 0.0, 0.0

    for _ in range(0, num_samples):
        # whether or not to count the current sample
        count_sample = True
        correct_value = True
        for i in range(0, len(query_params)):
            temp = node_list[i].happened()
            if query_params[i] == 't' and not temp:
                # break if outcome not consistent with given statement
                count_sample = False
                break
            if query_params[i] == 'f' and temp:
                # same as above
                count_sample = False
                break
            if query_params[i] == '?':
                correct_value = temp
        if count_sample:
            total_samples += 1
            if correct_value:
                # the ? param is true, and the whole sample is consistent with preconditions
                correct_samples += 1

        for a_node in node_list:
            a_node.been_checked = False
    # print(correct_samples, total_samples)
    return correct_samples/total_samples


# num_samples: the number of samples to do
# node_list: the list of the nodes in the network
# query_params: the query to follow
# does likelihood weighting on the given network with the given query,
# and returns the probability of the ? variable being true
def likelihood_weighting(num_samples, node_list, query_params):
    # likelihood weighting sampling
    correct_samples, total_samples = 0.0, 0.0
    for _ in range(0, num_samples):
        sample_weight = 0.0
        for i in range(0, len(query_params)):
            # go through list of nodes once and force true/false values
            if query_params[i] == 't':
                # force node to be true and add weight to sample weight
                sample_weight += node_list[i].weight
                node_list[i].status = True
            if query_params[i] == 'f':
                # force node to be true and add 1-weight to sample weight
                sample_weight += 1 - node_list[i].weight
                node_list[i].status = False

        for i in range(0, len(query_params)):
            # go through list of nodes again and check true/false value of variable in question
            temp = node_list[i].happened()
            if query_params[i] == '?':
                correct_value = temp

        total_samples += sample_weight
        if correct_value:
            # the ? param is true, and the whole sample is consistent with preconditions
            correct_samples += sample_weight
        for a_node in node_list:
            a_node.been_checked = False

    # print(correct_samples, total_samples)
    return correct_samples/total_samples


def main():
    network_file = sys.argv[1]
    query_file = sys.argv[2]
    num_samples = int(sys.argv[3])
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
        # print(node.node_place)
        node.find_parents(node_list)
        node.make_weight()
        # print(node.weight)
    query_params = []
    # open up query file and set up stuff
    with open(query_file, 'r') as f:
        for line in f:
            # remove any trailing newline characters
            line = line.rstrip()
            for word in line.split(','):
                query_params.append(word)

    print("Rejection sampling on", num_samples, "samples:", rejection_sampling(num_samples, node_list, query_params))

    print("Likelihood weighting on", num_samples, "samples:", likelihood_weighting(num_samples, node_list, query_params))




if __name__ == "__main__":
    main()
