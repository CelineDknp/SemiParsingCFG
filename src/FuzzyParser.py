from Utils.config import *
from Nodes.SimpleBranchConditionNode import SimpleBranchConditionNode
from Nodes.MultipleBranchConditionNode import MultipleBranchConditionNode
from Nodes.ConditionNode import ConditionNode
from Nodes.ParseNode import ParseNode
from Nodes.LoopNode import LoopNode
from Nodes.LabelLoopNode import LabelLoopNode
from Nodes.MultipleLabelLoopNode import MultipleLabelLoopNode
from Nodes.ControlLoopNode import ControlLoopNode
from Nodes.LabelNode import LabelNode
from Nodes.Node import Node
from Anchors.ConditionAnchor import ConditionAnchor
from Anchors.LoopAnchor import LoopAnchor
from Anchors.SpecialAnchor import SpecialAnchor
from Anchors.IgnoreAnchor import IgnoreAnchor
from Anchors.Anchor import Anchor

class FuzzyParser():
	def anchors_creation(self):
		self.anchors = []
		self.special_anchors = {}
		self.label_regex = []
		for elem in conditions:
				self.anchors.append(ConditionAnchor(elem))
		for elem in parsable:
			self.anchors.append(Anchor(elem["start"], PARSABLE))
		for elem in special:
			s = SpecialAnchor(elem)
			self.anchors.append(s)
			self.special_anchors[elem["effect"]] = s
		for elem in to_ignore:
			s = IgnoreAnchor(elem)
			self.anchors.append(s)
		for elem in loops:
			a = LoopAnchor(elem)
			self.anchors.append(a)
			if a.is_label_anchor():
				s = SpecialAnchor.from_explicit(elem["label-regex"], "label")
				self.label_regex.append(elem["label-regex"])
				self.anchors.append(s)
			elif a.is_control_anchor():
				s = SpecialAnchor.from_explicit(elem["control-regex"], "control", info=elem["control-type"])
				self.special_anchors["control-regex"] = s
		self.anchors_dict = self.current_anchors_and_regexes()

	def next_pos_init(self):
		for val in self.anchors_dict:
			res = val.finditer(self.input[self.pos:])
			elem = next(res, None)
			if elem is not None:
				self.next_pos_iter[val] = res
				self.next_pos[val] = [self.input.find(elem.group(0), self.pos), elem.group(0), self.anchors_dict[val]]
			else:
				self.banned_regex.append(val)

	def __init__(self, input):
		self.input = input
		self.pos = 0
		self.depth = 0
		self.open_control = False
		self.init = False
		self.next_pos = {}
		self.next_pos_iter = {}
		self.banned_regex = []
		self.anchors_creation()
		self.next_pos_init()
		self.clean_anchors()

	def current_anchors_and_regexes(self):
		result = {}
		for a in self.anchors:
			if a.get_type() == CONDITION:
				if a.get_start_pattern() not in self.banned_regex:
					result[a.get_start_pattern()] = a
				if a.get_branch_pattern() not in self.banned_regex:
					result[a.get_branch_pattern()] = a
				if a.get_end_pattern() not in self.banned_regex:
					result[a.get_end_pattern()] = a
			else:
				if a.get_pattern() not in self.banned_regex:
					result[a.get_pattern()] = a
		return result

	def useful_anchor(self, current_anchor, end_match):
		#print(f"Is {current_anchor} useful ?")
		if not current_anchor.get_type() == IGNORE: #If this isn't an ignore anchor, allow it
			return True
		else:
			for key in self.next_pos.keys():
				anchor = self.next_pos[key][2]
				if not anchor.get_type() == IGNORE: #If this is not an ignore key
					val = self.next_pos[key][0]
					if val != -1 and val <= end_match:
						return True
			return False

	def pick_next_anchor(self):
		# print("PICKING")
		min_val = len(self.input) + 1
		min_key = ""
		actual_match = ""
		anchor = None
		for key in self.next_pos.keys():
			# print(key)
			# print(f"Init is {self.init}")
			if not self.init: #Particular case for the init
				if self.next_pos[key][2].get_type() == SPECIAL and self.next_pos[key][2].get_effect() == "start_parse":
					self.clean_anchors(start_parse=True)
					val = self.next_pos[key][0]
					actual = self.next_pos[key][1]
					anchor = self.next_pos[key][2]
					self.next_pos.pop(key)
					self.init = True
					return 0, anchor, val, actual
			else:
				val = self.next_pos[key][0]
				# print(f"VAL: {val}")
				# Should we pick this anchor ?
				if val < min_val and val != -1:
					t_anchor = self.next_pos[key][2]
					if self.useful_anchor(t_anchor, val + len(self.next_pos[key][1].rstrip())):
						min_val = val
						min_key = key
						anchor = self.next_pos[key][2]
						actual_match = self.next_pos[key][1]
		if min_key != '':
			#print(f"picked: {min_val}, {anchor}, {min_key}, {actual_match}")
			return min_val, anchor, min_key, actual_match
		else:
			return min_val, None, min_key, None

	def get_next_value_regex(self, val):
		if val not in self.next_pos_iter:
			res = val.finditer(self.input[self.pos:])
			self.next_pos_iter[val] = res

		elem = next(self.next_pos_iter[val], None)
		if elem is not None:
			return [self.input.find(elem.group(0), self.pos), elem.group(0), self.anchors_dict[val]]
		else:
			return None


	def next_anchor(self):
		#print(f"Searching from: |{self.input[self.pos:self.pos+150]}|")
		for val in self.anchors_dict.keys():
			# print(f"Looking for {val}")
			if val not in self.next_pos:
				# print(f"Not in next_pos {val}")
				# print(f"Not in absent_regex")
				res = self.get_next_value_regex(val)
				if res != None:
					self.next_pos[val] = res
				else:
					self.banned_regex.append(val)
					#print(f"Found {val} not in next pos or absent_regex")
			elif self.next_pos[val][0] < self.pos:
				#print(f"Outdated next_pos for val {val} ! Update")
				while self.next_pos[val][0] < self.pos:
					res = self.get_next_value_regex(val)
					if res != None:
						self.next_pos[val] = res
					else:
						self.banned_regex.append(val)
						self.next_pos.pop(val)
						break
		# for elem in self.next_pos:
			# print(f"{elem} : {self.next_pos[elem]}")
		return self.pick_next_anchor()

	def len_next_match(self, pattern):
		res = pattern.search(self.input[self.pos:])
		return self.input.find(res.group(0), self.pos) + len(res.group(0))

	def clean_anchors(self, start_parse=False, found_control=False):
		if start_parse:
			self.anchors.remove(self.special_anchors["start_parse"])
			self.anchors_dict = self.current_anchors_and_regexes()
		elif found_control:
			if self.special_anchors["control-regex"] in self.anchors:
				self.anchors.remove(self.special_anchors["control-regex"])
				self.banned_regex.append(self.special_anchors["control-regex"].get_pattern())
				if self.special_anchors["control-regex"].get_pattern() in self.next_pos:
					self.next_pos.pop(self.special_anchors["control-regex"].get_pattern())
			else:
				self.anchors.append(self.special_anchors["control-regex"])
				if self.special_anchors["control-regex"].get_pattern() in self.banned_regex:
					self.banned_regex.remove(self.special_anchors["control-regex"].get_pattern())
		else:
			if "close_all" in self.special_anchors:
				if not self.init:
					self.banned_regex.append(self.special_anchors["close_all"].get_pattern())
					if self.special_anchors["close_all"].get_pattern() in self.next_pos:
						self.next_pos.pop(self.special_anchors["close_all"].get_pattern())
				if self.depth == 0 and self.special_anchors["close_all"].get_pattern() not in self.banned_regex:
					self.banned_regex.append(self.special_anchors["close_all"].get_pattern())
					if self.special_anchors["close_all"].get_pattern() in self.next_pos and not self.open_control:
						self.next_pos.pop(self.special_anchors["close_all"].get_pattern())
				elif self.depth > 0 and self.special_anchors["close_all"].get_pattern() in self.banned_regex:
					self.banned_regex.remove(self.special_anchors["close_all"].get_pattern())
		self.anchors_dict = self.current_anchors_and_regexes()

	def consume_ignore(self, n_anchor, next_val, actual_val, actual_match):
		if n_anchor.get_parse_type() == "comment":
			self.pos = next_val+len(actual_match)
		elif n_anchor.get_parse_type() == "string":
			self.pos = next_val+len(actual_match)

	def consume_condition(self, n_anchor, next_val, actual_val, lot, actual_match):
		#print(f"Found condition {actual_match}")
		# print(f"In condition ! anchor: {n_anchor}, next_val: {next_val}, actual: {actual_val}, match: {actual_match}")
		self.pos = next_val + len(actual_match)
		if actual_val == n_anchor.get_start_pattern(): #Found an opening condition
			# print(f'>>> FOUND COND start {actual_match}')
			node = None
			if n_anchor.is_multiple_branches():
				# print(">>> Multiple")
				node = MultipleBranchConditionNode(self.depth, NODE_COND_START, n_anchor.get_start())
			else:

				# print(">>> Simple")
				node = SimpleBranchConditionNode(self.depth, NODE_COND_START, n_anchor.get_start())
			if n_anchor.has_condition_delimiter():
				if n_anchor.is_delimiter_mandatory():
					self.pos = node.find_condition_delimiter(self.input, self.pos, n_anchor.get_delimiter())
				else:
					self.pos = node.find_condition(self.input, self.pos, n_anchor.get_delimiter())
			else:
					self.pos = node.find_condition_simple(self.input, self.pos)
			# print(f">>> COND COND: {node.get_condition()}")
			self.depth += 1
			lot.append(node)
		elif actual_val == n_anchor.get_branch_pattern() and (not n_anchor.is_multiple_branches()):
			# print('>>> FOUND COND single branch')
			node = SimpleBranchConditionNode(self.depth - 1, NODE_COND_BRANCH, n_anchor.get_start())
			lot.append(node)
		elif actual_val == n_anchor.get_branch_pattern() and n_anchor.is_multiple_branches():
			# print('>>> FOUND COND multiple branch')
			node = MultipleBranchConditionNode(self.depth - 1, NODE_COND_BRANCH, n_anchor.get_start())
			self.pos = node.find_condition_simple(self.input, self.pos)
			# print(f"Found condition: {node.get_condition()}")
			lot.append(node)
		elif actual_val == n_anchor.get_end_pattern(): #Found a COND end
			# print('>>> FOUND END-COND')
			self.depth -= 1
			node = ConditionNode(self.depth, NODE_COND_END, n_anchor.get_start())
			lot.append(node)

	def consume_parsable(self, n_anchor, next_val, lot):
		#print('>>> FOUND EXEC')
		node = ParseNode(self.depth, NODE_SQL, n_anchor.get_regex())
		lot.append(node)
		self.pos = node.find_parse_text(self.input, next_val)

	def consume_special(self, n_anchor, next_val, lot, actual_match):
		#print(f"Found special {actual_match}")
		#print(f"special ! {actual_match} effect: {n_anchor.get_effect()}")
		if n_anchor.get_effect() == "label":
			# print("found label")
			node = LabelNode(self.depth, NODE_LABEL, n_anchor.get_regex())
			self.pos = node.find_label(self.input, self.pos, n_anchor.get_pattern())
			lot.append(node)
			# print(f"label is : {node.get_label()}")
		elif n_anchor.get_effect() == "close_all":
			while self.depth > 0:
				self.depth -= 1
				node = ConditionNode(self.depth, NODE_COND_END_ANY, n_anchor.get_regex())
				lot.append(node)
			if self.open_control:
				node = Node(self.depth, NODE_COND_END_ANY)
				lot.append(node)
				self.open_control = False
				self.clean_anchors(found_control=True)
			self.pos = next_val+1
			#print(f"New pos is {self.pos}")
		elif n_anchor.get_effect() == "control":
			while self.depth > 0:
				self.depth -= 1
				node = ConditionNode(self.depth, NODE_COND_END_ANY, n_anchor.get_regex())
				lot.append(node)
			if self.open_control:
				node = Node(self.depth, n_anchor.get_info())
				lot.append(node)
				self.open_control = False
				self.clean_anchors(found_control=True)
			self.pos = next_val+1
			#print(f"New pos is {self.pos}")
		elif n_anchor.get_effect() == "start_parse":
			self.pos = self.len_next_match(n_anchor.get_pattern())

	def consume_loop(self, n_anchor, lot):
		#print("found loop !")
		# print(f"Current state of input is: |{self.input[self.pos:self.pos+150]}|")
		if n_anchor.is_label_anchor():
			node = None
			if n_anchor.is_multiple_anchor():
				node = MultipleLabelLoopNode(self.depth, NODE_LOOP, n_anchor)
			else:	
				node = LabelLoopNode(self.depth, NODE_LOOP, n_anchor)
			lot.append(node)
			self.pos = self.len_next_match(n_anchor.get_start_regex())
			# print(f"Current state of input is: |{self.input[self.pos:self.pos+150]}|")
			self.pos = node.find_label(self.input, self.pos)
			# print(f"Current state of input is: |{self.input[self.pos:self.pos+150]}|")
		elif n_anchor.is_control_anchor():
			node = ControlLoopNode(self.depth, NODE_LOOP, n_anchor)
			lot.append(node)
			self.open_control = True
			self.clean_anchors(found_control=True)
			self.pos = self.len_next_match(n_anchor.get_pattern())

	def fuzzy_parse(self):
		lot = []
		next_val, n_anchor, actual_val, actual_match = self.next_anchor()
		# print(f"First result from next_anchor: {next_val}, {n_anchor}, {actual_val}, {actual_match}")
		while next_val != len(self.input)+1:
			# print(f"Pos is {self.pos}")
			# print(f"Looking at next_anchor: {n_anchor} of val {actual_val} current depth is: {self.depth}")
			if n_anchor.get_type() == IGNORE:
				self.consume_ignore(n_anchor, next_val, actual_val, actual_match)
			elif n_anchor.get_type() == CONDITION:
				# print("IN COND")
				self.consume_condition(n_anchor, next_val, actual_val, lot, actual_match)
				self.clean_anchors()
			elif n_anchor.get_type() == PARSABLE:
				self.consume_parsable(n_anchor, next_val, lot)
			elif n_anchor.get_type() == SPECIAL:
				self.consume_special(n_anchor, next_val, lot, actual_match)
				self.clean_anchors()
			elif n_anchor.get_type() == LOOP:
				self.consume_loop(n_anchor, lot)
			else:
				self.pos += 1
			next_val, n_anchor, actual_val, actual_match = self.next_anchor()
			# print(f"Loop result from next_anchor: {next_val}, {n_anchor}, {actual_val}, {actual_match}")
		if self.input[-1] == ".": #If last character of input is a dot, close any remaining open things
			while self.depth > 0:
					self.depth -= 1
					node = ConditionNode(self.depth, NODE_COND_END_ANY, r"\.(\s)+")
					lot.append(node)
		return lot