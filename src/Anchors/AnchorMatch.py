from Utils.config import *


class AnchorMatch:
	def __init__(self, val, regex, match, anchor):
		self.input_start_index = val
		self.regex_matched = regex
		self.actual_match = match
		self.anchor_matched = anchor

	def __lt__(self, other):
		if self.get_start_index() == other.get_start_index():
			return len(self.get_actual_match()) > len(other.get_actual_match())
		return self.get_start_index() < other.get_start_index()

	def __eq__(self, other):
		if self.get_start_index() == other.get_start_index():
			return len(self.get_actual_match()) != len(other.get_actual_match())
		return False


	def __str__(self):
		return f"AnchorMatch of anchor {self.anchor_matched} on position {self.input_start_index} with match {self.actual_match}"

	def get_actual_match(self):
		return self.actual_match

	def get_start_index(self):
		return self.input_start_index

	def get_anchor(self):
		return self.anchor_matched

	def get_regex(self):
		return self.regex_matched

	def get_start_end(self):
		start = self.get_start_index()
		end = start + len(self.get_actual_match())
		return start, end