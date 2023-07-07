class LTSTransition:
	def __init__(self, fr, to, label):
		self.fr = fr
		self.to = to
		self.label = label
		self.match = -2

	def get_label(self):
		return self.label

	def set_match(self, value):
		self.match = value # 1 = sure match 0 = unsure, -1 = unmatch, -2 = unexplored

	def __eq__(self, other):
		if not isinstance(other, LTSTransition):
			return False
		return self.fr == other.fr and self.to == other.to and self.label == other.label

	def __str__(self):
		return f"Transition '{self.label}' {self.fr.__repr__()} -> {self.to.__repr__()} [{self.match}]"

	def __repr__(self):
		return f"Transition '{self.label}' {self.fr.__repr__()} -> {self.to.__repr__()} [{self.match}]"