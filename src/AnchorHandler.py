from Anchors.ConditionAnchor import ConditionAnchor
from Anchors.LoopAnchor import LoopAnchor
from Anchors.SpecialAnchor import SpecialAnchor
from Anchors.IgnoreAnchor import IgnoreAnchor
from Anchors.Anchor import Anchor
from Utils.config import *


class AnchorHandler:
	def __init__(self):
		self.label_regex = []
		self.special_anchors = {}
		self.anchors = []
		self.banned_regex = []
		self.anchors_creation()
		self.anchors_dict = {}
		self.initial_anchors = self.anchors.copy()
		self.initial_dict = self.get_anchors_and_regex_dict().copy()

	def reset_anchors(self):
		self.banned_regex = []
		self.anchors = self.initial_anchors.copy()
		self.anchors_dict = self.initial_dict.copy()

	def anchors_creation(self):
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

	def get_anchors_and_regex_dict(self):
		result = {}
		for a in self.anchors:
			if a.get_type() == CONDITION:
				if a.get_start_pattern() not in self.banned_regex:
					result[a.get_start_pattern()] = a
				if a.get_branch_pattern() not in self.banned_regex:
					result[a.get_branch_pattern()] = a
				if a.get_end_pattern() not in self.banned_regex:
					result[a.get_end_pattern()] = a
			elif a.get_type() == LOOP and a.is_block_anchor():
				result[a.get_start_pattern()] = a
				result[a.get_end_pattern()] = a
			else:
				if a.get_pattern() not in self.banned_regex:
					result[a.get_pattern()] = a
		return result

	def ban_anchor(self, anchor):
		self.ban_regex(anchor.get_pattern())

	def ban_regex(self, regex):
		if regex not in self.banned_regex:
			self.banned_regex.append(regex)
			self.anchors_dict.pop(regex)

	def unban_anchor(self, anchor):
		regex = anchor.get_pattern()
		if regex in self.banned_regex:
			self.banned_regex.remove(regex)
			self.anchors_dict[regex] = anchor

	def clean_anchors(self, depth, open_control, start_parse=False, found_control=False, init=False):
		if start_parse:
			start_parse_anchor = self.special_anchors["start_parse"]
			self.anchors.remove(start_parse_anchor)
			self.anchors_dict.pop(start_parse_anchor.get_pattern())
		elif found_control:
			control_anchor = self.special_anchors["control-regex"]
			if control_anchor in self.anchors:
				self.anchors.remove(control_anchor)
				self.ban_anchor(control_anchor)
				return "banned"
			else:
				self.anchors.append(control_anchor)
				if control_anchor.get_pattern() in self.banned_regex:
					self.unban_anchor(control_anchor)
					return "unbanned"
		else:
			if "close_all" in self.special_anchors:
				close_anchor = self.special_anchors["close_all"]
				if init:
					self.ban_anchor(close_anchor)
					return "banned"
				if depth == 0 and close_anchor.get_pattern() not in self.banned_regex and not open_control:
					self.ban_anchor(close_anchor)
					return "banned"
				elif depth > 0 and close_anchor.get_pattern() in self.banned_regex:
					self.unban_anchor(close_anchor)
					return "unbanned"
		return "nothing"

	def get_anchors(self):
		return self.anchors_dict.copy()

	def get_anchor(self, regex):
		return self.anchors_dict[regex]

	def get_special_anchor(self, tag):
		return self.special_anchors[tag]

	def get_special_pattern(self, tag):
		return self.special_anchors[tag].get_pattern()

	def has_special(self, tag):
		return tag in self.special_anchors

