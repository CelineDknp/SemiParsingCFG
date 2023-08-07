import pytest
from main import process_and_create_lts

def test_construct_lts_base_if():
	graph = process_and_create_lts("TestFiles/pytest/if_normal_test_file.COB")
	assert graph.get_size() == 3
	assert graph.get_link_size() == 3
	assert graph.get_transition(1).get_label() == "NOT (A > 0)"
	assert graph.get_transition(2).get_label() == "A > 0"

#Testing simple branches for if/else
def test_construct_lts_base_if_left_branch():
	graph = process_and_create_lts("TestFiles/pytest/if_left_branch_test_file.COB")
	assert graph.get_size() == 4
	assert graph.get_link_size() == 4
	assert graph.get_transition(1).get_label() == "A > 0"
	assert graph.get_transition(2).get_label() == "NOT (A > 0)"
	assert graph.get_transition(3).get_label() == "OPEN DB"

def test_construct_lts_base_if_right_branch():
	graph = process_and_create_lts("TestFiles/pytest/if_right_branch_test_file.COB")
	assert graph.get_size() == 4
	assert graph.get_link_size() == 4
	assert graph.get_transition(1).get_label() == "NOT (A > 0)"
	assert graph.get_transition(2).get_label() == "A > 0"
	assert graph.get_transition(3).get_label() == "OPEN DB"

def test_construct_lts_base_if_both_branch():
	graph = process_and_create_lts("TestFiles/pytest/if_both_branch_test_file.COB")
	assert graph.get_size() == 5
	assert graph.get_link_size() == 5
	assert graph.get_transition(1).get_label() == "A > 0"
	assert graph.get_transition(2).get_label() == "NOT (A > 0)"
	assert graph.get_transition(3).get_label() == "OPEN DB"
	assert graph.get_transition(4).get_label() == "OPEN DB"

#Testing nested branches for if/else
def test_construct_lts_base_if_nested_left_branch():
	graph = process_and_create_lts("TestFiles/pytest/if_nested_left_branch_test_file.COB")
	assert graph.get_size() == 4
	assert graph.get_link_size() == 5
	assert graph.get_transition(1).get_label() == "A > 0"
	assert graph.get_transition(2).get_label() == "NOT (A > 0)"
	assert graph.get_transition(3).get_label() == "NOT (B > 0)"
	assert graph.get_transition(4).get_label() == "B > 0"

def test_construct_lts_base_if_nested_right_branch():
	graph = process_and_create_lts("TestFiles/pytest/if_nested_right_branch_test_file.COB")
	assert graph.get_size() == 4
	assert graph.get_link_size() == 5
	assert graph.get_transition(1).get_label() == "NOT (A > 0)"
	assert graph.get_transition(2).get_label() == "A > 0"
	assert graph.get_transition(3).get_label() == "NOT (B > 0)"
	assert graph.get_transition(4).get_label() == "B > 0"

def test_construct_lts_base_if_nested_both_branch():
	graph = process_and_create_lts("TestFiles/pytest/if_nested_both_branch_test_file.COB")
	assert graph.get_size() == 5
	assert graph.get_link_size() == 7
	assert graph.get_transition(1).get_label() == "A > 0"
	assert graph.get_transition(2).get_label() == "NOT (A > 0)"
	assert graph.get_transition(3).get_label() == "NOT (B > 0)"
	assert graph.get_transition(4).get_label() == "B > 0"
	assert graph.get_transition(5).get_label() == "NOT (C > 0)"
	assert graph.get_transition(6).get_label() == "C > 0"

#Testing evaluates
def test_construct_lts_simple_evaluate():
	graph = process_and_create_lts("TestFiles/pytest/evaluate_simple_test_file.COB")
	assert graph.get_size() == 6
	assert graph.get_link_size() == 8
	assert graph.get_transition(1).get_label() == "A > 0"
	assert graph.get_transition(2).get_label() == "A < 0"
	assert graph.get_transition(3).get_label() == "A = 0"
	assert graph.get_transition(4).get_label() == "OTHER"
	assert graph.get_transition(5).get_label() == "OPEN DB1"
	assert graph.get_transition(6).get_label() == "OPEN DB2"
	assert graph.get_transition(7).get_label() == "OPEN DB3"

def test_construct_lts_mixed_evaluate():
	graph = process_and_create_lts("TestFiles/pytest/evaluate_if_mix_test_file.COB")
	assert graph.get_size() == 8
	assert graph.get_link_size() == 11
	assert graph.get_transition(1).get_label() == "A > 0"
	assert graph.get_transition(2).get_label() == "A < 0"
	assert graph.get_transition(3).get_label() == "A = 0"
	assert graph.get_transition(4).get_label() == "B > 1"
	assert graph.get_transition(5).get_label() == "NOT (B > 1)"
	assert graph.get_transition(6).get_label() == "OPEN DB1"
	assert graph.get_transition(7).get_label() == "NOT (B > 2)"
	assert graph.get_transition(8).get_label() == "B > 2"
	assert graph.get_transition(9).get_label() == "OPEN DB2"
	assert graph.get_transition(10).get_label() == "OPEN DB3"

#Testing the control-loop
def test_construct_lts_next_sentence():
	graph = process_and_create_lts("TestFiles/pytest/next_sentence_test_file.COB")
	assert graph.get_size() == 5
	assert graph.get_link_size() == 6
	assert graph.get_transition(1).get_label() == "A > 0"
	assert graph.get_transition(2).get_label() == "NOT (A > 0)"
	assert graph.get_transition(3).get_label() == "INTERNAL"
	assert graph.get_transition(4).get_label() == "NOT (B = 0)"
	assert graph.get_transition(5).get_label() == "B = 0"

#Testing the simple single label goback loop
def test_construct_lts_base_perform():
	graph = process_and_create_lts("TestFiles/pytest/perform_base_test_file.COB")
	assert graph.get_size() == 10
	assert graph.get_link_size() == 11
	assert graph.get_transition(3).get_label() == "GOBACK"
	assert graph.get_transition(4).get_label() == "PERFORM"
	assert graph.get_transition(5).get_label() == "INTERNAL"
	assert graph.get_transition(6).get_label() == "INTERNAL"

def test_construct_lts_chained_perform():
	graph = process_and_create_lts("TestFiles/pytest/perform_chained_test_file.COB")
	assert graph.get_size() == 11
	assert graph.get_link_size() == 14
	assert graph.get_transition(3).get_label() == "GOBACK"
	assert graph.get_transition(4).get_label() == "PERFORM"
	assert graph.get_transition(5).get_label() == "INTERNAL"
	assert graph.get_transition(6).get_label() == "INTERNAL"
	assert graph.get_transition(8).get_label() == "GOBACK"
	assert graph.get_transition(9).get_label() == "PERFORM"

def test_construct_lts_broken_perform(): #TODO check
	graph = process_and_create_lts("TestFiles/pytest/perform_broken_goto_test_file.COB")
	assert graph.get_size() == 11
	assert graph.get_link_size() == 12

#Testing the perform thru (multiple label goback)
def test_construct_lts_base_perform_thru():
	graph = process_and_create_lts("TestFiles/pytest/performThru_base_test_file.COB")
	assert graph.get_size() == 10
	assert graph.get_link_size() == 11

def test_construct_lts_chained_perform_thru():
	graph = process_and_create_lts("TestFiles/pytest/performThru_chained_test_file.COB")
	assert graph.get_size() == 11
	assert graph.get_link_size() == 14

def test_construct_lts_goto_perform_thru():
	graph = process_and_create_lts("TestFiles/pytest/performThru_goto_test_file.COB")
	assert graph.get_size() == 11
	assert graph.get_link_size() == 12

def test_construct_lts_broken_perform_thru():
	graph = process_and_create_lts("TestFiles/pytest/performThru_broken_goto_test_file.COB")
	assert graph.get_size() == 11
	assert graph.get_link_size() == 12