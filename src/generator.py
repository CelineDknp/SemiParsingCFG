import sys
import os
from main import process_file



if __name__ == '__main__':
	print("Running !", flush=True)
	main_dir = sys.argv[1]
	for dir in os.listdir(main_dir):
		output_dir = os.path.join(main_dir+"squishedResults", dir)
		print(f"Looking into {dir}", flush=True)
		count = 1
		all_files = os.listdir(os.path.join(main_dir, dir))
		for file in all_files:
			print(f"Found file: {file} ({count}/{len(all_files)})", flush=True)
			file_path = os.path.join(os.path.join(main_dir, dir), file)
			process_file(file_path, output_dir)
			count += 1
			print("Done !", flush=True)