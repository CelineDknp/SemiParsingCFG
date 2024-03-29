from .Node import Node
from .FusedNode import FusedNode
from .SimpleBranchConditionNode import SimpleBranchConditionNode
from .MultipleBranchConditionNode import MultipleBranchConditionNode
from .ControlLoopNode import ControlLoopNode
from .LabelLoopNode import LabelLoopNode
from .LabelNode import LabelNode
from .LoopNode import LoopNode
from .MultipleLabelLoopNode import MultipleLabelLoopNode
from .BlockLoopNode import BlockLoopNode
from Utils.config import *
from Utils.utils import clean_regex
import graphviz


class Graph:

	def __init__(self, start_node):
		self.start_node = start_node
		self.last_node = start_node
		self.open_ifs = []
		self.open_loops = {}
		self.open_control_loops = []
		self.all_labels = {}
		self.all_nodes = [start_node]

	def get_last_node(self):
		return self.all_nodes[-1]

	def get_size(self):
		return len(self.all_nodes)

	def get_link_size(self):
		total = 0
		for e in self.all_nodes:
			total += len(e.childs)
		return total

	def match_if(self, branch_node):
		res = None
		# print(f"Searching corr node for: {branch_node}")
		for cond_node in self.open_ifs:
			# print(f"Looking at {cond_node} at depth {cond_node.get_depth()}")
			# print(f"{cond_node.get_regex()} VS {branch_node.get_regex()}")
			if cond_node.get_depth() == branch_node.get_depth() and (
					cond_node.get_regex() == branch_node.get_regex() or branch_node.get_type() == NODE_COND_END_ANY):
				# print("match !")
				res = cond_node
		return res

	def match_varying_loops(self):
		first_block = None
		if "block" in self.open_loops:
			for e in self.open_loops["block"]:
				if e.is_close_node():
					e.add_child(first_block)
					e.set_target(first_block)
					first_block.set_target(e)
				else:
					first_block = e

	def match_loops(self, node):
		to_remove = []
		# print(f"IN MATCH LOOPS {node}")
		# print(self.open_loops)
		label = node.get_label()
		if label in self.open_loops.keys():
			for loop in self.open_loops[node.get_label()]:
				# print("MATCH")
				if isinstance(loop, LabelLoopNode):
					if isinstance(loop, MultipleLabelLoopNode):
						first_label = loop.get_label()[0]
						last_label = loop.get_label()[-1]
						if label == first_label:
							loop.add_child(node, label=True)
							to_remove.append(loop)
						elif label == last_label:
							node.add_child(loop)
							to_remove.append(loop)
					elif label == loop.get_label():
						loop.add_child(node, label=True)
						to_remove.append(loop)
				else:
					if label == loop.get_label():
						loop.add_child(node)
						to_remove.append(loop)
		for n in to_remove:
			self.open_loops[node.get_label()].remove(n)

	def match_control_node(self, control_node, child):
		to_remove = []
		found = False
		for n in self.open_control_loops:
			if isinstance(n, ControlLoopNode) and control_node.get_type() == n.get_control():
				n.add_child(child, match=True)
				found = True
				to_remove.append(n)
		for n in to_remove:
			self.open_control_loops.remove(n)
		return found

	def match_labels(self, loop_node):
		if isinstance(loop_node, ControlLoopNode):
			return True

		if isinstance(loop_node, MultipleLabelLoopNode):
			first_label = loop_node.get_label()[0]
			if first_label in self.all_labels.keys():
				# print("MATCH")
				loop_node.add_child(self.all_labels[first_label])
				if len(loop_node.get_childs()) == len(loop_node.get_label())+1:
					return False
		elif isinstance(loop_node, LabelLoopNode):
			if loop_node.get_label() in self.all_labels.keys():
				loop_node.add_child(self.all_labels[loop_node.get_label()])
				return False
		return True

	def update_open_loops(self, node):
		if node.is_control():
			self.open_control_loops.append(node)
		elif node.is_block():
			if node.is_close_node():#We must try to link it
				if "block" in self.open_loops and len(self.open_loops["block"]) > 0:
					prev_block = self.open_loops["block"][-1]
					node.add_child(prev_block)
					node.set_target(prev_block)
					prev_block.set_target(node)
					self.open_loops["block"].remove(prev_block)
			elif "block" not in self.open_loops.keys():
				self.open_loops["block"] = [node]
			else:
				self.open_loops["block"].append(node)
		elif self.match_labels(node):
			if node.is_multiple_labels():
				for l in node.get_label():
					if l in self.open_loops.keys():
						self.open_loops[l].append(node)
					else:
						self.open_loops[l] = [node]
			else:
				if node.get_label() in self.open_loops.keys():
					self.open_loops[node.get_label()].append(node)
				else:
					self.open_loops[node.get_label()] = [node]

	def add_single_node(self, node):
		if self.last_node is not None:
			self.last_node.add_child(node)
		self.last_node = node
		self.all_nodes.append(node)

	def add_node(self, node):
		# print(f"Adding node {node}")
		if node.get_type() == NODE_COND_START:
			# print(">>> In IF")
			self.add_single_node(node)
			self.open_ifs.append(node)
		elif node.get_type() == NODE_SQL:
			self.add_single_node(node)
		elif node.get_type() == NODE_LABEL:
			# print(">>> In EXEC")
			self.add_single_node(node)
			self.all_labels[node.get_label()] = node
			self.match_loops(node)
		elif node.get_type() == NODE_LOOP:
			self.add_single_node(node)
			#print(f"Loop node {node}")
			if not node.is_goback_node(): #If we don't need to go back to this node, don't
				#print("Node was a GOTO, cancel last node")
				self.last_node = None
			self.update_open_loops(node)
		elif node.get_type() == NODE_COND_BRANCH:
			# print(">>> In ELSE")
			corr_if = self.match_if(node)
			if corr_if is None:
				print(f"Was looking for node to match {node} in array {self.open_ifs}, but found none")
				raise Exception('Missmatched condition branch')
			temp = Node(corr_if.get_depth(), NODE_CONTROL)
			if isinstance(node, MultipleBranchConditionNode):  # We have a multiple condition, grab the condition
				corr_if.add_branch_condition(node, temp)
			corr_if.close_branch()  # If we found an else, we should close the previous branch
			corr_if.add_child(temp)
			self.all_nodes.append(temp)
			self.last_node = temp
		elif node.get_type() == NODE_COND_END or node.get_type() == NODE_COND_END_ANY:
			# print(">>> In END-IF")
			corr_if = self.match_if(node)
			temp = Node(0, NODE_CONTROL) if corr_if is None else Node(corr_if.get_depth(), NODE_CONTROL)
			f = False
			if node.get_type() == NODE_COND_END_ANY:
				f = self.match_control_node(node, temp)
			if corr_if is None and not f:
				print(f"Was looking for node to match {node} in array {self.open_ifs} or {self.open_control_loops}, but found none")
				raise Exception('Missmatched condition end')
			# print(f"Found matching if: {corr_if}", flush=True)
			if corr_if is not None:
				corr_if.close(temp)
				self.open_ifs.remove(corr_if)
			if self.last_node is not None:
				if not isinstance(self.last_node, SimpleBranchConditionNode) or self.last_node.false_branch_open():
					self.last_node.add_child(temp)
			self.last_node = temp
			self.all_nodes.append(temp)
		elif node.get_type() == "END":  # Adding the end_node
			self.add_single_node(node)
			#self.match_varying_loops()
		else:
			print(f"Issue during adding node {node}")

	def get_start_node(self):
		return self.start_node

	def get_size(self):
		return len(self.all_nodes)

	def get_all_nodes(self):
		return self.all_nodes

	def replace_child(self, target, old_child, new_child):
		if isinstance(target, SimpleBranchConditionNode):
			if target.true_child == old_child:
				target.remove_child(old_child)
				target.add_child(new_child, end=True, branch=True)
			if target.false_child == old_child:
				target.remove_child(old_child)
				target.add_child(new_child, end=True, branch=False)
		elif isinstance(target, LoopNode):
			target.remove_child(old_child)
			target.add_child(new_child, match=True)
		else:
			target.remove_child(old_child)
			target.add_child(new_child)
		for grand_child in old_child.get_childs():
			grand_child.remove_parent(old_child)
			grand_child.add_parent(target)
		if old_child in self.all_nodes:
			self.all_nodes.remove(old_child)
		return old_child

	def cleanup_triangle(self, current_node, new_child):
		return self.replace_child(current_node.get_parent()[0], current_node, new_child)

	def one_parent(self, node):
		if len(node.get_parent()) == 0:
			return False
		if len(node.get_parent()) == 1:  # Easy case, only one parent
			return True
		first = node.get_parent()[0]
		for elem in node.get_parent():
			if elem != node:  # Dirty
				if elem != first:
					return False
		return True

	def cleanup(self, label_clean=False):
		cleaned = True
		while cleaned == True:
			visited = []
			cleaned = False
			start_node = self.all_nodes.copy()
			while len(start_node) != 0:
				current_node = start_node[0]
				visited.append(current_node)
				deleted = []
				if current_node.get_type() == NODE_CONTROL:
					children = current_node.get_childs()
					# print(f">>> Found control node ! len children: {len(children)} len grand_children: {len(children[0].get_childs())}")
					if len(children) == 2:
						if children[0] == children[1]:  # Two links pointing the same direction
							current_node.remove_child(children[0])
							cleaned = True
						# We are dealing with a triangle (V1)
						elif len(children[0].get_childs()) > 0 and children[1] == children[0].get_childs()[0]:
							deleted.append(self.cleanup_triangle(current_node, children[1]))
							cleaned = True
						# We are dealing with a triangle (V2)
						elif len(children[1].get_childs()) > 0 and children[0] == children[1].get_childs()[0]:
							deleted.append(self.cleanup_triangle(current_node, children[0]))
							cleaned = True
					elif len(children) == 1:
						# We are in a control node having a single child of a control node
						parent_node = current_node.get_parent().copy()
						for p in parent_node:
							deleted.append(self.replace_child(p, current_node, children[0]))
						if len(parent_node) > 0:
							cleaned = True
						elif current_node in self.all_nodes:
							self.all_nodes.remove(current_node) #Degenerated node that needs removal
				elif current_node.get_type() == NODE_LABEL and label_clean:
					parents = current_node.get_parent()
					if len(parents) == 1 and parents[0].get_type() != NODE_LOOP:  # A single parent that is not a GOTO
						child_node = current_node.get_childs().copy()
						if not any(isinstance(child, LabelLoopNode) for child in child_node):
							for c in child_node:
								deleted.append(self.replace_child(parents[0], current_node, c))
								cleaned = True

				for child in current_node.get_childs().copy():  # Look at a node's childrens
					if child.get_type() == NODE_CONTROL:  # When we find a control node
						if len(child.get_childs()) == 1 and self.one_parent(child):  # Only one parent and one child
							deleted.append(self.replace_child(current_node, child, child.get_childs()[0]))
							cleaned = True
				for e in deleted:
					if e in start_node:
						start_node.remove(e)
				if current_node in start_node:
					start_node.remove(current_node)

	def fuse(self, node_up, node_down):
		if node_down.get_type() == NODE_FUSED:
			node_down.fuse_node(node_up, up=True)
			self.all_nodes.remove(node_up)
			return node_down
		elif node_up.get_type() == NODE_FUSED:
			node_up.fuse_node(node_down, down=True)
			self.all_nodes.remove(node_down)
		else:
			node = FusedNode(node_up.get_depth(), NODE_FUSED)
			self.all_nodes.append(node)
			node.fuse_node(node_up, up=True)
			self.all_nodes.remove(node_up)
			node.fuse_node(node_down, down=True)
			self.all_nodes.remove(node_down)
			return node

	def squish(self):
		squished = True
		while squished:
			squished = False
			start_node = self.all_nodes.copy()
			all_nodes = []
			while len(start_node) != 0:
				current_node = start_node[0]
				all_nodes.append(current_node)
				if (
						current_node.get_type() == NODE_COND_START or current_node.get_type() == NODE_FUSED) and current_node.point_to_one():
					# We are in a if node that points to a single node
					# print(f"Found a node that points to one: {current_node} with childs: {current_node.get_childs()}")
					child = current_node.get_childs()[0]
					if child.get_type() != "END" and child.get_type() != NODE_SQL:
						merge = True
						for c in child.get_childs():
							if c.get_type() == NODE_SQL:
								merge = False
						if merge:
							# print("Decided to merge !")
							res = self.fuse(current_node, child)
							squished = True
							break
				elif current_node.get_type() == NODE_FUSED and any(
						child.get_type() == NODE_FUSED for child in current_node.get_childs()):
					# print("Found a fused node having fused child")
					# We found a fused node having a FUSED child
					to_fuse = None
					for child in current_node.get_childs():
						if child.get_type() == NODE_FUSED:
							to_fuse = child
					if to_fuse != None:
						# print("Decided to fuse the fuse")
						res = self.fuse(current_node, to_fuse)
						squished = True
				start_node.remove(current_node)

	def save_as_file(self, filename, output_dir='doctest-output'):
		dot = graphviz.Digraph(filename)
		for current_node in self.all_nodes:
			if current_node.get_type() == NODE_COND_START:
				dot.attr('node', shape='ellipse')
				dot.node(str(current_node.id), clean_regex(current_node) + " " + current_node.condition)
			elif current_node.get_type() == NODE_LOOP:
				dot.attr('node', shape='ellipse')
				if isinstance(current_node, ControlLoopNode):
					dot.node(str(current_node.id), clean_regex(current_node))
				elif isinstance(current_node, MultipleLabelLoopNode):
					dot.node(str(current_node.id), "PERFORM " + current_node.get_label()[0]+" THRU "+ current_node.get_label()[1])
				elif isinstance(current_node, LabelLoopNode):
					dot.node(str(current_node.id), clean_regex(current_node)+" " + current_node.get_label())
				elif isinstance(current_node, BlockLoopNode):
					if current_node.is_close_node():
						dot.node(str(current_node.id), "END PERFORM")
					else:
						dot.node(str(current_node.id), "PERFORM " + current_node.get_branch_str()+" "+current_node.get_condition_str())
			elif current_node.get_type() == NODE_SQL:
				dot.attr('node', shape='box')
				dot.node(str(current_node.id), current_node.parsable)
			elif current_node.get_type() == NODE_LABEL:
				dot.attr('node', shape='note')
				dot.node(str(current_node.id), current_node.label)
			elif current_node.get_type() == NODE_CONTROL:
				dot.node(str(current_node.id), str(current_node.id))
			elif current_node.get_type() == "START":
				dot.attr('node', shape='diamond')
				dot.node(str(current_node.id), 'START')
			elif current_node.get_type() == "END":
				dot.attr('node', shape='diamond')
				dot.node(str(current_node.id), 'END')
			elif current_node.get_type() == NODE_FUSED:
				dot.attr('node', shape='circle')
				dot.node(str(current_node.id), str(current_node.amount_contained()))
		for n in self.all_nodes:
			if n.get_type() == NODE_COND_START and isinstance(n, SimpleBranchConditionNode):
				#print(n)
				dot.edge(str(n.id), str(n.true_child.id), label='True')
				dot.edge(str(n.id), str(n.false_child.id), label='False')
			elif n.get_type() == NODE_COND_START and isinstance(n, MultipleBranchConditionNode):
				for condition in n.get_branch_childs().keys():
					# print(condition)
					dot.edge(str(n.id), str(n.get_branch_child(condition).id), label=condition)
			elif n.get_type() == NODE_LOOP and n.is_goback_node():
				#print(f"Doing node {n}")
				perform_edge = False
				go_back_edge = False
				for link in n.get_childs():
					#print(f"Linking to {link}")
					if isinstance(n, BlockLoopNode) and not n.is_close_node() and link == n.get_target():
						if len(n.get_childs()) == 1 and isinstance(link, BlockLoopNode):  # We have an empty perform
							dot.edge(str(n.id), str(n.id), label=n.condition_str)
						dot.edge(str(n.id), str(link.id), label="NOT "+n.condition_str) #We need a link no to the end of the perform
					elif isinstance(n, BlockLoopNode) and not n.is_close_node():
						if len(n.get_childs()) == 1 and n.get_childs()[0] == n.get_target():#We have an empty perform
							dot.edge(str(n.id), str(n.id), label="NOT "+n.condition_str) #Loop link
							dot.edge(str(n.id), str(link.id), label=n.condition_str)  #Exit link
						elif n.get_target() != link: #We have code inside the perform, just link normally
							dot.edge(str(n.id), str(link.id), label=n.condition_str)
							if len(n.get_childs()) == 1: #If we have a single child, we should also add the jump to target if not cond
								dot.edge(str(n.id), str(n.get_target().id), label="NOT "+n.condition_str)
						else:
							dot.edge(str(n.id), str(link.id))
					elif isinstance(n, BlockLoopNode) and n.is_close_node(): #We are at the end perform
						if link == n.get_target():
							tar_childs = n.get_target().get_childs()
							if len(tar_childs) == 1 and tar_childs[0] == n: #Single perform, no link
								pass
							else:
								dot.edge(str(n.id), str(n.get_target().id), label=n.get_target().condition_str)
						else:
							tar_childs = n.get_target().get_childs()
							if len(tar_childs) == 1 and tar_childs[0] == n: #Single perform, no link
								dot.edge(str(n.id), str(link.id))
							else:
								dot.edge(str(n.id), str(link.id), label="NOT "+n.get_target().condition_str)
					elif isinstance(n, LabelLoopNode):
						if link == n.get_label_child() and not perform_edge:
							dot.edge(str(n.id), str(n.get_label_child().id),
									 label="PERFORM")  # Add the link to the label_child
							perform_edge = True
						else:
							dot.edge(str(n.id),str(link.id))
						# print(link)
						if not isinstance(n,
										  BlockLoopNode) and link.get_type() == NODE_LABEL \
								and link.get_label() == n.go_back_label() and not go_back_edge:
							dot.edge(str(link.id), str(n.id), label="Go back")
							go_back_edge = True
					else:
						dot.edge(str(n.id), str(link.id))
					
			elif isinstance(n, LabelNode):
				for link in n.get_childs():
					if isinstance(link, MultipleLabelLoopNode) and n.get_label() == link.label[-1]:
						dot.edge(str(n.id), str(link.id), label="Go back")
					else:
						dot.edge(str(n.id), str(link.id))

			else:
				for link in n.get_childs():
					dot.edge(str(n.id), str(link.id))
		dot.render(directory=output_dir, view=False)

	def add_node_to_list(self, node):
		self.all_nodes.append(node)

	def __str__(self):
		result = "Nodes in graph:\n"
		for n in self.all_nodes:
			# print(n.id)
			result += n.__repr__() + "\n"
		return result
