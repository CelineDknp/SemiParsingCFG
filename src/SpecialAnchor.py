from Anchor import Anchor
from Utils.config import *
class SpecialAnchor(Anchor):

	def __init__(self, elem):
		super().__init__(elem["regex"], SPECIAL)
		self.effect = elem["effect"]

	@classmethod
	def from_explicit(cls, regex, effect):
		elem = {"regex":regex, "effect":effect}
		return cls(elem)

	def get_effect(self):
		return self.effect