import pytest
from Utils.config import *
from Nodes.SimpleBranchConditionNode import SimpleBranchConditionNode
from Nodes.MultipleBranchConditionNode import MultipleBranchConditionNode
from Nodes.ConditionNode import ConditionNode
from Nodes.ParseNode import ParseNode
from Nodes.LoopNode import LoopNode
from Nodes.LabelLoopNode import LabelLoopNode
from Nodes.MultipleLabelLoopNode import MultipleLabelLoopNode
from Nodes.ControlLoopNode import ControlLoopNode
from Nodes.LabelNode import LabelNode
from Nodes.Node import Node
from main import process_and_parse

#Testing the base parsing for if/else
def test_node_type_base_if():
	node_array = process_and_parse("TestFiles/pytest/if_normal_test_file.COB")
	assert isinstance(node_array[0], SimpleBranchConditionNode)
	assert isinstance(node_array[1], SimpleBranchConditionNode)
	assert isinstance(node_array[2], ConditionNode)

#Testing the base parsing for if/else without END-IFs
def test_node_type_base_if_no_end_if():
	node_array = process_and_parse("TestFiles/pytest/if_no_end-if_test_file.COB")
	assert isinstance(node_array[0], SimpleBranchConditionNode)
	assert isinstance(node_array[1], SimpleBranchConditionNode)
	assert isinstance(node_array[2], ConditionNode)

#Testing simple branches for if/else
def test_node_type_base_if_left_branch():
	node_array = process_and_parse("TestFiles/pytest/if_left_branch_test_file.COB")
	assert isinstance(node_array[0], SimpleBranchConditionNode)
	assert isinstance(node_array[1], ParseNode)
	assert isinstance(node_array[2], SimpleBranchConditionNode)
	assert isinstance(node_array[3], ConditionNode)


def test_node_type_base_if_right_branch():
	node_array = process_and_parse("TestFiles/pytest/if_right_branch_test_file.COB")
	assert isinstance(node_array[0], SimpleBranchConditionNode)
	assert isinstance(node_array[1], SimpleBranchConditionNode)
	assert isinstance(node_array[2], ParseNode)
	assert isinstance(node_array[3], ConditionNode)

def test_node_type_base_if_both_branch():
	node_array = process_and_parse("TestFiles/pytest/if_both_branch_test_file.COB")
	assert isinstance(node_array[0], SimpleBranchConditionNode)
	assert isinstance(node_array[1], ParseNode)
	assert isinstance(node_array[2], SimpleBranchConditionNode)
	assert isinstance(node_array[3], ParseNode)
	assert isinstance(node_array[4], ConditionNode)

#Testing nested branches for if/else
def test_node_type_base_if_nested_left_branch():
	node_array = process_and_parse("TestFiles/pytest/if_nested_left_branch_test_file.COB")
	assert isinstance(node_array[0], SimpleBranchConditionNode)
	assert isinstance(node_array[1], SimpleBranchConditionNode)
	assert isinstance(node_array[2], ConditionNode)
	assert isinstance(node_array[3], SimpleBranchConditionNode)
	assert isinstance(node_array[4], ConditionNode)

def test_node_type_base_if_nested_right_branch():
	node_array = process_and_parse("TestFiles/pytest/if_nested_right_branch_test_file.COB")
	assert isinstance(node_array[0], SimpleBranchConditionNode)
	assert isinstance(node_array[1], SimpleBranchConditionNode)
	assert isinstance(node_array[2], SimpleBranchConditionNode)
	assert isinstance(node_array[3], ConditionNode)
	assert isinstance(node_array[4], ConditionNode)

def test_node_type_base_if_nested_both_branch():
	node_array = process_and_parse("TestFiles/pytest/if_nested_both_branch_test_file.COB")
	assert isinstance(node_array[0], SimpleBranchConditionNode)
	assert isinstance(node_array[1], SimpleBranchConditionNode)
	assert isinstance(node_array[2], ConditionNode)
	assert isinstance(node_array[3], SimpleBranchConditionNode)
	assert isinstance(node_array[4], SimpleBranchConditionNode)
	assert isinstance(node_array[5], ConditionNode)
	assert isinstance(node_array[6], ConditionNode)

#Tests for evaluate (multiple branch conditions)
def test_node_type_simple_evaluate():
	node_array = process_and_parse("TestFiles/pytest/evaluate_simple_test_file.COB")
	assert isinstance(node_array[0], MultipleBranchConditionNode)
	assert isinstance(node_array[1], MultipleBranchConditionNode)
	assert isinstance(node_array[3], MultipleBranchConditionNode)
	assert isinstance(node_array[5], MultipleBranchConditionNode)
	assert isinstance(node_array[7], ConditionNode)

def test_node_type_mixed_evaluate():
	node_array = process_and_parse("TestFiles/pytest/evaluate_if_mix_test_file.COB")
	assert isinstance(node_array[0], MultipleBranchConditionNode)
	assert isinstance(node_array[1], MultipleBranchConditionNode)
	assert isinstance(node_array[2], SimpleBranchConditionNode)
	assert isinstance(node_array[4], SimpleBranchConditionNode)
	assert isinstance(node_array[5], ConditionNode)
	assert isinstance(node_array[6], MultipleBranchConditionNode)
	assert isinstance(node_array[7], SimpleBranchConditionNode)
	assert isinstance(node_array[8], SimpleBranchConditionNode)
	assert isinstance(node_array[10], ConditionNode)
	assert isinstance(node_array[11], MultipleBranchConditionNode)
	assert isinstance(node_array[13], ConditionNode)


#Testing the comment part of parsing
def test_node_type_comment():
	node_array = process_and_parse("TestFiles/pytest/comment_normal_test_file.COB")
	assert isinstance(node_array[0], SimpleBranchConditionNode)
	assert isinstance(node_array[1], SimpleBranchConditionNode)
	assert isinstance(node_array[2], ConditionNode)


#Testing the string part of parsing, normal case
def test_node_type_string():
	node_array = process_and_parse("TestFiles/pytest/string_normal_test_file.COB")
	assert isinstance(node_array[0], SimpleBranchConditionNode)
	assert isinstance(node_array[1], SimpleBranchConditionNode)
	assert isinstance(node_array[2], ConditionNode)


#Testing the string part of parsing, special case with multiple line strings
def test_node_type_string_on_multiple_lines():
	node_array = process_and_parse("TestFiles/pytest/string_on_two_lines_test_file.COB")
	assert isinstance(node_array[0], SimpleBranchConditionNode)
	assert isinstance(node_array[1], SimpleBranchConditionNode)
	assert isinstance(node_array[2], ConditionNode)

#Testing the exec SQL part of parsing, all case insisitive possibilities
def test_node_type_exec_case_insensitive():
	node_array = process_and_parse("TestFiles/pytest/exec_sql_all_forms_test_file.COB")
	assert isinstance(node_array[0], ParseNode)
	assert isinstance(node_array[1], ParseNode)
	assert isinstance(node_array[2], ParseNode)
	assert isinstance(node_array[3], ParseNode)

#Testing the next sentence instruction (control loop)
def test_node_type_next_sentence():
	node_array = process_and_parse("TestFiles/pytest/next_sentence_test_file.COB")
	assert isinstance(node_array[0], SimpleBranchConditionNode)
	assert isinstance(node_array[1], ControlLoopNode)
	assert node_array[1].is_control()
	assert not node_array[1].is_goback_node()
	assert isinstance(node_array[2], SimpleBranchConditionNode)
	assert isinstance(node_array[3], ConditionNode)
	assert isinstance(node_array[4], Node)
	assert isinstance(node_array[5], SimpleBranchConditionNode)
	assert isinstance(node_array[6], ConditionNode)

#Testing the simple (single label) perform
def test_node_type_base_perform():
	node_array = process_and_parse("TestFiles/pytest/perform_base_test_file.COB")
	assert isinstance(node_array[0], LabelNode)
	assert isinstance(node_array[1], LabelLoopNode)
	assert node_array[1].is_label()
	assert node_array[1].is_goback_node()
	assert not node_array[1].is_multiple_labels()
	assert isinstance(node_array[2], LabelNode)
	assert isinstance(node_array[3], LabelNode)
	assert isinstance(node_array[4], LabelNode)
	assert isinstance(node_array[5], LabelNode)
	assert isinstance(node_array[6], LabelNode)
	assert isinstance(node_array[7], LabelNode)

def test_node_type_chained_perform():
	node_array = process_and_parse("TestFiles/pytest/perform_chained_test_file.COB")
	assert isinstance(node_array[0], LabelNode)
	assert isinstance(node_array[1], LabelLoopNode)
	assert node_array[1].is_label()
	assert node_array[1].is_goback_node()
	assert not node_array[1].is_multiple_labels()
	assert isinstance(node_array[2], LabelNode)
	assert isinstance(node_array[3], LabelNode)
	assert isinstance(node_array[4], LabelLoopNode)
	assert node_array[4].is_label()
	assert node_array[4].is_goback_node()
	assert not node_array[4].is_multiple_labels()
	assert isinstance(node_array[5], LabelNode)
	assert isinstance(node_array[6], LabelNode)
	assert isinstance(node_array[7], LabelNode)
	assert isinstance(node_array[8], LabelNode)

def test_node_type_broken_perform():
	node_array = process_and_parse("TestFiles/pytest/perform_broken_goto_test_file.COB")
	assert isinstance(node_array[0], LabelNode)
	assert isinstance(node_array[1], LabelLoopNode)
	assert node_array[1].is_label()
	assert node_array[1].is_goback_node()
	assert not node_array[1].is_multiple_labels()
	assert isinstance(node_array[2], LabelNode)
	assert isinstance(node_array[3], LabelNode)
	assert isinstance(node_array[4], LabelLoopNode)
	assert node_array[4].is_label()
	assert not node_array[4].is_goback_node()
	assert not node_array[4].is_multiple_labels()
	assert isinstance(node_array[5], LabelNode)
	assert isinstance(node_array[6], LabelNode)
	assert isinstance(node_array[7], LabelNode)
	assert isinstance(node_array[8], LabelNode)

#Testing the perform thru (multiple label goback)
def test_node_type_base_perform_thru():
	node_array = process_and_parse("TestFiles/pytest/performThru_base_test_file.COB")
	assert isinstance(node_array[0], LabelNode)
	assert isinstance(node_array[1], LabelLoopNode)
	assert node_array[1].is_label()
	assert node_array[1].is_goback_node()
	assert node_array[1].is_multiple_labels()
	assert isinstance(node_array[2], LabelNode)
	assert isinstance(node_array[3], LabelNode)
	assert isinstance(node_array[4], LabelNode)
	assert isinstance(node_array[5], LabelNode)
	assert isinstance(node_array[6], LabelNode)
	assert isinstance(node_array[7], LabelNode)

def test_node_type_chained_perform_thru():
	node_array = process_and_parse("TestFiles/pytest/performThru_chained_test_file.COB")

	assert isinstance(node_array[0], LabelNode)
	assert isinstance(node_array[1], LabelLoopNode)
	assert node_array[1].is_label()
	assert node_array[1].is_goback_node()
	assert node_array[1].is_multiple_labels()
	assert isinstance(node_array[2], LabelNode)
	assert isinstance(node_array[3], LabelNode)
	assert isinstance(node_array[4], LabelLoopNode)
	assert node_array[4].is_label()
	assert node_array[4].is_goback_node()
	assert node_array[4].is_multiple_labels()
	assert isinstance(node_array[5], LabelNode)
	assert isinstance(node_array[6], LabelNode)
	assert isinstance(node_array[7], LabelNode)
	assert isinstance(node_array[8], LabelNode)

def test_node_type_goto_perform_thru():
	node_array = process_and_parse("TestFiles/pytest/performThru_goto_test_file.COB")
	assert isinstance(node_array[0], LabelNode)
	assert isinstance(node_array[1], LabelLoopNode)
	assert node_array[1].is_label()
	assert node_array[1].is_goback_node()
	assert node_array[1].is_multiple_labels()
	assert isinstance(node_array[2], LabelNode)
	assert isinstance(node_array[3], LabelNode)
	assert isinstance(node_array[4], LabelLoopNode)
	assert node_array[4].is_label()
	assert not node_array[4].is_goback_node()
	assert not node_array[4].is_multiple_labels()
	assert isinstance(node_array[5], LabelNode)
	assert isinstance(node_array[6], LabelNode)
	assert isinstance(node_array[7], LabelNode)
	assert isinstance(node_array[8], LabelNode)

def test_node_type_broken_perform_thru():
	node_array = process_and_parse("TestFiles/pytest/performThru_broken_goto_test_file.COB")
	assert isinstance(node_array[0], LabelNode)
	assert isinstance(node_array[1], LabelLoopNode)
	assert node_array[1].is_label()
	assert node_array[1].is_goback_node()
	assert node_array[1].is_multiple_labels()
	assert isinstance(node_array[2], LabelNode)
	assert isinstance(node_array[3], LabelNode)
	assert isinstance(node_array[4], LabelLoopNode)
	assert node_array[4].is_label()
	assert not node_array[4].is_goback_node()
	assert not node_array[4].is_multiple_labels()
	assert isinstance(node_array[5], LabelNode)
	assert isinstance(node_array[6], LabelNode)
	assert isinstance(node_array[7], LabelNode)
	assert isinstance(node_array[8], LabelNode)
