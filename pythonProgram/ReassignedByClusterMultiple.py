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

    ## if VERSIONE 1:
    ## VERSIONE 1 --> APPLICO A classifiers_result IL METODO label_assignment_generalized,
    ## IN CUI VADO A SELEZIONARE UNA LABEL TRA QUELLE DEI VARI CLASSIFICATORI (SCELGO QUELLA PIU' FREQUENTE)
    ## start = time.time()
    ## clusters_list = ReassignedTools.label_assignment_generalized(classifiers_result)
    ## stop = time.time()
    ## print("Time for label assignment to all the reads: ", end - start)
    
    ## ENTRAMBE LE VERSIONI
    start = time.time()
    dataset = ReassignedTools.build_dataset(dataset_lines, clusters_list, classifiers_result)
    end = time.time()

    print("Time for loading the dataset: ", end - start)

    
    ## if VERSIONE 2:
    ## VERSIONE 2 --> HO UNA LISTA DI CLASSI PER OGNI READ, QUINDI
    ## APPLICO LA FUNZIONE get_generalized_inverted_index
    start = time.time()
    inverted_index = ReassignedTools.get_generalized_inverted_index(clusters_list, dataset)
    stop = time.time()

    ## if VERSIONE 1:
    ## VERSIONE 1 --> HO UNA LABEL PER OGNI READ, QUINDI
    ## APPLICO LA FUNZIONE get_inverted_index
    ## start = time.time()
    ## inverted_index = ReassignedTools.get_inverted_index(clusters_list, dataset)
    ## stop = time.time()
    
    print("Inverted index created in time: ", stop - start)

    start = time.time()
    #i = 0
    max_label_per_cluster_list = []
    max_label_list = []
    
    ## TOGLIERE DA QUI --------------------->
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
        #i = i + 1
    ## ----------------------------------> A QUI
    
    '''
    for cluster in inverted_index:
    
        # return a dictionary with {label: frequency} pairs that appear in the examinated cluster
        label_dict = frequency_search(cluster)
    
        ## if TRASH ZERO VERSION:
        # return a pair [label, frequency], where label is the label with max frequency and frequency is max frequency
        # max_label = get_max_label_zero_version(label_dict)
        
        ## else:
        # return a pair [label, frequency], where label is the label with max frequency and frequency is max frequency
        max_label = get_max_label(label_dict)
    
        # append the label with max frequncy in the list of all max labels that is used in the reassignment step
        max_label_list.append(max_label[0])
    
        # append the triplet [max label, max frequency, number of total reads in the cluster]
        max_label_per_cluster_list.append([max_label[0], max_label[1], len(cluster)])
    '''
    
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
