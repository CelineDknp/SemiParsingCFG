from LTSGraph.LTSGraph import LTSGraph
from Nodes.ConditionNode import ConditionNode
from Nodes.ParseNode import ParseNode
from TraceMatch import TraceMatch
from equivalence_config import *
import os


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
		self.rematch = 0
		self.performs_G1 = []
		self.performs_G2 = []
		self.temp_visited = []
		self.equivalent = None

	def compare(self, draw=False, filepath="trace_equivalence_output/", name1="V1", name2="V2"):
		g1_walker = self.g1.get_start()
		g2_walker = self.g2.get_start()
		self.walk(g1_walker, g2_walker)
		if self.equivalent:
			print("The graphs are trace equivalent !")
		else:
			print("The graphs are not trace equivalent")
		if draw:
			self.output_to_file(filepath, name1, name2)

	def mark_and_move(self, node, transition):
		if self.g1.has_node(node):
			self.matched_transition_g1.append(transition)
		else:
			self.matched_transition_g2.append(transition)
		transition.set_match(1)
		return transition.to


	def consume_internal_transitions(self, node1, node2):
		keep_walking = False
		if node1.has_single_out(self.performs_G1):  # A single transition out will be ignored (TODO: check)
			node1_t = node1.get_single_transition(self.performs_G1)
			if node1_t.get_label() == ignore:
				keep_walking = True
				node1 = self.mark_and_move(node1, node1_t)
		if node2.has_single_out(self.performs_G2):  # A single transition out will be ignored (TODO: check)
			node2_t = node2.get_single_transition(self.performs_G2)
			if node2_t.get_label() == ignore:
				keep_walking = True
				node2 = self.mark_and_move(node2, node2_t)
		return keep_walking, node1, node2

	def append_to_visited(self, elem):
		if elem not in self.visited_couples:
			self.visited_couples.append(elem)

	def mark_as_visited(self, array):
		for node in array:
			#self.append_to_visited(node)
			for transition in node.get_transition():
				self.mark_and_move(node, transition)

	def compare_and_match(self, node1, node2):
		transition_found = 0
		match = False
		for t1 in node1.get_transition():
			for t2 in node2.get_transition():
				match = False
				if t1.label == t2.label or try_simple_equivalence(t1.label, t2.label):  # Easiest case, perfect match
					match = True
				if isinstance(node1.initial_node, ParseNode) and isinstance(node2.initial_node,
																			ParseNode):  # Change this
					match = True
				if match:
					t1.set_match(1) #Perfect match
					t2.set_match(1)
					if t2.label == "PERFORM": #If we are following a double perform, take node
						t_m = TraceMatch(t1.label, node1, node2, t1.to, t2.to, other_label = t2.label)
					else:
						t_m = TraceMatch(t1.label, node1, node2, t1.to, t2.to)
					self.permutations.append(t_m)
					self.matched_transition_g1.append(t1)
					self.matched_transition_g2.append(t2)
					transition_found += 1
				else:
					t_m = TraceMatch(t1.label, node1, node2, t1.to, t2.to, match=False, other_label=t2.label)
					self.back_permutations.append(t_m)
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
			self.mark_and_move(node, t)
			if t != transition:  # Lauch the tests on the out branches
				for node in branch_out[:-1]:
					self.walk(t.to, node)
			elif len(branch_out) > 0:
				self.walk(t.to, branch_out[-1])

	def mark_all_transition_as_matched(self, node):
		for t in node.get_transition():
			self.mark_and_move(node, t)

	def try_factorize_ifs(self, node1, node2):
		for t1 in node1.get_transition():
			for t2 in node2.get_transition():
				if len(t1.label) >= len(t2.label):  # Check which node should be factorized
					#print(f"Trying to match {t1.label}")
					res, cond, fact_nodes, branch_out = try_factorize(t1.label, node2)
					for t in node1.get_transition():
						self.mark_and_move(node1, t)
				else:
					#print(f"Trying to match {t2.label}")
					res, cond, fact_nodes, branch_out = try_factorize(t2.label, node1)
				if res:  # Factorize
					#print("Factorization worked !")
					#Mark all transitions from fact nodes as matched
					#self.mark_all_transition_as_matched(node1) #This one should be in fact_nodes
					self.mark_all_transition_as_matched(node2)
					for n in fact_nodes:
						self.mark_all_transition_as_matched(n)
					if t1.label == cond or try_simple_equivalence(t1.label, cond):
						self.walk_after_fact(node1, t1, branch_out)
					elif t2.label == cond or try_simple_equivalence(t2.label, cond):
						self.walk_after_fact(node2, t2, branch_out)
					return True
		else:
			return False

	def walk_trace_match(self, trace_match):
		couple = trace_match.get_couple()
		if couple not in self.visited_couples:
			if trace_match.followed_perform_node1():
				self.performs_G1.append(trace_match.node1_from)
			if trace_match.followed_perform_node2():
				self.performs_G2.append(trace_match.node2_from)
			self.walk(trace_match.node1_to, trace_match.node2_to)

	def walk(self, node1, node2):
		if self.equivalent != False:
			if self.backtracking:
				self.temp_visited.append((node1, node2))
			else:
				self.append_to_visited((node1, node2))
			keep_walking, node1, node2 = self.consume_internal_transitions(node1, node2)
			if keep_walking:
				self.walk(node1, node2)
			elif len(node1.get_transition()) == len(node2.get_transition()) == 0 or (node1.get_tag() == "END" and node2.get_tag()=="END"): #Try and stop at the end
				if self.backtracking:
					self.backtracking = False  # Don't change this if we are not done backtracking
					self.permutations = []
					#self.backG1.pop()
					#self.backG2.pop()
					for elem in self.temp_visited:
						self.append_to_visited(elem)
					self.temp_visited = []
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
					if len(self.back_permutations) > 0:
						self.backtracking = True
						self.walk_trace_match(self.back_permutations.pop())
					else:
						print("wtf")
						pass
					print("We should branch")
				elif transition_found == 0:
					if self.rematch >= rematch:#We have tried everything
						print("Graphs are not equivalent !")
						print(node1.initial_node)
						print(node2.initial_node)
						self.equivalent = False
						return
					else:
						self.rematch += 1
						self.backG1.append(node1)
						self.backG2.append(node2)
						while len(self.back_permutations) > 0:
							self.backtracking = True
							self.walk_trace_match(self.back_permutations.pop())
				else: #Looks like we found our way
					self.back_permutations = []
					while len(self.permutations) > 0:
						self.walk_trace_match(self.permutations.pop())

	def output_to_file(self, filepath, file1, file2):
		file1 = file1.split("/")[-1][:-4]+"_V1.COB"
		file2 = file2.split("/")[-1][:-4]+"_V2.COB"
		full_path = filepath+file1
		path_tab = full_path.split("/")
		dir = path_tab[:-1]
		dir_path = "/".join(dir)
		if not os.path.exists(dir_path):
			#os.mkdir(dir_path)
			pass
		with open(filepath+file1, "w+") as file:
			file.write("digraph "+file1+"V1 {\n")
			for node in self.g1.all_states:
				file.write("node\n")
				file.write(f"{node.id} [{str(node.initial_node)}]\n")
			for transition in self.g1.all_transitions:
				file.write(f"{transition.fr.id} -> {transition.to.id} [match:{transition.match}]\n")

		with open(filepath+file2, "w+") as file:
			file.write("digraph "+file2+"V2 {\n")
			for node in self.g2.all_states:
				file.write("node\n")
				file.write(f"{node.id} [{str(node.initial_node)}]\n")
			for transition in self.g2.all_transitions:
				file.write(f"{transition.fr.id} -> {transition.to.id} [match:{transition.match}]\n")

