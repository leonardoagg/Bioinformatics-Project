import time
import ReassignmentTools
import sys


def main(dataset_path, clusters_path, IsFasta, TotalReassignment, Zero, classifier_path):
    start = time.time()

    if TotalReassignment:
        print("Total reassignment has been chosen")
    else:
        print("Partial reassignment has been chosen")

    dataset_lines = ReassignmentTools.load_dataset(dataset_path, IsFasta)

    if IsFasta:
        print("Fasta file loaded")
    else:
        print("Fastq file loaded")

    clusters_list = ReassignmentTools.load_clusters_result(clusters_path)
    classifier_results = ReassignmentTools.load_classifier_result(classifier_path)

    # new Structure : id , classifier result , cluster

    dataset = ReassignmentTools.build_dataset(dataset_lines, clusters_list, classifier_results)

    stop = time.time()

    print("Files loaded and datasets created in time: ", stop - start)

    if len(dataset_lines) != len(clusters_list):
        print("Error in input files!")
        exit()

    # INVERTED INDEX

    start = time.time()

    inverted_index = ReassignmentTools.score_get_inverted_index(clusters_list, dataset)

    stop = time.time()

    print("Inverted index created in time: ", stop - start)

    start = time.time()
    
    max_label_per_cluster_list = []
    max_label_list = []
    
    for cluster in inverted_index:
    
        # return a dictionary with {label: frequency} pairs that appear in the examinated cluster
        label_dict = ReassignmentTools.score_frequency_search(cluster)
    
        ##if ZERO VERSION:
        if Zero:
            # return a pair [label, frequency], where label is the label with max frequency and frequency is max frequency
            max_label = ReassignmentTools.get_max_label_zero_version(label_dict)
        
        else:
            # return a pair [label, frequency], where label is the label with max frequency and frequency is max frequency
            max_label = ReassignmentTools.get_max_label(label_dict)
    
        # append the label with max frequncy in the list of all max labels that is used in the reassignment step
        max_label_list.append(max_label[0])
    
        # append the triplet [max label, max frequency, number of total reads in the cluster]
        max_label_per_cluster_list.append([max_label[0], max_label[1], len(cluster)])
    

    if TotalReassignment:
        reassigned_classification = ReassignmentTools.total_reassignment(dataset, max_label_list)
    else:
        reassigned_classification = ReassignmentTools.partial_reassignment(dataset, max_label_list)
    stop = time.time()

    print("Classes have been elaborated in: ", stop - start)

    ReassignmentTools.printResults(dataset_path, classifier_path, TotalReassignment, reassigned_classification, Zero)

    print("Done")


if __name__ == "__main__":
    inputStream = sys.argv
    if len(inputStream) < 7 or \
            (inputStream[3] != 'True' and inputStream[3] != 'False' and inputStream[3] != 'true' and inputStream[3] != 'false')\
            or (inputStream[4] != 'True' and inputStream[4] != 'False' and inputStream[4] != 'true' and inputStream[4] != 'false') \
            or (inputStream[5] != 'True' and inputStream[5] != 'False' and inputStream[5] != 'true' and inputStream[5] != 'false'):
        print("No correct parameters:")
        print("1: dataset_path")
        print("2: clusters_path")
        print("3: True/False to indicate if the file is fasta o fastq")
        print("4: True/False to indicate if execute total(True) or partial(False) reassignment")
        print("5: True/False for the execution of zero program version")
        print("6: classifier path")
        exit()

    dataset_path = inputStream[1]
    clusters_path = inputStream[2]
    classifier_path = inputStream[6]

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

    main(dataset_path, clusters_path, IsFasta, TotalReassignment, Zero, classifier_path)
