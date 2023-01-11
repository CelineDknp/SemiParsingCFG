from .Node import Node
from Utils.config import *
from Utils.constants import *


class LoopNode(Node):

	def __init__(self, depth, node_type, anchor):
		super().__init__(depth, node_type, anchor.get_regex())
		self.go_back = anchor.is_goback_anchor()

	def __str__(self):
		#return f"Node {self.type} (simple) to {self.label}"
		if self.is_goback_node():
			return f"PERFORM {self.label}"
		elif self.is_control():
			return "NEXT SENTENCE"
		elif not self.is_goback_node():
			return f"GO TO {self.label}"
		elif self.is_block():
			return "Bloc ?"
		else:
			return super().__str__()

	def is_goback_node(self):
		return self.go_back

	def is_control(self):
		return False

	def is_multiple_labels(self):
		return False

	def is_label(self):
		return False

	def is_block(self):
		return False

	def add_child(self, node, match=False):
		if self.is_label():
			if node.get_type() != NODE_LABEL and not self.is_goback_node() and not self.is_block():  # We don't want the child
				return
		elif self.is_control():
			if not match:
				return
		super().add_child(node)

	def is_complete(self):
		if self.go_back:
			return len(self.childs) == 2 #One child is the next node, one because of the loop
		else:
			return len(self.childs) == 1

	def go_back_label(self):
		if self.go_back:
			return self.label
