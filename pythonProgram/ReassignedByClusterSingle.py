import time
import ReassignedTools
import sys


def main(dataset_path, clusters_path, IsFasta, TotalReassignment,classifier_path):
    start = time.time()

    if TotalReassignment:
        print("Total reassignment has been chosen")
    else:
        print("Partial reassignment has been chosen")

    dataset_lines = ReassignedTools.load_dataset(dataset_path, IsFasta)

    if IsFasta:
        print("Fasta file loaded")
    else:
        print("Fastq file loaded")

    clusters_list = ReassignedTools.load_clusters_result(clusters_path)
    classifier_results = ReassignedTools.load_classifier_result(classifier_path)

    # new Structure : id , classifier result , cluster

    dataset = ReassignedTools.build_dataset(dataset_lines, clusters_list, classifier_results)

    stop = time.time()

    print("Files loaded and datasets created in time: ", stop - start)

    if len(dataset_lines) != len(clusters_list):
        print("Error in input files!")
        exit()

    # INVERTED INDEX

    start = time.time()

    inverted_index = ReassignedTools.get_inverted_index(clusters_list, dataset)

    stop = time.time()

    print("Inverted index created in time: ", stop - start)

    start = time.time()
    i = 0
    max_label_per_cluster_list = []
    max_label_list = []
    for cluster in inverted_index:
        label_dict = ReassignedTools.frequency_search(cluster)
        max_label = ""
        max_count = 0
        for label, count in label_dict.items():
            if count > max_count:
                max_count = count
                max_label = label
        max_label_list.append(max_label)
        max_label_per_cluster_list.append([max_label, max_count, len(cluster)])
        i = i + 1

    if TotalReassignment:
        reassigned_classification = ReassignedTools.total_reassignment(dataset, max_label_list)
    else:
        reassigned_classification = ReassignedTools.partial_reassignment(dataset, max_label_list)
    stop = time.time()

    print("Classes have been elaborated in: ", stop - start)

    ReassignedTools.printResults(dataset_path, classifier_path, TotalReassignment, reassigned_classification)

    print("Done")


if __name__ == "__main__":
    inputStream = sys.argv
    if len(inputStream) < 6 or (inputStream[3] != 'True' and inputStream[3] != 'False') or (
            inputStream[4] != 'True' and inputStream[4] != 'False'):
        print("No correct parameters:")
        print("1: dataset_path")
        print("2: clusters_path")
        print("3: True/False to indicate if the file is fasta o fastq")
        print("4: True/False to indicate if execute total(True) or partial(False) reassignment")
        print("5: classifier path")
        exit()

    dataset_path = inputStream[1]
    clusters_path = inputStream[2]
    classifier_path = inputStream[5]

    if inputStream[3] == 'True':
        IsFasta = True
    else:
        IsFasta = False

    if inputStream[4] == 'True':
        TotalReassignment = True
    else:
        TotalReassignment = False

    main(dataset_path, clusters_path, IsFasta, TotalReassignment,classifier_path)
