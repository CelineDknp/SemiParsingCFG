import os
import sys
import subprocess

def partition_data(input_file, partitions, output_file):
	with open(input_file) as f1:
		all_data = []
		for line in f1:
			splitted = line.split(";")
			name = splitted[0]
			try:
				percent = float(splitted[6].replace(",",".")) #% file diff \w comments
				all_data.append((percent, name))
			except:
				print(line)
				pass #Just skip if it doesn't work
		all_data.sort()
		leftover = len(all_data) % partitions
		next_place = 0
		with open(output_file, "a") as output:
			for i in range(partitions):
				next_amount = len(all_data) // partitions
				if leftover > 0:
					next_amount += 1
					leftover -= 1
				for j in range(next_amount):
					#print(next_place)
					output.write(f"{all_data[next_place][1]}; Cat{i}; {all_data[next_place][0]}\n")
					next_place += 1




def main(argv):
	if len(argv) < 4:
		print("Usage: python calculate_parts.py input_file partitions ouput_target")
		return
	else: #More options were given
		f = open(argv[3], "w")
		f.write("filename; category; exact % value\n")
		f.close()
		partition_data(argv[1], int(argv[2]), argv[3])



if __name__ == '__main__':
	print("Running")
	main(sys.argv)