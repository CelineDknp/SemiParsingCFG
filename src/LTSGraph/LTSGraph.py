from Utils.config import *
from .LTSNode import LTSNode
from .LTSTransition import LTSTransition
from Nodes.BlockLoopNode import BlockLoopNode
from Nodes.LabelLoopNode import LabelLoopNode
from Nodes.MultipleLabelLoopNode import MultipleLabelLoopNode
from Nodes.LabelNode import LabelNode
from Nodes.MultipleBranchConditionNode import MultipleBranchConditionNode
import graphviz


class LTSGraph:
	"""
	Transformed CFG
	-> All info is on the links, not the nodes (nodes only have ID)
	-> All notions of code is stripped out, except when branching, executing SQL and following the PERFORM construct
		-> All labels are ignored, as well as the GOTO (they just point to the correct place in the code)
	-> The branches are no longer True/False, but CONDITION and NOT CONDITION (except for EVALUATEs who keep their branches)
	-> The text of the SQL is put on the link following its node
	-> All links that are not branching or SQL takes the "INTERNAL" tag, meaning that they are equivalent to 0...n other
	   INTERNAL links in the graph we are comparing to
	-> Graph is a list of node and list of transition between the nodes
	"""

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

	def has_node(self, node):
		return node in self.all_states

	def get_start(self):
		return self.start

	def get_size(self):
		return len(self.all_states)

	def get_matches(self):
		res = 0 
		for e in self.all_transitions:
			if e.match == 1:
				res += 1
		return res

	def get_unsure(self):
		res = 0 
		for e in self.all_transitions:
			if e.match == 0:
				res += 1
		return res

	def get_link_size(self):
		return len(self.all_transitions)

	def get_transition(self, id):
		return self.all_transitions[id]

	def add_node(self, n):
		if self.start is None:
			self.start = n
		self.all_states.append(n)

	def has_node(self, node):
		return node in self.all_states

	def has_tag(self, tag):
		for s in self.all_states:
			if s.get_tag() == tag:
				return s
		return None

	def create(self, input_node):
		to_add = LTSNode()
		tag = input_node.get_type()
		if input_node.get_type() == "LABEL":
			tag = input_node.get_label()
		if input_node.get_type() == "EXEC":
			tag = input_node.parsable
		to_add.tag(tag)
		to_add.set_initial_node(input_node)
		self.add_node(to_add)
		return to_add

	def link(self, node_from, node_to, cond_tag):
		t = LTSTransition(node_from, node_to, cond_tag)
		self.all_transitions.append(t)
		node_from.add_transition(t)
		if node_to != node_from:
			node_to.add_transition(t)


	def import_graph(self, graph):
		#Create all of the nodes
		for n in graph.all_nodes:
			to_add = self.create(n)
			self.corr[n] = to_add
			if n.get_type() == "LABEL":
				self.all_labels.append(to_add)
		for n in graph.all_nodes:
			if isinstance(n, MultipleBranchConditionNode): #Special case for EVALUATE
				f = self.corr[n]
				for tup in f.initial_node.get_branches():
					t = self.corr[tup[1]]
					self.link(f, t, tup[0])
			else:
				for child in n.get_childs():
					f = self.corr[n]
					t = self.corr[child]
					cancel_link = False
					tag = "INTERNAL"
					if n.get_type() == "COND_START" and child == n.true_child:
						tag = n.get_condition()
						if child == n.false_child: #Node pointing to a single child
							self.link(f, t, "NOT (" + n.get_condition()+")") #Add false link
					elif n.get_type() == "COND_START" and child == n.false_child:
						tag = "NOT (" + n.get_condition() + ")"
					elif n.get_type() == "EXEC": #SQL node, add the text
						tag = n.parsable
					elif isinstance(n, BlockLoopNode): #Block end
						if n.is_close_node() and n.get_target().get_childs()[0] == n and child == n.get_target():
							cancel_link = True
						else:
							if n.is_close_node() and child != n.get_target():
								if n.get_target().get_childs()[0] != n: #If not, out of a single perform, don't repeat cond !
									tag = n.get_target().get_condition_str()
							elif n.is_close_node() and n.get_target().condition is not None:
								#We have found an END PERFORM
								init_t = n.get_target().get_childs()[0] #Put the to to the perform's child
								t = self.corr[init_t]
								tag = "NOT (" + n.get_target().get_condition_str() + ")"
							elif n.is_close_node() and child == n.get_target():
								tag = "NOT (" + n.get_target().get_condition_str() + ")"
							elif not n.is_close_node():
								target = n.get_target()
								if len(n.get_childs()) == 1 and n.get_childs()[0] == target:  # We have an empty perform
									t = f
									end = self.corr[target]
									self.link(f, end, n.get_condition_str())  # Add link to end_perform
								else:
									end = self.corr[target.get_non_target_child()]
									self.link(f, end, n.get_condition_str())  # Add link to end_perform
								tag = "NOT (" + n.condition_str + ")"  # Loop link

					elif isinstance(n, LabelLoopNode) and n.is_goback_node(): #Link perform to its label
						if n.is_multiple_labels():
							if isinstance(child, LabelNode) and child.get_label() == n.start_label():
								if not f.has_perform_transition():
									tag = "PERFORM"  # Tag the in link
								# Get the out link
								out_label = n.label[-1] #Get the label of the out link
								if out_label in graph.all_labels:
									out_node = graph.all_labels[out_label] #Get the corresponding node
								else:
									return
								corr_node = self.corr[out_node]
								index = self.all_labels.index(corr_node)
								if index < len(self.all_labels)-1:
									next_label = self.all_labels[index + 1]  # Corner case with end Node !
								else:
									next_label = self.all_states[-1] #Link to last node (end)
								if not f.has_goback_transition():
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
					elif isinstance(n, LabelNode) and isinstance(child, MultipleLabelLoopNode) and n.get_label() == child.go_back_label():  # Pointing towards perform, ignore link
						cancel_link = True
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
