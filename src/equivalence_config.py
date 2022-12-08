from re import search
from Nodes.ConditionNode import ConditionNode

#Label to ignore
ignore = "INTERNAL"

# Straight equivalences
equiv = [('" "', "SPACE"), ("' '", "SPACE"), ("0", "ZERO"), ("+", "", r"\+(\d)+")]

# Structure transformations
struct = [("IF", "EVALUATE")]

# Factorisation
fact = {False: "OR", True: "AND"}  # Join with OR on true branch and with OR on false ??


def try_simple_equivalence(str1, str2):
	for tup in equiv:
		new_cond = ""
		if len(tup) == 2:
			if tup[0] in str1:
				new_cond = str1.replace(tup[0], tup[1])
			if tup[1] in str1:
				new_cond = str1.replace(tup[1], tup[0])
		elif len(tup) == 3:  # We need to regex match
			if search(tup[2], str1):
				new_cond = str1.replace(tup[0], tup[1])
			elif search(tup[2], str2):
				new_cond = str2.replace(tup[0], tup[1])
		if new_cond == str2 or new_cond == str1:
			return True
	return False


def evaluate_equivalence(node_evaluate, node_if):
	var = node_evaluate.initial_node.get_str_code().split()[-1]  # Var on which we do the evaluate
	if_matched = []
	couples = []
	new_if = None
	for t2 in node_evaluate.get_transition():
		if t2.label == "OTHER":  # End of matching the EVALUATE
			couples.append((t2.to, new_if))
			return if_matched, couples
		cond = var + " = " + t2.label
		if len(node_if.get_transition()) == 2:  # Only possible if the node has two transitions
			matched = False
			new_if = None
			for t1 in node_if.get_transition():
				if t1.label == cond or try_simple_equivalence(t1.label, cond):
					matched = True
					couples.append((t1.to, t2.to))
				else:
					new_if = t1.to
			if matched:
				if_matched.append(new_if)
				node_if = new_if
			else:
				return None, None


def try_transformations(node1, node2):
	str1 = node1.initial_node.get_str_code()
	str2 = node2.initial_node.get_str_code()
	for tup in struct:
		if tup[1] in str1:
			return evaluate_equivalence(node1, node2), False
		if tup[1] in str2:
			return evaluate_equivalence(node2, node1), True
	return (None, None), True


def try_factorize(goal, node2):  # Try and factorize node 2 to node 1
	true_cond = node2.initial_node.condition
	false_cond = node2.initial_node.condition
	if true_cond not in goal: #If we have no way to ceate a correct factorization, exit
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
			if isinstance(curr_init, ConditionNode):
				if curr_init == next_init.true_child or curr_init == next_init.false_child:
					fact_nodes.append(next)
					next = transition.to
					found = True
					if curr_init == next_init.true_child:
						true_cond += " " + fact[True] + " " + curr_init.condition
					if curr_init == next_init.false_child:
						false_cond += " " + fact[False] + " " + transition.to.initial_node.condition
			else:
				branch_out.append(transition.to)
		if goal == true_cond or try_simple_equivalence(goal, true_cond) or goal == false_cond or try_simple_equivalence(goal, false_cond):  # Check if we are not done
			if len(branch_out) == 0:
				for t in next.get_transition():
					branch_out.append(t.to)
			if goal == false_cond or try_simple_equivalence(goal, false_cond):
				return false_cond != node2.initial_node.condition, false_cond, fact_nodes, branch_out
			if goal == true_cond or try_simple_equivalence(goal, true_cond):
				return true_cond != node2.initial_node.condition, true_cond, fact_nodes, branch_out

		if len(false_cond) > len(goal) or len(true_cond) > len(goal):  # If we are over the length and still not equal, stop
			return False, true_cond, [], []

	return true_cond == goal, true_cond, fact_nodes, branch_out
