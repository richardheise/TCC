The project consists of 5 files : 
	i)  main.m
	ii)NetSheild.m 
	iii) Walk6_Algorithm.m
	vi)  Walk8_Algorithm.m
	v) greedyPlacement.m
Two folders are there 'Datasets' which contains the 
input graphs in the form of edge list and the resulting eigen drop percentages
are output in 'ResultFiles' folder.

Datasets folder contains the input graphs.The edge list file in Datasets
 has the following format:
node count
edge count
edge list(src dest)
 .
 .
 .

The output files in ResultFiles folder are of .csv format with name 
[graphName]_[hashCount]_[clusterCount]_[deletionCount].csv



### Running the code ### 

main.m is the main file which executes the code. You can change the controlling
variables like deletion count of nodes, number of clusters to be formed etc in main.m.
In addition to this, the graph name should also be given in main.m. 


NetSheild.m immunizes nodes on the technique based on NetSheild algorithm.

Walk6_Algorithm.m and Walk8_Algorithm.m immunize nodes based on closed walks
of length 6 and length 8 respectively.(our techniques)

greedyPlacement.m is a function to select nodes for immunization that are far apart to
maximize the effect of immunization.