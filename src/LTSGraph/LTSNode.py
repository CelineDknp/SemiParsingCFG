from Nodes.LabelLoopNode import LabelLoopNode
from Nodes.MultipleLabelLoopNode import MultipleLabelLoopNode
from Nodes.LabelNode import LabelNode


class LTSNode:
	id = 0
	def __init__(self):
		self.id = LTSNode.id
		self.t = None
		self.matches = []
		self.initial_id = None
		self.initial_node = None
		self.transition_in = []
		self.transition_out = []
		LTSNode.id += 1

	def __str__(self):
		return f"Node {self.id} {self.t} with {len(self.transition_in)} in and {len(self.transition_out)} out"

	def __repr__(self):
		return f"Node {self.id} {self.t}"

	def group_match_set(self, set):
		for node in set:
			if node.id not in self.matches:
				self.matches.append(node.id)

	def group_match(self, node):
		if node.id not in self.matches:
			self.matches.append(node.id)

	def has_condition(self):
		return self.initial_node.has_condition()

	def get_transition(self, out=True):
		if out:
			return self.transition_out
		else:
			return self.transition_in

	def has_perform_transition(self):
		for t in self.transition_out:
			if t.get_label() == "PERFORM":
				return True
		return False

	def has_goback_transition(self):
		for t in self.transition_out:
			if t.get_label() == "GOBACK":
				return True
		return False

	def has_single_out(self, go_back_list=[]):
		if len(self.transition_out) == 1:
			return True
		if isinstance(self.initial_node, LabelLoopNode):
			return True #LabelLoopNodes always have one available out link, either the label if we meet them, or the out if we come back
		available_count = 0
		if len(go_back_list) > 0:
			last_perform = go_back_list[-1]  # Can we only goback to the last perform ?
		else:
			last_perform = None
		for elem in self.transition_out:
			if elem.label == "GOBACK" and elem.to == last_perform:
				available_count += 1
			elif elem.label != "GOBACK":
				available_count += 1
		return available_count == 1

	def get_single_transition(self, go_back_list=[], all_performs = []):
		if len(self.transition_out) == 1:
			return self.transition_out[0]
		else:
			if isinstance(self.initial_node, LabelLoopNode):
				if self in all_performs:
					for t in self.transition_out:
						if t.get_label() == "INTERNAL":
							return t
				else:
					for t in self.transition_out:
						if t.get_label() == "PERFORM":
							return t
			if len(go_back_list) > 0:
				last_perform = go_back_list[-1]  # Can we only goback to the last perform ?
			else:
				last_perform = None
			for elem in self.transition_out:
				if elem.label == "GOBACK" and elem.to == last_perform:
					return elem
				elif elem.label != "GOBACK":
					return elem


	def next(self):
		if self.has_single_out():
			return self.transition_out[0].to
		else:
			return None

	def add_transition(self, t):
		if self.id == 21:
			a=0
		if t.fr == self:
			if t not in self.transition_out:
				self.transition_out.append(t)
		elif t.to == self:
			if t not in self.transition_in:
				self.transition_in.append(t)

	def tag(self, t):
		self.t = t

	def get_tag(self):
		return self.t

	def set_initial_id(self, id):
		self.initial_id = id

	def set_initial_node(self, node):
		self.initial_node = node
		self.set_initial_id(node.id)