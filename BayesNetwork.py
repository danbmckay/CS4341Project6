
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
        self.status = -1  # the prob for unknown, 1 True, 0 False, and 3 Query variable

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

    def change_status(self):

        if self.has_parents:
            probabilities = []
            place_in_table = []
            for a_parent in self.parent_nodes:
                temp_result = a_parent.change_status()
                place_in_table.append(temp_result[1])
                probabilities.append(temp_result[0])

            temp_place = 0
            counter = 1
            for a_place in place_in_table:
                if a_place:
                    temp_place += counter

                counter *= 2

            self.status = self.conditions[temp_place]

        else:
            if self.status == 1:
                return [self.conditions[0], True]
            elif self.status == 0:
                return [1 - self.conditions[0], False]

    def happened(self, a_prob):

        if self.status > a_prob:
            return True
