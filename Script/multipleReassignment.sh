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
Clusters="../../datiperpython/all_250000_1+RC.fasta.a16.t20.txt"
ClassificationPath="../../datiperpython"
PythonProgramPath="../pythonProgram"


# -true if the dataset is .fasta / .fa
# -false if the dataset is .fq / .fastq
IsFasta="False"

# -true if you want to execute the total reassignment
# -false if you want to execute only the partial 
# reassignment 
TotalReassignemnt="True"

#choose if you want to execute the Zero version 
#of the program
Zero="False"

#choose the version of the program (look at the documentation)
#version 1 or 2
Version="1"

############################################################################

echo "Dataset selected: "$Dataset

NumClassifiers=$(ls $ClassificationPath/*.res | wc -l)

echo "There are "$NumClassifiers" classifiers"

PythonProgramName="ReassignedByClusterMultiple.py"

Classifiers=$(ls $ClassificationPath/*.res)

i=1
for Classifier in $(ls $ClassificationPath/*.res); do
	echo "Classifier "$i" : "$Classifier
	
   	i=$((i+1))
done

python $PythonProgramPath/$PythonProgramName $Dataset $Clusters $IsFasta $TotalReassignemnt $Zero $Version $Classifiers


