from Anchor import Anchor
from Utils.config import *
class LoopAnchor(Anchor):

	def __init__(self, elem):
		super().__init__(elem["start"], LOOP)
		if elem["type"] == "label":
			self.label = elem["label-regex"]
			self.is_label = True
			self.is_control = False
		elif elem["type"] == "control-flow":
			self.control = elem["control-type"]
			self.is_control = True
			self.is_label = False

	def is_label_anchor(self):
		return self.is_label

	def get_label(seld):
		return self.label

	def is_control_anchor(self):
		return self.is_control

	def get_control(self):
		return self.control
