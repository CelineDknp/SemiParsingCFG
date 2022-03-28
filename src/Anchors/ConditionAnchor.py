from .Anchor import Anchor
from Utils.config import *
class ConditionAnchor(Anchor):

	def __init__(self, elem):
		all_regex = []
		for key in elem.keys():
			all_regex.append(elem[key])
			# print(key)
			if key == "start":
				self.start_regex = elem[key]
				self.start_pattern = re.compile(elem[key], re.MULTILINE) 
			elif key == "end":
				self.end_regex = elem[key]
				self.end_pattern = re.compile(elem[key], re.MULTILINE) 
			else:
				self.branch_regex = elem[key]
				self.branch_pattern = re.compile(elem[key], re.MULTILINE) 
		super().__init__(all_regex, CONDITION)
		if "multiple_branch" in elem.keys():
			self.multiple_branches = True
		else:
			self.multiple_branches = False

	def get_start(self):
		return self.start_regex

	def get_start_pattern(self):
		return self.start_pattern

	def get_branch(self):
		return self.branch_regex

	def get_branch_pattern(self):
		return self.branch_pattern

	def get_end(self):
		return self.end_regex

	def get_end_pattern(self):
		return self.end_pattern

	def is_multiple_branches(self):
		return self.multiple_branches
