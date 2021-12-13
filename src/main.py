import sys
import re
from Nodes.ConditionNode import ConditionNode
from Nodes.ParseNode import ParseNode
from Nodes.Node import Node
from Nodes.Graph import Graph
import graphviz


# SQLL = MySqlLexer
# SQLP = MySqlParser

# class WriteTreeListener(ParseTreeListener):
	# def visitTerminal(self, node:TerminalNode):
		# print ("Visit Terminal: " + str(node) + " - " + repr(node))

def def_anchors():
	#GOTO, PERFORM, IF, EVALUATE
	identifier = "(\S)+" #At least one character, no whitespace
	operators = "(NOT|=|NOT =|>|>=|<|<=)"
	logic_links = "AND|OR"
	anchors = ["\sIF(\s)+", "ELSE", "END-IF", "\.(\s)+","EXEC SQL", "'", "\*"]
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
	# print(f">>> TEST: {input[0:15]}")
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
			# print(f">>> Looking at: {input[next_val-1:pos+20]}")
			old = pos-1
			next_quote = input.find("'", next_val+1)
			next_line = input.find("\n", next_val+1)
			if next_quote <= next_line:
				pos = next_quote+1
			elif next_line < next_quote:
				pos = next_line+1
			else:
				pos = next_val+len(n_anchor)
			# print(f">>> Selected at: {input[old:pos]}")
		elif n_anchor == anchors[0]: #Found a if, take note
			# print('>>> FOUND IF')
			pos = next_val+len(re.search(n_anchor, input[pos:]).group(0))
			node = ConditionNode(if_depth, "IF")
			pos = node.find_condition(input, pos)
			if_depth += 1
			# print(f"IN IF, adding depth: if_depth: {if_depth}")
			# print(node)
			lot.append(node)
		elif n_anchor == anchors[1]:
			# print('>>> FOUND ELSE')
			node = ConditionNode(if_depth-1, "ELSE")
			lot.append(node)

			pos = next_val+len(n_anchor)
		elif n_anchor == anchors[2]: #Found a end-if, take note
			# print('>>> FOUND END-IF')
			if_depth -= 1
			# print(f"IN END-IF, removing depth: if_depth: {if_depth}")
			node = ConditionNode(if_depth, "END-IF")
			lot.append(node)
			pos = next_val+len(n_anchor)
		elif n_anchor == anchors[3]:
			# print(f"HERE: if_depth: {if_depth}")
			while if_depth > 0:
				node = ConditionNode(if_depth, "END-IF")
				lot.append(node)
				if_depth -= 1
			if_depth = 0
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

#def parse(input, lexer_base, parser_base):
#	input_stream = InputStream(input)
#	lexer = lexer_base(input_stream)
#	stream = CommonTokenStream(CaseChangingStream(lexer, True))
#	parser = parser_base(stream)
#	tree = parser.root()
#	return tree


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
			if node.get_type() == "EXEC":
				print(str(node))
		#Contruct and clean the graph
		g = construct_graph(lot)
		g.cleanup()
		g.squish()
		g.save_as_file()





if __name__ == '__main__':
	print("Running")
	main(sys.argv)