from Anchor import Anchor
from Utils.config import *


class SpecialAnchor(Anchor):

	def __init__(self, elem, info=None):
		super().__init__(elem["regex"], SPECIAL)
		self.effect = elem["effect"]
		self.info = info

	@classmethod
	def from_explicit(cls, regex, effect, info=None):
		elem = {"regex": regex, "effect": effect}
		return cls(elem, info)

	def get_info(self):
		return self.info

	def get_effect(self):
		return self.effect
