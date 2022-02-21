import sys
import xml.etree.ElementTree as ET 
from Nodes.ConditionNode import ConditionNode
from Nodes.ParseNode import ParseNode
from Nodes.Node import Node
from Nodes.Graph import Graph
from Utils.utils import *

def get_condition_helper(current, answer):
	if current.text.strip() != "":
		answer.append(current.text)
	for child in current:
		get_condition_helper(child, answer)

def get_condition(statement):
	cond = []
	get_condition_helper(statement, cond)
	return cond 

def consume_if(statement, current_node, graph, depth):
	# print("found if !")
	cond = get_condition(statement.find("TheCondition"))
	node = ConditionNode(depth, "IF")
	# depth += 1
	# print(cond)
	node.set_condition(" ".join(cond))
	current_node.add_child(node)
	graph.add_node_to_list(node)
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
	node = ParseNode(depth, "EXEC")
	parse_text = get_parse_text(statement)
	# print(parse_text)
	node.set_parse_text(" ".join(parse_text))
	current_node.add_child(node)
	graph.add_node_to_list(node)
	return node

def close_all(current_node):
	# print("Found end !")
	# print(f"Node is {current_node}")
	while True:
		if current_node.get_type() == "IF":
			current_node.close(Node(-1, "CONTROL"))
			break
		current_node = current_node.get_parent()

def close_true(current_node):
	# print("Found else !")
	# print(f"Node is {current_node}")
	while True:
		if current_node.get_type() == "IF":
			current_node.close_branch()
			break
		current_node = current_node.get_parent()


def handle_statement(statement, current_node, graph, depth):
	# print(statement.tag)
	if statement.get("{http://www.w3.org/2001/XMLSchema}type") == "IfStatement":
		current_node = consume_if(statement, current_node, graph, depth)
	if statement.get("{http://www.w3.org/2001/XMLSchema}type") == "ExecStatement":
		current_node = consume_exec(statement, current_node, graph, depth)
	if statement.tag == "TheElseStatementList":
		close_true(current_node)
	if statement.tag == "TheEnd":
		close_all(current_node)
	for child in statement.getchildren():
		handle_statement(child, current_node, graph, depth)



if __name__ == '__main__':
	print("Running")
	# Pass the path of the xml document 
	tree = ET.parse(sys.argv[1])
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
	graph.cleanup()
	print(graph)
	graph.save_as_file("test.gvz")
