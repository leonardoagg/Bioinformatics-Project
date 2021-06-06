from random import seed
from random import randint


# two different ways to load the dataset in order to manage both fasta and fastq files
# it returns the list of reads' id
def load_dataset(path, datset_format: bool):
    dataset = open(path, "r")
    dataset_lines = []

    if (datset_format):
        divisor = 2
    else:
        divisor = 4

    index = 0
    for line in dataset:
        if index % divisor == 0:    
            read_id = line.split()[0]  
            if '/' in read_id:
                dataset_lines.append(read_id[1: read_id.index('/')]
            else:
                dataset_lines.append(read_id[1: len(read_id)])
        index = index + 1

    dataset.close()

    return dataset_lines
                                    
# it loads the multiple outputs of the classifiers for the multiple version
def load_multi_classifier_result(path_list):
    classifiers_result = {}

    num_classifiers = len(path_list)

    for i in range(0, num_classifiers):

        classification = open(path_list[i], 'r')

        for line in classification:
            col = []
            for j in range(0, len(line.split())):
                col.append(line.split()[j])

            if col[0] not in classifiers_result.keys():
                classifiers_result[col[0]] = []
                classifiers_result[col[0]].append(col[1])

            else:
                classifiers_result[col[0]].append(col[1])

        print("Classifier", i + 1, " of ", len(path_list), " loaded")
        classification.close()

    return classifiers_result                                    


# it scans the binning output and returns a list which contains the cluster index assigned to the corresponding read 
# (the i-th read of the input dataset is associated with the i-th line of the binning output)
def load_clusters_result(path):
    clusters = open(path, "r")
    clusters_list = []

    for group in clusters:
        clusters_list.append(int(group))

    clusters.close()

    return clusters_list


# it returns a dictionary where the key is the read id and the value is the corresponding class
# class got from classifier 
def load_classifier_result(path):
    classification = open(path, 'r')
    classifier_results = {}

    for line in classification:
        col = []
        for j in range(0, len(line.split())):
            col.append(line.split()[j])

        classifier_results[col[0]] = col[1]

    classification.close()

    return classifier_results


# this function manages the 3 main structures. 
# it returns a list where each element contains : [id, class, cluster]
# of course this list has the same length of the number of reads in the dataset
def build_dataset(dataset_ids, clusters, classifier):
    final_dataset = []
    for i in range(0, len(dataset_ids)):
        final_dataset.append([])
        if dataset_ids[i] in classifier:
            final_dataset[i].append(dataset_ids[i])
            final_dataset[i].append(classifier[dataset_ids[i]])
            final_dataset[i].append(clusters[i])
        else:
            final_dataset[i].append(dataset_ids[i])
            final_dataset[i].append('0')
            final_dataset[i].append(clusters[i])
    return final_dataset


# it returns a list with the same length of the number of clusters
# each element contains the list of all the classes which occur in the corresponding cluster
def get_inverted_index(clusters, dataset):
    num_clusters = max(clusters) + 1
    num_reads = len(dataset)
    inverted_index = []

    for i in range(0, num_clusters):
        inverted_index.append([])

    for i in range(0, num_reads):
        inverted_index[dataset[i][2]].append(dataset[i][1])

    return inverted_index

'''
# deprecated function
def find_labels(read_ids, classification_output):
    complete_classifier_result = []
    found: bool = False
    count = 0
    for i in range(0, len(read_ids)):
        for j in range(0, len(classification_output)):
            col = []
            if read_ids[i] == classification_output[j][0]:
                complete_classifier_result.append(classification_output[j])
                found = True
                break
        if not found:
            count = count + 1
            complete_classifier_result.append(read_ids[i], '0')

    print("count: ", count)
    print("length classification output: ", len(classification_output))
    print("length complete classification output: ", len(complete_classifier_result))

    return complete_classifier_result
'''

# given a cluster occurence [class1, class2,...,class1]
# it returns a dictionary --> (class, occurences)
def frequency_search(cluster):
    label_dict = {}

    for label in cluster:

        if label in list(label_dict):
            label_dict[label] = label_dict[label] + 1
        else:
            # if it does not exist, it's automatically created
            label_dict[label] = 1

    return label_dict


# it returns the total assignment with the max label
def total_reassignment(dataset, max_labels):
    reassigned_classification = []

    for i in range(0, len(dataset)):
        cluster_index = dataset[i][2]
        reassigned_classification.append([dataset[i][0], max_labels[cluster_index]])

    return reassigned_classification

# it return a partial reassignment (only unclassified ones)
def partial_reassignment(dataset, max_labels):
    reassigned_classification = []

    for i in range(0, len(dataset)):
        cluster_index = dataset[i][2]
        if dataset[i][1] == '0':
            reassigned_classification.append([dataset[i][0], max_labels[cluster_index]])
        else:
            reassigned_classification.append([dataset[i][0], dataset[i][1]])

    return reassigned_classification


# function used to store the result in a file
# used to manage the name in the right way
def printResults(dataset_path, classifier_path, TotalReassignment, reassigned_classification, Zero):
    starting_point = 0
    end_point = 0

    for i in range(len(classifier_path)):
        if classifier_path[i] == '/':
            starting_point = i + 1

    for i in range(len(classifier_path)):
        if classifier_path[len(classifier_path) - i - 1] == '.':
            end_point = len(classifier_path) - i - 2
            break

    outputfile = classifier_path[starting_point:end_point] + "_S"

    if TotalReassignment:
        outputfile = outputfile + "T"
    else:
        outputfile = outputfile + "P"

    if Zero:
        outputfile = outputfile + "Z.res"
    else:
        outputfile = outputfile + ".res"

    f = open(outputfile, "w")

    for element in reassigned_classification:
        f.write(element[0])
        f.write("\t")
        f.write(str(element[1]))
        f.write("\n")
    f.close()

    print("File ", outputfile, " created.")

                                     
# get_inverted_index for multiple version 2 variant
def get_generalized_inverted_index(clusters, dataset):
    num_clusters = max(clusters) + 1
    num_reads = len(dataset)
    inverted_index = []

    for i in range(0, num_clusters):
        inverted_index.append([])

    for i in range(0, num_reads):
        for j in range(0, len(dataset[i][1])):
            inverted_index[dataset[i][2]].append(dataset[i][1][j])

    return inverted_index


# It takes in input a dictionary that contains {label: frequency} pairs.
# Returns a pair {label: frequency} with maximal frequency.
# Ties broken randomly.
def get_max_label(label_dict):
    candidates = []  # list of max label candidates

    max_frequency = 0

    for label, frequency in label_dict.items():  # find max frequency

        if frequency > max_frequency:
            max_frequency = frequency

    for label, frequency in label_dict.items():  # find labels with frequency equals to max frequency

        if frequency == max_frequency:
            candidates.append(label)

    value = randint(0,
                    len(candidates) - 1)  # choose randomly the label with max frequency if there are multiple candidate labels

    max_label = candidates[value]

    return [max_label, max_frequency]
                                     

# It takes in input a dictionary that contains {label: frequency} pairs.
# Returns a pair {label: frequency} with maximal frequency.
# Ties broken randomly.
# BUT IF MAX LABEL IS EQUAL TO '0', THEN THE SECOND MOST FREQUENT LABEL IS SELECTED IF IT EXISTS
def get_max_label_zero_version(label_dict):
    candidates = []  # list of max label candidates

    max_frequency = 0
    max_label = ''

    # if only one item is contained in the label dict then just return the {label: frequency} pair as max label and correspondent max frequency
    if len(label_dict) == 1:
        # access the only item in the dict
        for label, frequency in label_dict.items():
            # set max label and max frequency
            max_label = label
            max_frequency = frequency

    else:
        for label, frequency in label_dict.items():  # find max frequency

            if frequency > max_frequency and label != '0':  # if the label is equal to zero then we ignore its frequency
                max_frequency = frequency

        for label, frequency in label_dict.items():  # find labels with frequency equals to max frequency different from zero

            if frequency == max_frequency and label != '0':
                candidates.append(label)

        value = randint(0,
                        len(candidates) - 1)  # choose randomly the label with max frequency if there are multiple candidate labels

        max_label = candidates[value]

    return [max_label, max_frequency]

                                     
# it applies majority vote rule to classifiers' outputs to select the label of each read
# used by multiple version                                   
def label_assignment_generalized(classifiers_result):
    seed(1)
    classifier_ensamble = {}

    for read in classifiers_result.keys():

        labels = classifiers_result[read]
        label_dict = frequency_search(labels)

        max_frequency = - 1

        for label in label_dict.keys():
            if (label_dict[label] >= max_frequency):
                max_frequency = label_dict[label]

        max_labels = []
        for label in label_dict.keys():
            if label_dict[label] == max_frequency:
                max_labels.append(label)

        if len(max_labels) == 1:
            classifier_ensamble[read] = max_labels[0]

        else:
            value = randint(0, len(max_labels) - 1)
            classifier_ensamble[read] = max_labels[value]

    return classifier_ensamble


'''
# SCORE VERSION

# it returns two list: one containing reads' ids and one containing the quality score for each read
def load_dataset(path, dataset_format : bool):

    dataset = open(path, "r")
    
    dataset_lines = [] # list to store ids of reads
    line_score = [] # list to store quality scores of reads if Fastq dataset format
    
    if (dataset_format):
        divisor = 2
        
    else:
        divisor = 4

    index = 0
    for line in dataset:
        
        if index % divisor == 0:
            
            read_id = line.split()[0]
            
            if '/' in read_id:
                dataset_lines.append(read_id[1: read_id.index('/')])
            
            else:
                dataset_lines.append(read_id[1: len(read_id)])
        
        if not dataset_format and index % divisor == 3:
            read_score = line.split()[0]
            line_score.append(read_score)
            
        index = index + 1

    dataset.close()
    
    if dataset_format:
        return dataset_lines 
    else:
        return (dataset_lines,line_score)
  
  
#score start from 0 to 93 but it's represented using ASCII characters starting from 33 to 126.
def computeScore(line_score):
    scores = []
    length = len(line_score[0])
    for line in(line_score):
        count = 0
        for char in(line):
            count += ord(char) - 33
        scores.append(count/length)
    return scores


def score_get_inverted_index(clusters, dataset, scores):
    num_clusters = max(clusters) + 1
    num_reads = len(dataset)
    inverted_index = []

    for i in range(0, num_clusters):
        inverted_index.append([])

    for i in range(0, num_reads):
        inverted_index[dataset[i][2]].append((dataset[i][1],scores[i]))

    return inverted_index


def score_search(cluster):
    label_dict = {}

    #pair = (label,score)
    for pair in cluster:

        if pair[0] in list(label_dict):
            label_dict[pair[0]] = label_dict[pair[0]] + pair[1] 
        else:
            # if it does not exist, it's automatically created
            label_dict[pair[0]] = pair[1]

    return label_dict

'''