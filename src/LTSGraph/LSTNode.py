class LTSNode:
	id = 0
	def __init__(self):
		self.id = LTSNode.id
		self.t = None
		self.transition_in = []
		self.transition_out = []
		LTSNode.id += 1

	def __str__(self):
		return f"Node {self.id} {self.t} with {len(self.transition_in)} in and {len(self.transition_out)} out"

	def __repr__(self):
		return f"Node {self.id} {self.t}"

	def add_transition(self, t):
		if t.fr == self:
			self.transition_out.append(t)
		elif t.to == self:
			self.transition_in.append(t)

	def tag(self, t):
		self.t = t

	def get_tag(self):
		return self.t