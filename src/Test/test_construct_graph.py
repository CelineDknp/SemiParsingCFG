import pytest
from main import process_and_create

#Testing the base parsing for if/else
def test_construct_graph_base_if():
	graph = process_and_create("TestFiles/pytest/if_normal_test_file.COB")
	assert graph.get_size() == 5

#Testing simple branches for if/else
def test_construct_graph_base_if_left_branch():
	graph = process_and_create("TestFiles/pytest/if_left_branch_test_file.COB")
	assert graph.get_size() == 6

def test_construct_graph_base_if_right_branch():
	graph = process_and_create("TestFiles/pytest/if_right_branch_test_file.COB")
	assert graph.get_size() == 6

def test_construct_graph_base_if_both_branch():
	graph = process_and_create("TestFiles/pytest/if_both_branch_test_file.COB")
	assert graph.get_size() == 7

#Testing nested branches for if/else
def test_construct_graph_base_if_nested_left_branch():
	graph = process_and_create("TestFiles/pytest/if_nested_left_branch_test_file.COB")
	assert graph.get_size() == 7

def test_construct_graph_base_if_nested_right_branch():
	graph = process_and_create("TestFiles/pytest/if_nested_right_branch_test_file.COB")
	assert graph.get_size() == 7

def test_construct_graph_base_if_nested_both_branch():
	graph = process_and_create("TestFiles/pytest/if_nested_both_branch_test_file.COB")
	assert graph.get_size() == 9
