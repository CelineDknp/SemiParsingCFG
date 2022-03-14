from Nodes.Node import Node
from Utils.config import *
import re


class LoopNode(Node):

    def __init__(self, depth, node_type):
        super().__init__(depth, node_type)

    def __str__(self):
        return f"Node {self.type} to {self.label}"
