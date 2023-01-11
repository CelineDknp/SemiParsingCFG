class LTSTransition:
	def __init__(self, fr, to, label):
		self.fr = fr
		self.to = to
		self.label = label
		self.match = -1

	def get_label(self):
		return self.label

	def set_match(self, value):
		self.match = value # 1 = sure match 0 = unsure and -1 = unmatch

	def __str__(self):
		return f"Transition '{self.label}' {self.fr.__repr__()} -> {self.to.__repr__()} [{self.match}]"

	def __repr__(self):
		return f"Transition '{self.label}' {self.fr.__repr__()} -> {self.to.__repr__()} [{self.match}]"