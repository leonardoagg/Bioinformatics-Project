import time
import ReassignedTools
import sys


def main(dataset_path, clusters_path, IsFasta, TotalReassignment, path_list):

    if TotalReassignment:
        print("Total reassignment has been chosen")
    else:
        print("Partial reassignment has been chosen")

    start = time.time()
    classifiers_result = ReassignedTools.load_multi_classifier_result(path_list)
    end = time.time()

    print("loading multi classifier:", end - start)

    dataset_lines = ReassignedTools.load_dataset(dataset_path, IsFasta)
    clusters_list = ReassignedTools.load_clusters_result(clusters_path)

    if IsFasta:
        print("Fasta file loaded")
    else:
        print("Fastq file loaded")

    start = time.time()
    dataset = ReassignedTools.build_dataset(dataset_lines, clusters_list, classifiers_result)
    end = time.time()

    print("Time for loading the dataset: ", end - start)

    start = time.time()
    inverted_index = ReassignedTools.get_generalized_inverted_index(clusters_list, dataset)
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
            if (count > max_count):
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

    outputfile = "multioutputfilespecies.res"

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
    inputStream = sys.argv

    if len(inputStream) < 6 or (inputStream[3] != 'True' and inputStream[3] != 'False') or (
            inputStream[4] != 'True' and inputStream[4] != 'False'):
        print("No correct parameters:")
        print("1: dataset_path")
        print("2: clusters_path")
        print("3: True/False to indicate if the file is fasta o fastq")
        print("4: True/False to indicate if execute total(True) or partial(False) reassignment")
        print("5 and successive: classifiers paths")
        exit()

    dataset_path = inputStream[1]
    clusters_path = inputStream[2]

    if inputStream[3] == 'True':
        IsFasta = True
    else:
        IsFasta = False

    if inputStream[4] == 'True':
        TotalReassignment = True
    else:
        TotalReassignment = False

    path_list = []
    count = 5
    while len(inputStream) > count:
        path_list.append(inputStream[count])
        count = count + 1

    main(dataset_path, clusters_path, IsFasta, TotalReassignment, path_list)
