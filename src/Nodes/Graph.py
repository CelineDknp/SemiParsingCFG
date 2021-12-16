from Nodes.Node import Node
from Nodes.FusedNode import FusedNode
import graphviz

class Graph:

	def __init__(self, start_node):
		self.start_node = start_node
		self.last_node = start_node
		self.open_ifs = []
		self.all_nodes = [start_node]

	def match_if(self, else_node):
		res = None
		for if_node in self.open_ifs:
			if if_node.get_depth() == else_node.get_depth():
				res = if_node
		return res

	def add_node(self, node):
		if node.get_type() == "IF":
			# print(">>> In IF")
			self.last_node.add_child(node)
			self.last_node = node
			self.open_ifs.append(node)
			self.all_nodes.append(node)
		elif node.get_type() == "EXEC":
			# print(">>> In EXEC")
			self.last_node.add_child(node)
			self.last_node = node
			self.all_nodes.append(node)
		elif node.get_type() == "ELSE":
			# print(">>> In ELSE")
			corr_if = self.match_if(node)
			corr_if.close_branch() #If we found an else, we should close the previous branch
			temp = Node(corr_if.get_depth(), "CONTROL")
			corr_if.add_child(temp)
			self.all_nodes.append(temp)
			self.last_node = temp
		elif node.get_type() == "END-IF":
			# print(">>> In END-IF")
			corr_if = self.match_if(node)
			temp = Node(corr_if.get_depth(), "CONTROL")
			corr_if.close(temp)
			self.open_ifs.remove(corr_if)
			self.last_node = temp
			self.all_nodes.append(temp)
		elif node.get_type() == "END": #Adding the end_node
			self.last_node.add_child(node)
			self.last_node = node
			self.all_nodes.append(node)
			# print("Added the last_node")
		else:
			print("Issue during adding node")

	def get_start_node(self):
		return self.start_node

	def get_size(self):
		return len(self.all_nodes)

	def get_all_nodes(self):
		return self.all_nodes


	def replace_child(self, target, old_child, new_child):
		if target.get_type() == "IF":
			if target.true_child == old_child:
				target.remove_child(old_child)
				target.add_child(new_child, end=True, branch=True)
			if target.false_child == old_child:
				target.remove_child(old_child)
				target.add_child(new_child, end=True, branch=False)
		else:
			target.remove_child(old_child)
			target.add_child(new_child)
		if old_child in self.all_nodes:
			self.all_nodes.remove(old_child)

	def cleanup_triangle(self, current_node, new_child):
		replace_child(current_node.get_parent()[0], current_node, new_child)

	def one_parent(self, node):
		if len(node.get_parent()) == 0:
			return False
		if len(node.get_parent()) == 1: #Easy case, only one parent
			return True
		first = node.get_parent()[0]
		for elem in node.get_parent():
			if elem != node: #Dirty
				if elem != first:
					return False
		return True


	def cleanup(self):
		cleaned = True
		while cleaned == True:
			cleaned = False
			start_node = []
			start_node.append(self.get_start_node())
			while len(start_node) != 0:
				current_node = start_node[0]
				if current_node.get_type() == "CONTROL":
					children = current_node.get_childs()
					# print(f">>> Found control node ! len children: {len(children)} len grand_children: {len(children[0].get_childs())}")
					if len(children) == 2:
						if children[0] == children[1]: #Two links pointing the same direction
							current_node.remove_child(children[0])
							cleaned = True
						#We are dealing with a triangle (V1)
						elif children[1] == children[0].get_childs()[0]:
							self.cleanup_triangle(current_node, children[1])
							cleaned = True
						#We are dealing with a triangle (V2)
						elif children[0] == children[1].get_childs()[0]:
							self.cleanup_triangle(current_node, children[0])
							cleaned = True
					elif len(children) == 1:
						#We are in a control node having a single child of a control node 
						parent_node = current_node.get_parent()
						for p in parent_node:
							self.replace_child(p, current_node, children[0])
						cleaned = True
				
				for child in current_node.get_childs(): #Look at a node's childrens
					if child.get_type() == "CONTROL": #When we find a control node
						if len(child.get_childs()) == 1 and self.one_parent(child): #Only one parent and one child
							self.replace_child(current_node, child, child.get_childs()[0])
							cleaned = True

				for child in current_node.get_childs():
					if child not in start_node:
						start_node.append(child)
				start_node.remove(current_node)

	def fuse(self, node_up, node_down):
		if node_down.get_type() == "FUSED":
			node_down.fuse_node(node_up, up = True)
			self.all_nodes.remove(node_up)
			return node_down
		elif node_up.get_type() == "FUSED":
			node_up.fuse_node(node_down, down = True)
			self.all_nodes.remove(node_down)
		else:
			node = FusedNode(node_up.get_depth(), "FUSED")
			self.all_nodes.append(node)
			node.fuse_node(node_up, up=True)
			self.all_nodes.remove(node_up)
			node.fuse_node(node_down, down=True)
			self.all_nodes.remove(node_down)
			return node


	def squish(self): #Sqwish if nodes that go to a singe node
		squished = True
		while squished:
			squished = False
			start_node = []
			start_node.append(self.get_start_node())
			while len(start_node) != 0:
				current_node = start_node[0]
				if (current_node.get_type() == "IF" or current_node.get_type() == "FUSED") and current_node.point_to_one(): 
				#We are in a if node that points to a single node
					child = current_node.get_childs()[0]
					if child.get_type() != "END" and child.get_type() != "EXEC":
						merge = True
						for c in child.get_childs():
							if c.get_type() == "EXEC":
								merge = False
						if merge:
							res = self.fuse(current_node, child)
							squished = True
							break	
				for child in current_node.get_childs():
					if child not in start_node:
						start_node.append(child)
				start_node.remove(current_node)



	def save_as_file(self):
		dot = graphviz.Digraph('control-flow')
		start_node = []
		start_node.append(self.get_start_node())
		all_nodes = []
		while len(start_node) != 0:
			current_node = start_node[0]
			all_nodes.append(current_node)
			start_node.remove(current_node)
			if current_node.get_type() == "IF":
				dot.attr('node', shape='ellipse')
				dot.node(str(current_node.id), "IF "+current_node.condition) 
			elif current_node.get_type() == "EXEC":
				dot.attr('node', shape='box')
				dot.node(str(current_node.id), current_node.parsable)
			elif current_node.get_type() == "CONTROL":
				dot.node(str(current_node.id), str(current_node.id))
			elif current_node.get_type() == "START":
				dot.attr('node', shape='diamond')
				dot.node(str(current_node.id), 'START')
			elif current_node.get_type() == "END":
				dot.attr('node', shape='diamond')
				dot.node(str(current_node.id), 'END')
			elif current_node.get_type() == "FUSED":
				dot.attr('node', shape='circle') 
				dot.node(str(current_node.id), str(current_node.amount_contained()))
			for c in current_node.get_childs():
				if c not in all_nodes and c not in start_node:
					start_node.append(c)
		for n in all_nodes:
			if n.get_type() == "IF":
				dot.edge(str(n.id), str(n.true_child.id), label='True')
				dot.edge(str(n.id), str(n.false_child.id), label='False')
			else:
				for link in n.get_childs():
					dot.edge(str(n.id), str(link.id))
		dot.render(directory='doctest-output', view=False) 
