import sys
import re
from Nodes.ConditionNode import ConditionNode
from Nodes.ParseNode import ParseNode
from Nodes.Node import Node
from Nodes.Graph import Graph
import graphviz
#Windows-specific Graphiz import
import os
total_path = os.pathsep + 'C:\Program Files\Graphviz/bin/'
if total_path not in os.environ["PATH"]:
	os.environ["PATH"] += total_path


def def_anchors():
	#GOTO, PERFORM, IF, EVALUATE
	identifier = r"(\S)+" #At least one character, no whitespace
	operators = "(NOT|=|NOT =|>|>=|<|<=)"
	logic_links = "AND|OR"
	anchors = [r"\sIF(\s)+", "ELSE", "END-IF", r"\.(\s)+","EXEC SQL", "'", r"\*"]
	return anchors

def next_anchor(input, pos, anchors):
	# print(f"Searching from: {input[pos:pos+50]}")
	next_pos = []
	for val in anchors:
		res = re.search(val, input[pos:].upper())
		if res != None:
			next_pos.append({val:input.upper().find(res.group(0), pos)})
		else:
			next_pos.append({val:-1})
	min_val = len(input)+1
	min_key = ""
	for index in range(len(next_pos)):
		for key in next_pos[index]:
			val = next_pos[index][key]
			if val < min_val and val != -1:
				min_val = val 
				min_key = key
	return [min_val, min_key]



def fuzzy_parse(input, anchors):
	pos = 0
	lot = []
	if_depth = 0
	[next_val, n_anchor] = next_anchor(input, pos, anchors)
	while next_val != len(input)+1:
		# print(f"Looking at: {input[pos:pos+20]}")
		if n_anchor == anchors[-1]: #Found a comment, skip the whole line !
			# print(">>> FOUND Comment")
			if input.find("\n", next_val) != -1:
				pos = input.find("\n", next_val) +1
			else:
				pos = next_val+len(n_anchor)
		elif n_anchor == anchors[5]:
			# print(">>> Found string")
			old = pos-1
			next_quote = input.find("'", next_val+1)
			next_line = input.find("\n", next_val+1)
			dash = input[:next_line+30].find("-", next_line)
			if next_quote <= next_line:
				pos = next_quote+1
			elif next_line < next_quote and dash != -1:
				pos = next_line+1
			else:
				pos = next_val+len(n_anchor)
		elif n_anchor == anchors[0]: #Found a if, take note
			# print('>>> FOUND IF')
			pos = next_val+len(re.search(n_anchor, input[pos:]).group(0))
			node = ConditionNode(if_depth, "IF")
			pos = node.find_condition(input, pos)
			if_depth += 1
			lot.append(node)
		elif n_anchor == anchors[1]:
			# print('>>> FOUND ELSE')
			node = ConditionNode(if_depth-1, "ELSE")
			lot.append(node)
			pos = next_val+len(n_anchor)
		elif n_anchor == anchors[2]: #Found a end-if, take note
			# print('>>> FOUND END-IF')
			if_depth -= 1
			node = ConditionNode(if_depth, "END-IF")
			lot.append(node)
			pos = next_val+len(n_anchor)
		elif n_anchor == anchors[3]:
			# print(">>> FOUND DOT")
			while if_depth > 0:
				if_depth -= 1
				node = ConditionNode(if_depth, "END-IF")
				lot.append(node)
			pos = next_val+1
		elif n_anchor == anchors[4]:
			# print('>>> FOUND EXEC')
			node = ParseNode(if_depth, "EXEC")
			lot.append(node)
			pos = node.find_parse_text(input, next_val)
		else:
			pos += 1
		[next_val, n_anchor] = next_anchor(input, pos, anchors)
	if input[-1] == ".": #If last character of input is a dot, close any remaining open things
		while if_depth > 0:
				if_depth -= 1
				node = ConditionNode(if_depth, "END-IF")
				lot.append(node)
	return lot


def construct_graph(node_array):
	graph = Graph(Node(0, "START") )
	for node in node_array:
		graph.add_node(node)
	graph.add_node(Node(0, "END"))
	return graph

def process_file(filename, dir_path):
	with open(filename, "r") as f:
		print(f"Opened {filename}", flush=True)
		lot = fuzzy_parse(f.read(), def_anchors())
		print(f"Fuzzy parsing done !", flush=True)
		g = construct_graph(lot)
		print(f"Graph constructed !", flush=True)
		g.cleanup()
		print(f"Graph cleaned !", flush=True)
		g.squish()
		print(f"Graph squished !", flush=True)
		g.save_as_file(os.path.basename(f.name), output_dir=dir_path)
		print(f"Done !")




def main(argv):
	process_file(argv[1],"")





if __name__ == '__main__':
	print("Running")
	main(sys.argv)