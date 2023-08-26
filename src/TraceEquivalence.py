from LTSGraph.LTSGraph import LTSGraph
from Nodes.ConditionNode import ConditionNode
from Nodes.ParseNode import ParseNode
from Nodes.BlockLoopNode import BlockLoopNode
from TraceMatch import TraceMatch
from equivalence_config import *
import os


class TraceEquivalence:

	def __init__(self, g1, g2):
		self.g1 = g1
		self.g2 = g2
		self.bag_g1 = set()
		self.bag_g2 = set()
		self.back_bag_g1 = set()
		self.back_bag_g2 = set()
		self.all_paths_g1 = []
		self.all_paths_g2 = []
		self.current_path_g1 = []
		self.current_path_g2 = []
		self.visited_couples = []
		self.matched_transition_g1 = []
		self.matched_transition_g2 = []
		self.backG1 = []
		self.backG2 = []
		self.skipped_links = []
		self.permutations = []
		self.error = 0
		self.temp_permutations =[]
		self.back_permutations = []
		self.tried_permutations = []
		self.backtracking = False
		self.current_back_track = None
		self.starting_backtrack = None
		self.backtrack_mode = ""
		self.rematch = 0
		self.loc_rematch = 0
		self.performs_G1 = []
		self.temp_performs_G1 = []
		self.performs_G2 = []
		self.temp_performs_G2 = []
		self.temp_visited = []
		self.temp_links_matched = []
		self.temp_unsure = []
		self.correct_backtrack = 0
		self.backtrack_goal = 0
		self.equivalent = True
		self.rematch_type = rematch_type

	def is_equivalent(self):
		return self.equivalent

	def compare(self, draw=False, filepath="trace_equivalence_output/", name1="V1", name2="V2"):
		g1_walker = self.g1.get_start()
		g2_walker = self.g2.get_start()
		t_m = TraceMatch("", None, None, g1_walker, g2_walker, self.performs_G1, self.performs_G2)
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
		elif self.g2.has_node(transition.fr) and transition not in self.matched_transition_g2:
			self.matched_transition_g2.append(transition)
		#Else, already matched transition

	def mark_group_match(self, node1, node2):
		node1.group_match(node2)
		node2.group_match(node1)

	def mark_and_move(self, node, transition, force_match=False):
		if not self.backtracking or force_match:
			transition.set_match(self.error, 1)
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

	def add_bag_g1(self, node):
		if self.backtracking:
			self.back_bag_g1.add(node)
		else:
			self.bag_g1.add(node)

	def add_bag_g2(self, node):
		if self.backtracking:
			self.back_bag_g2.add(node)
		else:
			self.bag_g2.add(node)

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
				self.add_bag_g1(node1)
		if len(self.performs_G2) > 0:
			t = self.relevant_goback(node2, self.performs_G2)
			if t is not None:
				keep_walking = True
				new_node2 = self.mark_and_move(node2, t)
				self.add_bag_g2(node2)
		if new_node1 is None and node1.has_single_out(self.performs_G1):  # A single transition out will be ignored (TODO: check)
			node1_t = node1.get_single_transition(self.performs_G1, self.temp_performs_G1)
			if node1_t.get_label() == ignore or node1_t.get_label() == perform:
				keep_walking = True
				new_node1 = self.mark_and_move(node1, node1_t)
				self.add_bag_g1(node1)
				if node1_t.get_label() == perform: #and node1 not in self.temp_performs_G1:
					self.performs_G1.append(node1)
					self.temp_performs_G1.append(node1)
		if new_node2 is None and node2.has_single_out(self.performs_G2):  # A single transition out will be ignored (TODO: check)
			node2_t = node2.get_single_transition(self.performs_G2, self.temp_performs_G2)
			if node2_t.get_label() == ignore or node2_t.get_label() == perform:
				keep_walking = True
				new_node2 = self.mark_and_move(node2, node2_t)
				self.add_bag_g2(node2)
				if node2_t.get_label() == perform: #and node2 not in self.temp_performs_G2:
					self.performs_G2.append(node2)
					self.temp_performs_G2.append(node2)
		if new_node1 is not None:
			if new_node2 is not None:
				t_m = TraceMatch(ignore, node1, node2, new_node1, new_node2, self.performs_G1, self.performs_G2) #All new nodes
			else:
				t_m = TraceMatch(ignore, node1, trace_match.node2_from, new_node1, node2, self.performs_G1, self.performs_G2) #Only node 1 changes
		else:
			if new_node2 is not None:
				t_m = TraceMatch(ignore, trace_match.node1_from, node2, node1, new_node2, self.performs_G1, self.performs_G2) #Only node 1 changes
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
						t1.set_match(self.error, 1) #Perfect match
						t2.set_match(self.error,1)
						self.mark_group_match(node1, node2)
					if t2.label == perform: #If we are following a double perform, take node
						t_m = TraceMatch(t1.label, node1, node2, t1.to, t2.to, self.performs_G1, self.performs_G2, other_label = t2.label)
					else:
						t_m = TraceMatch(t1.label, node1, node2, t1.to, t2.to, self.performs_G1, self.performs_G2)
					if t_m not in self.visited_couples and t_m not in self.permutations: #Don't add if it is already visited or queued
						if self.backtracking:
							if t_m not in self.temp_visited:
								self.temp_permutations.append(t_m)
						else:
							if not self.already_seen(t_m):
								self.permutations.append(t_m)
					transition_found += 1
					break #We found a match for the transition, no need to explore further !!! skip backtracking ???
					#TODO: list like we do with the backtracks ? : opti
		match = transition_found >= self.transition_number(node1, node2)
		if not match and not self.backtracking:
			self.total_unmatch(node1, node2)
		return match, transition_found #Change this to match the expected number of transition

	def try_if_to_evaluate(self, node1, node2):
		(array, couple_array, transitions_to_match, exit_transitions), was_node_2 = try_transformations(node1, node2, self.performs_G1, self.performs_G2)
		if array is not None:
			self.mark_as_visited(array)
			if was_node_2:
				self.mark_as_visited([node2])
				for e in array:
					self.mark_group_match(node2, e)
			else:
				self.mark_as_visited([node1])
				for e in array:
					self.mark_group_match(node1, e)
			for t in transitions_to_match:
				self.mark_transition(t)
				t.set_match(self.error, 1)
			self.back_permutations = []
			if self.backtracking:
				self.valid_backtrack()
			for couple in couple_array:
				if not self.already_seen(couple):
					self.walk(couple)
			return True
		return False

	def walk_after_fact(self, node, transition, branch_out):
		for t in node.get_transition():
			self.mark_and_move(node, t)
			if t != transition:  # Lauch the tests on the out branches
				for node in branch_out[:-1]:
					t_m = TraceMatch("", None, None, t.to, node, self.performs_G1, self.performs_G2, match=True) # TODO check
					self.walk(t_m)
			elif len(branch_out) > 0:
				self.back_permutations = []
				t_m = TraceMatch("", None, None, t.to, branch_out[-1], self.performs_G1, self.performs_G2, match=True)  # TODO check
				self.walk(t_m)

	def mark_all_transition_as_matched(self, node):
		for t in node.get_transition():
			if -1 in t.match:#If we marked it wrong, remove
				t.match.remove(-1)
			self.mark_and_move(node, t)

	def try_factorize_ifs(self, node1, node2):
		for t1 in node1.get_transition():
			for t2 in node2.get_transition():
				if len(t1.label) >= len(t2.label):  # Check which node should be factorized
					#print(f"Trying to match {t1.label}")
					res, cond, fact_nodes, branch_out = try_factorize(t1.label, node2)
					#for t in node1.get_transition():
					#	self.mark_and_move(node1, t)
				else:
					#print(f"Trying to match {t2.label}")
					res, cond, fact_nodes, branch_out = try_factorize(t2.label, node1)
				if res:  # Factorize
					self.mark_all_transition_as_matched(node2)
					for n in fact_nodes:
						self.mark_all_transition_as_matched(n)
						if cond == node1.initial_node.condition:
							self.mark_group_match(node1, n)
						else:
							self.mark_group_match(node2, n)
					if self.backtracking:
						self.valid_backtrack()
					if t1.label == cond or try_simple_equivalence(t1.label, cond):
						self.walk_after_fact(node1, t1, branch_out)
					elif t2.label == cond or try_simple_equivalence(t2.label, cond):
						self.walk_after_fact(node2, t2, branch_out)
					return True
		else:
			return False

	def walk_trace_match(self, trace_match):
		if trace_match not in self.visited_couples:
			if trace_match.followed_perform_node1():
				self.performs_G1.append(trace_match.node1_from)
				self.temp_performs_G1.append(trace_match.node1_from)
			if trace_match.followed_perform_node2():
				self.performs_G2.append(trace_match.node2_from)
				self.temp_performs_G2.append(trace_match.node2_from)
			if (not self.backtracking and not self.already_seen(trace_match)) or (self.backtracking and not self.has_tried_permutation(trace_match)):
				self.walk(trace_match)
			else:
				if self.backtracking and len(self.back_permutations) > 0:
					self.walk_trace_match(self.back_permutations.pop())
				elif not self.backtracking and len(self.permutations) > 0:
					self.walk_trace_match(self.permutations.pop())
				elif self.backtracking and len(self.back_permutations) == 0:#We are trying to backtrack but there is nothing left to try
					self.backtracking = False
					if len(self.permutations) > 0:
						self.walk_trace_match(self.permutations.pop())
					else:
						return
				else:
					return

	def mark_unsure(self, node):
		for t in node.get_transition():
			t.set_match(self.error, 0)
			self.skipped_links.append(t)

	def mark_matched(self, node):
		for t in node.get_transition():
			t.set_match(self.error, 1)

	def mark_unmatch(self, link):
		link.set_match(self.error, -1)

	def unmatch(self, link):
		link.set_match(self.error, -1, remove=True)

	def total_unmatch(self, node1, node2):
		for t1 in node1.get_transition():
			self.mark_unmatch(t1)
		for t2 in node2.get_transition():
			self.mark_unmatch(t2)

	def different_to(self, transition):
		tot = set()
		for t in transition:
			tot.add(t.to)
		return len(tot)

	def transition_number(self, node1, node2, rematch_mode="None"):
		len_right = self.different_to(node1.get_transition())
		len_left = self.different_to(node2.get_transition())
		return len_right if len_right >= len_left else len_left

	def has_tried_permutation(self, trace_match):
		for p in self.tried_permutations[:-1]: #Look at all permutation except last one just added
			if trace_match.followed_label == p.followed_label:
				if trace_match.node1_from == p.node1_from and trace_match.node1_to == p.node1_to:
					if trace_match.node2_from == p.node2_from and trace_match.node2_to == p.node2_to:
						return True
		return False

	def launch_permutations(self, node1, node2):
		self.correct_backtrack = 0
		current_rematch = ""
		if (rematch_mode == "skip_left" and self.rematch_type == 3) or (rematch_type == 3 and self.rematch_type == 2):
			current_rematch = "skip_left"
			self.mark_unsure(node1)
			if node1 not in self.temp_unsure:
				self.temp_unsure.append(node1)
		if rematch_mode == "skip_right" or (rematch_type == 3 and self.rematch_type == 2 or self.rematch_type == 1):
			if current_rematch == "skip_left":
				current_rematch = "skip_both"
			else:
				current_rematch = "skip_right"
			self.mark_unsure(node2)
			if node2 not in self.temp_unsure:
				self.temp_unsure.append(node2)
		self.rematch_type -= 1
		self.loc_rematch = 0
		goal = self.transition_number(node1, node2, current_rematch)
		print(f"Trying backtrack with {current_rematch}")
		if current_rematch == "skip_left":
			for t in node1.get_transition():
				t_m = TraceMatch("Skipped", node1, node2, t.to, node2, self.performs_G1, self.performs_G2, match=False)
				if not self.has_tried_permutation(t_m):
					self.back_permutations.append(t_m)
		elif current_rematch == "skip_right":
			for t in node2.get_transition():
				t_m = TraceMatch("Skipped", node1, node2, node1, t.to, self.performs_G1, self.performs_G2, match=False)
				if not self.has_tried_permutation(t_m):
					self.back_permutations.append(t_m)
		elif current_rematch == "skip_both":
			for t1 in node1.get_transition():
				for t2 in node2.get_transition():
					t_m = TraceMatch("Skipped", node1, node2, t1.to, t2.to, self.performs_G1, self.performs_G2, match=False)
					if not self.has_tried_permutation(t_m):
						self.back_permutations.append(t_m)
		self.backtrack_mode = current_rematch
		self.backtracking = True
		self.backtrack_goal = goal
		if len(self.back_permutations) > 0:
			self.current_back_track = self.back_permutations.pop()
		else:
			self.backtrack(node1, node2)

	def backtrack(self, node1, node2):
		if self.backtracking and self.correct_backtrack >= self.backtrack_goal: #Did the backtrack work ?
			print("Backtrack fully worked !")
			self.backtracking = False
			self.correct_backtrack = 0
			self.backtrack_goal = 0
			self.rematch_type = rematch_type
			for node in self.temp_unsure:
				for t_out in node.get_transition():
					if -1 in t_out.match:
						t_out.match.remove(-1)
			self.temp_unsure = []
			for n in self.back_bag_g1:
				n.group_match_set(self.back_bag_g2)
			for n in self.back_bag_g2:
				n.group_match_set(self.back_bag_g1)
			self.back_bag_g1 = set()
			self.back_bag_g1 = set()
			if len(self.permutations) > 0:
				self.walk_trace_match(self.permutations.pop())
			return
		elif self.backtracking: #If we are backtraching but it's not worked yet
			if len(self.back_permutations) == 0: #No more permutations ?
				if self.rematch_type < 1: #No more available, we failed
					self.equivalent = False
					print("Backtrack couldn't work !")
					print(self.current_back_track.node1_from.initial_node)
					print(self.current_back_track.node2_from.initial_node)
					self.error += 1
					self.correct_backtrack = 0
					self.rematch = 0
					self.loc_rematch = 0
					self.rematch_type = rematch_type
					self.backtracking = False
					self.equivalent = False
					for node in self.temp_unsure:
						for t_out in node.get_transition():
							if 0 in t_out.match:
								t_out.match.remove(0)
					self.temp_unsure = []
					if len(self.permutations) > 0: #Should we do this ?
						self.walk(self.permutations.pop())
					return
				else:#recreate more permutations
					if self.starting_backtrack:
						self.launch_permutations(self.starting_backtrack.node1_from, self.starting_backtrack.node2_from)
					else:
						self.launch_permutations(node1, node2)
						self.starting_backtrack = self.current_back_track
					self.tried_permutations.append(self.current_back_track)
					self.walk_trace_match(self.current_back_track)

			else:
				while len(self.back_permutations) > 0 and self.correct_backtrack < self.backtrack_goal:
					self.backtracking = True
					self.current_back_track = self.back_permutations.pop()
					self.tried_permutations.append(self.current_back_track)
					self.walk_trace_match(self.current_back_track)
		else: #We are not backtracking yet, launch it
			self.launch_permutations(node1, node2)
			self.starting_backtrack = self.current_back_track
			self.tried_permutations.append(self.current_back_track)
			self.walk_trace_match(self.current_back_track)



	def valid_backtrack(self):
		#self.backtracking = False
		self.rematch = 0 #We found our way so reset rematches
		self.loc_rematch = 0
		self.correct_backtrack += 1
		if self.correct_backtrack >= self.backtrack_goal:
			for elem in self.temp_visited:
				self.append_to_visited(elem)
			self.temp_visited = []
			for link in self.temp_links_matched:
				self.mark_and_move(link.fr, link, force_match=True)
			for elem in self.temp_permutations:
				if elem not in self.permutations and elem not in self.visited_couples and not self.already_seen(elem):
					self.permutations.append(elem)
			self.temp_permutations = []
			self.temp_links_matched = []
		if len(self.back_permutations) > self.backtrack_goal-self.correct_backtrack:
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
		print(f"Backtrack worked ! {self.starting_backtrack}")
		self.backtrack(self.starting_backtrack.node1_f(), self.starting_backtrack.node2_f())

	def invalid_backtrack(self):
		#self.backtracking = False
		print(f"Backtrack failed ! {self.starting_backtrack}")
		self.temp_visited = []
		self.temp_links_matched = []
		for link in self.temp_links_matched:
			self.unmatch(link)
		for link in self.skipped_links:
			self.unmatch(link)
		self.back_permutations = []
		self.backtrack(self.starting_backtrack.node1_f(), self.starting_backtrack.node2_f())

	def keep_moving(self, node1, node2):
		next = []
		if self.backtrack_mode == "skip_left":
			for t in node1.get_transition():
				t_m = TraceMatch("Skipped", node1, node2, t.to, node2, self.performs_G1, self.performs_G2)
				next.append(t_m)
		elif self.backtrack_mode == "skip_right":
			for t in node2.get_transition():
				t_m = TraceMatch("Skipped", node1, node2, node1, t.to, self.performs_G1, self.performs_G2)
				next.append(t_m)
		else:
			for t1 in node1.get_transition():
				for t2 in node2.get_transition():
					t_m = TraceMatch("Skipped", node1, node2, t1.to, t2.to, self.performs_G1, self.performs_G2)
					next.append(t_m)
		for e in next:
			if not self.has_tried_permutation(e):
				self.back_permutations.append(e)
		self.backtrack(node1, node2)

	def already_seen(self, trace_match):
		for e in self.visited_couples:
			if e == trace_match:
				return True
		return False

	def walk(self, trace_match):
		node1 = trace_match.node1()
		node2 = trace_match.node2()
		if not self.backtracking and self.already_seen(trace_match):
			print("This path is equivalent")
			self.all_paths_g1.append(self.current_path_g1)
			self.all_paths_g2.append(self.current_path_g2)
			self.current_path_g1 = []
			self.current_path_g2 = []
			if self.equivalent is None or self.equivalent:
				self.equivalent = True
				return
			return
		if not self.backtracking:
			self.current_path_g1.append(node1)
			self.current_path_g2.append(node2)
		#if self.equivalent != False:
		if self.backtracking:
			self.temp_visited.append(trace_match)
		else:
			self.append_to_visited(trace_match)
		keep_walking, new_trace_match = self.consume_internal_transitions(trace_match)
		if keep_walking:
			self.walk(new_trace_match)
		else:
			if not self.backtracking:
				for n in self.bag_g1:
					n.group_match_set(self.bag_g2)
				for n in self.bag_g2:
					n.group_match_set(self.bag_g1)
				self.bag_g1 = set()
				self.bag_g2 = set()
		if not keep_walking and len(node1.get_transition()) == len(node2.get_transition()) == 0 or (node1.get_tag() == "END" and node2.get_tag()=="END"): #Try and stop at the end
			if self.backtracking:
				self.valid_backtrack()
			print("This path is equivalent")
			node1.group_match(node2)
			node2.group_match(node1)
			self.all_paths_g1.append(self.current_path_g1)
			self.all_paths_g2.append(self.current_path_g2)
			self.current_path_g1 = []
			self.current_path_g2 = []
			if self.equivalent is None or self.equivalent:
				self.equivalent = True
				return
		elif not keep_walking:
			# print("We need to compare two branches")
			match, transition_found = self.compare_and_match(node1, node2)
			if not match and isinstance(node1.initial_node, ConditionNode) and isinstance(node2.initial_node, ConditionNode): #First try special cases
				if self.try_if_to_evaluate(node1, node2):
					#self.back_permutations = []
					return
				if self.try_factorize_ifs(node1, node2):
					#self.back_permutations = []
					return
			if not match:
				if self.backtracking:
					if self.loc_rematch >= rematch:#No more path creation
						if len(self.back_permutations) == 0:
							self.invalid_backtrack()
						else:
							self.current_back_track = self.back_permutations.pop()
							self.tried_permutations.append(self.current_back_track)
							self.walk_trace_match(self.current_back_track)
					else:
						self.loc_rematch += 1 #Skip more nodes
						self.keep_moving(node1, node2)
				else:
					if self.rematch >= rematch:#We have tried everything
						print("Graphs are not equivalent !")
						print(node1.initial_node)
						print(node2.initial_node)
						self.equivalent = False
						self.error += 1
					else:
						self.rematch += 1
						self.backtrack(node1, node2)
			else: #Looks like we found our way
				if not self.backtracking:
					self.back_permutations = []
				if self.backtracking: #We were backtracking but we found a match on this path !
					self.valid_backtrack()
				while len(self.permutations) > 0:
					t_m = self.permutations.pop()
					if not self.already_seen(t_m):
						self.walk_trace_match(t_m)

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
				str_match = "" 
				for i in node.matches:
					str_match += str(i)+" "
				str_match = str_match.strip()
				file.write(f"{node.id} [{str(node.initial_node)}] |{str_match}|\n")
			for transition in self.g1.all_transitions:
				file.write(f"{transition.fr.id} -> {transition.to.id} [match:|{transition.match_str()}|]\n")

		with open(filepath+file2, "w+") as file:
			file.write("digraph "+file2+"V2 {\n")
			for node in self.g2.all_states:
				file.write("node\n")
				str_match = "" 
				for i in node.matches:
					str_match += str(i)+" "
				str_match = str_match.strip()
				file.write(f"{node.id} [{str(node.initial_node)}] |{str_match}|\n")
			for transition in self.g2.all_transitions:
				file.write(f"{transition.fr.id} -> {transition.to.id} [match:|{transition.match_str()}|]\n")

