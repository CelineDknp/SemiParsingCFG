class LTSTransition:
	def __init__(self, fr, to, label):
		self.fr = fr
		self.to = to
		self.label = label

	def get_label(self):
		return self.label

	def __str__(self):
		return f"Transition '{self.label}' {self.fr.__repr__()} -> {self.to.__repr__()}"

	def __repr__(self):
		return f"Transition '{self.label}' {self.fr.__repr__()} -> {self.to.__repr__()}"