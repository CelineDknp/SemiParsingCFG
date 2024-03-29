class LTSTransition:
	def __init__(self, fr, to, label):
		self.fr = fr
		self.to = to
		self.label = label
		self.match = [-2]

	def get_label(self):
		return self.label

	def set_match(self, number, value, remove=False):
		#if remove and number in self.match:
		#	self.match[number].pop() #Remove last elem
		#if number in self.match:
		#	array = self.match[number]
		#	if -2 in array:
		#		array.remove(-2)
		#	if len(array) > 0 and array[-1] == value:
		#		return
		#	else:
		#		if value not in array:
		#			array.append(value) # 1 = sure match 0 = unsure, -1 = unmatch, -2 = unexplored
		#else:
		#	self.match[number] = [value]
		#self.match[number] = value
		if self.match == [-2]: #First add, just remove the -2
			self.match = [value]
		elif value not in self.match:
			self.match.append(value)

	def match_str(self):
		res = ""
		for e in self.match:
			res += str(e)+" "
		res = res.strip()
		return res

	def __eq__(self, other):
		if not isinstance(other, LTSTransition):
			return False
		return self.fr == other.fr and self.to == other.to and self.label == other.label

	def __str__(self):
		return f"Transition '{self.label}' {self.fr.__repr__()} -> {self.to.__repr__()} [{self.match}]"

	def __repr__(self):
		return f"Transition '{self.label}' {self.fr.__repr__()} -> {self.to.__repr__()} [{self.match}]"