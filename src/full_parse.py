import sys
import xml.etree.ElementTree as ET 
from Nodes.ConditionNode import ConditionNode
from Nodes.SimpleBranchConditionNode import SimpleBranchConditionNode
from Nodes.MultipleBranchConditionNode import MultipleBranchConditionNode
from Nodes.LoopNode import LoopNode
from Nodes.ControlLoopNode import ControlLoopNode
from Nodes.LabelLoopNode import LabelLoopNode
from Nodes.MultipleLabelLoopNode import MultipleLabelLoopNode
from Nodes.LabelNode import LabelNode
from Nodes.ParseNode import ParseNode
from Nodes.Node import Node
from Nodes.Graph import Graph
from Utils.utils import *
from Utils.config import *
import re

all_labels = {}
loops = []
conditions = []

def get_condition_helper(current, answer):
	if current.text.strip() != "":
		answer.append(current.text)
	for child in current:
		get_condition_helper(child, answer)

def get_condition(statement):
	cond = []
	get_condition_helper(statement, cond)
	return cond

def add_node(node, last_node, graph):
	graph.add_node_to_list(node)
	if isinstance(last_node, LabelLoopNode) and not last_node.is_goback_node():
		if not isinstance(node, LabelNode):
			return
		if node.get_label() not in flatten([last_node.get_label()]):
			return
	if last_node is not None:
		last_node.add_child(node)


def consume_if(statement, current_node, graph, depth):
	# print("found if !")
	cond = get_condition(statement.find("TheCondition"))
	node = SimpleBranchConditionNode(depth, NODE_COND_START, "IF")
	# depth += 1
	# print(cond)
	node.set_condition(" ".join(cond))
	add_node(node, current_node, graph)
	conditions.append(node)
	return node

def get_parse_text_helper(current, answer):
	if current.tag == "TheStmt":
		answer.append(current.get("{http://www.w3.org/2001/XMLSchema}type"))
	if current.text.strip() != "":
		answer.append(current.text)
	for child in current:
		get_parse_text_helper(child, answer)

def get_parse_text(statement):
	parsed = []
	get_parse_text_helper(statement, parsed)
	return parsed

def consume_exec(statement, current_node, graph, depth):
	# print("found exec !")
	# print(f"current_node is: {current_node}")
	node = ParseNode(depth, NODE_SQL, "EXEC")
	parse_text = get_parse_text(statement)
	# print(parse_text)
	node.set_parse_text(" ".join(parse_text))
	add_node(node, current_node, graph)
	return node

def consume_evaluate(statement, current_node, graph, depth):
	# print("found evaluate !")
	cond = get_condition(statement.find("TheEnd"))
	node = MultipleBranchConditionNode(depth, NODE_COND_START, "EVALUATE")
	# depth += 1
	# print(cond)
	node.set_condition(" ".join(cond))
	add_node(node, current_node, graph)
	return node

def consume_next_sentence(statement, current_node, graph, depth):
	# print("hello")
	node = ControlLoopNode.from_explicit(depth, NODE_LOOP, "NEXT SENTENCE", NODE_COND_END_ANY)
	add_node(node, current_node, graph)
	loops.append(node)

def consume_goto(statement, current_node, graph, depth):
	# print("hello")
	label = get_condition(statement)
	node = LabelLoopNode.from_explicit(depth, NODE_LOOP, "GOTO", r"([^\s*.])+(\s)*",False)
	node.set_label(" ".join(label))
	add_node(node, current_node, graph)
	loops.append(node)

def consume_perform(statement, current_node, graph, depth):
	# print("hello")
	label = get_condition(statement.find("TheCodeRef"))
	if len(label) == 1:
		node = LabelLoopNode.from_explicit(depth, NODE_LOOP, "PERFORM", r"([^\s*.])+(\s)*",True)
		node.set_label(" ".join(label))
		add_node(node, current_node, graph)
		loops.append(node)
	elif len(label) == 2:
		node = MultipleLabelLoopNode.from_explicit(depth, NODE_LOOP, "PERFORM", r"(\s)+THRU(\s)*", r"([^\s*.])+(\s)*",True)
		node.set_label(label)
		add_node(node, current_node, graph)
		loops.append(node)
	return node

def consume_label(statement, current_node, graph, depth):
	label = get_condition(statement)
	node = LabelNode(depth, NODE_LABEL, "label")
	node.set_label(" ".join(label))
	all_labels[node.get_label()] = node
	add_node(node, current_node, graph)
	return node

def new_branch(statement, current_node, graph, depth):
	# print("Found new branch !")
	# print(f"current_node is: {current_node}")
	node = find_open_conf(depth)
	node.close_branch()
	cond = get_condition(statement.find("TheGuardList"))
	# print(cond)
	current_node.add_branch_condition(" ".join(cond))
	# print(f"Current node branches: {current_node.branch_childs}")

def find_open_conf(depth):
	result = None
	print(f"Looking for node at depth {depth}")
	for n in conditions:
		print(f"Found open node at depth {n.get_depth()}")
		if n.get_depth() == depth-1:
			result = n
	return result


def close_all(current_node, graph):
	# print("Found end !")
	# print(f"Node is {current_node}")
	while True:
		if isinstance(current_node, list):
			current_node = current_node[0]
		if current_node.get_type() == NODE_COND_START:
			node = Node(-1, NODE_CONTROL)
			current_node.close(node)
			graph.add_node_to_list(node)
			conditions.remove(current_node)
			break
		current_node = current_node.get_parent()

def close_all_conditions(node, graph):
	for c in conditions:
		c.close(node)
		graph.add_node_to_list(node)

def close_true(depth):
	# print("Found else !")
	node = find_open_conf(depth)
	node.close_branch()

def match_labels():
	for l in loops:
		if isinstance(l, LabelLoopNode):
			if isinstance(l.get_label(), str):
				l.add_child(all_labels[l.get_label()])
			else:
				for label in l.get_label():
					l.add_child(all_labels[label])

def match_control(node):
	to_remove = []
	for l in loops:
		if isinstance(l, ControlLoopNode):
			l.add_child(node, match=True)
			to_remove.append(l)
	for l in to_remove:
		loops.remove(l)


def handle_statement(statement, current_node, graph, depth):
	# print(f"Handle start: {statement.tag}")
	if current_node != None:
		current_node = flatten(current_node.get_last_childs())[-1]
		#print(current_node)
		#print(f"node: {current_node} node depth: {current_node.get_depth()} depth: {depth}")

	# print(f"last{graph.get_last_node()}")
	#if current_node != graph.get_last_node():
	#	if not isinstance(graph.get_last_node(), LoopNode):
	#		current_node = graph.get_last_node()
	#	elif isinstance(graph.get_last_node(), LoopNode) and graph.get_last_node().is_goback_node():
	#		current_node = graph.get_last_node()
	#	elif isinstance(graph.get_last_node(), LoopNode) and not graph.get_last_node().is_goback_node():
	#		current_node = None
	#print(statement.tag)
	if statement.get("{http://www.w3.org/2001/XMLSchema}type") == "IfStatement":
		current_node = consume_if(statement, current_node, graph, depth)
	elif statement.get("{http://www.w3.org/2001/XMLSchema}type") == "ExecStatement":
		current_node = consume_exec(statement, current_node, graph, depth)
	elif statement.get("{http://www.w3.org/2001/XMLSchema}type") == "EvaluateStatement":
		current_node = consume_evaluate(statement, current_node, graph, depth)
	elif statement.get("{http://www.w3.org/2001/XMLSchema}type") == "NextSentenceStatement":
		current_node = consume_next_sentence(statement, current_node, graph, depth)
	elif statement.get("{http://www.w3.org/2001/XMLSchema}type") == "PerformStatement":
		current_node = consume_perform(statement, current_node, graph, depth)
	elif statement.get("{http://www.w3.org/2001/XMLSchema}type") == "GotoStatement":
		current_node = consume_goto(statement, current_node, graph, depth)
	if statement.get("NbPeriods") == "1":
		el = ET.Element('DOT')
		print("FOUND DOT")
		statement.append(el)
	if statement.tag == "TheElseStatementList":
		close_true(depth)
	elif statement.tag == "ALabelIdent":
		current_node = consume_label(statement, current_node, graph, depth)
	elif statement.tag == "TheClauses" and statement.get("{http://www.w3.org/2001/XMLSchema}type") == "ElseClause":
		new_branch(statement, current_node, graph, depth)
	elif statement.tag == "TheEnd":
		close_all(current_node, graph)
	elif statement.tag == "DOT":
		node = Node(-1, NODE_CONTROL)
		close_all_conditions(node, graph)
		match_control(node)
		add_node(node, current_node, graph)

	for child in statement.getchildren():
		# print(f"Sending {current_node} with {child} from {statement}")
		handle_statement(child, current_node, graph, depth+1)


def make_graph(filename):
	tree = ET.parse(filename)
	root = tree.getroot()
	procedure = root.getchildren()[0].find("TheProcedureDivision")
	root = Node(0, "START")
	graph = Graph(root)
	for statements in procedure:
		handle_statement(statements, root, graph, 0)
	end = Node(0, "END")
	last = flatten(graph.all_nodes[-1].get_last_childs())[0]
	last.add_child(end)
	graph.add_node_to_list(end)
	match_labels()
	graph.cleanup()
	# print(graph)
	graph.save_as_file("test.gvz")

if __name__ == '__main__':
	print("Running")
	# Pass the path of the xml document 
	make_graph(sys.argv[1])
