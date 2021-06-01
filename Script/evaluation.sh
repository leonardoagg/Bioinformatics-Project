#!/bin/bash

set -e

time_root="/usr/bin"
temp_root="/ext/tesistad"
#Main directory
working_root="/home/leonardo/bioinfo/AlgoBio/cavattoni/AlgoBio/SimDataset"

#Directory with the evaluation materials
db_root="/home/leonardo/bioinfo/AlgoBio/Evaluation"

#Directory with all the .res files corresponding to the selected dataset
# IMPORTANT: this directory has to contains only files corresponding to $dataset_name
results_dir="$working_root/Results"

#Name of dataset to evaluate. 
dataset_name="SRR1804065"

#The name of Truth (.tsv)
truth_name=$dataset_name"_truth.tsv"

#choose between species and genus (remember to remove the opposite res file)
version="species"

if [ ! -d "$results_dir" ]
then
    mkdir -p $working_root/Results
fi

NumClassifiers=$(ls $results_dir/*.res | wc -l)

echo "There are "$NumClassifiers" classifiers"


echo "Evaluation at $version level"

outputfile="results_evaluation_$version.csv"

printf "Classifier\ttp\tfp\tfn\tok\tno\t(tp+fp+fn+ok+no)\tsens\tprec\tf1\tpearson\n" >> $outputfile

i=1

for Classifier in $(ls $results_dir/*.res); do
	printf "Classifier "$i" : "$Classifier"\n"
	
	Output=$($db_root/Utilities/evaluate_calls $db_root/Taxonomy/nodes.dmp $version $working_root/truth/$truth_name ${Classifier}) 
	filename="${Classifier##*/}"
        printf "$filename\t${Output}\n" >> $outputfile 
   	i=$((i+1))
done
