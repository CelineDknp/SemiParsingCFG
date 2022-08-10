from LTSGraph.LTSGraph import LTSGraph

class TraceEquivalence:

	def __init__(self, g1, g2):
		self.g1 = g1
		self.g2 = g2
		self.visited_g1 = []
		self.visited_g2 = []
		self.backG1 = []
		self.backG2 = []
		self.permutations = []
		self.backtracking = False
		self.temp_visited = []

	def compare(self):
		g1_walker = self.g1.get_start()
		g2_walker = self.g2.get_start()
		self.walk(g1_walker, g2_walker)

	def consume_internal_transitions(self, node1, node2):
		keep_walking = False
		if node1.has_single_out():  # A single transition out will be ignored (TODO: check)
			node1_tag = node1.get_transition()[0].get_label()
			if node1_tag == "INTERNAL":
				keep_walking = True
				node1 = node1.next()
			if node2.has_single_out():  # Same
				if node1_tag == node2.get_transition()[0].get_label():
					node2 = node2.next()
		elif node2.has_single_out():  # A single transition out will be ignored (TODO: check)
			node2_tag = node2.get_transition()[0].get_label()
			if node2_tag == "INTERNAL":
				keep_walking = True
				node2 = node2.next()
		return (keep_walking, node1, node2)

	def append_to_visited(self, node, array):
		if node not in array:
			array.append(node)

	def walk(self, node1, node2):
		if self.backtracking:
			self.temp_visited.append((node1, node2))
			keep_walking, node1, node2 = self.consume_internal_transitions(node1, node2)
			if keep_walking:
				self.walk(node1, node2)
			else:
				if node1.get_tag() == node2.get_tag():
					self.backtracking = False #We found our way !
					self.permutations = []
					self.backG1.pop()
					self.backG2.pop()
					for elem in self.temp_visited:
						self.append_to_visited(elem[0], self.visited_g1)
						self.append_to_visited(elem[1], self.visited_g2)
					self.walk(node1, node2)
				else:
					self.temp_visited = []
					if len(self.permutations) > 0:
						tup = self.permutations.pop()
						self.walk(tup[0], tup[1])
					else:
						print("Graphs are not trace equivalent !")
						return
		else:
			self.append_to_visited(node1, self.visited_g1)
			self.append_to_visited(node2, self.visited_g2)
			keep_walking, node1, node2 = self.consume_internal_transitions(node1, node2)
			if keep_walking:
				self.walk(node1, node2)
			else:
				print("We are at two nodes that branch !")
				print(f"Node G1: {node1}")
				print(f"Node G2: {node2}")
				self.backG1.append(node1)
				self.backG2.append(node2)
				self.backtracking = True
				for t1 in node1.get_transition():
					for t2 in node2.get_transition():
						self.permutations.append((t1.to, t2.to))
						if t1.label == t2.label: #We found the same label, let's definitely go that way !
							self.walk(t1.to, t2.to)
				tup = self.permutations.pop()
				self.walk(tup[0], tup[1])