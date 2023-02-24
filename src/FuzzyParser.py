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
from Anchors.AnchorMatch import AnchorMatch
from Anchors.ConditionAnchor import ConditionAnchor


class FuzzyParser:
	def __init__(self):
		self.anchorHandler = AnchorHandler()

	def reset_vars(self, input):
		self.input_str = input
		self.pos = 0
		self.depth = 0
		self.open_control = False
		self.all_matches = []
		self.all_ignore = []
		self.anchorHandler.reset_anchors()
		self.start_parse()
		self.start_pos = self.pos
		self.next_pos_init()

	def start_parse(self):
		if self.anchorHandler.has_special("start_parse"):
			anchor = self.anchorHandler.get_special_anchor("start_parse")
			iter = anchor.pattern.finditer(self.input_str[self.pos:])
			match = next(iter, None)
			if match:
				elem = AnchorMatch(self.input_str.find(match.group(0), self.pos), anchor, match.group(0), anchor)
				self.pos = elem.get_start_index() + len(elem.get_actual_match())
			self.anchorHandler.remove_anchor(anchor)

	def get_anchorMatch(self, match, val):
		start = self.start_pos+match.start(0)
		return AnchorMatch(start, val, match.group(0), self.anchorHandler.get_anchor(val), temp_match = match.string[match.start(0)-40:match.end(0)+40])

	def next_pos_init(self):
		for val in self.anchorHandler.get_anchors():
			iter = val.finditer(self.input_str[self.start_pos:])
			match = next(iter, None)
			if match:
				elem = self.get_anchorMatch(match, val)
				#current_match =
			while match is not None and elem is not None:
				if elem.get_anchor().get_type() == IGNORE:
					self.all_ignore.append(elem)
				else:
					self.all_matches.append(elem)
				match = next(iter, None)
				if match is not None:
					elem = self.get_anchorMatch(match, val)
					#current_match = match.string[match.start(0)-10:match.end(0)+10]

		self.all_matches.sort() #Sort all the matches in order
		self.all_ignore.sort()
		self.pos = self.start_pos

	def overlap(self, match):
		start_match, end_match = match.get_start_end()
		to_remove = []
		for elem in self.all_ignore:
			start_ignore, end_ignore = elem.get_start_end()
			if end_ignore < start_match: #If we found something that ends before our match starts
				to_remove.append(elem) #Remove it
			elif start_ignore < start_match and end_ignore > start_match: #We have an overlap
				return True
		for elem in to_remove:
			self.all_ignore.remove(elem)
		return False

	def pick_next_anchor(self):
		looking = True
		next = None
		while looking and len(self.all_matches) > 0:
			next = self.all_matches[0]
			if not self.overlap(next):
				looking = False
			if next.get_start_index() < self.pos: #We had a duplicated node and need to skip this
				looking = True
			#If it is a dot and we don't want it, don't take it
			#if next.get_anchor().get_type() == SPECIAL and next.get_anchor().get_effect() == "close_all" and self.depth == 0:
			#	looking = True
			self.all_matches.remove(next)
		return next

	def len_next_match(self, pattern):
		res = pattern.search(self.input_str[self.pos:])
		return self.input_str.find(res.group(0), self.pos) + len(res.group(0))

	def consume_ignore(self, anchorMatched):
		self.pos = anchorMatched.get_start_index() + len(anchorMatched.get_actual_match())

	def consume_condition(self, anchorMatched, lot):
		anchor = anchorMatched.get_anchor()
		actual_match = anchorMatched.get_actual_match()
		regex_match = anchorMatched.get_regex()
		start_index = anchorMatched.get_start_index()
		self.pos = start_index + len(actual_match.rstrip())
		if regex_match == anchor.get_start_pattern(): #Found an opening condition
			node = None
			if anchor.is_multiple_branches():
				node = MultipleBranchConditionNode(self.depth, NODE_COND_START, anchor.get_start())
			else:
				node = SimpleBranchConditionNode(self.depth, NODE_COND_START, anchor.get_start())
			if anchor.has_condition_delimiter():
				if anchor.is_delimiter_mandatory():
					self.pos = node.find_condition_delimiter(self.input_str, self.pos, anchor.get_delimiter())
				else:
					self.pos = node.find_condition(self.input_str, self.pos, anchor.get_delimiter())
			else:
					self.pos = node.find_condition_simple(self.input_str, self.pos)
			self.depth += 1
			lot.append(node)
		elif regex_match == anchor.get_branch_pattern() and (not anchor.is_multiple_branches()):
			node = SimpleBranchConditionNode(self.depth - 1, NODE_COND_BRANCH, anchor.get_start())
			lot.append(node)
		elif regex_match == anchor.get_branch_pattern() and anchor.is_multiple_branches():
			node = MultipleBranchConditionNode(self.depth - 1, NODE_COND_BRANCH, anchor.get_start())
			self.pos = node.find_condition_simple(self.input_str, self.pos)
			lot.append(node)
		elif regex_match == anchor.get_end_pattern(): #Found a COND end
			self.depth -= 1
			node = ConditionNode(self.depth, NODE_COND_END, anchor.get_start())
			lot.append(node)

	def consume_parsable(self, anchorMatched, lot):
		node = ParseNode(self.depth, NODE_SQL, anchorMatched.get_anchor().get_regex())
		lot.append(node)
		self.pos = node.find_parse_text(self.input_str, anchorMatched.get_start_index())

	def consume_special(self, anchorMatched, lot):
		anchor = anchorMatched.get_anchor()
		actual_match = anchorMatched.get_actual_match()
		start_index = anchorMatched.get_start_index()
		if anchor.get_effect() == "label":
			node = LabelNode(self.depth, NODE_LABEL, anchor.get_regex())
			node.find_label(actual_match)
			self.pos = start_index+len(actual_match)-1
			lot.append(node)
		elif anchor.get_effect() == "close_all":
			if self.depth > 0:
				while self.depth > 0:
					self.depth -= 1
					node = ConditionNode(self.depth, NODE_COND_END_ANY, anchor.get_regex())
					lot.append(node)
				if self.open_control:
					self.open_control = False
			else:
				if self.open_control:
					node = Node(self.depth, NODE_COND_END_ANY)
					lot.append(node)
					self.open_control = False
			self.pos = start_index+1
		elif anchor.get_effect() == "control":
			while self.depth > 0:
				self.depth -= 1
				node = ConditionNode(self.depth, NODE_COND_END_ANY, anchor.get_regex())
				lot.append(node)
			if self.open_control:
				node = Node(self.depth, anchor.get_info())
				lot.append(node)
				self.open_control = False
			self.pos = start_index+1
		elif anchor.get_effect() == "start_parse":
			self.pos = self.len_next_match(anchor.get_pattern())
		elif anchor.get_effect() == "special_case": #Special case to treat
			if anchor.info == ConditionAnchor: #We have a double EVALUATE
				node = MultipleBranchConditionNode(self.depth - 1, NODE_COND_BRANCH, '\sEVALUATE(\s)+')
				self.pos = node.find_condition_double(self.input_str, self.pos)
				lot.append(node)

	def consume_loop(self, anchorMatched, lot):
		anchor = anchorMatched.get_anchor()
		actual_match = anchorMatched.get_actual_match()
		start_index = anchorMatched.get_start_index()
		if anchor.is_label_anchor():
			if anchor.is_multiple_anchor():
				node = MultipleLabelLoopNode(self.depth, NODE_LOOP, anchor)
			else:	
				node = LabelLoopNode(self.depth, NODE_LOOP, anchor)
			lot.append(node)
			node.find_label(actual_match)
		elif anchor.is_control_anchor():
			node = ControlLoopNode(self.depth, NODE_LOOP, anchor)
			lot.append(node)
			self.open_control = True
		elif anchor.is_block_anchor():
			if anchorMatched.get_regex() == anchor.get_start_pattern():
				node = BlockLoopNode(self.depth, NODE_LOOP, anchor)
				lot.append(node)
				node.find_conditions(actual_match, self.input_str, self.pos)
			elif anchorMatched.get_regex() == anchor.get_end_pattern():
				node = BlockLoopNode(self.depth, NODE_LOOP, anchor, close=True)
				lot.append(node)
		self.pos = start_index + len(actual_match.strip()) - 1

	def fuzzy_parse(self, input):
		lot = []
		self.reset_vars(input)
		anchorMatch = self.pick_next_anchor()
		while anchorMatch:
			if anchorMatch.get_anchor().get_type() == IGNORE:
				self.consume_ignore(anchorMatch)
			elif anchorMatch.get_anchor().get_type() == CONDITION:
				self.consume_condition(anchorMatch, lot)
			elif anchorMatch.get_anchor().get_type() == PARSABLE:
				self.consume_parsable(anchorMatch, lot)
			elif anchorMatch.get_anchor().get_type() == SPECIAL:
				self.consume_special(anchorMatch, lot)
			elif anchorMatch.get_anchor().get_type() == LOOP:
				self.consume_loop(anchorMatch, lot)
			else:
				self.pos += 1
			anchorMatch = self.pick_next_anchor()
		if self.input_str[-1] == ".": #If last character of input is a dot, close any remaining open things
			while self.depth > 0:
					self.depth -= 1
					node = ConditionNode(self.depth, NODE_COND_END_ANY, r"\.(\s)+")
					lot.append(node)
		return lot