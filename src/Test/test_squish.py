import pytest
from main import process_and_squish

#Testing the base parsing for if/else
def test_squish_base_if():
	graph = process_and_squish("TestFiles/pytest/if_three_to_squish_test_file.COB")
	assert graph.get_size() == 3


#Testing simple branches for if/else
def test_squish_base_if_with_exec():
	graph = process_and_squish("TestFiles/pytest/if_two_to_squish_test_file.COB")
	assert graph.get_size() == 5

def test_squish_base_if_with_middle_exec():
	graph = process_and_squish("TestFiles/pytest/if_squish_middle_test_file.COB")
	assert graph.get_size() == 6

def test_squish_base_if_with_start_exec():
	graph = process_and_squish("TestFiles/pytest/if_squish_start_test_file.COB")
	assert graph.get_size() == 4

def test_squish_base_if_with_end_exec():
	graph = process_and_squish("TestFiles/pytest/if_squish_end_test_file.COB")
	assert graph.get_size() == 5 #One more node for context