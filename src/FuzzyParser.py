from Utils.config import *
from Nodes.SimpleBranchConditionNode import SimpleBranchConditionNode
from Nodes.MultipleBranchConditionNode import MultipleBranchConditionNode
from Nodes.ConditionNode import ConditionNode
from Nodes.ParseNode import ParseNode
from Nodes.Node import Node
from ConditionAnchor import ConditionAnchor
from Anchor import Anchor
import re

class FuzzyParser():
	def anchors_creation(self):
		self.anchors = []
		self.special_anchors = {}
		for elem in conditions:
				self.anchors.append(ConditionAnchor(elem))
		for elem in parsable:
			self.anchors.append(Anchor(elem["start"], PARSABLE))
		for elem in special:
			s = Anchor(elem["regex"], SPECIAL)
			self.anchors.append(s)
			self.special_anchors[elem["effect"]] = s
		for elem in to_ignore:
			self.anchors.append(Anchor(elem, IGNORE))
		self.anchors_dict = self.current_anchors_and_regexes()

	def __init__(self, input):
		self.anchors_creation()
		self.input = input
		self.pos = 0
		self.depth = 0

	def current_anchors_and_regexes(self):
		result = {}
		for a in self.anchors:
			if a.get_type() == CONDITION:
				result[a.get_start()] = a
				result[a.get_branch()] = a
				result[a.get_end()] = a
			else:
				result[a.get_regex()] = a
		return result

	def next_anchor(self):
		# print(f"Searching from: {self.input[self.pos:self.pos+50]}")
		next_pos = []
		for val in self.anchors_dict.keys():
			res = re.search(val, self.input[self.pos:].upper())
			if res != None:
				next_pos.append({val:self.input.upper().find(res.group(0), self.pos)})
			else:
				next_pos.append({val:-1})
		min_val = len(self.input)+1
		min_key = ""
		for index in range(len(next_pos)):
			for key in next_pos[index]:
				val = next_pos[index][key]
				if val < min_val and val != -1:
					min_val = val 
					min_key = key
		# print(f"Anchors: {next_pos}", flush=True)
		# print(f"picked: {min_val}, {min_key}")
		if min_key != '':
			return min_val, self.anchors_dict[min_key], min_key
		else:
			return min_val, None, min_key

	def clean_anchors(self):
		#Clean the close-all anchor
		if self.depth == 0 and self.special_anchors["close_all"] in self.anchors:
			self.anchors.remove(self.special_anchors["close_all"])
		elif self.depth > 0 and self.special_anchors["close_all"] not in self.anchors:
			self.anchors.append(self.special_anchors["close_all"])

	def consume_ignore(self, n_anchor, next_val, actual_val):
		if actual_val == r"\*": #Found a comment, skip the whole line !
			# print(">>> FOUND Comment")
			if self.input.find("\n", next_val) != -1:
				self.pos = self.input.find("\n", next_val) +1
			else:
				self.pos = next_val+len(n_anchor)
		elif actual_val == "'":
			# print(">>> Found string")
			old = self.pos-1
			next_quote = self.input.find("'", next_val+1)
			next_line = self.input.find("\n", next_val+1)
			dash = self.input[:next_line+30].find("-", next_line)
			if next_quote <= next_line:
				self.pos = next_quote+1
			elif next_line < next_quote and dash != -1:
				self.pos = next_line+1
			else:
				self.pos = next_val+len(n_anchor)

	def consume_condition(self, n_anchor, next_val, actual_val, lot):
		if actual_val == n_anchor.get_start(): #Found an opening condition
			# print(f'>>> FOUND COND start {actual_val}')
			self.pos = next_val+len(re.search(actual_val, self.input[self.pos:]).group(0))
			node = None
			if n_anchor.is_multiple_branches():
				node = MultipleBranchConditionNode(self.depth, NODE_COND_START, n_anchor.get_start())
			else:
				node = SimpleBranchConditionNode(self.depth, NODE_COND_START, n_anchor.get_start())
			self.pos = node.find_condition(self.input, self.pos)
			self.depth += 1
			lot.append(node)
		elif actual_val == n_anchor.get_branch() and (not n_anchor.is_multiple_branches()):
			# print('>>> FOUND COND single branch')
			node = SimpleBranchConditionNode(self.depth - 1, NODE_COND_BRANCH, n_anchor.get_start())
			lot.append(node)
			self.pos = next_val+len(actual_val)
		elif actual_val == n_anchor.get_branch() and n_anchor.is_multiple_branches():
			# print('>>> FOUND COND multiple branch')
			self.pos = next_val+len(re.search(actual_val, self.input[self.pos:]).group(0))
			node = MultipleBranchConditionNode(self.depth - 1, NODE_COND_BRANCH, n_anchor.get_start())
			self.pos = node.find_condition(self.input, self.pos)
			# print(f"Found condition: {node.get_condition()}")
			lot.append(node)
		elif actual_val == n_anchor.get_end(): #Found a COND end
			# print('>>> FOUND END-COND')
			self.depth -= 1
			node = ConditionNode(self.depth, NODE_COND_END, n_anchor.get_start())
			lot.append(node)
			self.pos = next_val+len(actual_val)

	def consume_parsable(self, n_anchor, next_val, actual_val, lot):
		# print('>>> FOUND EXEC')
		node = ParseNode(self.depth, NODE_SQL)
		lot.append(node)
		self.pos = node.find_parse_text(self.input, next_val)

	def consume_special(self, n_anchor, next_val, actual_val, lot):
		# print(">>> FOUND DOT")
		while self.depth > 0:
			self.depth -= 1
			node = ConditionNode(self.depth, NODE_COND_END_ANY, n_anchor.get_regex())
			lot.append(node)
		self.pos = next_val+1

	def fuzzy_parse(self):
		lot = []
		self.clean_anchors()
		next_val, n_anchor, actual_val = self.next_anchor()
		while next_val != len(self.input)+1:
			# print(f"Looking at next_anchor: {n_anchor} of val {actual_val} current depth is: {self.if_depth}")
			if n_anchor.get_type() == IGNORE:
				self.consume_ignore(n_anchor, next_val, actual_val)
			elif n_anchor.get_type() == CONDITION:
				self.consume_condition(n_anchor, next_val, actual_val, lot)
				self.clean_anchors()
			elif n_anchor.get_type() == PARSABLE:
				self.consume_parsable(n_anchor, next_val, actual_val, lot)
			elif n_anchor.get_type() == SPECIAL:
				self.consume_special(n_anchor, next_val, actual_val, lot)
				self.clean_anchors()
			else:
				self.pos += 1
			next_val, n_anchor, actual_val = self.next_anchor()
		if self.input[-1] == ".": #If last character of input is a dot, close any remaining open things
			while self.depth > 0:
					self.depth -= 1
					node = ConditionNode(self.depth, NODE_COND_END_ANY, r"\.(\s)+")
					lot.append(node)
		return lot