from Nodes.LoopNode import LoopNode
from Utils.config import *
import re


class ControlLoopNode(LoopNode):

	def __init__(self, depth, node_type, anchor):
		super().__init__(depth, node_type, anchor)
		self.control_node = anchor.get_control()

	def __str__(self):
		return f"Node {self.type} to {self.control_node}"

	def is_control(self):
		return True

	def get_control(self):
		return self.control_node
