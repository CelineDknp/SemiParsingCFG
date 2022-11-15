from .LoopNode import LoopNode
from Anchors import LoopAnchor
from Utils.config import *
from Utils.utils import *


class BlockLoopNode(LoopNode):

	def __init__(self, depth, node_type, anchor, close=False):
		super().__init__(depth, node_type, anchor)
		self.target_node = None
		self.close_node = close
		self.statements_starts = [r"\sIF(\s)+", r"ELSE", r"WHEN", r"EXEC\sSQL", r"\*", r"PERFORM", r"GO(\s)*TO", "MOVE", "DISPLAY", "CONTINUE", "EXIT"]
		self.statements_str = [r"IF", r"ELSE", r"WHEN", r"EXEC SQL", r"\*", r"PERFORM", r"GOTO", r"GO TO", "MOVE", "DISPLAY", "CONTINUE", "EXIT"]
		self.branch_str = ""
		if not close:
			self.branch = anchor.branch
			self.condition = anchor.condition

			self.condition_str = ""
	def __str__(self):
		if self.is_close_node():
			return f"Node {self.type} (block end)"
		else:
			return f"Node {self.type} (block) {self.get_condition_str()}"

	def is_block(self):
		return True

	def is_close_node(self):
		return self.close_node

	#Points to target node: end block for the start, start for the end
	def set_target(self, target):
		self.target_node = target

	def get_target(self):
		return self.target_node

	def find_conditions(self, actual_match, input, pos):
		until_start = actual_match.find(self.condition)
		if self.branch in actual_match:
			self.branch_str = clean_str(actual_match[actual_match.find(self.branch):until_start])
		until_full = input.find("UNTIL",pos)
		self.condition_str = self.find_condition_simple(input,until_full+5)#5 = length "UNTIl"

	def is_anchor(self, input):
		if not any(substring in input for substring in self.statements_str):
			return -1
		for val in self.statements_starts:
			# print(f"Looking for {val}")
			res = re.search(val, input)
			if res != None:
				return input.find(res.group(0))
		return -1

	def find_condition_simple(self, input, pos):
		go = True
		cond = ""
		test = input[pos:pos+100]
		new_line = input.find("\n", pos)
		is_anchor = self.is_anchor(input[pos:new_line])
		if is_anchor != -1:
			next = input[pos + 1:pos + is_anchor]
			self.condition = clean_str(next)
			# print(f"COND: {self.condition} for {input[pos-10:pos+15]}")
			return pos + len(next)
		else:
			next_line = input[pos + 1:new_line]
		first = True
		temp_pos = pos
		while go:
			# print(f"Current cond is: {cond}")
			# print(f"Looking at next line: {next_line}")
			if not first:
				if self.is_anchor(next_line) != -1:
					# print("saw anchor")
					go = False
				elif re.search(r'^(\s)*[^\s-]+(\s)*$', next_line):  # Special case of just one thing to finish the line
					# print("saw signe element")
					if any(x in next_line for x in self.statements_starts):
						# print("saw move")
						go = False
					else:
						# print("condition kept going")
						cond += next_line.lstrip()
						temp_pos = new_line + 1
				elif any(x in next_line for x in [">", "<", " IS ", " NOT ", " OR ", " AND ", " NUMERIC "]):
					# print("Saw signe")
					cond += next_line.strip() + " "
					temp_pos = new_line + 1
				else:
					# print("Saw nothing of interest, stop")
					go = False
			else:
				cond += next_line.strip() + " "
				temp_pos = new_line + 1
			first = False
			new_line = input.find("\n", temp_pos)
			next_line = input[temp_pos:new_line]
		return clean_str(cond)

	def get_branch_str(self):
		return self.branch_str

	def get_condition_str(self):
		return self.condition_str

	def set_condition_str(self, cond):
		self.condition_str = cond

	def get_end_block(self):
		for e in self.parents:
			if isinstance(e, BlockLoopNode):
				return e
