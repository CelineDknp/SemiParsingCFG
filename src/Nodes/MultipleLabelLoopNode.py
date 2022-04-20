from .LabelLoopNode import LabelLoopNode
from Anchors import LoopAnchor


class MultipleLabelLoopNode(LabelLoopNode):

	def __init__(self, depth, node_type, anchor):
		super().__init__(depth, node_type, anchor)
		self.separator = anchor.get_separator()

	@classmethod
	def from_explicit(cls, depth, node_type, regex, separator, label, goback):
		elem = {"type":"multiple_label", "start":regex, "separator":separator, "inline-label":label,"goback":goback}
		anchor = LoopAnchor.LoopAnchor(elem)
		return cls(depth, node_type, anchor)

	def __str__(self):
		return f"Node {self.type} (multiple labels) to {self.label}"

	def go_back_label(self):
		if self.go_back:
			return self.label[-1]

	def set_label(self, label):
		self.label = label

	def is_label(self):
		return True

	def is_complete(self):
		if self.go_back:
			return len(self.childs) == len(self.label)+1 #One child is the next node, one because of the loop
		else:
			return len(self.childs) == len(self.label)+1

	def is_multiple_labels(self):
		return True

	def find_label(self, actual_match):
		splitted = actual_match.strip().split(" ")
		self.label = [splitted[1], splitted[3]]
		#print(f"Found labels: {self.label}")