from Utils.config import *
from .LTSNode import LTSNode
from .LTSTransition import LTSTransition
from Nodes.BlockLoopNode import BlockLoopNode
from Nodes.LabelLoopNode import LabelLoopNode
from Nodes.MultipleLabelLoopNode import MultipleLabelLoopNode
from Nodes.LabelNode import LabelNode
import graphviz


class LTSGraph:

	def __init__(self):
		self.start = None
		self.all_states = []
		self.all_transitions = []
		self.all_labels = []
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
			if n.get_type() == "LABEL":
				self.all_labels.append(to_add)
		test = True
		for n in graph.all_nodes:
			for child in n.get_childs():
				f = self.corr[n]
				t = self.corr[child]
				cancel_link = False
				tag = "INTERNAL"
				if n.get_type() == "COND_START" and child == n.true_child:
					tag = n.get_condition()
					if child == n.false_child: #Node pointing to a single child
						self.link(f, t, "NOT " + n.get_condition()) #Add false link
				elif n.get_type() == "COND_START" and child == n.false_child:
					tag = "NOT " + n.get_condition()
				elif isinstance(n, BlockLoopNode): #Block end
					if n.is_close_node() and n.get_target().get_childs()[0] ==n and child == n.get_target():
						cancel_link = True
					else:
						if n.is_close_node() and child != n.get_target():
							if n.get_target().get_childs()[0] != n: #If not, out of a single perform, don't repeat cond !
								tag = n.get_target().get_condition_str()
						elif n.is_close_node() and child == n.get_target():
							tag = "NOT " + n.get_target().get_condition_str()

						elif not n.is_close_node():
							if len(n.get_childs()) == 1 and n.get_childs()[0] == n.get_target():  # We have an empty perform
								t = f
								end = self.corr[n.get_target()]
								self.link(f, end, n.get_condition_str())  # Add link to end_perform
							else:
								end = self.corr[n.get_target().get_childs()[0]]
								self.link(f, end, n.get_condition_str())  # Add link to end_perform
							tag = "NOT " + n.condition_str  # Loop link

				elif isinstance(n, LabelLoopNode) and n.is_goback_node(): #Link perform to its label
					if n.is_multiple_labels():
						if isinstance(child, LabelNode) and child.get_label() == n.start_label():
							tag = "PERFORM"  # Tag the in link
							# Get the out link
							out_label = n.label[-1] #Get the label of the out link
							out_node = graph.all_labels[out_label] #Get the corresponding node
							corr_node = self.corr[out_node]
							index = self.all_labels.index(corr_node)
							if index < len(self.all_labels)-1:
								next_label = self.all_labels[index + 1]  # Corner case with end Node !
							else:
								next_label = self.all_states[-1] #Link to last node (end)
							self.link(next_label, f, "GOBACK")
							if len(n.get_childs()) == 1: #If we have one single child in the perform, we probaby point only to the label
								self.link(f, t, "")
					else:
						if isinstance(child, LabelNode) and child.get_label() == n.go_back_label():
							tag = "PERFORM" #Tag the in link
							#Get the out link
							index = self.all_labels.index(t)
							if index < len(self.all_labels)-1:
								next_label = self.all_labels[index + 1]  # Corner case with end Node !
							else:
								next_label = self.all_states[-1] #Link to last node (end)
							self.link(next_label, f, "GOBACK")

				if not cancel_link:
					self.link(f, t, tag)

	def save_as_file(self, filename, output_dir='doctest-output'):
		dot = graphviz.Digraph(filename)
		for current_node in self.all_states:
			#dot.attr('node', shape='ellipse')
			dot.node(str(current_node.id))
		for n in self.all_transitions:
			dot.edge(str(n.fr.id), str(n.to.id), label=n.label)
		dot.render(directory=output_dir, view=False)
