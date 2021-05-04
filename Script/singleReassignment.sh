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
Clusters="../../datiperpython/all_250000_1+RC.fasta.a16.t25.txt"
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
Zero="false"

############################################################################


echo "Dataset selected: "$Dataset

NumClassifiers=$(ls $ClassificationPath/*.res | wc -l)

echo "There are "$NumClassifiers" classifiers"

i=1

#PythonProgramName="ReassignedByClusterSingle.py"
PythonProgramName="ReassignedByClusterSingle-Copy1.py"
for Classifier in $(ls $ClassificationPath/*.res); do
	echo "Classifier "$i" : "$Classifier

	python $PythonProgramPath/$PythonProgramName $Dataset $Clusters $IsFasta $TotalReassignemnt $Zero $Classifier
	
   	i=$((i+1))
done




