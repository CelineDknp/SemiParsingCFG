import sys
from antlr4 import *
from Parse.MySqlLexer import MySqlLexer
from Parse.MySqlParser import MySqlParser
import re
from Nodes.ConditionNode import ConditionNode
from Nodes.ParseNode import ParseNode
from Nodes.Node import Node
from Nodes.Graph import Graph
import graphviz


SQLL = MySqlLexer
SQLP = MySqlParser

class WriteTreeListener(ParseTreeListener):
	def visitTerminal(self, node:TerminalNode):
		print ("Visit Terminal: " + str(node) + " - " + repr(node))


class CaseChangingStream():
	def __init__(self, stream, upper):
		self._stream = stream
		self._upper = upper

	def __getattr__(self, name):
		return self._stream.__getattribute__(name)

	def LA(self, offset):
		c = self._stream.LA(offset)
		if c <= 0:
			return c
		return ord(chr(c).upper() if self._upper else chr(c).lower())

def def_anchors():
	#GOTO, PERFORM, IF, EVALUATE
	identifier = "(\S)+" #At least one character, no whitespace
	operators = "(NOT|=|NOT =|>|>=|<|<=)"
	logic_links = "AND|OR"
	anchors = ["\sIF(\s)+", "ELSE", "END-IF", "\.(\s)+","EXEC SQL","'", "\*"]
	return anchors

def next_anchor(input, pos, anchors):
	# print(f"Searching from: {input[pos:pos+50]}")
	next_pos = []
	for val in anchors:
		res = re.search(val, input[pos:])
		if res != None:
			next_pos.append({val:input.find(res.group(0), pos)})
		else:
			next_pos.append({val:-1})
	min_val = len(input)+1
	min_key = ""
	# print(f"Found next anchors: {next_pos}")
	for index in range(len(next_pos)):
		for key in next_pos[index]:
			val = next_pos[index][key]
			if val < min_val and val != -1:
				min_val = val 
				min_key = key
	# print(f"Picked {min_val} and {min_key}")
	return [min_val, min_key]



def fuzzy_parse(input, anchors):
	pos = 0
	lot = []
	if_depth = 0
	[next_val, n_anchor] = next_anchor(input, pos, anchors)
	while next_val != len(input)+1:
		if n_anchor == anchors[-1]: #Found a comment, skip the whole line !
			# print(">>> FOUND Comment")
			if input.find("\n", next_val) != -1:
				pos = input.find("\n", next_val) +1
			else:
				pos = next_val+len(n_anchor)
		elif n_anchor == anchors[5]:
			# print(">>> Found string")
			if input.find("'", next_val+1) != -1:
				pos = input.find("'", next_val+1) +1
			else:
				pos = next_val+len(n_anchor)
		elif n_anchor == anchors[0]: #Found a if, take note
			# print('>>> FOUND IF')
			pos = next_val+len(re.search(n_anchor, input[pos:]).group(0))
			node = ConditionNode(if_depth, "IF")
			pos = node.find_condition(input, pos)
			if_depth += 1
			print(node)
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
			while if_depth != 0:
				node = ConditionNode(if_depth, "END-IF")
				lot.append(node)
				if_depth -= 1
			pos = next_val+len(n_anchor)

		elif n_anchor == anchors[4]:
			# print('>>> FOUND EXEC')
			node = ParseNode(if_depth, "EXEC")
			lot.append(node)
			pos = node.find_parse_text(input, next_val)
		else:
			pos += 1
		[next_val, n_anchor] = next_anchor(input, pos, anchors)
	return lot

def parse(input, lexer_base, parser_base):    
	input_stream = InputStream(input)
	lexer = lexer_base(input_stream)
	stream = CommonTokenStream(CaseChangingStream(lexer, True))
	parser = parser_base(stream)
	tree = parser.root()
	return tree


def construct_graph(node_array):
	graph = Graph(Node(0, "START") )
	for node in node_array:
		graph.add_node(node)
	graph.add_node(Node(0, "END"))
	return graph




def main(argv):
	with open(argv[1], "r") as f:
		lot = fuzzy_parse(f.read(), def_anchors())
		# print(lot)
		print(">>> WTF")
		for node in lot:
			print(str(node))
		#Contruct and clean the graph
		g = construct_graph(lot)
		g.cleanup()
		g.save_as_file()





if __name__ == '__main__':
	print("Running")
	main(sys.argv)