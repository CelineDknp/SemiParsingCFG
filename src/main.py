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
	dot = r"\.(\s)+"
	anchors = [r"\sIF(\s)+", "ELSE", "END-IF", "EXEC SQL", "'", r"\*", r"\.(\s)+"]
	return anchors

def pre_process(file):
	result = ""
	for line in file.readlines():
		if len(line) == 81:
			result += "      "+(line[6:-9])+"        \n" #Remove the first 6 char (line number) and last 9 (id + \n)
		else:
			result += "      "+(line[6:])#Remove the first 6 char (line number), but not the end
	print(result)
	return result

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
	# print(f"Anchors: {next_pos}", flush=True)
	# print(f"picked: {min_val}, {min_key}")
	return [min_val, min_key]

def clean_anchors(anchors, if_depth):
	if if_depth == 0 and r"\.(\s)+" in anchors:
		return anchors[:-1]
	elif if_depth > 0 and r"\.(\s)+" not in anchors:
		return anchors+[r"\.(\s)+"]
	else:
		return anchors



def fuzzy_parse(input, anchors):
	pos = 0
	lot = []
	if_depth = 0
	anchors = clean_anchors(anchors, if_depth)
	[next_val, n_anchor] = next_anchor(input, pos, anchors)
	while next_val != len(input)+1:
		if n_anchor == r"\*": #Found a comment, skip the whole line !
			# print(">>> FOUND Comment")
			if input.find("\n", next_val) != -1:
				pos = input.find("\n", next_val) +1
			else:
				pos = next_val+len(n_anchor)
		elif n_anchor == "'":
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
		elif n_anchor == r"\sIF(\s)+": #Found a if, take note
			# print('>>> FOUND IF')
			pos = next_val+len(re.search(n_anchor, input[pos:]).group(0))
			node = ConditionNode(if_depth, "IF")
			pos = node.find_condition(input, pos)
			if_depth += 1
			lot.append(node)
			anchors = clean_anchors(anchors, if_depth)
		elif n_anchor == "ELSE":
			# print('>>> FOUND ELSE')
			node = ConditionNode(if_depth-1, "ELSE")
			lot.append(node)
			pos = next_val+len(n_anchor)
		elif n_anchor == "END-IF": #Found a end-if, take note
			# print('>>> FOUND END-IF')
			if_depth -= 1
			node = ConditionNode(if_depth, "END-IF")
			lot.append(node)
			pos = next_val+len(n_anchor)
			anchors = clean_anchors(anchors, if_depth)
		elif n_anchor == r"\.(\s)+":
			# print(">>> FOUND DOT")
			while if_depth > 0:
				if_depth -= 1
				node = ConditionNode(if_depth, "END-IF")
				lot.append(node)
			pos = next_val+1
			anchors = clean_anchors(anchors, if_depth)
		elif n_anchor == "EXEC SQL":
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
		pre_processed_input = pre_process(f)
		print(f"Pre-processed", flush=True)
		lot = fuzzy_parse(pre_processed_input, def_anchors())
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