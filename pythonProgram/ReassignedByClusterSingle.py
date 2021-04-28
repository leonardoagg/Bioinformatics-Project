import time
import ReassignedTools
import sys


def main(dataset_path, clusters_path, classifier_path, IsFasta, TotalReassignment):
    start = time.time()

    dataset_lines = ReassignedTools.load_dataset(dataset_path, IsFasta)
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
            # print(label, count)
            if count > max_count:
                max_count = count
                max_label = label
        # print("CLUSTER: ", i, " MAX_LABEL: ", max_label, "MAX COUNT: ", max_count, "CLUSTER LENGTH: ", len(cluster))
        max_label_list.append(max_label)
        max_label_per_cluster_list.append([max_label, max_count, len(cluster)])
        i = i + 1

    # Choose the type of reassignment
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
    dataset_path = inputStream[1]
    clusters_path = inputStream[2]
    classifier_path = inputStream[3]
    IsFasta = bool(inputStream[4])
    TotalReassignment = bool(inputStream[5])

    main(dataset_path, clusters_path, classifier_path, IsFasta, TotalReassignment)
