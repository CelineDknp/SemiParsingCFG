from main import compare_and_return
import os
import sys

def make_bar(input_file, output_file):
	partition = {(0, 10): [0,0], (11, 20): [0,0], (21, 30): [0,0], (31, 40): [0,0], (41, 50): [0,0], (51, 60): [0,0], (61, 70): [0,0], (71, 80): [0,0], (81, 90): [0,0], (91, 100): [0,0]}
	with open(input_file) as f:
		for line in f:
			line = line.replace(',', '.')
			splitted = line.split(";")
			print(splitted)
			for bound in partition.keys():
				if bound[0] <= float(splitted[0].strip())*100 <= bound[1]:
					partition[bound][0] += 1
				if bound[0] <= float(splitted[1].strip())*100 <= bound[1]:
					partition[bound][1] += 1
		print(partition)

def main(argv):
	if len(argv) < 3:
		print("Usage: python make_bar.py input output_target")
		return
	else: #More options were given
		make_bar(argv[1], argv[2])



if __name__ == '__main__':
	print("Running")
	main(sys.argv)