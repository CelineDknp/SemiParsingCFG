class TraceMatch:

	def __init__(self, followed_label, node1_f, node2_f, node1_t, node2_t, perform_g1, perform_g2, match=True, other_label=None):
		self.followed_label = followed_label
		self.node1_from = node1_f
		self.node1_to = node1_t
		self.node2_from = node2_f
		self.node2_to = node2_t
		self.match = match
		self.perform_g1 = perform_g1.copy()
		self.perform_g2 = perform_g2.copy()
		if other_label is None:
			self.other_label = followed_label
		else:
			self.other_label = other_label

	def __str__(self):
		return f"TraceMatch between {self.node1_from} and {self.node2_from} label {self.followed_label}"

	def __repr__(self):
		return f"TraceMatch between {self.node1_from} and {self.node2_from}"

	def __eq__(self, other): # Ugly but should work
		if isinstance(other, TraceMatch):
			if self.node1_from == other.node1_from and self.node2_from == other.node2_from:
				if self.node1_to == other.node1_to and self.node2_to == other.node2_to:
					return True
				elif self.node1_to == other.node2_to and self.node2_to == other.node1_to:
					return True
			elif self.node1_from == other.node2_from and self.node2_from == other.node1_from:
				if self.node1_to == other.node1_to and self.node2_to == other.node2_to:
					return True
				elif self.node1_to == other.node2_to and self.node2_to == other.node1_to:
					return True
		return False

	def node1(self):
		return self.node1_to

	def node2(self):
		return self.node2_to

	def node1_f(self):
		return self.node1_from

	def node2_f(self):
		return self.node2_from

	def was_match(self):
		return self.match

	def get_couple(self):
		return self.node1_to, self.node2_to

	def followed_perform(self):
		return self.followed_label == "PERFORM"

	def followed_perform_node1(self):
		return self.followed_perform()

	def followed_perform_node2(self):
		return self.other_label == "PERFORM"

	def __eq__(self, other):
		nodes = (self.node1() == other.node1() and self.node2() == other.node2() and self.node1_f() == other.node1_f() and self.node2_f() == other.node2_f()) or (self.node1() == other.node2() and self.node2() == other.node1() and self.node1_f() == other.node2_f() and self.node2_f() == other.node1_f())
		return nodes and self.perform_g1 == other.perform_g1 and self.perform_g2 == other.perform_g2
