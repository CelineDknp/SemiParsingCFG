from .LoopNode import LoopNode
from Anchors import LoopAnchor
from Utils.config import *


class ControlLoopNode(LoopNode):

	def __init__(self, depth, node_type, anchor):
		super().__init__(depth, node_type, anchor)
		self.control_node = anchor.get_control()

	@classmethod
	def from_explicit(cls, depth, node_type, regex, control):
		elem = {"type":"control-flow", "start":regex, "control-type": control, "control-regex":r"\.(\s)+", "goback":False}
		anchor = LoopAnchor.LoopAnchor(elem)
		return cls(depth, node_type, anchor)

	def __str__(self):
		#return f"Node {self.type} to {self.control_node}"
		return super().__str__()

	def is_control(self):
		return True

	def get_control(self):
		return self.control_node
