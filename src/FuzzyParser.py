from config import *
from Nodes.ConditionNode import ConditionNode
from Nodes.ParseNode import ParseNode
from Nodes.Node import Node
import re

class FuzzyParser():
	def anchors_creation(self):
		self.ignore_anchors = []
		self.condition_anchors = []
		self.loop_anchors = []
		self.parse_anchors = []
		self.special_anchors = []
		self.anchors = []
		for elem in conditions:
			self.condition_anchors += elem.values()
		for elem in parsable:
			self.parse_anchors.append(elem["start"])
		for elem in special:
			self.special_anchors.append(elem["regex"])
		self.ignore_anchors = to_ignore
		self.anchors = self.ignore_anchors+self.condition_anchors+self.parse_anchors+self.special_anchors

	def __init__(self, input):
		self.anchors_creation()
		self.input = input
		self.pos = 0
		self.if_depth = 0

	def next_anchor(self):
		# print(f"Searching from: {input[pos:pos+50]}")
		next_pos = []
		for val in self.anchors:
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
		return [min_val, min_key]

	def clean_anchors(self):
		if self.if_depth == 0 and r"\.(\s)+" in self.anchors:
			self.anchors = self.anchors[:-1]
		elif self.if_depth > 0 and r"\.(\s)+" not in self.anchors:
			self.anchors += [r"\.(\s)+"]

	def consume_ignore(self, n_anchor, next_val):
		if n_anchor == r"\*": #Found a comment, skip the whole line !
			# print(">>> FOUND Comment")
			if self.input.find("\n", next_val) != -1:
				self.pos = self.input.find("\n", next_val) +1
			else:
				self.pos = next_val+len(n_anchor)
		elif n_anchor == "'":
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

	def consume_condition(self, n_anchor, next_val, lot):
		if n_anchor == r"\sIF(\s)+": #Found a if, take note
			# print('>>> FOUND IF')
			self.pos = next_val+len(re.search(n_anchor, self.input[self.pos:]).group(0))
			node = ConditionNode(self.if_depth, "IF")
			self.pos = node.find_condition(self.input, self.pos)
			self.if_depth += 1
			lot.append(node)
		elif n_anchor == "ELSE":
			# print('>>> FOUND ELSE')
			node = ConditionNode(self.if_depth-1, "ELSE")
			lot.append(node)
			self.pos = next_val+len(n_anchor)
		elif n_anchor == "END-IF": #Found a end-if, take note
			# print('>>> FOUND END-IF')
			self.if_depth -= 1
			node = ConditionNode(self.if_depth, "END-IF")
			lot.append(node)
			self.pos = next_val+len(n_anchor)

	def fuzzy_parse(self):
		lot = []
		self.clean_anchors()
		[next_val, n_anchor] = self.next_anchor()
		while next_val != len(self.input)+1:
			if n_anchor in self.ignore_anchors:
				self.consume_ignore(n_anchor, next_val)
			elif n_anchor in self.condition_anchors:
				self.consume_condition(n_anchor, next_val, lot)
				self.clean_anchors()
			elif n_anchor == r"\.(\s)+":
				# print(">>> FOUND DOT")
				while self.if_depth > 0:
					self.if_depth -= 1
					node = ConditionNode(self.if_depth, "END-IF")
					lot.append(node)
				self.pos = next_val+1
				self.clean_anchors()
			elif n_anchor == r"EXEC\sSQL":
				# print('>>> FOUND EXEC')
				node = ParseNode(self.if_depth, "EXEC")
				lot.append(node)
				self.pos = node.find_parse_text(self.input, next_val)
			else:
				self.pos += 1
			[next_val, n_anchor] = self.next_anchor()
		if self.input[-1] == ".": #If last character of input is a dot, close any remaining open things
			while self.if_depth > 0:
					self.if_depth -= 1
					node = ConditionNode(self.if_depth, "END-IF")
					lot.append(node)
		return lot