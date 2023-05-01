from main import compare_and_return
import os
import sys

def calculate_metrics(directory, output_file):
	versions = os.listdir(directory)
	if len(versions) != 2:
		print("Given directory did not contain two subdirectories, could not compare the files !")
	else:
		v1path = os.path.join(directory, versions[0])
		v2path = os.path.join(directory, versions[1])
		with open(output_file, "a") as f:
			for file in os.listdir(v1path):
				fileV1 = os.path.join(v1path, file)
				fileV2 = os.path.join(v2path, file)
				sizeV1 = 0 
				sizeV2 = 0
				with open(fileV1) as f1:
					sizeV1 = len(f1.readlines())
				with open(fileV2) as f2:
					sizeV2 = len(f2.readlines())
				try:
					ltsV1, ltsV2, teq = compare_and_return(fileV1, fileV2)
					f.write(f"{file} ; {sizeV1} ; {sizeV2} ; {ltsV1.get_link_size()} ; {ltsV2.get_link_size()}; {teq.is_equivalent()};{len(teq.matched_transition_g1)} ; {len(teq.matched_transition_g2)} ; {ltsV1.get_matches()}; {ltsV2.get_matches()};  {ltsV1.get_unsure()}; {ltsV2.get_unsure()}\n")
				except:
					f.write(f"{file} ; {sizeV1} ; {sizeV2} ; ERROR; ERROR; ERROR; ERROR; ERROR; ERROR; ERROR\n")


def main(argv):
	if len(argv) < 3:
		print("Usage: python teq_metrics.py directory output_target")
		return
	else: #More options were given
		f = open(argv[2], "w")
		f.write("filename; file size V1; file size V2; LTS size V1; LTS size V2; Equivalent; Explored V1 ; Explored V2 ; matches V1; matches V2; skipped V1; skipped V2\n")
		f.close()
		calculate_metrics(argv[1], argv[2])



if __name__ == '__main__':
	print("Running")
	main(sys.argv)