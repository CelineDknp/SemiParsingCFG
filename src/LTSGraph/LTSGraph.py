from Nodes.Graph import Graph
from Utils.config import *
from .LSTNode import LTSNode
from .LSTTransition import LTSTransition


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

	def add_node(self, n):
		self.all_states.append(n)

	def has_node(self, tag):
		for s in self.all_states:
			if s.get_tag() == tag:
				return s
		return None

	def create(self, tag):
		to_add = LTSNode()
		to_add.tag(tag)
		self.add_node(to_add)
		return to_add

	def link(self, node_from, node_to, cond_tag):
		t = LTSTransition(node_from, node_to, cond_tag)
		node_from.add_transition(t)
		node_to.add_transition(t)


	def import_graph(self, graph):
		#Create all of the nodes
		for n in graph.all_nodes:
			tag = str(n.id)+n.get_type()
			if n.get_type() == "LABEL":
				tag = str(n.id)+n.get_label()
			to_add = self.create(tag)
			self.corr[n] = to_add

		for n in graph.all_nodes:
			for child in n.get_childs():
				f = self.corr[n]
				t = self.corr[child]
				tag = ""
				if n.get_type() == "COND_START" and child == n.true_child:
					tag = n.get_condition()
				elif n.get_type() == "COND_START" and child == n.false_child:
					tag = "NOT " + n.get_condition()
				elif n.get_type() == "LABEL":
					tag = "Lab: "+n.get_label()
				elif n.get_type() == "LOOP": #TODO figure out how to draw the performs until
					a = "test"
					print(n.get_condition_str())
				self.link(f, t, tag)
