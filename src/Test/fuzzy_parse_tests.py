import pytest
from main import fuzzy_parse, def_anchors

#Testing the base parsing
def test_fuzzy_parse_base():
	with open("TestFiles/pytest/normal_if_test_file.COB", "r") as f:
		node_array = fuzzy_parse(f.read(), def_anchors())
		assert len(node_array) == 3
		assert node_array[0].get_type() == "IF"
		assert node_array[1].get_type() == "ELSE"
		assert node_array[2].get_type() == "END-IF"

#Testing the comment part of parsing
def test_fuzzy_parse_comment():
	with open("TestFiles/pytest/normal_comment_test_file.COB", "r") as f:
		node_array = fuzzy_parse(f.read(), def_anchors())
		assert len(node_array) == 3
		assert node_array[0].get_type() == "IF"
		assert node_array[1].get_type() == "ELSE"
		assert node_array[2].get_type() == "END-IF"

#Testing the string part of parsing, normal case
def test_fuzzy_parse_string():
	with open("TestFiles/pytest/normal_string_test_file.COB", "r") as f:
		node_array = fuzzy_parse(f.read(), def_anchors())
		assert len(node_array) == 3
		assert node_array[0].get_type() == "IF"
		assert node_array[1].get_type() == "ELSE"
		assert node_array[2].get_type() == "END-IF"

#Testing the string part of parsing, special case with multiple line strings
def test_fuzzy_parse_string_on_multiple_lines():
	with open("TestFiles/pytest/string_on_two_lines_test_file.COB", "r") as f:
		node_array = fuzzy_parse(f.read(), def_anchors())
		assert len(node_array) == 3
		assert node_array[0].get_type() == "IF"
		assert node_array[1].get_type() == "ELSE"
		assert node_array[2].get_type() == "END-IF"


