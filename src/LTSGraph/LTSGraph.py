from Utils.config import *
from .LSTNode import LTSNode
from .LSTTransition import LTSTransition
from Nodes.BlockLoopNode import BlockLoopNode
import graphviz


class LTSGraph:

	def __init__(self):
		self.start = None
		self.all_states = []
		self.all_transitions = []
		self.corr= {}

	def __str__(self):
		result = "Nodes in graph:\n"
		for n in self.all_states:
			result += n.__repr__() + "\n"
		return result

	def get_start(self):
		return self.start

	def add_node(self, n):
		if self.start is None:
			self.start = n
		self.all_states.append(n)

	def has_node(self, tag):
		for s in self.all_states:
			if s.get_tag() == tag:
				return s
		return None

	def create(self, input_node):
		to_add = LTSNode()
		tag = input_node.get_type()
		if input_node.get_type() == "LABEL":
			tag = input_node.get_label()
		to_add.tag(tag)
		to_add.set_initial_id(input_node.id)
		self.add_node(to_add)
		return to_add

	def link(self, node_from, node_to, cond_tag):
		t = LTSTransition(node_from, node_to, cond_tag)
		self.all_transitions.append(t)
		node_from.add_transition(t)
		node_to.add_transition(t)


	def import_graph(self, graph):
		#Create all of the nodes
		for n in graph.all_nodes:
			to_add = self.create(n)
			self.corr[n] = to_add

		for n in graph.all_nodes:
			for child in n.get_childs():
				f = self.corr[n]
				t = self.corr[child]
				tag = "INTERNAL"
				if n.get_type() == "COND_START" and child == n.true_child:
					tag = n.get_condition()
					if child == n.false_child: #Node pointing to a single child
						self.link(f, t, "NOT " + n.get_condition()) #Add false link
				elif n.get_type() == "COND_START" and child == n.false_child:
					tag = "NOT " + n.get_condition()
				elif isinstance(n, BlockLoopNode): #Block end
					if n.is_close_node(): #End of the perform
						if child.get_type() == "LOOP": #Block start
							tag = "NOT "+child.get_condition_str()
						else:
							tag = n.childs[-1].get_condition_str()
					else:#Start of the perform
						end = self.corr[n.get_target()]
						self.link(f, end, n.get_condition_str())  # Add link to end_perform
						tag = "NOT "+n.get_condition_str()
					#print(n)
				self.link(f, t, tag)

	def save_as_file(self, filename, output_dir='doctest-output'):
		dot = graphviz.Digraph(filename)
		for current_node in self.all_states:
			#dot.attr('node', shape='ellipse')
			dot.node(str(current_node.id))
		for n in self.all_transitions:
			dot.edge(str(n.fr.id), str(n.to.id), label=n.label)
		dot.render(directory=output_dir, view=False)
