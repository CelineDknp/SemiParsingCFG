from LTSGraph.LTSGraph import LTSGraph


class TraceEquivalence:

	def __init__(self, g1, g2):
		self.g1 = g1
		self.g2 = g2
		self.visited_couples = []
		self.matched_transition_g1 = []
		self.matched_transition_g2 = []
		self.backG1 = []
		self.backG2 = []
		self.permutations = []
		self.back_permutations = []
		self.backtracking = False
		self.perform_followed = 0
		self.temp_visited = []
		self.equivalent = None

	def compare(self):
		g1_walker = self.g1.get_start()
		g2_walker = self.g2.get_start()
		self.walk(g1_walker, g2_walker)
		if self.equivalent:
			print("The graphs are trace equivalent !")
		else:
			print("The graphs are not trace equivalent")

	def consume_internal_transitions(self, node1, node2):
		keep_walking = False
		if node1.has_single_out():  # A single transition out will be ignored (TODO: check)
			node1_t= node1.get_transition()[0]
			if node1_t.get_label() == "INTERNAL":
				keep_walking = True
				self.matched_transition_g1.append(node1_t)
				node1 = node1.next()
			if node2.has_single_out():  # Same
				node2_t = node2.get_transition()[0]
				if node2_t.get_label() == "INTERNAL":
					self.matched_transition_g2.append(node2_t)
					node2 = node2.next()
		elif node2.has_single_out():  # A single transition out will be ignored (TODO: check)
			node2_t = node2.get_transition()[0]
			if node2_t.get_label() == "INTERNAL":
				self.matched_transition_g2.append(node2_t)
				keep_walking = True
				node2 = node2.next()
		return keep_walking, node1, node2

	def append_to_visited(self, elem):
		if elem not in self.visited_couples:
			self.visited_couples.append(elem)

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
						self.append_to_visited(elem)
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
			self.append_to_visited((node1,node2))
			keep_walking, node1, node2 = self.consume_internal_transitions(node1, node2)
			if keep_walking:
				self.walk(node1, node2)
			elif len(node1.get_transition()) == len(node2.get_transition()) == 0:
				print("This path is equivalent")
				if self.equivalent is None or self.equivalent:
					self.equivalent = True
					return
			else:
				#print("We need to compare two branches")
				transition_found = 0
				for t1 in node1.get_transition():
					for t2 in node2.get_transition():
						if t1.label == t2.label: #We found the same label, let's definitely go that way !
							if t1.label == "PERFORM": #We are following a perform, increment the counter
								self.perform_followed += 1
							self.permutations.append((t1.to, t2.to))
							self.matched_transition_g1.append(t1)
							self.matched_transition_g2.append(t2)
							transition_found += 1
						else:
							self.back_permutations.append((t1.to, t2.to))

				if (node1.tag == "COND_START" or node1.tag == "COND_START") and transition_found < len(node1.get_transition()) and transition_found < len(node2.get_transition()):
					print("Missing transitions, need to backtrack")
					self.backG1.append(node1)
					self.backG2.append(node2)
					self.backtracking = True
					if len(self.back_permutations) > 0:
						tup = self.back_permutations.pop()
						self.walk(tup[0], tup[1])
					else:
						print("wtf")
						pass
					print("We should branch")
				elif transition_found == 0:
					print("Graphs are not equivalent !")
					print(node1.initial_node)
					print(node2.initial_node)
					self.equivalent = False
					return
				else:
					self.back_permutations = []
					while len(self.permutations) > 0:
						elem = self.permutations.pop()
						if elem not in self.visited_couples:
							self.walk(elem[0], elem[1])

