from .Anchor import Anchor
from Utils.config import *

class LoopAnchor(Anchor):
	def __init__(self, elem):
		self.is_label = False
		self.is_multiple = False
		self.is_control = False
		self.is_block = False
		if elem["type"] == "multiple_label":
			super().__init__(elem["start"]+elem["inline-label"]+elem["separator"]+elem["inline-label"], LOOP)
			self.start_regex = re.compile(elem["start"], flags=re.MULTILINE|re.IGNORECASE)
			self.label = re.compile(elem["inline-label"], flags=re.MULTILINE|re.IGNORECASE)
			self.separator = re.compile(elem["separator"], flags=re.MULTILINE|re.IGNORECASE)
			self.is_multiple = True
			self.is_label = True
		elif elem["type"] == "label":
			super().__init__(elem["start"]+elem["inline-label"], LOOP)
			self.start_regex = re.compile(elem["start"], flags=re.MULTILINE|re.IGNORECASE)
			self.label = re.compile(elem["inline-label"], flags=re.MULTILINE|re.IGNORECASE)
			self.is_label = True
		elif elem["type"] == "control-flow":
			super().__init__(elem["start"], LOOP)
			self.control = elem["control-type"]
			self.is_control = True
		elif elem["type"] == "block":
			self.end_regex = elem["end"]
			self.start_pattern = re.compile(elem["start"], flags=re.MULTILINE|re.IGNORECASE)
			self.end_pattern = re.compile(elem["end"], flags=re.MULTILINE|re.IGNORECASE)
			self.branch = elem["branch"]
			self.condition = elem["condition"]
			super().__init__([elem["start"], elem["end"]], LOOP)
			self.is_block = True
		self.go_back = elem["goback"]

	def is_label_anchor(self):
		return self.is_label

	def is_multiple_anchor(self):
		return self.is_multiple

	def is_block_anchor(self):
		return self.is_block

	def is_goback_anchor(self):
		return self.go_back

	def get_separator(self):
		return self.separator

	def get_label(self):
		return self.label

	def get_start_regex(self):
		return self.start_regex

	def is_control_anchor(self):
		return self.is_control

	def get_control(self):
		return self.control

	def get_start_pattern(self):
		return self.start_pattern

	def get_end_pattern(self):
		return self.end_pattern
