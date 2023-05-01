import os
import sys
import subprocess
from main import process_and_create_cfg_lts

def calculate_metrics(directory, output_file):
	versions = os.listdir(directory)
	if len(versions) != 2:
		print("Given directory did not contain two subdirectories, could not compare the files !")
	else:
		v1path = os.path.join(directory, versions[0])
		v2path = os.path.join(directory, versions[1])
		for file in os.listdir(v1path):
			fileV1 = os.path.join(v1path, file)
			fileV2 = os.path.join(v2path, file)
			sizeV1 = 0 
			sizeV1_no_com = 0
			sizeV2 = 0
			sizeV2_no_com = 0
			with open(fileV1) as f1:
				for l in f1:
					sizeV1+= 1
					if l[6] != "*":
						sizeV1_no_com += 1
			with open(fileV2) as f2:
				for l in f2:
					sizeV2+= 1
					if l[6] != "*":
						sizeV2_no_com += 1
			diff_output = int(subprocess.check_output("diff "+fileV1+" "+fileV2+" | wc -l", shell=True))
			try:
				g1, lts1 = process_and_create_cfg_lts(fileV1)
				g2, lts2 = process_and_create_cfg_lts(fileV2)
			except:
				with open(output_file, "a") as f:
					f.write(f"{file} ; {sizeV1} ; {sizeV2} ; {sizeV1_no_com} ; {sizeV2_no_com}; {diff_output}; ERROR; ERROR; ERROR; ERROR\n")
			with open(output_file, "a") as f:
				f.write(f"{file} ; {sizeV1} ; {sizeV2} ; {sizeV1_no_com} ; {sizeV2_no_com}; {diff_output}; {lts1.get_link_size()}; {lts2.get_link_size()}; {g1.get_link_size()}; {g2.get_link_size()}\n")



def main(argv):
	if len(argv) < 3:
		print("Usage: python static_metrics.py directory output_target")
		return
	else: #More options were given
		f = open(argv[2], "w")
		f.write("filename; file size V1; file size V2; file size V1 no comment; file size V2 no comment; diff line count;LTS size V1; LTS size V2; CFG size V1; CFG size V2\n")
		f.close()
		calculate_metrics(argv[1], argv[2])



if __name__ == '__main__':
	print("Running")
	main(sys.argv)