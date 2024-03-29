from re import search
from Nodes.ConditionNode import ConditionNode
from Nodes.SimpleBranchConditionNode import SimpleBranchConditionNode
from TraceMatch import TraceMatch
from cobol_semi.parse import *

#Label to ignore
ignore = "INTERNAL"
#Label perform
perform = "PERFORM"
#Label gocback
goback = "GOBACK"

# Straight equivalences
equiv = [('" "', "SPACE"), ("' '", "SPACE"), ("0", "ZERO"), ("+", "", r"\+(\d)+")]

# Bool negation
bool = "NOT "

# Structure transformations
struct = [("IF", "EVALUATE")]
auto_cast_evaluate = True #Option to allow auto-cast of int to str in evaluate WHEN

# Factorisation
fact = {False: "OR", True: "AND"}  # Join with OR on true branch and with AND on false

# Rematch after no match
rematch = 20
# Values: skip_right (skip one from the right graph) skip_left (skip one from the left right)
# skip_both (try to skip one from the right and/or one from the left)
rematch_mode = "skip_left"
rematch_type = 3 #All rematches


def try_simple_equivalence(str1, str2):
	new_cond = ""
	for tup in equiv:
		if len(tup) == 2:
			if tup[1] in str1 and tup[0] in str2:
				new_cond = str1.replace(tup[1], tup[0])
			elif len(tup) == 3:  # We need to regex match
				if search(tup[2], str1):
					new_cond = str1.replace(tup[0], tup[1])
					vadim_parsing = diff(new_cond, str2)
					if vadim_parsing: return True
				elif search(tup[2], str2):
					new_cond = str2.replace(tup[0], tup[1])
	if new_cond != "":
		return diff(new_cond, str2)
	else:
		return diff(str1, str2)


def cast_equivalence(str1, str2):
	if "'" in str1:
		other = str1.replace("'", "")
		return other == str2
	elif "'" in str2:
		other = str2.replace("'", "")
		return other == str1
	return False


def evaluate_equivalence(node_evaluate, node_if, perform_g1, perform_g2):
	var = node_evaluate.initial_node.condition  # Var on which we do the evaluate
	if_matched = []
	couples = []
	all_transition = []
	exit_transitions = []
	new_if = None
	for t2 in node_evaluate.get_transition():
		if t2.label == "OTHER":  # End of matching the EVALUATE
			if len(if_matched) > 0:
				next_couples = []
				t_m = TraceMatch(t2.label, if_matched[-1], node_evaluate, node_if, t2.to, perform_g1, perform_g2) #Last match between last if and exit of evaluate
				next_couples.append(t_m)
				for elem in exit_transitions: #match all exit transitions with correct last exit
					t_m = TraceMatch(t2.label, elem.fr, node_evaluate, node_if, t2.to, perform_g1, perform_g2)
					next_couples.append(t_m)
				all_transition.append(t2)
				return if_matched, next_couples, all_transition, exit_transitions
		if var == "TRUE":#EVALUATE TRUE means condition will be fully on branches
			cond = t2.label
		else:
			cond = var + " = " + t2.label
		if len(node_if.get_transition()) == 2:  # Only possible if the node has two transitions
			matched = False
			new_if = None
			for t1 in node_if.get_transition():
				if t1.label == cond or try_simple_equivalence(t1.label, cond) or (auto_cast_evaluate and cast_equivalence(t1.label, cond)):
					matched = True
					t_m = TraceMatch(t1.label, node_if, node_evaluate, t1.to, t2.to, perform_g1, perform_g2)
					couples.append(t_m)
					all_transition.append(t1)
					all_transition.append(t2)
				else:
					all_transition.append(t1)
					exit_transitions.append(t1)
					new_if = t1.to
			if matched:
				if_matched.append(node_if)
				if couples[-1].node1_to == new_if: #We are pointing to the next if, that won't do
					couples.pop()
				node_if = new_if
			else:
				return None, None, all_transition, exit_transitions
	return None, None, all_transition, exit_transitions


def try_transformations(node1, node2, perform_g1, perform_g2):
	str1 = node1.initial_node.get_str_code()
	str2 = node2.initial_node.get_str_code()
	for tup in struct:
		if tup[1] in str1:
			return evaluate_equivalence(node1, node2, perform_g1, perform_g2), False
		if tup[1] in str2:
			return evaluate_equivalence(node2, node1, perform_g1, perform_g2), True
	return (None, None, None, None), True


def try_factorize(goal, node2):  # Try and factorize node 2 to node 1
	true_cond = node2.initial_node.condition
	false_cond = node2.initial_node.condition
	if true_cond not in goal and false_cond not in goal or not isinstance(node2.initial_node, SimpleBranchConditionNode): #If we have no way to ceate a correct factorization, exit
		return False, true_cond, [], []
	next = node2
	found = True
	fact_nodes = []
	branch_out = []
	while found:
		found = False
		for transition in next.get_transition():
			curr_init = transition.to.initial_node
			next_init = next.initial_node
			if isinstance(curr_init, SimpleBranchConditionNode):
				if curr_init == next_init.true_child or curr_init == next_init.false_child:
					fact_nodes.append(next)
					next = transition.to
					found = True
					if curr_init == next_init.true_child:
						true_cond += " " + fact[True] + " " + curr_init.condition
					if curr_init == next_init.false_child:
						false_cond += " " + fact[False] + " " + transition.to.initial_node.condition
			else:
				if transition.to not in branch_out:
					branch_out.append(transition.to)
		if goal == true_cond or try_simple_equivalence(goal, true_cond) or goal == false_cond or try_simple_equivalence(goal, false_cond):  # Check if we are not done
			if len(branch_out) == 0:
				for t in next.get_transition():
					branch_out.append(t.to)
			fact_nodes.append(next)
			if goal == false_cond or try_simple_equivalence(goal, false_cond):
				return false_cond != node2.initial_node.condition, false_cond, fact_nodes, branch_out
			if goal == true_cond or try_simple_equivalence(goal, true_cond):
				return true_cond != node2.initial_node.condition, true_cond, fact_nodes, branch_out

		if len(false_cond) > len(goal) or len(true_cond) > len(goal):  # If we are over the length and still not equal, stop
			return False, true_cond, [], []

	return true_cond == goal, true_cond, fact_nodes, branch_out
