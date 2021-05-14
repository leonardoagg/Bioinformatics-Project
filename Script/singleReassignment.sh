#!/bin/bash

############################################################################
############################################################################
#Script for executing the signle reassignment for all 
# classification files
############################################################################
############################################################################


############################################################################

            ######## CHANGE THESE VALUES WITH YOURS #########

Dataset="../../datiperpython/all_250000_2.fq"
Clusters="../../datiperpython/all_250000_1+RC.fasta.a40.t50.txt"
ClassificationPath="../../datiperpython"
PythonProgramPath="../pythonProgram"

# -true if the dataset is .fasta / .fa
# -false if the dataset is .fq / .fastq
IsFasta="False"

# -true if you want to execute the total reassignment
# -false if you want to execute only the partial 
# reassignment 
TotalReassignemnt="true"

#choose if you want to execute the Zero version 
#of the program
Zero="true"

#debug mode: to execute each type
Debug="true"
############################################################################


echo "Dataset selected: "$Dataset

NumClassifiers=$(ls $ClassificationPath/*.res | wc -l)

echo "There are "$NumClassifiers" classifiers"

i=1

PythonProgramName="ReassignedByClusterSingle.py"

for Classifier in $(ls $ClassificationPath/*.res); do
	echo "Classifier "$i" : "$Classifier
	if [ "$Debug" = "false" ]; then
		python $PythonProgramPath/$PythonProgramName $Dataset $Clusters $IsFasta $TotalReassignemnt $Zero $Classifier
	else
		python $PythonProgramPath/$PythonProgramName $Dataset $Clusters $IsFasta True True $Classifier
		python $PythonProgramPath/$PythonProgramName $Dataset $Clusters $IsFasta True False $Classifier
		python $PythonProgramPath/$PythonProgramName $Dataset $Clusters $IsFasta False True $Classifier
		python $PythonProgramPath/$PythonProgramName $Dataset $Clusters $IsFasta False False $Classifier
	fi
	
   	i=$((i+1))
done




