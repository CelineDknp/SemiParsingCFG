from .Node import Node
import re


class LabelNode(Node):

    def __init__(self, depth, node_type, regex):
        super().__init__(depth, node_type, regex)

    def __str__(self):
        return f"Node {self.type} {self.label}"

    def get_label(self):
        return self.label

    def set_label(self, label):
        self.label = label

    def find_label(self, input_str, pos, pattern):
        res = pattern.search(input_str[pos:].upper())
        self.label = res.group(0)[:-1].strip()
        # print(f"Label found: {self.label}")
        return input_str.upper().find(res.group(0), pos) + 7 + len(self.label)
