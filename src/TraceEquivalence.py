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
		self.all_paths_g1 = []
		self.all_paths_g2 = []
		self.current_path_g1 = []
		self.current_path_g2 = []
		self.visited_couples = []
		self.matched_transition_g1 = []
		self.matched_transition_g2 = []
		self.backG1 = []
		self.backG2 = []
		self.permutations = []
		self.temp_permutations =[]
		self.back_permutations = []
		self.backtracking = False
		self.current_back_track = None
		self.rematch = 0
		self.performs_G1 = []
		self.temp_performs_G1 = []
		self.performs_G2 = []
		self.temp_performs_G2 = []
		self.temp_visited = []
		self.temp_links_matched = []
		self.correct_backtrack = 0
		self.equivalent = None

	def compare(self, draw=False, filepath="trace_equivalence_output/", name1="V1", name2="V2"):
		g1_walker = self.g1.get_start()
		g2_walker = self.g2.get_start()
		t_m = TraceMatch("", None, None, g1_walker, g2_walker)
		self.walk(t_m)
		if self.equivalent:
			print("The graphs are trace equivalent !")
		else:
			print("The graphs are not trace equivalent")
		if draw:
			self.output_to_file(filepath, name1, name2)

	def mark_transition(self, transition):
		if self.g1.has_node(transition.fr) and transition not in self.matched_transition_g1:
			self.matched_transition_g1.append(transition)
		elif transition not in self.matched_transition_g2:
			self.matched_transition_g2.append(transition)

	def mark_and_move(self, node, transition):
		if not self.backtracking:
			transition.set_match(1)
			self.mark_transition(transition)
		else:
			self.temp_links_matched.append(transition)
		return transition.to

	def relevant_goback(self, node, perform_list):
		last_perform = perform_list[-1] #Can we only goback to the last perform ?
		for t in node.get_transition():
			if t.get_label() == goback and t.to == last_perform:
				perform_list.remove(t.to)
				return t
		return None

	def consume_internal_transitions(self, trace_match):
		node1 = trace_match.node1()
		node2 = trace_match.node2()
		keep_walking = False
		new_node1 = None
		new_node2 = None
		if len(self.performs_G1) > 0: #If we have followed performs
			t = self.relevant_goback(node1, self.performs_G1)
			if t is not None:
				keep_walking = True
				new_node1 = self.mark_and_move(node1, t)
		if len(self.performs_G2) > 0:
			t = self.relevant_goback(node2, self.performs_G2)
			if t is not None:
				keep_walking = True
				new_node2 = self.mark_and_move(node2, t)
		if new_node1 is None and node1.has_single_out(self.performs_G1):  # A single transition out will be ignored (TODO: check)
			node1_t = node1.get_single_transition(self.performs_G1)
			if node1_t.get_label() == ignore:
				keep_walking = True
				new_node1 = self.mark_and_move(node1, node1_t)
		if new_node2 is None and node2.has_single_out(self.performs_G2):  # A single transition out will be ignored (TODO: check)
			node2_t = node2.get_single_transition(self.performs_G2)
			if node2_t.get_label() == ignore:
				keep_walking = True
				new_node2 = self.mark_and_move(node2, node2_t)
		if new_node1 is not None:
			if new_node2 is not None:
				t_m = TraceMatch(ignore, node1, node2, new_node1, new_node2) #All new nodes
			else:
				t_m = TraceMatch(ignore, node1, trace_match.node2_from, new_node1, node2) #Only node 1 changes
		else:
			if new_node2 is not None:
				t_m = TraceMatch(ignore, trace_match.node1_from, node2, node1, new_node2) #Only node 1 changes
			else:
				t_m = trace_match
		return keep_walking, t_m

	def append_to_visited(self, elem):
		if elem not in self.visited_couples:
			self.visited_couples.append(elem)

	def mark_as_visited(self, array):
		for node in array:
			for transition in node.get_transition():
				self.mark_and_move(node, transition)

	def compare_and_match(self, node1, node2):
		transition_found = 0
		match = False
		for t1 in node1.get_transition():
			for t2 in node2.get_transition():
				self.mark_transition(t1)
				self.mark_transition(t2)
				match = False
				if t1.label == t2.label or (node1.has_condition() and node2.has_condition() and try_simple_equivalence(t1.label, t2.label)):  # Easiest case, perfect match
					match = True

				if isinstance(node1.initial_node, ParseNode) and isinstance(node2.initial_node,	ParseNode):  # Change this
					match = True
				if match:
					if self.backtracking:
						self.temp_links_matched.append(t1)
						self.temp_links_matched.append(t2)
					else:
						t1.set_match(1) #Perfect match
						t2.set_match(1)
					if t2.label == "PERFORM": #If we are following a double perform, take node
						t_m = TraceMatch(t1.label, node1, node2, t1.to, t2.to, other_label = t2.label)
					else:
						t_m = TraceMatch(t1.label, node1, node2, t1.to, t2.to)
					if t_m not in self.visited_couples and t_m not in self.permutations: #Don't add if it is already visited or queued
						if self.backtracking:
							if t_m not in self.temp_visited:
								self.temp_permutations.append(t_m)
						else:
							self.permutations.append(t_m)
					transition_found += 1
					break #We found a match for the transition, no need to explore further !!! skip backtracking ???
					#TODO: list like we do with the backtracks ? : opti
				else:
					if not self.backtracking:
						t_m = TraceMatch(t1.label, node1, node2, t1.to, t2.to, match=False, other_label=t2.label)
						self.back_permutations.append(t_m)
		match = transition_found >= self.transition_number(node1, node2)
		return match, transition_found #Change this to match the expected number of transition

	def try_if_to_evaluate(self, node1, node2):
		(array, couple_array, transitions_to_match), was_node_2 = try_transformations(node1, node2)
		if array is not None:
			self.mark_as_visited(array)
			if was_node_2:
				self.mark_as_visited([node2])
			else:
				self.mark_as_visited([node1])
			for t in transitions_to_match:
				self.mark_transition(t)
				t.set_match(1)
			self.back_permutations = []
			for couple in couple_array:
				self.walk(couple)
			return True
		return False

	def walk_after_fact(self, node, transition, branch_out):
		for t in node.get_transition():
			self.mark_and_move(node, t)
			if t != transition:  # Lauch the tests on the out branches
				for node in branch_out[:-1]:
					t_m = TraceMatch("", None, None, t.to, node, match=True) # TODO check
					self.walk(t_m)
			elif len(branch_out) > 0:
				self.back_permutations = []
				t_m = TraceMatch("", None, None, t.to, branch_out[-1], match=True)  # TODO check
				self.walk(t_m)

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
		if trace_match not in self.visited_couples or (self.backtracking and trace_match not in self.temp_visited): # Usure
			if trace_match.followed_perform_node1():
				self.performs_G1.append(trace_match.node1_from)
			if trace_match.followed_perform_node2():
				self.performs_G2.append(trace_match.node2_from)
			self.walk(trace_match)

	def mark_unsure(self, node):
		for t in node.get_transition():
			t.set_match(0)

	def mark_matched(self, node):
		for t in node.get_transition():
			t.set_match(1)

	def transition_number(self, node1, node2):
		return len(node1.get_transition()) if len(node1.get_transition()) >= len(node2.get_transition()) else len(node2.get_transition())

	def backtrack(self, node1, node2):
		#self.backG1.append(node1)
		#self.backG2.append(node2)
		goal = 0
		if rematch_mode == "skip_left" or rematch_mode == "skip_both":
			self.mark_unsure(node1)
		elif rematch_mode == "skip_right" or rematch_mode == "skip_both":
			self.mark_unsure(node2)
		if rematch_mode == "skip_left":
			for t in node1.get_transition():
				goal += self.transition_number(t.to, node2)
				self.backtracking = True
				self.current_back_track = TraceMatch("Skipped", node1, node2, t.to, node2, match=False)
				self.walk_trace_match(self.current_back_track)

		elif rematch_mode == "skip_right":
			for t in node2.get_transition():
				goal += self.transition_number(t.to, node1)
				self.backtracking = True
				self.current_back_track = TraceMatch("Skipped", node1, node2, node1, t.to, match=False)
				self.walk_trace_match(self.current_back_track)
		else:
			goal = self.transition_number(node1, node2)
			while len(self.back_permutations) > 0 and self.correct_backtrack < goal:
				self.backtracking = True
				self.current_back_track = self.back_permutations.pop()
				self.walk_trace_match(self.current_back_track)
		if self.correct_backtrack >= goal: #Did the backtrack work ?
			pass
		else:
			self.equivalent = False
			print("Backtrack couldn't work !")
			print(self.current_back_track.node1_from.initial_node)
			print(self.current_back_track.node2_from.initial_node)
			self.rematch = 0
			return
		self.correct_backtrack = 0

	def valid_backtrack(self):
		self.backtracking = False
		self.rematch = 0 #We found our way so reset rematches
		#self.permutations = []
		for elem in self.temp_visited:
			self.append_to_visited(elem)
		self.temp_visited = []
		for link in self.temp_links_matched:
			self.mark_and_move(link.fr, link)
		for elem in self.temp_permutations:
			if elem not in self.permutations and elem not in self.visited_couples:
				self.permutations.append(elem)
		self.temp_permutations = []
		self.temp_links_matched = []
		self.correct_backtrack += 1
		to_remove = []
		node1_back = self.current_back_track.node1_to
		node2_back = self.current_back_track.node2_to
		for elem in self.back_permutations:
			if elem.node1_to == node1_back or elem.node2_to == node1_back:
				to_remove.append(elem)
			elif elem.node1_to == node2_back or elem.node2_to == node2_back:
				to_remove.append(elem)
		for elem in to_remove: #Remove all elems that have no chance to be a good backtrack
			if elem in self.back_permutations:
				self.back_permutations.remove(elem)

	def invalid_backtrack(self):
		self.backtracking = False
		print("Backtrack failed !")
		self.temp_visited = []
		self.temp_links_matched = []

	def walk(self, trace_match):
		node1 = trace_match.node1()
		node2 = trace_match.node2()
		if not self.backtracking:
			self.current_path_g1.append(node1)
			self.current_path_g2.append(node2)
		if self.equivalent != False:
			if self.backtracking:
				self.temp_visited.append(trace_match)
			else:
				self.append_to_visited(trace_match)
			keep_walking, new_trace_match = self.consume_internal_transitions(trace_match)
			if keep_walking:
				self.walk(new_trace_match)
			elif len(node1.get_transition()) == len(node2.get_transition()) == 0 or (node1.get_tag() == "END" and node2.get_tag()=="END"): #Try and stop at the end
				if self.backtracking:
					self.valid_backtrack()
				print("This path is equivalent")
				self.all_paths_g1.append(self.current_path_g1)
				self.all_paths_g2.append(self.current_path_g2)
				self.current_path_g1 = []
				self.current_path_g2 = []
				if self.equivalent is None or self.equivalent:
					self.equivalent = True
					return
			else:
				# print("We need to compare two branches")
				match, transition_found = self.compare_and_match(node1, node2)
				if not match:
					if isinstance(node1.initial_node, ConditionNode) and isinstance(node2.initial_node, ConditionNode):
						if self.try_if_to_evaluate(node1, node2):
							self.back_permutations = []
							return
						if self.try_factorize_ifs(node1, node2):
							self.back_permutations = []
							return
				if (node1.tag == "COND_START" or node2.tag == "COND_START") and transition_found < len(
						node1.get_transition()) and transition_found < len(node2.get_transition()):
					print("Missing transitions, need to backtrack")
					self.backtrack(node1, node2) #We only need to count a rematch if we are not trying if branches
				elif not match:
					if self.backtracking:
						self.invalid_backtrack()
					else:
						if self.rematch >= rematch:#We have tried everything
							print("Graphs are not equivalent !")
							print(node1.initial_node)
							print(node2.initial_node)
							self.equivalent = False
						else:
							self.rematch += 1
							self.backtrack(node1, node2)
				else: #Looks like we found our way
					if not self.backtracking:
						self.back_permutations = []
					if self.backtracking: #We were backtracking but we found a match on this path !
						self.valid_backtrack()
						#while len(self.temp_permutations) > 0:
						#	self.walk_trace_match(self.temp_permutations.pop())
					while len(self.permutations) > 0:
						self.walk_trace_match(self.permutations.pop())

	def output_to_file(self, filepath, file1, file2):
		file1 = file1.split("/")[-1][:-4]+"_V1.gv"
		file2 = file2.split("/")[-1][:-4]+"_V2.gv"
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

