class Node:

	def __init__(self, depth, type):
		self.depth = depth
		self.type = type

	def __str__(self):
		return f"Node {self.type} at depth {self.depth}"

	def __repr__(self):
		return f"Node {self.type}"

	def get_depth(self):
		return self.depth