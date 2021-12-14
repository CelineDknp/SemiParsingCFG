import pytest
from main import fuzzy_parse, def_anchors, construct_graph

#Testing the base parsing for if/else
def test_construct_graph_base_if():
	with open("TestFiles/pytest/if_normal_test_file.COB", "r") as f:
		node_array = fuzzy_parse(f.read(), def_anchors())
		graph = construct_graph(node_array)
		graph.cleanup()
		assert graph.get_size() == 3


#Testing simple branches for if/else
def test_construct_graph_base_if_left_branch():
	with open("TestFiles/pytest/if_left_branch_test_file.COB", "r") as f:
		node_array = fuzzy_parse(f.read(), def_anchors())
		graph = construct_graph(node_array)
		graph.cleanup()
		assert graph.get_size() == 4

def test_construct_graph_base_if_right_branch():
	with open("TestFiles/pytest/if_right_branch_test_file.COB", "r") as f:
		node_array = fuzzy_parse(f.read(), def_anchors())
		graph = construct_graph(node_array)
		graph.cleanup()
		assert graph.get_size() == 4

def test_construct_graph_base_if_both_branch():
	with open("TestFiles/pytest/if_both_branch_test_file.COB", "r") as f:
		node_array = fuzzy_parse(f.read(), def_anchors())
		graph = construct_graph(node_array)
		graph.cleanup()
		assert graph.get_size() == 5

#Testing nested branches for if/else
def test_construct_graph_base_if_nested_left_branch():
	with open("TestFiles/pytest/if_nested_left_branch_test_file.COB", "r") as f:
		node_array = fuzzy_parse(f.read(), def_anchors())
		graph = construct_graph(node_array)
		graph.cleanup()
		assert graph.get_size() == 4

def test_construct_graph_base_if_nested_right_branch():
	with open("TestFiles/pytest/if_nested_right_branch_test_file.COB", "r") as f:
		node_array = fuzzy_parse(f.read(), def_anchors())
		graph = construct_graph(node_array)
		graph.cleanup()
		assert graph.get_size() == 4

def test_construct_graph_base_if_nested_both_branch():
	with open("TestFiles/pytest/if_nested_both_branch_test_file.COB", "r") as f:
		node_array = fuzzy_parse(f.read(), def_anchors())
		graph = construct_graph(node_array)
		graph.cleanup()
		assert graph.get_size() == 5
