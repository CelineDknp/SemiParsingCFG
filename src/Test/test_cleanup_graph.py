import pytest
from main import process_and_cleanup

#Testing the base parsing for if/else
def test_cleanup_graph_base_if():
	graph = process_and_cleanup("TestFiles/pytest/if_normal_test_file.COB")
	assert graph.get_size() == 3


#Testing simple branches for if/else
def test_cleanup_graph_base_if_left_branch():
	graph = process_and_cleanup("TestFiles/pytest/if_left_branch_test_file.COB")
	assert graph.get_size() == 4

def test_cleanup_graph_base_if_right_branch():
	graph = process_and_cleanup("TestFiles/pytest/if_right_branch_test_file.COB")
	assert graph.get_size() == 4

def test_cleanup_graph_base_if_both_branch():
	graph = process_and_cleanup("TestFiles/pytest/if_both_branch_test_file.COB")
	assert graph.get_size() == 5

#Testing nested branches for if/else
def test_cleanup_graph_base_if_nested_left_branch():
	graph = process_and_cleanup("TestFiles/pytest/if_nested_left_branch_test_file.COB")
	assert graph.get_size() == 4

def test_cleanup_graph_base_if_nested_right_branch():
	graph = process_and_cleanup("TestFiles/pytest/if_nested_right_branch_test_file.COB")
	assert graph.get_size() == 4

def test_cleanup_graph_base_if_nested_both_branch():
	graph = process_and_cleanup("TestFiles/pytest/if_nested_both_branch_test_file.COB")
	assert graph.get_size() == 5

#Testing evaluates
def test_cleanup_graph_simple_evaluate():
	graph = process_and_cleanup("TestFiles/pytest/evaluate_simple_test_file.COB")
	assert graph.get_size() == 6

def test_cleanup_graph_mixed_evaluate():
	graph = process_and_cleanup("TestFiles/pytest/evaluate_if_mix_test_file.COB")
	assert graph.get_size() == 8

#Testing the control-loop
def test_cleanup_graph_next_sentence():
	graph = process_and_cleanup("TestFiles/pytest/next_sentence_test_file.COB")
	assert graph.get_size() == 5

#Testing the simple single label goback loop
def test_cleanup_graph_base_perform():
	graph = process_and_cleanup("TestFiles/pytest/perform_base_test_file.COB")
	assert graph.get_size() == 5

def test_cleanup_graph_chained_perform():
	graph = process_and_cleanup("TestFiles/pytest/perform_chained_test_file.COB")
	assert graph.get_size() == 8

def test_cleanup_graph_broken_perform():
	graph = process_and_cleanup("TestFiles/pytest/perform_broken_goto_test_file.COB")
	assert graph.get_size() == 8

#Testing the perform thru (multiple label goback)
def test_cleanup_graph_base_perform_thru():
	graph = process_and_cleanup("TestFiles/pytest/performThru_base_test_file.COB")
	assert graph.get_size() == 6

def test_cleanup_graph_chained_perform_thru():
	graph = process_and_cleanup("TestFiles/pytest/performThru_chained_test_file.COB")
	assert graph.get_size() == 10

def test_cleanup_graph_goto_perform_thru():
	graph = process_and_cleanup("TestFiles/pytest/performThru_goto_test_file.COB")
	assert graph.get_size() == 8

def test_cleanup_graph_broken_perform_thru():
	graph = process_and_cleanup("TestFiles/pytest/performThru_broken_goto_test_file.COB")
	assert graph.get_size() == 9
