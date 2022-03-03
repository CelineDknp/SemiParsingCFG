from Anchor import Anchor
from Utils.config import *
class ConditionAnchor(Anchor):

	def __init__(self, elem):
		all_regex = []
		for key in elem.keys():
			all_regex.append(elem[key])
			# print(key)
			if key == "start":
				self.start_regex = elem[key]
			elif key == "end":
				self.end_regex = elem[key]
			else:
				self.branch_regex = elem[key]
		super().__init__(all_regex, CONDITION)
		if "multiple_branch" in elem.keys():
			self.multiple_branches = True
		else:
			self.multiple_branches = False

	def get_start(self):
		return self.start_regex

	def get_branch(self):
		return self.branch_regex

	def get_end(self):
		return self.end_regex

	def is_multiple_branches(self):
		return self.multiple_branches
