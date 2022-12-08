from LTSGraph.LTSGraph import LTSGraph
from Nodes.ConditionNode import ConditionNode
from Nodes.ParseNode import ParseNode
from TraceMatch import TraceMatch
from equivalence_config import *


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
		self.performs_G1 = []
		self.performs_G2 = []
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
		if node1.has_single_out(self.performs_G1):  # A single transition out will be ignored (TODO: check)
			node1_t = node1.get_single_transition(self.performs_G1)
			if node1_t.get_label() == ignore:
				keep_walking = True
				self.matched_transition_g1.append(node1_t)
				node1 = node1_t.to
			if node2.has_single_out(self.performs_G2):  # Same
				node2_t = node2.get_single_transition(self.performs_G2)
				if node2_t.get_label() == ignore:
					self.matched_transition_g2.append(node2_t)
					node2 = node2_t.to
		elif node2.has_single_out(self.performs_G2):  # A single transition out will be ignored (TODO: check)
			node2_t = node2.get_single_transition(self.performs_G2)
			if node2_t.get_label() == ignore:
				self.matched_transition_g2.append(node2_t)
				keep_walking = True
				node2 = node2_t.to
		return keep_walking, node1, node2

	def append_to_visited(self, elem):
		if elem not in self.visited_couples:
			self.visited_couples.append(elem)

	def mark_as_visited(self, array):
		for node in array:
			self.append_to_visited(node)
			for transition in node.get_transition():
				self.matched_transition_g1.append(transition) if self.g1.has_node(
					node) else self.matched_transition_g2.append(transition)

	def compare_and_match(self, node1, node2):
		match = False
		transition_found = 0
		for t1 in node1.get_transition():
			for t2 in node2.get_transition():
				if t1.label == t2.label or try_simple_equivalence(t1.label, t2.label):  # Easiest case, perfect match
					match = True
				if isinstance(node1.initial_node, ParseNode) and isinstance(node2.initial_node,
																			ParseNode):  # Change this
					match = True
				if match:
					t_m = TraceMatch(t1.label, node1, node2, t1.to, t2.to)
					self.permutations.append(t_m)
					self.matched_transition_g1.append(t1)
					self.matched_transition_g2.append(t2)
					transition_found += 1
				else:
					self.back_permutations.append((t1.to, t2.to))
		return match, transition_found

	def try_if_to_evaluate(self, node1, node2):
		(array, couple_array), was_node_2 = try_transformations(node1, node2)
		if array is not None:
			self.mark_as_visited(array)
			if was_node_2:
				self.mark_as_visited([node2])
			else:
				self.mark_as_visited([node1])
			for couple in couple_array:
				self.walk(couple[0], couple[1])
			return True
		return False

	def walk_after_fact(self, node, transition, branch_out):
		for t in node.get_transition():
			if t != transition:  # Lauch the tests on the out branches
				for node in branch_out[:-1]:
					self.walk(t.to, node)
			elif len(branch_out) > 0:
				self.walk(t.to, branch_out[-1])

	def try_factorize_ifs(self, node1, node2):
		for t1 in node1.get_transition():
			for t2 in node2.get_transition():
				if len(t1.label) >= len(t2.label):  # Check which node should be factorized
					print(f"Trying to match {t1.label}")
					res, cond, fact_nodes, branch_out = try_factorize(t1.label, node2)
				else:
					print(f"Trying to match {t2.label}")
					res, cond, fact_nodes, branch_out = try_factorize(t2.label, node1)
				if res:  # Factorize
					print("Factorization worked !")
					self.mark_as_visited(fact_nodes)
					if t1.label == cond or try_simple_equivalence(t1.label, cond):
						self.walk_after_fact(node1, t1, branch_out)
					elif t2.label == cond or try_simple_equivalence(t2.label, cond):
						self.walk_after_fact(node2, t2, branch_out)
					return True
		else:
			return False

	def walk(self, node1, node2):
		if self.equivalent != False:
			if self.backtracking:
				self.temp_visited.append((node1, node2))
				keep_walking, node1, node2 = self.consume_internal_transitions(node1, node2)
				if keep_walking:
					self.walk(node1, node2)
				else:
					if node1.get_tag() == node2.get_tag():
						self.backtracking = False  # We found our way !
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
				self.append_to_visited((node1, node2))
				keep_walking, node1, node2 = self.consume_internal_transitions(node1, node2)
				if keep_walking:
					self.walk(node1, node2)
				elif len(node1.get_transition()) == len(node2.get_transition()) == 0:
					print("This path is equivalent")
					if self.equivalent is None or self.equivalent:
						self.equivalent = True
						return
				else:
					# print("We need to compare two branches")
					match, transition_found = self.compare_and_match(node1, node2)
					if not match:
						if isinstance(node1.initial_node, ConditionNode) and isinstance(node2.initial_node,
																						ConditionNode):
							if self.try_if_to_evaluate(node1, node2):
								return
							if self.try_factorize_ifs(node1, node2):
								return

					if (node1.tag == "COND_START" or node2.tag == "COND_START") and transition_found < len(
							node1.get_transition()) and transition_found < len(node2.get_transition()):
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
							t_m = self.permutations.pop()
							couple = t_m.get_couple()
							if couple not in self.visited_couples:
								if t_m.followed_perform():
									self.performs_G1.append(t_m.node1_from)
									self.performs_G2.append(t_m.node2_from)
								self.walk(t_m.node1_to, t_m.node2_to)
