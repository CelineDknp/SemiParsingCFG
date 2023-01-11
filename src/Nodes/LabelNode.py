from .Node import Node


class LabelNode(Node):

    def __init__(self, depth, node_type, regex):
        super().__init__(depth, node_type, regex)

    def __str__(self):
        #return f"Node {self.type} {self.label}"
        return self.get_label()

    def get_label(self):
        return self.label

    def set_label(self, label):
        self.label = label

    def find_label(self, match):
        self.label = match[:-1].strip() #Remove trailing spaces and the dot at the end
