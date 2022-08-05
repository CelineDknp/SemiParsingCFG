import sys
from Nodes.Node import Node
from Nodes.Graph import Graph
from LTSGraph.LTSGraph import LTSGraph
from Utils.config import *
from FuzzyParser import FuzzyParser
from TraceEquivalence import TraceEquivalence
#import graphviz
import cProfile
#Windows-specific Graphiz import
import os
total_path = os.path.join("c:", "Program Files", "Graphviz", "bin")# os.pathsep + "C:\Program Files\Graphviz/bin/"
if total_path not in os.environ["PATH"]:
	os.environ["PATH"] += total_path

def pre_process(file):
	l = []
	for line in file.readlines():
		l.append("      ")
		if len(line) == 81:
			l.append(line[6:-9])
			l.append("        \n") #Remove the first 6 char (line number) and last 9 (id + \n)
		else:
			l.append(line[6:])#Remove the first 6 char (line number), but not the end
	result = "".join(l)
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
		pre_processed_input = pre_process(f)
		# print(pre_processed_input)
		# print(f"Pre-processed", flush=True)
		parser = FuzzyParser()
		lot = parser.fuzzy_parse(pre_processed_input)
		# print(f"Fuzzy parsing done!", flush=True)
		return lot

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
	#g = process_and_parse(filename)
	g = process_and_cleanup(filename,label_clean=False)
	# g = process_and_squish(filename,label_clean=True)
	g.save_as_file(os.path.basename(filename), output_dir=dir_path)
	lts = LTSGraph()
	lts.import_graph(g)
	lts.save_as_file("graph_test")
	print(f"Done!")


def compare_graphs(filename1, filename2):
	g1 = process_and_cleanup(filename1, label_clean=False)
	print("G1 processed")
	g2 = process_and_cleanup(filename2, label_clean=False)
	print("G2 processed")
	lst_g1 = LTSGraph()
	lst_g1.import_graph(g1)
	lst_g2 = LTSGraph()
	lst_g2.import_graph(g2)
	print("LTSs created !")
	teq = TraceEquivalence(lst_g1, lst_g2)
	teq.compare()


def main(argv):
	if len(argv) == 2:
		process_file(argv[1],"")
	elif len(argv) == 3:
		compare_graphs(argv[1], argv[2])
	else :
		cProfile.run("process_and_parse('raincodeData/Delivery/V1/ALCB018.COB')")





if __name__ == '__main__':
	print("Running")
	main(sys.argv)