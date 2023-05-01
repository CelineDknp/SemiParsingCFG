import os
import sys
import subprocess
import random
import matplotlib.pyplot as plt

def graph(input_file, output_file):

	fig, ax = plt.subplots()
	#partition = {(-10, 23):[], (24, 29):[], (30, 36):[], (37, 44):[], (45,96):[]} #Change value splitted to 5 !
	partition = {(5, 33):[], (34, 40):[], (41, 47):[], (48, 55):[], (55,93):[]}#Change value splitted to 6 !
	with open(input_file) as f1:
		for line in f1:
			splitted = line.split(";")
			try:
				percent = float(splitted[6].replace(",",".")) #% file diff \w comments
				for e in partition.keys():
					if  e[0] <= percent*100 <= e[1]:
						partition[e].append(splitted[0])
			except:
				print(line)
				pass #Just skip if it doesn't work
	x = []
	count = []
	for elem in partition.keys():
		x.append(f"{elem[0]}-{elem[1]}")
		count.append(len(partition[elem]))

	counts = partition.values()

	#ax.bar(x, counts)

	ax.set_ylabel('# of files')
	ax.set_title('% of changes between V1 and V2')
	ax.legend(title='File partitions')
	#plt.savefig(output_file)

	print("One file at random from every partition")
	#print(partition)
	for e in partition.keys():
		n = random.randint(0, len(partition[e])-1)
		print(partition[e][n])




def main(argv):
	if len(argv) < 3:
		print("Usage: python generate_graph.py input_file output_file")
		return
	else: #More options were given
		graph(argv[1], argv[2])



if __name__ == '__main__':
	print("Running")
	main(sys.argv)