from .Anchor import Anchor
from Utils.config import *
class ConditionAnchor(Anchor):

	def __init__(self, elem):
		all_regex = []
		self.condition_delimiter = None
		for key in elem.keys():
			if key == "start":
				self.start_regex = elem[key]
				self.start_pattern = re.compile(elem[key], flags=re.MULTILINE|re.IGNORECASE)
				all_regex.append(elem[key])
			elif key == "end":
				self.end_regex = elem[key]
				self.end_pattern = re.compile(elem[key], flags=re.MULTILINE|re.IGNORECASE)
				all_regex.append(elem[key])
			elif key == "condition_delimiter":
				self.condition_delimiter = re.compile(elem[key], flags=re.MULTILINE|re.IGNORECASE)
			elif key == "mandatory_delimiter":
				self.delimiter_mandatory = elem[key]
			elif key == "special_case": #Skip the special case key
				continue
			else:
				self.branch_regex = elem[key]
				self.branch_pattern = re.compile(elem[key], flags=re.MULTILINE|re.IGNORECASE)
				all_regex.append(elem[key])
		super().__init__(all_regex, CONDITION)
		if "multiple_branch" in elem.keys():
			self.multiple_branches = True
		else:
			self.multiple_branches = False

	def has_condition_delimiter(self):
		return self.condition_delimiter is not None

	def is_delimiter_mandatory(self):
		return self.delimiter_mandatory

	def get_delimiter(self):
		return self.condition_delimiter

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
