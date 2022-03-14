from Nodes.LoopNode import LoopNode
from Utils.config import *
import re


class LabelLoopNode(LoopNode):

    def __init__(self, depth, node_type):
        super().__init__(depth, node_type)

    def __str__(self):
        return f"Node {self.type} to {self.label}"

    def get_label(self):
        return self.label

    def find_label(self, input_str, pos):
        self.label = input_str[pos + 6:input_str.upper().find("\n", pos)].strip()
        if self.label[-1] == ".":
            self.label = self.label[:-1]
        # print(f"Label found: {self.label}")
        return input_str.upper().find(self.label, pos) + len(self.label)

    def add_child(self, node):
        if node.get_type() != NODE_LABEL:
            return
        if node == self: #Don't add yourself as a child ! #Dirtyfix
            print(">>> Trying to add myself as child (Node)")
            return
        if node in self.childs: #Dirty
            return
        self.childs.append(node)
        node.add_parent(self)
