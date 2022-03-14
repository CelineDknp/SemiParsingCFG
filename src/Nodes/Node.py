class Node:
	id = 0
	def __init__(self, depth, type):
		self.depth = depth
		self.type = type
		self.childs = []
		self.parents = []
		self.id = Node.id 
		Node.id += 1

	def __str__(self):
		return self.depth*"\t"+f"Node {self.id} {self.type} at depth {self.depth}"

	def __repr__(self):
		return f"Node {self.id} {self.type}"

	def get_depth(self):
		return self.depth

	def get_type(self):
		return self.type

	def point_to_one(self):
		return len(self.childs) == 1

	def get_last_childs_helper(self, visited):
		if self not in visited:
			visited.append(self)
		if len(self.get_childs()) == 0:
			return [self]
		else:
			return [child.get_last_childs_helper(visited) for child in self.get_childs() if child not in visited]


	def get_last_childs(self):
		# print(f"Looking for children in {self}: {self.get_childs()} !", flush=True)
		if len(self.get_childs()) == 0:
			return [self]
		else:
			return self.get_last_childs_helper([])

	def get_childs(self):
		# print(f">>> In get_childs of Node {self}")
		return self.childs

	def add_child(self, node):
		if node == self: #Don't add yourself as a child ! #Dirtyfix
			print(">>> Trying to add myself as child (Node)")
			return
		if node in self.childs: #Dirty
			return
		self.childs.append(node)
		node.add_parent(self)

	def remove_child(self, node):
		if node in self.childs:
			self.childs.remove(node)
			node.remove_parent(self)

	def get_parent(self):
		return self.parents

	def add_parent(self, node):
		if node == self: #Don't add yourself as a child ! #Dirtyfix
			print(">>> Trying to add myself as parent (Node)")
			return
		if node in self.parents: #Dirty
			return
		self.parents.append(node)

	def remove_parent(self, node):
		if node in self.parents:
			self.parents.remove(node)