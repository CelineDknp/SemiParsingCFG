import sys
from Nodes.Node import Node
from Nodes.Graph import Graph
from Utils.config import *
from FuzzyParser import FuzzyParser
import cProfile
# import graphviz
#Windows-specific Graphiz import
import os
total_path = os.path.join("c:", "Program Files", "Graphviz", "bin")# os.pathsep + "C:\Program Files\Graphviz/bin/"
if total_path not in os.environ["PATH"]:
	os.environ["PATH"] += total_path

def pre_process(file):
	result = ""
	for line in file.readlines():
		if len(line) == 81:
			result += "      "+(line[6:-9])+"        \n" #Remove the first 6 char (line number) and last 9 (id + \n)
		else:
			result += "      "+(line[6:])#Remove the first 6 char (line number), but not the end
	# print(result)
	return result


def construct_graph(node_array):
	graph = Graph(Node(0, "START") )
	for node in node_array:
		graph.add_node(node)
	graph.add_node(Node(0, "END"))
	return graph

def process_and_parse(filename):
	with open(filename, "r", encoding='latin-1') as f:
		#print(f"Opened {filename}", flush=True)
		pre_processed_input = pre_process(f)
		# print(pre_processed_input)
		# print(f"Pre-processed", flush=True)
		parser = FuzzyParser(pre_processed_input)
		lot = parser.fuzzy_parse()
		# print(f"Fuzzy parsing done!", flush=True)
		# return lot

def process_and_create(filename):
	lot = process_and_parse(filename)
	#print(f"Final array of nodes: {lot}")
	#for n in lot:
	#	print(n)
	# print(f"Final size of array of nodes: {len(lot)}")
	g = construct_graph(lot)
	print(f"Graph constructed!", flush=True)
	# print(f"Intermediary size of graph: {g.get_size()}")
	return g

def create(lot):
	#print(f"Final array of nodes: {lot}")
	#for n in lot:
	#	print(n)
	# print(f"Final size of array of nodes: {len(lot)}")
	g = construct_graph(lot)
	print(f"Graph constructed!", flush=True)
	# print(f"Intermediary size of graph: {g.get_size()}")
	return g

def process_and_cleanup(filename, label_clean=False):
	g = process_and_create(filename)
	g.cleanup(label_clean)
	print(f"Graph cleaned!", flush=True)
	# print(f"Final size of graph: {g.get_size()}")
	return g

def create_and_cleanup(lot, label_clean=False):
	g = create(lot)
	g.cleanup(label_clean)
	print(f"Graph cleaned!", flush=True)
	# print(f"Final size of graph: {g.get_size()}")
	return g

def process_and_squish(filename,label_clean=False):
	g = process_and_cleanup(filename, label_clean=label_clean)
	g.squish()
	print(f"Graph squished!", flush=True)
	return g

def process_file(filename, dir_path):
	g = process_and_parse(filename)
	# g = process_and_cleanup(filename,label_clean=False)
	# g = process_and_squish(filename,label_clean=True)
	# g.save_as_file(os.path.basename(filename), output_dir=dir_path)
	# print(f"Done!")




def main(argv):
	if len(argv) == 2:
		process_file(argv[1],"")
	else :
		cProfile.run("process_and_parse('raincodeData/Delivery/V1/ALCB025.COB')")





if __name__ == '__main__':
	print("Running")
	main(sys.argv)