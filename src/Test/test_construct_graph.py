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

#Testing evaluates
def test_fuzzy_parse_simple_evaluate():
	graph = process_and_create("TestFiles/pytest/evaluate_simple_test_file.COB")
	assert graph.get_size() == 10

def test_fuzzy_parse_mixed_evaluate():
	graph = process_and_create("TestFiles/pytest/evaluate_if_mix_test_file.COB")
	assert graph.get_size() == 16

#Testing the control-loop
def test_fuzzy_parse_next_sentence():
	graph = process_and_create("TestFiles/pytest/next_sentence_test_file.COB")
	assert graph.get_size() == 9

#Testing the simple single label goback loop
def test_fuzzy_parse_base_perform():
	graph = process_and_create("TestFiles/pytest/perform_base_test_file.COB")
	assert graph.get_size() == 10

def test_fuzzy_parse_chained_perform():
	graph = process_and_create("TestFiles/pytest/perform_chained_test_file.COB")
	assert graph.get_size() == 11

def test_fuzzy_parse_broken_perform():
	graph = process_and_create("TestFiles/pytest/perform_broken_goto_test_file.COB")
	assert graph.get_size() == 11