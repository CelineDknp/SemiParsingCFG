from .LoopNode import LoopNode
from Anchors import LoopAnchor
from Utils.config import *


class LabelLoopNode(LoopNode):

	def __init__(self, depth, node_type, anchor):
		super().__init__(depth, node_type, anchor)
		self.label_regex = anchor.get_label()

	@classmethod
	def from_explicit(cls, depth, node_type, regex, label, goback):
		elem = {"type":"label", "start":regex, "inline-label":label,"goback":goback}
		anchor = LoopAnchor.LoopAnchor(elem)
		return cls(depth, node_type, anchor)

	def __str__(self):
		return f"Node {self.type} (label) to {self.label}"

	def get_label(self):
		return self.label

	def set_label(self, label):
		self.label = label

	def get_label_regex(self):
		return self.label_regex

	def is_label(self):
		return True

	def find_label(self, input_str, pos):
		# print(f"Looking from: |{input_str[pos:pos+80]}|")
		res = self.get_label_regex().search(input_str[pos:])
		self.label = res.group(0).strip()
		# print(f"Label found: {self.label}")
		return input_str.find(res.group(0), pos) + len(res.group(0).rstrip())
