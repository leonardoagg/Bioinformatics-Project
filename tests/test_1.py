def main():

	#dataset_path = "../Bio_Project/SRR184065/reads_datasets/SRR1804065_1.filtr.fq"
	dataset_path = "../Bio_Project/SmallDataset/reads_datasets/all_118309_1.fq"

	#clusters_path =  "../Bio_Project/1_upSingleOutput/1_up+RC.fasta.a16.t20.txt"
	clusters_path =  "../Bio_Project/results/all_1/all_118309_1+RC.fasta.a16.t20.txt"
	#clusters_path =  "../Bio_Project/results/all_2/all_118309_2+RC.fasta.a16.t20.txt"
	#clusters_path =  "../Bio_Project/results/paired/all_118309_1+RC.fasta.a16.t20.txt"
	#clusters_path =  "../Bio_Project/results/output1_up/1_up+RC.fasta.a16.t20.txt"

	classifier_path = "../Bio_Project/SmallDataset/classifiers_results/strex_centrifuge_118309.res"

	dataset_lines = load_dataset_fq(dataset_path)
	clusters_list = load_clusters_result(clusters_path)
	classifier_results = load_classifier_result(classifier_path)

	if (len(dataset_lines) == len(clusters_list)):
		num_reads = len(dataset_lines)
		print("ok")
	else:
		print ("Error in input files!")
		exit()

	num_clusters = max(clusters_list) + 1

	print("number of clusters: ", num_clusters)
	print("number of reads: ", num_reads)

	#print(classifier_results)

	#rows, cols = (len(dataset_lines), 2) # two cols : one for read_id, one for the cluster index.
	#matrix = []
	#for i in range(rows):
	#	col = []
	#	col.append(dataset_lines[i])
	#	col.append(clusters_list[i])
		##for j in range(cols):
		##	col.append(0)
	#	matrix.append(col)

	# DA SCOMMENTARE PER INVERTED INDEX
	inverted_index = get_inverted_index(clusters_list, dataset_lines)

	#print(len(inverted_index))
	#print(len(inverted_index[0]))
	#print(inverted_index[28084])

	non_classified_reads = find_non_classified_reads(dataset_lines, classifier_results)
	print("number of non classified_reads: ", len(non_classified_reads))
	print(non_classified_reads)
	print(" ")
	lonely_reads = find_lonely_reads(inverted_index)
	print("number of non grouped reads: ", len(lonely_reads))
	print(lonely_reads)

	i = intersection(non_classified_reads, lonely_reads)
	print(len(i))
	print(i)

def load_dataset_fq(path):

	dataset = open(path, "r")
	dataset_lines = []

	index = 0
	for line in dataset:
		if (index%4==0):
			read_id = line.split()[0]
			dataset_lines.append(read_id[1: len(read_id)-2])
		index = index + 1

	dataset.close()

	return dataset_lines


def load_clusters_result(path):

	clusters = open(path, "r")
	clusters_list = []

	for group in clusters:
		clusters_list.append(int(group))

	clusters.close()

	return clusters_list


def load_classifier_result(path):

	classification = open(path, 'r')
	classifier_results = []

	for line in classification:
		col = []
		for j in range(0, len(line.split())):
			col.append(line.split()[j])
		#read_id = line.split()[0]
		#class_id = line.split()[1]
		#col.append(read_id)
		#col.append(class_id)
		classifier_results.append(col)

	classification.close()

	return classifier_results 


def get_inverted_index(clusters, read_ids):

	inverted_index = []
	num_clusters = max(clusters) + 1
	num_reads = len(read_ids)

	for i in range(0, num_clusters):
		col = []
		for j in range(0, num_reads):
			if (clusters[j] == i):
				col.append(read_ids[j])
		inverted_index.append(col)

	return inverted_index



#def find_labels(read_ids, classification_output):
#	return

# This function takes in input a cluster (group of reads, each read is identified by its read_id) and the classification of reads performed by a classifiers
#def reassignment(cluster, classification_output):
#	return

def find_lonely_reads(clusters):

	lonely_reads = []

	for i in range(0, len(clusters)):
		if (len(clusters[i]) == 1):
			lonely_reads.append(clusters[i][0])

	return lonely_reads


def find_non_classified_reads(read_ids, classification_output):

	non_classified_reads = []

	if (len(read_ids) > len(classification_output)):
		print("le read non classificate non sono presenti nel file di output, DA IMPLEMENTARE")
	elif (len(read_ids) == len(classification_output)):
		print("le read non classificate hanno label = 0")
		for i in range(0, len(classification_output)):
			if (classification_output[i][1] == '0'):
				non_classified_reads.append(classification_output[i][0])
	else:
		print("Error in input files!")

	return non_classified_reads


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3



if __name__ == "__main__":
	main()