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
		self.anchors_creation()
		self.anchors_dict = {}
		self.initial_anchors = self.anchors.copy()
		self.initial_dict = self.get_anchors_and_regex_dict().copy()

	def reset_anchors(self):
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
				result[a.get_start_pattern()] = a
				result[a.get_branch_pattern()] = a
				result[a.get_end_pattern()] = a
			elif a.get_type() == LOOP and a.is_block_anchor():
				result[a.get_start_pattern()] = a
				result[a.get_end_pattern()] = a
			else:
				result[a.get_pattern()] = a
		return result

	def get_anchors(self):
		return self.anchors_dict.copy()

	def get_anchor(self, regex):
		if regex in self.anchors_dict:
			return self.anchors_dict[regex]
		else:
			print(f"Error, looking for anchor {regex} but was not in anchor handler !")

	def get_special_anchor(self, tag):
		return self.special_anchors[tag]

	def get_special_pattern(self, tag):
		return self.special_anchors[tag].get_pattern()

	def has_special(self, tag):
		return tag in self.special_anchors

