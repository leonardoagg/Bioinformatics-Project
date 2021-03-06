import time
import ReassignmentTools
import sys


def main(dataset_path, clusters_path, IsFasta, TotalReassignment, Zero, Version, path_list):

    if TotalReassignment:
        print("Total reassignment has been chosen")
    else:
        print("Partial reassignment has been chosen")

    start = time.time()
    classifiers_result = ReassignmentTools.load_multi_classifier_result(path_list) # outputs of the multiple classifiers loading
    end = time.time()

    print("loading multi classifier:", end - start)

    dataset_lines = ReassignmentTools.load_dataset(dataset_path, IsFasta) # dataset loading
    clusters_list = ReassignmentTools.load_clusters_result(clusters_path) # binning output loading

    if IsFasta:
        print("Fasta file loaded")
    else:
        print("Fastq file loaded")

    # if version 1:
    # version 1 --> apply to classifiers_result the method label_assignment_generalized
    # to select for each read by choosing the most frequent label the outputs of the multiple classifiers 
    if Version == 1:
        start = time.time()
        classifiers_result = ReassignmentTools.label_assignment_generalized(classifiers_result)
        stop = time.time()
        print("Time for label selection to all the reads: ", stop - start)
    
    start = time.time()
    dataset = ReassignmentTools.build_dataset(dataset_lines, clusters_list, classifiers_result)
    end = time.time()

    print("Time for loading the dataset: ", end - start)

    # INVERTED INDEX
    # if version 2:
    # version 2 --> there is a list of labels for each read, for this reason
    # we apply the function get_generalized_inverted_index
    if Version == 2:
        start = time.time()
        inverted_index = ReassignmentTools.get_generalized_inverted_index(clusters_list, dataset)
        stop = time.time()

    # if version 1:
    # version 1 --> there is a single label for each read -> call the function get_inverted_index
    else:
        start = time.time()
        inverted_index = ReassignmentTools.get_inverted_index(clusters_list, dataset)
        stop = time.time()
    
    print("Inverted index created in time: ", stop - start)

    start = time.time()
    
    # MAX LABEL PER CLUSTER SEARCH
    max_label_per_cluster_list = []
    max_label_list = []

    # work on each cluster in order to define the right reassignment
    for cluster in inverted_index:
    
        # return a dictionary with {label: frequency} pairs that appear in the examinated cluster
        label_dict = ReassignmentTools.frequency_search(cluster)
    
        # if ZERO VERSION:
        if Zero:
            # return a pair [label, frequency], where label is the label with max frequency and frequency is max frequency
            max_label = ReassignmentTools.get_max_label_zero_version(label_dict) # label '0' is ignored
        
        else:
            # return a pair [label, frequency], where label is the label with max frequency and frequency is max frequency
            max_label = ReassignmentTools.get_max_label(label_dict)
    
        # append the label with max frequncy in the list of all max labels that is used in the reassignment step
        max_label_list.append(max_label[0])
    
        # append the triplet [max label, max frequency, number of total reads in the cluster]
        # (only for analysis purpose)
        max_label_per_cluster_list.append([max_label[0], max_label[1], len(cluster)]) 
        
    # REASSIGNMENT STEP
    # the reassignment version is specified in the input parameters
    if TotalReassignment:
        reassigned_classification = ReassignmentTools.total_reassignment(dataset, max_label_list)    
    else:
        # if Version 2 we have to assign a single label to each read before computing the partial reassignment  
        if Version == 2: 
            # we apply majority vote rule to select the label of each read among the labels assigned by each input classifier
            classifiers_result = ReassignmentTools.label_assignment_generalized(classifiers_result)
            # build the data structure needed by partial_reassignment function in input
            dataset = ReassignmentTools.build_dataset(dataset_lines, clusters_list, classifiers_result)
        # compute the partial reassignment
        reassigned_classification = ReassignmentTools.partial_reassignment(dataset, max_label_list)

    stop = time.time()

    print("Classes have been elaborated in: ", stop - start)

    # saving the result into a correct named file
    starting_point = 0
    end_point = 0

    for i in range(len(dataset_path)):
        if dataset_path[i] == '/':
            starting_point = i + 1

    outputfile = dataset_path[starting_point:len(dataset_path)]
	
    outputfile = outputfile + "_M"

    if TotalReassignment:
        outputfile = outputfile + "T"
    else:
        outputfile = outputfile + "P"

    if Zero:
        outputfile = outputfile + "Z"

    if Version == 1:
        outputfile = outputfile + ".V1.res"
    else:
        outputfile = outputfile + ".V2.res"

    f = open(outputfile, "w")

    for element in reassigned_classification:
        f.write(element[0])
        f.write("\t")
        f.write(str(element[1]))
        f.write("\n")
    f.close()

    print("File ", outputfile, " created.")

    print("Done")


if __name__ == "__main__":
    # control of the inputstream
    inputStream = sys.argv
    if len(inputStream) < 8\
            or (inputStream[3] != 'True' and inputStream[3] != 'False' and inputStream[3] != 'true' and inputStream[3] != 'false') \
            or (inputStream[4] != 'True' and inputStream[4] != 'False' and inputStream[4] != 'true' and inputStream[4] != 'false') \
            or (inputStream[5] != 'True' and inputStream[5] != 'False' and inputStream[5] != 'true' and inputStream[5] != 'false')\
            or (inputStream[6] != '1' and inputStream[6] != '2'):
        print("No correct parameters:")
        print("1: dataset_path")
        print("2: clusters_path")
        print("3: True/False to indicate if the file is fasta o fastq")
        print("4: True/False to indicate if execute total(True) or partial(False) reassignment")
        print("5: True/False for the execution of zero program version")
        print("6: Number of the program's version to execute (look at readme file)")
        print("7 and successive: classifiers paths")
        exit()

    dataset_path = inputStream[1]
    clusters_path = inputStream[2]

    if inputStream[3] == 'True' or inputStream[3] == 'true':
        IsFasta = True
    else:
        IsFasta = False

    if inputStream[4] == 'True' or inputStream[4] == 'true':
        TotalReassignment = True
    else:
        TotalReassignment = False

    if inputStream[5] == 'True' or inputStream[5] == 'true':
        Zero = True
    else:
        Zero = False
    
    if inputStream[6] == '1':
        Version= 1
    else:
        Version = 2
        
    path_list = []
    count = 7
    while len(inputStream) > count:
        path_list.append(inputStream[count])
        count = count + 1

    main(dataset_path, clusters_path, IsFasta, TotalReassignment, Zero, Version, path_list)
