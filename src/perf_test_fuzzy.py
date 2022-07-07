import sys
import time
import os
import subprocess
from multiprocessing import Queue 
from multiprocessing import Process
import sqlite3
from main import process_and_parse
from FuzzyParser import FuzzyParser
from main import pre_process
import gc

def run_batch_fuzzy(dir_name, all_runs_fuzzy):
	fuzzy_p = FuzzyParser()
	all_runs = []
	for file in os.listdir(dir_name):
		filename = os.path.join(dir_name, file)
		print(f"Doing file {filename}", flush=True)
		target = open(filename, "r", encoding='latin-1')
		file_size = len(target.readlines())
		target.close()
		target = open(filename, "r", encoding='latin-1')
		start_time_fuzzy = time.time()
		input_str = pre_process(target)
		lot = fuzzy_p.fuzzy_parse(input_str)
		end_time_fuzzy = time.time()
		target.close()
		delta_fuzzy = end_time_fuzzy - start_time_fuzzy
		all_runs.append([filename, file_size, delta_fuzzy])
	all_runs_fuzzy.put(all_runs)

def run_single_fuzzy(filename, all_runs_fuzzy):
	start_time_fuzzy = time.time()
	process_and_parse(filename)
	end_time_fuzzy = time.time()
	delta_fuzzy = end_time_fuzzy - start_time_fuzzy
	all_runs_fuzzy.put(delta_fuzzy)

def stat_run(filename, output_file, multi=1, runs=20):
	with open(output_file, "a") as f:
		target = open(filename, "r",encoding='latin-1')
		file_size = len(target.readlines())
		target.close()
		all_runs_fuzzy = 0

		print(f"Doing file {filename}", flush=True)
		#Actual calcul
		all_runs_fuzzy = Queue()
		rets = []
		while len(rets) != runs:
			processes = []
			launch = multi if len(rets)+multi <= runs else runs-len(rets)
			# print(f"Launching {launch} processe(s) !")
			for pid in range(launch):
				p = Process(target=run_single_fuzzy, args=(filename, all_runs_fuzzy ,))
				processes.append(p)
				p.start()
			for p in processes:
				ret = all_runs_fuzzy.get() # will block
				rets.append(ret)
			for p in processes:
				p.join()
		total = 0
		for elem in rets:
			total += elem
		mean_fuzzy = total/runs


		f.write(f"{filename}; {file_size} ; {mean_fuzzy} \n")
		return mean_fuzzy

def batch_run(dir_name, output_file, multi=1, runs=20):
	with open(output_file, "a") as f:
		all_runs_fuzzy = 0
		#Actual calcul
		all_runs_fuzzy = Queue()
		fuzzy_rets = []
		while len(fuzzy_rets) != runs:
			processes = []
			launch = multi if len(fuzzy_rets)+multi <= runs else runs-len(fuzzy_rets)
			# print(f"Launching {launch} processe(s) !")
			for pid in range(launch):
				p = Process(target=run_batch_fuzzy, args=(dir_name, all_runs_fuzzy ,))
				processes.append(p)
				p.start()
			for p in processes:
				ret = all_runs_fuzzy.get() # will block
				fuzzy_rets.append(ret)
			for p in processes:
				p.join()

		all_infos= {}
		for elem in fuzzy_rets:
			for line in elem:
				if line[0] not in all_infos.keys():
					all_infos[line[0]] = [line[1], line[2]]
				else:
					all_infos[line[0]][1] += line[2]

		for elem in all_infos.keys():
			data = all_infos[elem]
			mean_fuzzy = data[1]/runs
			f.write(f"{elem}; {data[0]} ; {mean_fuzzy}\n")


def crawl_dirs(argv):
	runs = 20
	if "-runs" in argv:
		runs = int(argv[argv.index("-runs")+1])
	multi = 1
	if "-thread" in argv:
		multi = int(argv[argv.index("-thread")+1])
	batch = True if "-batch" in argv else False
	print(f"Crawling directory {argv[1]} (batched={batch}), "+
		f"{runs} runs for each file, {multi} parallel processes", flush=True)
	if batch:
		batch_run(argv[1], argv[2], runs=runs, multi=multi)
	else:
		for file in os.listdir(argv[1]):
			stat_run(os.path.join(argv[1],file), argv[2], runs=runs, multi=multi)
		print("Done!")
	return


def main(argv):
	if len(argv) < 3:
		print("Usage: python perf_test filename|directory output_target *-dir *-batch *-runs N *-thread M")
		return
	else: #More options were given
		f = open(argv[2], "w")
		f.write("filename; file size; fuzzy time (s); \n")
		f.close()
		if "-dir" in argv:
			crawl_dirs(argv)
		else:
			runs = 20
			if "-runs" in argv:
				runs = int(argv[argv.index("-runs")+1])
			multi = 1
			if "-thread" in argv:
				multi = int(argv[argv.index("-thread")+1])
			print(f"Comparing performance on file {argv[1]} ({runs} runs)")
			stat_run(argv[1], argv[2], runs=runs, multi=multi)



if __name__ == '__main__':
	print("Running")
	main(sys.argv)