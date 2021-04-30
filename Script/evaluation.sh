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

#Name of dataset to evaluate. The name of Truth (truth_$dataset_name.tsv)
dataset_name="all_250000"

#choose between species and genus (remember to remove the opposite res file)
version="species"

if [ ! -d "$results_dir" ]
then
    mkdir -p $working_root/Results
fi


echo "Evaluation at $version level"

outputfile="results_evaluation_$version.csv"

echo "Classifier\ttp\tfp\tfn\tok\tno\t(tp+fp+fn+ok+no)\tsens\tprec\tf1\tpearson" >> $outputfile

i=1

for Classifier in $(ls $results_dir/*.res); do
	echo "Classifier "$i" : "$Classifier
	
	Output=$($db_root/Utilities/evaluate_calls $db_root/Taxonomy/nodes.dmp $version $working_root/truth/truth_$dataset_name.tsv ${Classifier}) 
	filename="${Classifier##*/}"
        echo "$filename\t${Output}" >> $outputfile 
   	i=$((i+1))
done
