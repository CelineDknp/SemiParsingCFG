from .LabelLoopNode import LabelLoopNode
from .LabelNode import LabelNode
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
		#return f"Node {self.type} (multiple labels) to {self.label}"
		return f"PERFORM {self.label[0]} THRU {self.label[-1]}"

	def go_back_label(self):
		if self.go_back:
			return self.label[-1]

	def start_label(self):
		if self.go_back:
			return self.label[0]

	def set_label(self, label):
		self.label = label

	def is_label(self):
		return True

	def find_label_child(self):
		for c in self.get_childs():
			if isinstance(c, LabelNode) and c.get_label() in self.label:
				self.label_child = c
				break

	def is_complete(self):
		if self.go_back:
			return len(self.childs) == len(self.label)+1 #One child is the next node, one because of the loop
		else:
			return len(self.childs) == len(self.label)+1

	def is_multiple_labels(self):
		return True

	def find_label(self, actual_match):
		actual_match = (' ').join(actual_match.split()) #Clean up any extra space by splitting and joining a first time
		splitted = actual_match.strip().split(" ")
		self.label = [splitted[1], splitted[3]]
		#print(f"Found labels: {self.label}")