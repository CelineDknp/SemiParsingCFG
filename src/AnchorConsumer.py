class AnchorConsumer:
	def __init__(self):
		pass 

	def consume_ignore(self, n_anchor, next_val, actual_val, actual_match):
		if n_anchor.get_parse_type() == "comment":
			pos = next_val+len(actual_match)
		elif n_anchor.get_parse_type() == "string":
			pos = next_val+len(actual_match)
		return pos

	def consume_condition(self, n_anchor, next_val, actual_val, lot, actual_match):
		#print(f"Found condition {actual_match}")
		# print(f"In condition ! anchor: {n_anchor}, next_val: {next_val}, actual: {actual_val}, match: {actual_match}")
		self.pos = next_val + len(actual_match.rstrip())
		if actual_val == n_anchor.get_start_pattern(): #Found an opening condition
			# print(f'>>> FOUND COND start {actual_match}')
			node = None
			if n_anchor.is_multiple_branches():
				# print(">>> Multiple")
				node = MultipleBranchConditionNode(self.depth, NODE_COND_START, n_anchor.get_start())
			else:

				# print(">>> Simple")
				node = SimpleBranchConditionNode(self.depth, NODE_COND_START, n_anchor.get_start())
			if n_anchor.has_condition_delimiter():
				if n_anchor.is_delimiter_mandatory():
					self.pos = node.find_condition_delimiter(self.input_str, self.pos, n_anchor.get_delimiter())
				else:
					self.pos = node.find_condition(self.input_str, self.pos, n_anchor.get_delimiter())
			else:
					self.pos = node.find_condition_simple(self.input_str, self.pos)
			# print(f">>> COND COND: {node.get_condition()}")
			self.depth += 1
			if self.depth == 1:
				self.clean_anchors()
			lot.append(node)
		elif actual_val == n_anchor.get_branch_pattern() and (not n_anchor.is_multiple_branches()):
			# print('>>> FOUND COND single branch')
			node = SimpleBranchConditionNode(self.depth - 1, NODE_COND_BRANCH, n_anchor.get_start())
			lot.append(node)
		elif actual_val == n_anchor.get_branch_pattern() and n_anchor.is_multiple_branches():
			# print('>>> FOUND COND multiple branch')
			node = MultipleBranchConditionNode(self.depth - 1, NODE_COND_BRANCH, n_anchor.get_start())
			self.pos = node.find_condition_simple(self.input_str, self.pos)
			# print(f"Found condition: {node.get_condition()}")
			lot.append(node)
		elif actual_val == n_anchor.get_end_pattern(): #Found a COND end
			# print('>>> FOUND END-COND')
			self.depth -= 1
			if self.depth == 0:
				self.clean_anchors()
			node = ConditionNode(self.depth, NODE_COND_END, n_anchor.get_start())
			lot.append(node)

	def consume_parsable(self, n_anchor, next_val, lot):
		#print('>>> FOUND EXEC')
		node = ParseNode(self.depth, NODE_SQL, n_anchor.get_regex())
		lot.append(node)
		self.pos = node.find_parse_text(self.input_str, next_val)

	def consume_special(self, n_anchor, next_val, lot, actual_match):
		#print(f"Found special {actual_match}")
		#print(f"special ! {actual_match} effect: {n_anchor.get_effect()}")
		if n_anchor.get_effect() == "label":
			# print("found label")
			node = LabelNode(self.depth, NODE_LABEL, n_anchor.get_regex())
			node.find_label(actual_match)
			self.pos = next_val+len(actual_match)-1
			lot.append(node)
		elif n_anchor.get_effect() == "close_all":
			if self.depth > 0:
				while self.depth > 0:
					self.depth -= 1
					node = ConditionNode(self.depth, NODE_COND_END_ANY, n_anchor.get_regex())
					lot.append(node)
				if self.open_control:
					self.open_control = False
				self.clean_anchors()


			else:
				if self.open_control:
					node = Node(self.depth, NODE_COND_END_ANY)
					lot.append(node)
					self.open_control = False
					self.clean_anchors(found_control=True)
			self.pos = next_val+1
			#print(f"New pos is {self.pos}")
		elif n_anchor.get_effect() == "control":
			while self.depth > 0:
				self.depth -= 1
				node = ConditionNode(self.depth, NODE_COND_END_ANY, n_anchor.get_regex())
				lot.append(node)
			if self.open_control:
				node = Node(self.depth, n_anchor.get_info())
				lot.append(node)
				self.open_control = False
				self.clean_anchors(found_control=True)
			self.pos = next_val+1
			#print(f"New pos is {self.pos}")
		elif n_anchor.get_effect() == "start_parse":
			self.pos = self.len_next_match(n_anchor.get_pattern())

	def consume_loop(self, n_anchor, lot, next_val, actual_val, actual_match):
		#print(f"found loop ! {actual_match}")
		# print(f"Current state of input is: |{self.input[self.pos:self.pos+150]}|")
		if n_anchor.is_label_anchor():
			node = None
			if n_anchor.is_multiple_anchor():
				node = MultipleLabelLoopNode(self.depth, NODE_LOOP, n_anchor)
			else:	
				node = LabelLoopNode(self.depth, NODE_LOOP, n_anchor)
			lot.append(node)
			node.find_label(actual_match)
			# print(f"Current state of input is: |{self.input[self.pos:self.pos+150]}|")
		elif n_anchor.is_control_anchor():
			node = ControlLoopNode(self.depth, NODE_LOOP, n_anchor)
			lot.append(node)
			self.open_control = True
			self.clean_anchors(found_control=True)
		elif n_anchor.is_block_anchor():
			if actual_val == n_anchor.get_start_pattern():
				node = BlockLoopNode(self.depth, NODE_LOOP, n_anchor)
				lot.append(node)
				node.find_conditions(actual_match)
			elif actual_val == n_anchor.get_end_pattern():
				node = BlockLoopNode(self.depth, NODE_LOOP, n_anchor, close=True)
				lot.append(node)
		self.pos = next_val + len(actual_match.strip()) - 1