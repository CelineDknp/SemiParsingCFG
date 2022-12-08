class TraceMatch:

	def __init__(self, followed_label, node1_f, node2_f, node1_t, node2_t):
		self.followed_label = followed_label
		self.node1_from = node1_f
		self.node1_to = node1_t
		self.node2_from = node2_f
		self.node2_to = node2_t

	def followed_label(self):
		return self.followed_label()

	def node1_from(self):
		return self.node1_from

	def node1_to(self):
		return self.node1_to

	def node2_from(self):
		return self.node2_from

	def node2_from(self):
		return self.node2_to

	def get_couple(self):
		return (self.node1_to, self.node2_to)

	def followed_perform(self):
		return self.followed_label == "PERFORM"