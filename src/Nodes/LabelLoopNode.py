from .LoopNode import LoopNode
from .LabelNode import LabelNode
from Anchors import LoopAnchor
from Utils.config import *


class LabelLoopNode(LoopNode):

	def __init__(self, depth, node_type, anchor):
		super().__init__(depth, node_type, anchor)
		self.label_regex = anchor.get_label()
		self.label_child = None

	@classmethod
	def from_explicit(cls, depth, node_type, regex, label, goback):
		elem = {"type":"label", "start":regex, "inline-label":label,"goback":goback}
		anchor = LoopAnchor.LoopAnchor(elem)
		return cls(depth, node_type, anchor)

	def __str__(self):
		#return f"Node {self.type} (label) to {self.label}"
		return super().__str__()

	def add_child(self, node, match=False, label=False):
		if match:
			super().add_child(node, match=match)
		if label:
			self.label_child = node
			if node in self.childs: #If the node was already a child, add it again
				self.childs.append(node)
		super().add_child(node)

	def find_label_child(self):
		for c in self.get_childs():
			if isinstance(c, LabelNode) and c.get_label() == self.label:
				self.label_child = c
				break

	def get_childs_h(self):
		self.find_label_child()
		res = []
		for c in self.get_childs():
			if c != self.label_child:
				res.append(c)
		return res

	def get_label_child(self):
		return self.label_child

	def get_label(self):
		return self.label

	def set_label(self, label):
		self.label = label

	def get_label_regex(self):
		return self.label_regex

	def is_label(self):
		return True

	def find_label(self, actual_match):
		actual_match = (' ').join(actual_match.split()) #Clean up any extra space by splitting and joining a first time
		splitted = actual_match.strip().split(" ")
		self.label = splitted[-1].strip()
		#print(f"Label found: {self.label}")
