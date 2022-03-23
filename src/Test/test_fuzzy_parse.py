import pytest
from Utils.config import *
from main import process_and_parse

#Testing the base parsing for if/else
def test_fuzzy_parse_base_if():
	node_array = process_and_parse("TestFiles/pytest/if_normal_test_file.COB")
	assert len(node_array) == 3
	assert node_array[0].get_type() == NODE_COND_START
	assert node_array[1].get_type() == NODE_COND_BRANCH
	assert node_array[2].get_type() == NODE_COND_END
	assert node_array[0].get_depth() == 0
	assert node_array[1].get_depth() == 0
	assert node_array[2].get_depth() == 0

#Testing the base parsing for if/else without END-IFs
def test_fuzzy_parse_base_if_no_end_if():
	node_array = process_and_parse("TestFiles/pytest/if_no_end-if_test_file.COB")
	assert len(node_array) == 3
	assert node_array[0].get_type() == NODE_COND_START
	assert node_array[1].get_type() == NODE_COND_BRANCH
	assert node_array[2].get_type() == NODE_COND_END_ANY
	assert node_array[0].get_depth() == 0
	assert node_array[1].get_depth() == 0
	assert node_array[2].get_depth() == 0

#Testing simple branches for if/else
def test_fuzzy_parse_base_if_left_branch():
	node_array = process_and_parse("TestFiles/pytest/if_left_branch_test_file.COB")
	assert len(node_array) == 4
	assert node_array[0].get_type() == NODE_COND_START
	assert node_array[1].get_type() == NODE_SQL
	assert node_array[2].get_type() == NODE_COND_BRANCH
	assert node_array[3].get_type() == NODE_COND_END
	assert node_array[0].get_depth() == 0
	assert node_array[1].get_depth() == 1
	assert node_array[2].get_depth() == 0
	assert node_array[3].get_depth() == 0

def test_fuzzy_parse_base_if_right_branch():
	node_array = process_and_parse("TestFiles/pytest/if_right_branch_test_file.COB")
	assert len(node_array) == 4
	assert node_array[0].get_type() == NODE_COND_START
	assert node_array[1].get_type() == NODE_COND_BRANCH
	assert node_array[2].get_type() == NODE_SQL
	assert node_array[3].get_type() == NODE_COND_END
	assert node_array[0].get_depth() == 0
	assert node_array[1].get_depth() == 0
	assert node_array[2].get_depth() == 1
	assert node_array[3].get_depth() == 0

def test_fuzzy_parse_base_if_both_branch():
	node_array = process_and_parse("TestFiles/pytest/if_both_branch_test_file.COB")
	assert len(node_array) == 5
	assert node_array[0].get_type() == NODE_COND_START
	assert node_array[1].get_type() == NODE_SQL
	assert node_array[2].get_type() == NODE_COND_BRANCH
	assert node_array[3].get_type() == NODE_SQL
	assert node_array[4].get_type() == NODE_COND_END
	assert node_array[0].get_depth() == 0
	assert node_array[1].get_depth() == 1
	assert node_array[2].get_depth() == 0
	assert node_array[3].get_depth() == 1
	assert node_array[4].get_depth() == 0

#Testing nested branches for if/else
def test_fuzzy_parse_base_if_nested_left_branch():
	node_array = process_and_parse("TestFiles/pytest/if_nested_left_branch_test_file.COB")
	assert len(node_array) == 5
	assert node_array[0].get_type() == NODE_COND_START
	assert node_array[1].get_type() == NODE_COND_START
	assert node_array[2].get_type() == NODE_COND_END
	assert node_array[3].get_type() == NODE_COND_BRANCH
	assert node_array[4].get_type() == NODE_COND_END
	assert node_array[0].get_depth() == 0
	assert node_array[1].get_depth() == 1
	assert node_array[2].get_depth() == 1
	assert node_array[3].get_depth() == 0
	assert node_array[3].get_depth() == 0

def test_fuzzy_parse_base_if_nested_right_branch():
	node_array = process_and_parse("TestFiles/pytest/if_nested_right_branch_test_file.COB")
	assert len(node_array) == 5
	assert node_array[0].get_type() == NODE_COND_START
	assert node_array[1].get_type() == NODE_COND_BRANCH
	assert node_array[2].get_type() == NODE_COND_START
	assert node_array[3].get_type() == NODE_COND_END
	assert node_array[4].get_type() == NODE_COND_END
	assert node_array[0].get_depth() == 0
	assert node_array[1].get_depth() == 0
	assert node_array[2].get_depth() == 1
	assert node_array[3].get_depth() == 1
	assert node_array[4].get_depth() == 0

def test_fuzzy_parse_base_if_nested_both_branch():
	node_array = process_and_parse("TestFiles/pytest/if_nested_both_branch_test_file.COB")
	assert len(node_array) == 7
	assert node_array[0].get_type() == NODE_COND_START
	assert node_array[1].get_type() == NODE_COND_START
	assert node_array[2].get_type() == NODE_COND_END
	assert node_array[3].get_type() == NODE_COND_BRANCH
	assert node_array[4].get_type() == NODE_COND_START
	assert node_array[5].get_type() == NODE_COND_END
	assert node_array[6].get_type() == NODE_COND_END
	assert node_array[0].get_depth() == 0
	assert node_array[1].get_depth() == 1
	assert node_array[2].get_depth() == 1
	assert node_array[3].get_depth() == 0
	assert node_array[4].get_depth() == 1
	assert node_array[5].get_depth() == 1
	assert node_array[6].get_depth() == 0

#Testing the conditions of ifs
def test_fuzzy_parse_base_if_condition():
	node_array = process_and_parse("TestFiles/pytest/if_condition_base_test_file.COB")
	assert len(node_array) == 2
	assert node_array[0].get_type() == NODE_COND_START
	assert node_array[1].get_type() == NODE_COND_END
	assert node_array[0].get_condition() == "A > 0"

def test_fuzzy_parse_if_condition_two_lines():
	node_array = process_and_parse("TestFiles/pytest/if_condition_two_lines_test_file.COB")
	assert len(node_array) == 2
	assert node_array[0].get_type() == NODE_COND_START
	assert node_array[1].get_type() == NODE_COND_END
	assert node_array[0].get_condition() == "A > 0 AND B = 10"

def test_fuzzy_parse_if_condition_three_lines():
	node_array = process_and_parse("TestFiles/pytest/if_condition_three_lines_test_file.COB")
	assert len(node_array) == 2
	assert node_array[0].get_type() == NODE_COND_START
	assert node_array[1].get_type() == NODE_COND_END
	assert node_array[0].get_condition() == "A > 0 AND B = 10 AND C"

def test_fuzzy_parse_if_condition_case_insensitive():
	node_array = process_and_parse("TestFiles/pytest/if_condition_case_insensitive_test_file.COB")
	assert len(node_array) == 2
	assert node_array[0].get_type() == NODE_COND_START
	assert node_array[1].get_type() == NODE_COND_END
	assert node_array[0].get_condition() == "A > 0 and B > 0"

def test_fuzzy_parse_simple_evaluate():
	node_array = process_and_parse("TestFiles/pytest/evaluate_simple_test_file.COB")
	assert len(node_array) == 8
	assert node_array[0].get_type() == NODE_COND_START
	assert node_array[0].get_condition() == "TRUE"
	assert node_array[1].get_type() == NODE_COND_BRANCH
	assert node_array[1].get_condition() == "A > 0"
	assert node_array[3].get_type() == NODE_COND_BRANCH
	assert node_array[3].get_condition() == "A < 0"
	assert node_array[5].get_type() == NODE_COND_BRANCH
	assert node_array[5].get_condition() == "A = 0"
	assert node_array[7].get_type() == NODE_COND_END

def test_fuzzy_parse_mixed_evaluate():
	node_array = process_and_parse("TestFiles/pytest/evaluate_if_mix_test_file.COB")
	assert len(node_array) == 14
	assert node_array[0].get_type() == NODE_COND_START
	assert node_array[0].get_condition() == "TRUE"
	assert node_array[1].get_type() == NODE_COND_BRANCH
	assert node_array[1].get_condition() == "A > 0"
	assert node_array[2].get_type() == NODE_COND_START
	assert node_array[2].get_condition() == "B > 1"
	assert node_array[4].get_type() == NODE_COND_BRANCH
	assert node_array[5].get_type() == NODE_COND_END
	assert node_array[6].get_type() == NODE_COND_BRANCH
	assert node_array[6].get_condition() == "A < 0"
	assert node_array[7].get_type() == NODE_COND_START
	assert node_array[7].get_condition() == "B > 2"
	assert node_array[8].get_type() == NODE_COND_BRANCH
	assert node_array[10].get_type() == NODE_COND_END
	assert node_array[11].get_type() == NODE_COND_BRANCH
	assert node_array[11].get_condition() == "A = 0"
	assert node_array[13].get_type() == NODE_COND_END

#Testing the comment part of parsing
def test_fuzzy_parse_comment():
	node_array = process_and_parse("TestFiles/pytest/comment_normal_test_file.COB")
	assert len(node_array) == 3
	assert node_array[0].get_type() == NODE_COND_START
	assert node_array[1].get_type() == NODE_COND_BRANCH
	assert node_array[2].get_type() == NODE_COND_END
	assert node_array[0].get_depth() == 0
	assert node_array[1].get_depth() == 0
	assert node_array[2].get_depth() == 0

#Testing the string part of parsing, normal case
def test_fuzzy_parse_string():
	node_array = process_and_parse("TestFiles/pytest/string_normal_test_file.COB")
	assert len(node_array) == 3
	assert node_array[0].get_type() == NODE_COND_START
	assert node_array[1].get_type() == NODE_COND_BRANCH
	assert node_array[2].get_type() == NODE_COND_END
	assert node_array[0].get_depth() == 0
	assert node_array[1].get_depth() == 0
	assert node_array[2].get_depth() == 0

#Testing the string part of parsing, special case with multiple line strings
def test_fuzzy_parse_string_on_multiple_lines():
	node_array = process_and_parse("TestFiles/pytest/string_on_two_lines_test_file.COB")
	assert len(node_array) == 3
	assert node_array[0].get_type() == NODE_COND_START
	assert node_array[1].get_type() == NODE_COND_BRANCH
	assert node_array[2].get_type() == NODE_COND_END
	assert node_array[0].get_depth() == 0
	assert node_array[1].get_depth() == 0
	assert node_array[2].get_depth() == 0

#Testing the exec SQL part of parsing, all case insisitive possibilities
def test_fuzzy_parse_exec_case_insensitive():
	node_array = process_and_parse("TestFiles/pytest/exec_sql_all_forms_test_file.COB")
	assert len(node_array) == 4
	assert node_array[0].get_type() == NODE_SQL
	assert node_array[1].get_type() == NODE_SQL
	assert node_array[2].get_type() == NODE_SQL
	assert node_array[3].get_type() == NODE_SQL
	assert node_array[0].get_depth() == 0
	assert node_array[1].get_depth() == 0
	assert node_array[2].get_depth() == 0
	assert node_array[3].get_depth() == 0

def test_fuzzy_parse_next_sentence():
	node_array = process_and_parse("TestFiles/pytest/next_sentence_test_file.COB")
	assert len(node_array) == 7
	assert node_array[0].get_type() == NODE_COND_START
	assert node_array[0].get_condition() == "A > 0"
	assert node_array[1].get_type() == NODE_LOOP
	assert node_array[2].get_type() == NODE_COND_BRANCH
	assert node_array[3].get_type() == NODE_COND_END
	assert node_array[4].get_type() == NODE_COND_END_ANY
	assert node_array[5].get_type() == NODE_COND_START
	assert node_array[6].get_type() == NODE_COND_END

def test_fuzzy_parse_base_perform():
	node_array = process_and_parse("TestFiles/pytest/perform_base_test_file.COB")
	assert len(node_array) == 8
	assert node_array[0].get_type() == NODE_LABEL
	assert node_array[1].get_type() == NODE_LOOP
	assert node_array[2].get_type() == NODE_LABEL
	assert node_array[3].get_type() == NODE_LABEL
	assert node_array[4].get_type() == NODE_LABEL
	assert node_array[5].get_type() == NODE_LABEL
	assert node_array[6].get_type() == NODE_LABEL
	assert node_array[7].get_type() == NODE_LABEL

def test_fuzzy_parse_chained_perform():
	node_array = process_and_parse("TestFiles/pytest/perform_chained_test_file.COB")
	assert len(node_array) == 9
	assert node_array[0].get_type() == NODE_LABEL
	assert node_array[1].get_type() == NODE_LOOP
	assert node_array[2].get_type() == NODE_LABEL
	assert node_array[3].get_type() == NODE_LABEL
	assert node_array[4].get_type() == NODE_LOOP
	assert node_array[5].get_type() == NODE_LABEL
	assert node_array[7].get_type() == NODE_LABEL
	assert node_array[7].get_type() == NODE_LABEL
	assert node_array[8].get_type() == NODE_LABEL

def test_fuzzy_parse_broken_perform():
	node_array = process_and_parse("TestFiles/pytest/perform_broken_goto_test_file.COB")
	assert len(node_array) == 9
	assert node_array[0].get_type() == NODE_LABEL
	assert node_array[1].get_type() == NODE_LOOP
	assert node_array[2].get_type() == NODE_LABEL
	assert node_array[3].get_type() == NODE_LABEL
	assert node_array[4].get_type() == NODE_LOOP
	assert node_array[5].get_type() == NODE_LABEL
	assert node_array[7].get_type() == NODE_LABEL
	assert node_array[7].get_type() == NODE_LABEL
	assert node_array[8].get_type() == NODE_LABEL

def test_fuzzy_parse_base_perform_thru():
	node_array = process_and_parse("TestFiles/pytest/performThru_base_test_file.COB")
	assert len(node_array) == 8
	assert node_array[0].get_type() == NODE_LABEL
	assert node_array[1].get_type() == NODE_LOOP
	assert node_array[2].get_type() == NODE_LABEL
	assert node_array[3].get_type() == NODE_LABEL
	assert node_array[4].get_type() == NODE_LABEL
	assert node_array[5].get_type() == NODE_LABEL
	assert node_array[6].get_type() == NODE_LABEL
	assert node_array[7].get_type() == NODE_LABEL

def test_fuzzy_parse_chained_perform_thru():
	node_array = process_and_parse("TestFiles/pytest/performThru_chained_test_file.COB")
	assert len(node_array) == 9
	assert node_array[0].get_type() == NODE_LABEL
	assert node_array[1].get_type() == NODE_LOOP
	assert node_array[2].get_type() == NODE_LABEL
	assert node_array[3].get_type() == NODE_LABEL
	assert node_array[4].get_type() == NODE_LOOP
	assert node_array[5].get_type() == NODE_LABEL
	assert node_array[7].get_type() == NODE_LABEL
	assert node_array[7].get_type() == NODE_LABEL
	assert node_array[8].get_type() == NODE_LABEL

def test_fuzzy_parse_goto_perform_thru():
	node_array = process_and_parse("TestFiles/pytest/performThru_goto_test_file.COB")
	assert len(node_array) == 9
	assert node_array[0].get_type() == NODE_LABEL
	assert node_array[1].get_type() == NODE_LOOP
	assert node_array[2].get_type() == NODE_LABEL
	assert node_array[3].get_type() == NODE_LABEL
	assert node_array[4].get_type() == NODE_LOOP
	assert node_array[5].get_type() == NODE_LABEL
	assert node_array[7].get_type() == NODE_LABEL
	assert node_array[7].get_type() == NODE_LABEL
	assert node_array[8].get_type() == NODE_LABEL

def test_fuzzy_parse_broken_perform_thru():
	node_array = process_and_parse("TestFiles/pytest/performThru_broken_goto_test_file.COB")
	assert len(node_array) == 9
	assert node_array[0].get_type() == NODE_LABEL
	assert node_array[1].get_type() == NODE_LOOP
	assert node_array[2].get_type() == NODE_LABEL
	assert node_array[3].get_type() == NODE_LABEL
	assert node_array[4].get_type() == NODE_LOOP
	assert node_array[5].get_type() == NODE_LABEL
	assert node_array[7].get_type() == NODE_LABEL
	assert node_array[7].get_type() == NODE_LABEL
	assert node_array[8].get_type() == NODE_LABEL

