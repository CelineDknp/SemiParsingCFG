from .Anchor import Anchor
from Utils.config import *


class IgnoreAnchor(Anchor):

	def __init__(self, elem):
		super().__init__(elem["regex"], IGNORE)
		self.parse_type = elem["type"]

	@classmethod
	def from_explicit(cls, regex, type):
		elem = {"regex": regex, "type": type}
		return cls(elem)

	def get_parse_type(self):
		return self.parse_type