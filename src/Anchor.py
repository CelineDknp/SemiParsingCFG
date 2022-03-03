from Utils.config import *
class Anchor():
	def __init__(self, regex, type):
		self.regex = regex
		self.type = type

	def get_type(self):
		return self.type

	def get_regex(self):
		return self.regex

	def __str__(self):
		return f"Anchor with {self.regex} of type {self.type}"

	def __repr__(self):
		return f"Anchor with {self.regex} of type {self.type}"