from Nodes.LoopNode import LoopNode
from Utils.config import *
import re


class ControlLoopNode(LoopNode):

    def __init__(self, depth, node_type, control_node):
        super().__init__(depth, node_type)
        self.control_node = control_node

    def __str__(self):
        return f"Node {self.type} to {self.label}"

    def get_control(self):
        return self.control_node
