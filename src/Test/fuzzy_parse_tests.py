import pytest
from main import fuzzy_parse, def_anchors

#Testing the base parsing for if/else
def test_fuzzy_parse_base_if():
	with open("TestFiles/pytest/if_normal_test_file.COB", "r") as f:
		node_array = fuzzy_parse(f.read(), def_anchors())
		assert len(node_array) == 3
		assert node_array[0].get_type() == "IF"
		assert node_array[1].get_type() == "ELSE"
		assert node_array[2].get_type() == "END-IF"
		assert node_array[0].get_depth() == 0
		assert node_array[1].get_depth() == 0
		assert node_array[2].get_depth() == 0

#Testing the base parsing for if/else without END-IFs
def test_fuzzy_parse_base_if_no_end_if():
	with open("TestFiles/pytest/if_no_end-if_test_file.COB", "r") as f:
		node_array = fuzzy_parse(f.read(), def_anchors())
		assert len(node_array) == 3
		assert node_array[0].get_type() == "IF"
		assert node_array[1].get_type() == "ELSE"
		assert node_array[2].get_type() == "END-IF"
		assert node_array[0].get_depth() == 0
		assert node_array[1].get_depth() == 0
		assert node_array[2].get_depth() == 0

#Testing simple branches for if/else
def test_fuzzy_parse_base_if_left_branch():
	with open("TestFiles/pytest/if_left_branch_test_file.COB", "r") as f:
		node_array = fuzzy_parse(f.read(), def_anchors())
		assert len(node_array) == 4
		assert node_array[0].get_type() == "IF"
		assert node_array[1].get_type() == "EXEC"
		assert node_array[2].get_type() == "ELSE"
		assert node_array[3].get_type() == "END-IF"
		assert node_array[0].get_depth() == 0
		assert node_array[1].get_depth() == 1
		assert node_array[2].get_depth() == 0
		assert node_array[3].get_depth() == 0

def test_fuzzy_parse_base_if_right_branch():
	with open("TestFiles/pytest/if_right_branch_test_file.COB", "r") as f:
		node_array = fuzzy_parse(f.read(), def_anchors())
		assert len(node_array) == 4
		assert node_array[0].get_type() == "IF"
		assert node_array[1].get_type() == "ELSE"
		assert node_array[2].get_type() == "EXEC"
		assert node_array[3].get_type() == "END-IF"
		assert node_array[0].get_depth() == 0
		assert node_array[1].get_depth() == 0
		assert node_array[2].get_depth() == 1
		assert node_array[3].get_depth() == 0

def test_fuzzy_parse_base_if_both_branch():
	with open("TestFiles/pytest/if_both_branch_test_file.COB", "r") as f:
		node_array = fuzzy_parse(f.read(), def_anchors())
		assert len(node_array) == 5
		assert node_array[0].get_type() == "IF"
		assert node_array[1].get_type() == "EXEC"
		assert node_array[2].get_type() == "ELSE"
		assert node_array[3].get_type() == "EXEC"
		assert node_array[4].get_type() == "END-IF"
		assert node_array[0].get_depth() == 0
		assert node_array[1].get_depth() == 1
		assert node_array[2].get_depth() == 0
		assert node_array[3].get_depth() == 1
		assert node_array[4].get_depth() == 0

#Testing nested branches for if/else
def test_fuzzy_parse_base_if_nested_left_branch():
	with open("TestFiles/pytest/if_nested_left_branch_test_file.COB", "r") as f:
		node_array = fuzzy_parse(f.read(), def_anchors())
		assert len(node_array) == 5
		assert node_array[0].get_type() == "IF"
		assert node_array[1].get_type() == "IF"
		assert node_array[2].get_type() == "END-IF"
		assert node_array[3].get_type() == "ELSE"
		assert node_array[4].get_type() == "END-IF"
		assert node_array[0].get_depth() == 0
		assert node_array[1].get_depth() == 1
		assert node_array[2].get_depth() == 1
		assert node_array[3].get_depth() == 0
		assert node_array[3].get_depth() == 0

def test_fuzzy_parse_base_if_nested_right_branch():
	with open("TestFiles/pytest/if_nested_right_branch_test_file.COB", "r") as f:
		node_array = fuzzy_parse(f.read(), def_anchors())
		assert len(node_array) == 5
		assert node_array[0].get_type() == "IF"
		assert node_array[1].get_type() == "ELSE"
		assert node_array[2].get_type() == "IF"
		assert node_array[3].get_type() == "END-IF"
		assert node_array[4].get_type() == "END-IF"
		assert node_array[0].get_depth() == 0
		assert node_array[1].get_depth() == 0
		assert node_array[2].get_depth() == 1
		assert node_array[3].get_depth() == 1
		assert node_array[4].get_depth() == 0

def test_fuzzy_parse_base_if_nested_both_branch():
	with open("TestFiles/pytest/if_nested_both_branch_test_file.COB", "r") as f:
		node_array = fuzzy_parse(f.read(), def_anchors())
		assert len(node_array) == 7
		assert node_array[0].get_type() == "IF"
		assert node_array[1].get_type() == "IF"
		assert node_array[2].get_type() == "END-IF"
		assert node_array[3].get_type() == "ELSE"
		assert node_array[4].get_type() == "IF"
		assert node_array[5].get_type() == "END-IF"
		assert node_array[6].get_type() == "END-IF"
		assert node_array[0].get_depth() == 0
		assert node_array[1].get_depth() == 1
		assert node_array[2].get_depth() == 1
		assert node_array[3].get_depth() == 0
		assert node_array[4].get_depth() == 1
		assert node_array[5].get_depth() == 1
		assert node_array[6].get_depth() == 0

#Testing the comment part of parsing
def test_fuzzy_parse_comment():
	with open("TestFiles/pytest/comment_normal_test_file.COB", "r") as f:
		node_array = fuzzy_parse(f.read(), def_anchors())
		assert len(node_array) == 3
		assert node_array[0].get_type() == "IF"
		assert node_array[1].get_type() == "ELSE"
		assert node_array[2].get_type() == "END-IF"
		assert node_array[0].get_depth() == 0
		assert node_array[1].get_depth() == 0
		assert node_array[2].get_depth() == 0

#Testing the string part of parsing, normal case
def test_fuzzy_parse_string():
	with open("TestFiles/pytest/string_normal_test_file.COB", "r") as f:
		node_array = fuzzy_parse(f.read(), def_anchors())
		assert len(node_array) == 3
		assert node_array[0].get_type() == "IF"
		assert node_array[1].get_type() == "ELSE"
		assert node_array[2].get_type() == "END-IF"
		assert node_array[0].get_depth() == 0
		assert node_array[1].get_depth() == 0
		assert node_array[2].get_depth() == 0

#Testing the string part of parsing, special case with multiple line strings
def test_fuzzy_parse_string_on_multiple_lines():
	with open("TestFiles/pytest/string_on_two_lines_test_file.COB", "r") as f:
		node_array = fuzzy_parse(f.read(), def_anchors())
		assert len(node_array) == 3
		assert node_array[0].get_type() == "IF"
		assert node_array[1].get_type() == "ELSE"
		assert node_array[2].get_type() == "END-IF"
		assert node_array[0].get_depth() == 0
		assert node_array[1].get_depth() == 0
		assert node_array[2].get_depth() == 0

#Testing the exec SQL part of parsing, all case insisitive possibilities
def test_fuzzy_parse_exec_case_insensitive():
	with open("TestFiles/pytest/exec_sql_all_forms_test_file.COB", "r") as f:
		node_array = fuzzy_parse(f.read(), def_anchors())
		assert len(node_array) == 4
		assert node_array[0].get_type() == "EXEC"
		assert node_array[1].get_type() == "EXEC"
		assert node_array[2].get_type() == "EXEC"
		assert node_array[3].get_type() == "EXEC"
		assert node_array[0].get_depth() == 0
		assert node_array[1].get_depth() == 0
		assert node_array[2].get_depth() == 0
		assert node_array[3].get_depth() == 0


