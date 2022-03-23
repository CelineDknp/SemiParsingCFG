from Nodes.LabelLoopNode import LabelLoopNode
import re


class MultipleLabelLoopNode(LabelLoopNode):

	def __init__(self, depth, node_type, anchor):
		super().__init__(depth, node_type, anchor)
		self.separator = anchor.get_separator()

	def __str__(self):
		return f"Node {self.type} (multiple labels) to {self.label}"

	def go_back_label(self):
		if self.go_back:
			return self.label[-1]

	def is_label(self):
		return True

	def is_complete(self):
		if self.go_back:
			return len(self.childs) == len(self.label)+1 #One child is the next node, one because of the loop
		else:
			return len(self.childs) == len(self.label)+1

	def is_multiple_labels(self):
		return True

	def find_label(self, input_str, pos):
		self.label = []
		res = self.get_label_regex().search(input_str[pos:].upper())
		self.label.append(res.group(0).strip())
		pos = input_str.upper().find(res.group(0), pos) + len(res.group(0).rstrip())
		# print(f"[MOVING POS 1] Current state of input is: |{input_str[pos:pos+150]}|")
		res = self.separator.search(input_str[pos:].upper())
		pos = input_str.upper().find(res.group(0), pos) + len(res.group(0).rstrip())
		# print(f"[MOVING POS 2]Current state of input is: |{input_str[pos:pos+150]}|")
		res = self.get_label_regex().search(input_str[pos:].upper())
		self.label.append(res.group(0).strip())
		# print(f"Label found: {self.label}")
		pos = input_str.upper().find(res.group(0), pos) + len(res.group(0).rstrip())

		# print(f"[MOVING POS 3]Current state of input is: |{input_str[pos:pos+150]}|")
		return pos