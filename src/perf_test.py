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
from full_parse import make_graph
import gc

def run_single_full(filename, p_num, all_runs_full):
	FNULL = open(os.devnull, 'w')  # use this if you want to suppress output to stdout from the subprocess
	file = "Compilers/bin/cobrc.exe "
	flags = f" :DBConnectString=perf_output{p_num}.sqlite :DBDriver=Sqlite :IncludeSearchDir=Compilers/includes/cobol/ :MaxMem=500"
	args = file + filename + flags
	r = subprocess.run(args, capture_output=True, text=True, shell=False)
	conn = None
	try:
		conn = sqlite3.connect(f"perf_output{p_num}.sqlite")
	except Error as e:
		print(f"Error while connecting to the database to find parsing time {e}")
	cur = conn.cursor()
	cur.execute("SELECT RC_PARSING_TIME FROM RC_PROGRAM")
	row = cur.fetchone()
	delta_full = int(row[0])/1000
	try:
		conn.close()
	except Error as e:
		print(f"Error while closing the database {e}")
	os.remove(f"perf_output{p_num}.sqlite") 
	all_runs_full.put(delta_full)

def run_batch_fuzzy(dir_name, all_runs_fuzzy):
	fuzzy_p = FuzzyParser()
	# gc.disable()
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
	# gc.enable()

def run_single_fuzzy(filename, all_runs_fuzzy):
	# gc.disable()
	start_time_fuzzy = time.time()
	process_and_parse(filename)
	end_time_fuzzy = time.time()
	# gc.enable()
	delta_fuzzy = end_time_fuzzy - start_time_fuzzy
	all_runs_fuzzy.put(delta_fuzzy)

def stat_run(filename, output_file, multi=1, runs=20, verbose=False, condense=True):
	with open(output_file, "a") as f:
		target = open(filename, "r",encoding='latin-1')
		file_size = len(target.readlines())
		target.close()
		all_runs_fuzzy = 0
		if verbose:
			print("PURE PARSING")

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
		if not condense:
			f.write(f"F; {filename}; {file_size} ; fuzzy; {delta_fuzzy}\n")
			if verbose:
				print(f"Fuzzy parsing time: {delta_fuzzy}", flush=True)
		total = 0
		for elem in rets:
			total += elem
		mean_fuzzy = total/runs
		if verbose:
			print(f"Mean fuzzy parsing time: {mean_fuzzy}", flush=True)
		#Actual calcul
		all_runs_full = Queue()
		rets = []
		while len(rets) != runs:
			processes = []
			launch = multi if len(rets)+multi <= runs else runs-len(rets)
			# print(f"Launching {launch} processe(s) !")
			for pid in range(launch):
				p = Process(target=run_single_full, args=(filename, pid, all_runs_full ,))
				processes.append(p)
				p.start()
			for p in processes:
				ret = all_runs_full.get() # will block
				rets.append(ret)
			for p in processes:
				p.join()
		if not condense:
			for elem in rets:
				f.write(f"F; {filename}; {file_size} ; full; {elem}\n")
			if verbose:
				print(f"Full parsing time: {elem}",flush=True)
		total = 0
		for elem in rets:
			total += elem
		mean_full = total/runs
		diff = mean_full/mean_fuzzy
		mean_full_str = str(mean_full).replace(".", ",")
		mean_fuzzy_str = str(mean_fuzzy).replace(".", ",")
		diff_str = str(diff).replace(".", ",")


		f.write(f"T; {filename}; {file_size} ; {mean_fuzzy_str} ; {mean_full_str} ; {diff_str} \n")
		if verbose:
			print(f"Mean full parsing time: {mean_full}",flush=True)
			if mean_full > mean_fuzzy:
				if mean_fuzzy != 0:
					print(f"Fuzzy wins ! Difference is {(mean_full/mean_fuzzy)} ({(mean_full)-(mean_fuzzy)})", flush=True)
				else:
					print(f"Fuzzy wins ! Difference is ({(mean_full)-(mean_fuzzy)})", flush=True)
			elif mean_full == mean_fuzzy:
				print(f"Both executions took the same time", flush=True)
			else:
				if mean_full != 0:
					print((f"Full wins ! Difference is {mean_fuzzy/mean_full} ({mean_fuzzy-mean_full})"), flush=True)
				else:
					print((f"Full wins ! Difference is ({mean_fuzzy-mean_full})"), flush=True)
		return mean_fuzzy, mean_full

def batch_run(dir_name, output_file, multi=1, runs=20, verbose=False, condense=True):
	with open(output_file, "a") as f:
		all_runs_fuzzy = 0
		if verbose:
			print("PURE PARSING")
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
			mean_fuzzy_str = str(mean_fuzzy).replace(".", ",")
			f.write(f"T; {elem}; {data[0]} ; {mean_fuzzy_str}\n")


def crawl_dirs(argv):
	runs = 20
	if "-runs" in argv:
		runs = int(argv[argv.index("-runs")+1])
	multi = 1
	if "-thread" in argv:
		multi = int(argv[argv.index("-thread")+1])
	verbose = True if "-verbose" in argv else False
	batch = True if "-batch" in argv else False
	condense = False if "-uncondense" in argv else True
	print(f"Crawling directory {argv[1]} (batched={batch}), {runs} runs for each file, {multi} parallel processes (verbose={verbose})", flush=True)
	if batch:
		batch_run(argv[1], argv[2], runs=runs, multi=multi, verbose=verbose, condense=condense)
	else:
		for file in os.listdir(argv[1]):
			stat_run(os.path.join(argv[1],file), argv[2], runs=runs, multi=multi, verbose=verbose, condense=condense)
		print("Done!")
	return


def main(argv):
	if len(argv) < 3:
		print("Usage: python perf_test filename|directory output_target *-dir *-batch *-runs N *-thread M *-verbose *-uncondense")
		return
	else: #More options were given
		f = open(argv[2], "w")
		f.write("mean(T/F); filename; file size; fuzzy time (s); parsing time (s); parsing/fuzzy\n")
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
			verbose = True if "-verbose" in argv else False
			condense = False if "-uncondense" in argv else True
			print(f"Comparing performance on file {argv[1]} ({runs} runs)")
			stat_run(argv[1], argv[2], runs=runs, multi=multi, verbose=verbose, condense=condense)



if __name__ == '__main__':
	print("Running")
	main(sys.argv)