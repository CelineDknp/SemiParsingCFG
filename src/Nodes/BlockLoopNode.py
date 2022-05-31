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
			self.branch_str = None
			self.condition_str = None

	def __str__(self):
		return f"Node {self.type} (block) until {self.until_condition}"

	def is_block(self):
		return True

	def is_close_node(self):
		return self.close_node

	def find_conditions(self, actual_match):
		until_start = actual_match.find(self.condition)
		if self.branch in actual_match:
			self.branch_str = actual_match[actual_match.find(self.branch):until_start].strip()
		self.condition_str = actual_match[until_start:].strip()

	def get_branch_str(self):
		return self.branch_str

	def get_condition_str(self):
		return self.condition_str
