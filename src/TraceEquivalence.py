from LTSGraph.LTSGraph import LTSGraph

class TraceEquivalence:

	def __init__(self, g1, g2):
		self.g1 = g1
		self.g2 = g2
		self.visited_g1 = []
		self.visited_g2 = []

	def compare(self):
		g1_walker = self.g1.get_start()
		g2_walker = self.g2.get_start()
		self.walk(g1_walker, g2_walker)

	def walk(self, node1, node2):
		self.visited_g1.append(node1)
		self.visited_g2.append(node2)
		keep_walking = False
		if node1.has_single_out(): #A single transition out will be ignored (TODO: check)
			keep_walking = True
			node1 = node1.next()
		if node2.has_single_out(): #Same
			keep_walking = True
			node2 = node2.next()
		if keep_walking:
			self.walk(node1, node2)
		else:
			print("stop !")