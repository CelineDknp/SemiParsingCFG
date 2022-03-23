from Anchor import Anchor
from Utils.config import *
class LoopAnchor(Anchor):

	def __init__(self, elem):
		if elem["type"] == "multiple_label":
			super().__init__(elem["start"]+elem["inline-label"]+elem["separator"], LOOP)
			self.start_regex = re.compile(elem["start"], re.MULTILINE)
			self.label = re.compile(elem["inline-label"], re.MULTILINE)
			self.separator = re.compile(elem["separator"], re.MULTILINE)
			self.is_multiple = True
			self.is_label = True
			self.is_control = False
		elif elem["type"] == "label":
			super().__init__(elem["start"]+elem["inline-label"], LOOP)
			self.start_regex = re.compile(elem["start"], re.MULTILINE)
			self.label = re.compile(elem["inline-label"], re.MULTILINE)
			self.is_label = True
			self.is_multiple = False
			self.is_control = False
		elif elem["type"] == "control-flow":
			super().__init__(elem["start"], LOOP)
			self.control = elem["control-type"]
			self.is_control = True
			self.is_multiple = False
			self.is_label = False
		self.go_back = elem["goback"]

	def is_label_anchor(self):
		return self.is_label

	def is_multiple_anchor(self):
		return self.is_multiple

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
