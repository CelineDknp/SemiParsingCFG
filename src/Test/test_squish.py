import pytest
from main import fuzzy_parse, def_anchors, construct_graph

#Testing the base parsing for if/else
def test_squish_base_if():
	with open("TestFiles/pytest/if_three_to_squish_test_file.COB", "r") as f:
		node_array = fuzzy_parse(f.read(), def_anchors())
		graph = construct_graph(node_array)
		graph.cleanup()
		graph.squish()
		assert graph.get_size() == 3


#Testing simple branches for if/else
def test_squish_base_if_with_exec():
	with open("TestFiles/pytest/if_two_to_squish_test_file.COB", "r") as f:
		node_array = fuzzy_parse(f.read(), def_anchors())
		graph = construct_graph(node_array)
		graph.cleanup()
		graph.squish()
		assert graph.get_size() == 5

def test_squish_base_if_with_middle_exec():
	with open("TestFiles/pytest/if_squish_middle_test_file.COB", "r") as f:
		node_array = fuzzy_parse(f.read(), def_anchors())
		graph = construct_graph(node_array)
		graph.cleanup()
		graph.squish()
		assert graph.get_size() == 6

def test_squish_base_if_with_start_exec():
	with open("TestFiles/pytest/if_squish_start_test_file.COB", "r") as f:
		node_array = fuzzy_parse(f.read(), def_anchors())
		graph = construct_graph(node_array)
		graph.cleanup()
		graph.squish()
		assert graph.get_size() == 4

def test_squish_base_if_with_end_exec():
	with open("TestFiles/pytest/if_squish_end_test_file.COB", "r") as f:
		node_array = fuzzy_parse(f.read(), def_anchors())
		graph = construct_graph(node_array)
		graph.cleanup()
		graph.squish()
		assert graph.get_size() == 5 #One more node for context