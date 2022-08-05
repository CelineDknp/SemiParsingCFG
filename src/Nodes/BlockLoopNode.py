from .LoopNode import LoopNode
from Anchors import LoopAnchor
from Utils.config import *


class BlockLoopNode(LoopNode):

	def __init__(self, depth, node_type, anchor, close=False):
		super().__init__(depth, node_type, anchor)
		self.close_node = close
		if not close:
			self.branch = anchor.branch
			self.condition = anchor.condition
			self.branch_str = ""
			self.condition_str = ""

	def __str__(self):
		if self.is_close_node():
			return f"Node {self.type} (block end)"
		else:
			return f"Node {self.type} (block) {self.get_condition_str()}"

	def is_block(self):
		return True

	def is_close_node(self):
		return self.close_node

	#Points to target node: end block for the start, start for the end
	def set_target(self, target):
		self.target_node = target

	def get_target(self):
		return self.target_node

	def find_conditions(self, actual_match):
		until_start = actual_match.find(self.condition)
		if self.branch in actual_match:
			self.branch_str = actual_match[actual_match.find(self.branch):until_start].strip()
		self.condition_str = actual_match[until_start+len(self.condition):].strip()

	def get_branch_str(self):
		return self.branch_str

	def get_condition_str(self):
		return self.condition_str

	def set_condition_str(self, cond):
		self.condition_str = cond

	def get_end_block(self):
		for e in self.parents:
			if isinstance(e, BlockLoopNode):
				return e
