from Utils.config import *
import re
class Anchor():
	def __init__(self, regex, type):
		if isinstance(regex,str): 
			self.pattern = re.compile(regex, flags=re.MULTILINE|re.IGNORECASE) 
		self.regex = regex
		self.type = type

	def get_type(self):
		return self.type

	def get_regex(self):
		return self.regex

	def get_pattern(self):
		return self.pattern

	def __str__(self):
		return f"Anchor with {self.regex} of type {self.type}"

	def __repr__(self):
		return f"Anchor with {self.regex} of type {self.type}"