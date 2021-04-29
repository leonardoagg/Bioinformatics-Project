import time

def main():

#################################################################################################

	# INPUT DATA PATHS
	#dataset_path = "../Bio_Project/SRR184065/reads_datasets/SRR1804065_1.filtr.fq"
	dataset_path = "../Bio_Project/SmallDataset/reads_datasets/all_118309_1.fq"

	#clusters_path =  "../Bio_Project/1_upSingleOutput/1_up+RC.fasta.a16.t20.txt"
	#clusters_path =  "../Bio_Project/results/all_1/all_118309_1+RC.fasta.a16.t20.txt"
	#clusters_path =  "../Bio_Project/results/all_2/all_118309_2+RC.fasta.a16.t20.txt"
	clusters_path =  "../Bio_Project/results/paired/all_118309_1+RC.fasta.a16.t20.txt"
	#clusters_path =  "../Bio_Project/results/output1_up/1_up+RC.fasta.a16.t20.txt"

	# classifier_path = "../Bio_Project/SmallDataset/classifiers_results/strex_centrifuge_118309.res"
	classifier_path = "../Bio_Project/SmallDataset/classifiers_results/strex_kraken1_118309.res"

#################################################################################################

	#dataset_lines = load_dataset_fq(dataset_path)
	dataset_lines = load_dataset(dataset_path, False)
	clusters_list = load_clusters_result(clusters_path)
	classifier_results = load_classifier_result(classifier_path)

	###print ("Lenght of dataset_lines: ", len(dataset_lines))
	###print ("Length of classifier_results: ", len(classifier_results))

	if (len(dataset_lines) == len(clusters_list)):
		num_reads = len(dataset_lines)
		#print("ok")
	else:
		###print ("Error in input files!")
		exit()

	# we add 1 to the max found value because the indexes of clusters start from 0 up to the max value.
	num_clusters = max(clusters_list) + 1

	###print("number of clusters: ", num_clusters)
	###print("number of reads: ", num_reads)

	#print(classifier_results)

################################################################################################

	# I DON'T REMEMBER WHAT THIS PIECE OF CODE WAS SUPPOSE TO DO (I SHOULD READ IT AGAIN), HOWEVER I THINK IT SIMPLY CREATES A LIST OF PAIR (read_id, cluster_index).
	#rows, cols = (len(dataset_lines), 2) # two cols : one for read_id, one for the cluster index.
	#matrix = []
	#for i in range(rows):
	#	col = []
	#	col.append(dataset_lines[i])
	#	col.append(clusters_list[i])
		##for j in range(cols):
		##	col.append(0)
	#	matrix.append(col)

################################################################################################

	# INVERTED INDEX
	inverted_index = get_inverted_index(clusters_list, dataset_lines)
	###print("Inverted index len: ", len(inverted_index))
	#print(len(inverted_index[0]))
	#print("Cluster 28084 len: ", len(inverted_index[28084]))
	#print("Cluster 28084")
	#print(inverted_index[28084])

	#label_dict = reassignment(inverted_index[28084], classifier_results)
	#print("Label_dict len: ", len(label_dict))
	#for label, count in label_dict.items():
		#print(label, count)

	i = 0
	max_label_per_cluster_list = []
	max_label_list = []
	for cluster in inverted_index:
		label_dict = find_labels_frequency(cluster, classifier_results)
		max_label = ""
		max_count = 0
		for label, count in label_dict.items():
			#print(label, count)
			if (count > max_count):
				max_count = count
				max_label = label
		#print("CLUSTER: ", i, " MAX_LABEL: ", max_label, "MAX COUNT: ", max_count, "CLUSTER LENGTH: ", len(cluster))
		max_label_list.append(max_label)
		max_label_per_cluster_list.append([max_label, max_count, len(cluster)])
		i = i + 1

	###print("Max_label_per_cluster length: ", len(max_label_per_cluster_list))
	###print("Max_label_per_cluster: [max_label, max_count, len(cluster)]")
	#print(max_label_per_cluster_list)

	non_cl_rds = 0
	for triplet in max_label_per_cluster_list:
		#print(triplet)
		if triplet[0] == '0':
			#print(triplet)
			non_cl_rds = non_cl_rds + triplet[2]
	
	###print("number of non classidied reads with LiME_binning clusters: ", non_cl_rds)

#################################################################################################

	# REASSIGNMENT BASED ON MAJOR VOTE RULE
	# Take in input the inverted index, that is a list of [cluster_index, [set of reads]] pairs for cluster_index that goes from 0 up to num_clusters.
	# Take in input the value max_label for each cluster, so we will have a list of num_cluster + 1 values: [max_label_cl_0, max_label_cl_1, ..., max_label_cl_nume_cluster]
	# Return in output a list [read_id, label], where label is assigned to read_id dependig on the max_label value of the cluster the read belong to.
	# LET'S SEE IF I AM ABLE TO DO THIS!!

	reassigned_classification = reassignment(inverted_index, max_label_list) 

	###print("The value displayed below should be equal to: ", len(classifier_results))
	###for element in classifier_results:
		###print(element)
	###print("reassigned_classification length: ", len(reassigned_classification))
	###print("reassigned_classification ")
	for element in reassigned_classification:
		###print(element)
		print(element[0], end=' ')
		print(element[1])

#################################################################################################

	# NON CLASSIFIED READS
	non_classified_reads = find_non_classified_reads(dataset_lines, classifier_results)
	###print("number of non classified_reads: ", len(non_classified_reads))
	#print(non_classified_reads)
	#print(" ")

#################################################################################################

	# NON GROUPED READS
	#lonely_reads = find_lonely_reads(inverted_index)
	#print("number of non grouped reads: ", len(lonely_reads))
	#print(lonely_reads)

	#i = intersection(non_classified_reads, lonely_reads)
	#print(len(i))
	#print(i)

#################################################################################################

	# COMPLETE CLASSIFIER : IF THE INPUT CLASSIFIER DOESN'T SHOW UNASSIGNED READS, THEN WE COMPLETE IT BY ADDING THESE READS WITH LABEL EQUAL TO 0

""" # NOT EFFICIENT
	start = time.time()
	complete_classifier_result = find_labels(dataset_lines, classifier_results)
	end = time.time()
	print("start: ", start)
	print("end: ", end)
	print ("complete_classifier_result running time: ", end - start)

"""
	# MORE EFFICIENT
	#start = time.time()
	#complete_classifier_result_2 = find_labels_improved(dataset_lines, classifier_results)
	#end = time.time()
	#print("start: ", start)
	#print("end: ", end)
	#print ("complete_classifier_result_2 running time: ", end - start)

	#print(complete_classifier_result)

	#i = intersection(classifier_results, complete_classifier_result)

	#print("Length of intersection: ", len(i))
	#print("Intersection list")
	#print(i)

	#diff = Diff(classifier_results, complete_classifier_result)

	#print("Length of difference: ", len(diff))
	#print("Difference list")
	#print(diff)

	# PROBLEMATIC READ IN strex_centrifuge_118309.res CLASSIFIER OUTPUT, TO BE HANDLED AND CORRECTED
	# [['taxid_1042876.47195', '76759']]

#################################################################################################

# DEPRECATED FUNCTION

#def load_dataset_fq(path):
#
#	dataset = open(path, "r")
#	dataset_lines = []
#
#	index = 0
#	for line in dataset:
#		if (index%4==0):
#			read_id = line.split()[0]
#			dataset_lines.append(read_id[1: len(read_id)-2])
#		index = index + 1

#	dataset.close()

#	return dataset_lines

#################################################################################################

# If dataset is in fasta format then dataset_format parameter equals TRUE,
# if dataset is in fastq format then dataset_format equals FALSE.
def load_dataset(path, datset_format : bool):

	dataset = open(path, "r")
	dataset_lines = []

	if (datset_format):
		divisor = 2
	else:
		divisor = 4

	index = 0
	for line in dataset:
		if (index%divisor==0):
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



def find_labels(read_ids, classification_output):

	complete_classifier_result = []
	found : bool = False
	count = 0
	for i in range(0, len(read_ids)):
		for j in range(0, len(classification_output)):
			col = []
			if (read_ids[i] == classification_output[j][0]):
				complete_classifier_result.append(classification_output[j])
				found = True
				break
		if not found:
			count = count +1
			complete_classifier_result.append(read_ids[i], '0')

	print("count: ", count)
	print("length classification output: ", len(classification_output))
	print("length complete classification output: ", len(complete_classifier_result))

	return complete_classifier_result



	return

# This function takes in input a cluster (group of reads, each read is identified by its read_id) and the classification of reads performed by a classifier
# and return a dictionary composed by key-value pairs where the key is a label and value equals to the frequency of such label in the cluster provided in input
def find_labels_frequency(cluster, classification_output):

	label_dict = {}

	classification_output = insertion_sort(classification_output)

	for read in cluster:

		position = binary_search_list(classification_output, read)

		if (position == -1):
			print("Something went wrong :-(")
			break

		read_label = classification_output[position][1]
		# print(read_label)

		found : bool = False

		labels = list(label_dict)

		for label in list(label_dict):
			if (label == read_label):
				label_dict[read_label] = label_dict[read_label] + 1
				found = True
				break
		if not found:
			label_dict[read_label] = 1
	return label_dict


"""
		if (len(label_dict) == 0):
			label_dict[read_label] = 1
			print("A")
		else:
			labels = list(label_dict)
			for label in labels:
				if (read_label == label):
					label_dict[read_label] = label_dict[read_label] + 1
					found = True
					print("B")
					break
			label_dict[read_label] = 1
			print("C")

	return label_dict
"""


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
		###print("le read non classificate hanno label = 0")
		for i in range(0, len(classification_output)):
			if (classification_output[i][1] == '0'):
				non_classified_reads.append(classification_output[i][0])
	else:
		print("Error in input files!")

	return non_classified_reads


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


# Iterative Binary Search Function
# It returns index of x in given array arr if present,
# else returns -1
def binary_search(arr, x):
	low = 0
	high = len(arr) - 1
	mid = 0
	while low <= high:
		mid = (high + low) // 2
		# If x is greater, ignore left half
		if arr[mid] < x:
			low = mid + 1
		# If x is smaller, ignore right half
		elif arr[mid] > x:
			high = mid - 1
		# means x is present at mid
		else:
			return mid
	# If we reach here, then the element was not present
	return -1


def insertion_sort(arr):
        
    for i in range(len(arr)):
        cursor = arr[i]
        pos = i  
        while pos > 0 and arr[pos - 1] > cursor:
            # Swap the number down the list
            arr[pos] = arr[pos - 1]
            pos = pos - 1
        # Break and do the final swap
        arr[pos] = cursor
    return arr

# Python code t get difference of two lists
# Not using set()
def Diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif


# Iterative Binary Search Function
# It returns index of x in given array arr if present,
# else returns -1
def binary_search_list(arr, x):
	low = 0
	high = len(arr) - 1
	mid = 0
	while low <= high:
		mid = (high + low) // 2
		#print(arr[mid][0])
		# If x is greater, ignore left half
		if arr[mid][0] < x:
			low = mid + 1
		# If x is smaller, ignore right half
		elif arr[mid][0] > x:
			high = mid - 1
		# means x is present at mid
		else:
			return mid
	# If we reach here, then the element was not present
	return -1



def insertion_sort_list(arr):
        
    for i in range(len(arr)):
        cursor = arr[i][0]
        pos = i
        while pos > 0 and arr[pos - 1][0] > cursor:
            # Swap the number down the list
            arr[pos][0] = arr[pos - 1][0]
            pos = pos - 1
        # Break and do the final swap
        arr[pos][0] = cursor

    return arr


def find_labels_improved(read_ids, classification_output):

	complete_classifier_result = []
	found : bool = False
	count = 0

	classification_output = insertion_sort(classification_output)

	print("classification_output sorted")

	for i in range(0, len(read_ids)):
		position = binary_search_list(classification_output, str(read_ids[i]))
		if (position == -1):
			count = count + 1
			complete_classifier_result.append([read_ids[i], '0'])
		else:
			complete_classifier_result.append(classification_output[position])

	print("count: ", count)
	print("length classification output: ", len(classification_output))
	print("length complete classification output: ", len(complete_classifier_result))

	return complete_classifier_result


def reassignment(inverted_index, max_labels):

	reassigned_classification = []

	for i in range(0, len(inverted_index)):
		for j in range(0, len(inverted_index[i])):
			reassigned_classification.append([inverted_index[i][j], max_labels[i]])

	return reassigned_classification



if __name__ == "__main__":
	main()