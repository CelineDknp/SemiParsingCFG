from Utils.config import *
from Nodes.SimpleBranchConditionNode import SimpleBranchConditionNode
from Nodes.MultipleBranchConditionNode import MultipleBranchConditionNode
from Nodes.ConditionNode import ConditionNode
from Nodes.ParseNode import ParseNode
from Nodes.LoopNode import LoopNode
from Nodes.BlockLoopNode import BlockLoopNode
from Nodes.LabelLoopNode import LabelLoopNode
from Nodes.MultipleLabelLoopNode import MultipleLabelLoopNode
from Nodes.ControlLoopNode import ControlLoopNode
from Nodes.LabelNode import LabelNode
from Nodes.Node import Node
from AnchorHandler import AnchorHandler


class FuzzyParser:
	def __init__(self):
		self.anchorHandler = AnchorHandler()

	def reset_vars(self, input):
		self.input_str = input
		self.pos = 0
		self.depth = 0
		self.open_control = False
		self.init = False
		self.stop_close_all_look = False
		self.close_all_iter = None
		self.stop_control_look = False
		self.control_iter = None
		self.next_pos = {}
		self.next_pos_iter = {}
		self.anchorHandler.reset_anchors()
		self.next_pos_init()
		self.clean_anchors()


	def next_pos_init(self):
		for val in self.anchorHandler.get_anchors():
			res = val.finditer(self.input_str[self.pos:])
			elem = next(res, None)
			if elem is not None:
				self.next_pos_iter[val] = res
				self.next_pos[val] = self.get_next_pos_array(val, elem)
			else:
				self.anchorHandler.ban_regex(val)

	def useful_anchor(self, current_anchor, end_match):
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
		min_val = len(self.input_str) + 1
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
				curr_length = 0
				# print(f"VAL: {val}")
				# Should we pick this anchor ?
				temp_length = len(self.next_pos[key][1])
				if (val < min_val or (val == min_val and temp_length > curr_length)) and val != -1:
					t_anchor = self.next_pos[key][2]
					if self.useful_anchor(t_anchor, val + len(self.next_pos[key][1].rstrip())):
						min_val = val
						min_key = key
						anchor = self.next_pos[key][2]
						actual_match = self.next_pos[key][1]
						curr_length = len(actual_match)
		if min_key != '':
			#print(f"picked: {min_val}, {anchor}, {min_key}, {actual_match}")
			return min_val, anchor, min_key, actual_match
		else:
			return min_val, None, min_key, None

	def get_next_pos_array(self, val, elem):
		if val == self.anchorHandler.get_special_anchor("close_all").get_pattern() or \
				val == self.anchorHandler.get_special_anchor("control-regex").get_pattern():
			# print("Picked find")
			return [self.input_str.find(elem.group(0), self.pos), elem.group(0), self.anchorHandler.get_anchor(val)]
		else:
			# print("picked span")
			return [elem.span()[0], elem.group(0), self.anchorHandler.get_anchor(val)]

	def get_next_value_regex(self, val):
		if val not in self.next_pos_iter:
			next_iter = val.finditer(self.input_str[self.pos:])
			self.next_pos_iter[val] = next_iter
		else:
			next_iter = self.next_pos_iter[val]
		elem = next(next_iter, None)
		if elem is not None:
			return self.get_next_pos_array(val, elem)
		else:
			return None

	def get_next_or_ban(self, val):
		res = self.get_next_value_regex(val)
		if res != None:
			self.next_pos[val] = res
			return False
		else:
			self.anchorHandler.ban_regex(val)
			return True

	def next_anchor(self):
		#print(f"Searching from: |{self.input_str[self.pos:self.pos+150]}|")
		for val in self.anchorHandler.get_anchors():
			# print(f"Looking for {val}")
			if val not in self.next_pos:
				self.get_next_or_ban(val)
			elif self.next_pos[val][0] < self.pos:
				#print(f"Outdated next_pos for val {val} ! Update")
				while self.next_pos[val][0] < self.pos:
					if self.get_next_or_ban(val):
						self.next_pos.pop(val)
						break
		# for elem in self.next_pos:
			# print(f"{elem} : {self.next_pos[elem]}")
		return self.pick_next_anchor()

	def len_next_match(self, pattern):
		res = pattern.search(self.input_str[self.pos:])
		return self.input_str.find(res.group(0), self.pos) + len(res.group(0))

	def remove_regex_from_next_pos(self, regex):
		if regex in self.next_pos:
			self.next_pos.pop(regex)
		if regex in self.next_pos_iter:
			return self.next_pos_iter.pop(regex)

	def update_iters_and_next(self, result, regex, iterator):
		if result == "banned": #We banned the regex, remove it
			return self.remove_regex_from_next_pos(regex) #Remove regex from next_pos and the iterator array, but return the iterator
		elif result == "unbanned": #We unbanned the regex, fetch it
			if iterator is not None:
				self.next_pos_iter[regex] = iterator #We already had an iterator
			else:
				new_it = regex.finditer(self.input_str[self.pos:]) #Making a new iteratoor
				self.next_pos_iter[regex] = new_it
			#Let's update next_pos and make sure it's not empty
			banned = self.get_next_or_ban(regex)
			if banned:
				return None
			else:
				return new_it

	def clean_anchors(self, start_parse=False, found_control=False):
		if start_parse:
			self.anchorHandler.clean_anchors(self.depth, self.open_control, start_parse=True)
		elif found_control:
			regex = self.anchorHandler.get_special_pattern("control-regex")
			if self.stop_control_look:
				self.anchorHandler.ban_regex(regex)
				self.remove_regex_from_next_pos(regex)
				return
			result = self.anchorHandler.clean_anchors(self.depth, self.open_control, found_control=True)
			is_iter = self.update_iters_and_next(result, regex, self.control_iter)
			if is_iter is not None:
				self.control_iter = is_iter
			else:
				self.stop_control_look = True
		else:
			if self.anchorHandler.has_special("close_all"):
				regex = self.anchorHandler.get_special_pattern("close_all")
				if self.stop_close_all_look:
					self.anchorHandler.ban_regex(regex)
					self.remove_regex_from_next_pos(regex)
					return
				result = self.anchorHandler.clean_anchors(self.depth, self.open_control, init=not self.init)
				if result != "nothing":
					is_iter = self.update_iters_and_next(result, regex, self.control_iter)
					if is_iter is not None:
						self.close_all_iter = is_iter
					else:
						self.stop_close_all_look = True

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
					self.pos = node.find_condition_delimiter(self.input_str, self.pos, n_anchor.get_delimiter())
				else:
					self.pos = node.find_condition(self.input_str, self.pos, n_anchor.get_delimiter())
			else:
					self.pos = node.find_condition_simple(self.input_str, self.pos)
			# print(f">>> COND COND: {node.get_condition()}")
			self.depth += 1
			if self.depth == 1:
				self.clean_anchors()
			lot.append(node)
		elif actual_val == n_anchor.get_branch_pattern() and (not n_anchor.is_multiple_branches()):
			# print('>>> FOUND COND single branch')
			node = SimpleBranchConditionNode(self.depth - 1, NODE_COND_BRANCH, n_anchor.get_start())
			lot.append(node)
		elif actual_val == n_anchor.get_branch_pattern() and n_anchor.is_multiple_branches():
			# print('>>> FOUND COND multiple branch')
			node = MultipleBranchConditionNode(self.depth - 1, NODE_COND_BRANCH, n_anchor.get_start())
			self.pos = node.find_condition_simple(self.input_str, self.pos)
			# print(f"Found condition: {node.get_condition()}")
			lot.append(node)
		elif actual_val == n_anchor.get_end_pattern(): #Found a COND end
			# print('>>> FOUND END-COND')
			self.depth -= 1
			if self.depth == 0:
				self.clean_anchors()
			node = ConditionNode(self.depth, NODE_COND_END, n_anchor.get_start())
			lot.append(node)

	def consume_parsable(self, n_anchor, next_val, lot):
		#print('>>> FOUND EXEC')
		node = ParseNode(self.depth, NODE_SQL, n_anchor.get_regex())
		lot.append(node)
		self.pos = node.find_parse_text(self.input_str, next_val)

	def consume_special(self, n_anchor, next_val, lot, actual_match):
		#print(f"Found special {actual_match}")
		#print(f"special ! {actual_match} effect: {n_anchor.get_effect()}")
		if n_anchor.get_effect() == "label":
			# print("found label")
			node = LabelNode(self.depth, NODE_LABEL, n_anchor.get_regex())
			node.find_label(actual_match)
			self.pos = next_val+len(actual_match)-1
			lot.append(node)
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

	def consume_loop(self, n_anchor, lot, next_val, actual_val, actual_match):
		#print(f"found loop ! {actual_match}")
		# print(f"Current state of input is: |{self.input[self.pos:self.pos+150]}|")
		if n_anchor.is_label_anchor():
			node = None
			if n_anchor.is_multiple_anchor():
				node = MultipleLabelLoopNode(self.depth, NODE_LOOP, n_anchor)
			else:	
				node = LabelLoopNode(self.depth, NODE_LOOP, n_anchor)
			lot.append(node)
			node.find_label(actual_match)
			# print(f"Current state of input is: |{self.input[self.pos:self.pos+150]}|")
		elif n_anchor.is_control_anchor():
			node = ControlLoopNode(self.depth, NODE_LOOP, n_anchor)
			lot.append(node)
			self.open_control = True
			self.clean_anchors(found_control=True)
		elif n_anchor.is_block_anchor():
			if actual_val == n_anchor.get_start_pattern():
				node = BlockLoopNode(self.depth, NODE_LOOP, n_anchor)
				lot.append(node)
				node.find_conditions(actual_match)
			elif actual_val == n_anchor.get_end_pattern():
				node = BlockLoopNode(self.depth, NODE_LOOP, n_anchor, close=True)
				lot.append(node)
		self.pos = next_val + len(actual_match) - 1

	def fuzzy_parse(self, input):
		lot = []
		self.reset_vars(input)
		next_val, n_anchor, actual_val, actual_match = self.pick_next_anchor()
		# print(f"First result from next_anchor: {next_val}, {n_anchor}, {actual_val}, {actual_match}")
		while next_val != len(self.input_str)+1:
			# print(f"Pos is {self.pos}")
			# print(f"Looking at next_anchor: {n_anchor} of val {actual_val} current depth is: {self.depth}")
			if n_anchor.get_type() == IGNORE:
				self.consume_ignore(n_anchor, next_val, actual_val, actual_match)
			elif n_anchor.get_type() == CONDITION:
				# print("IN COND")
				self.consume_condition(n_anchor, next_val, actual_val, lot, actual_match)
			elif n_anchor.get_type() == PARSABLE:
				self.consume_parsable(n_anchor, next_val, lot)
			elif n_anchor.get_type() == SPECIAL:
				self.consume_special(n_anchor, next_val, lot, actual_match)
			elif n_anchor.get_type() == LOOP:
				self.consume_loop(n_anchor, lot, next_val, actual_val, actual_match)
			else:
				self.pos += 1
			next_val, n_anchor, actual_val, actual_match = self.next_anchor()
			# print(f"Loop result from next_anchor: {next_val}, {n_anchor}, {actual_val}, {actual_match}")
		if self.input_str[-1] == ".": #If last character of input is a dot, close any remaining open things
			while self.depth > 0:
					self.depth -= 1
					node = ConditionNode(self.depth, NODE_COND_END_ANY, r"\.(\s)+")
					lot.append(node)
		return lot