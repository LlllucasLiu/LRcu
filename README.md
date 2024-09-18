# LRcu
LRCu: A high-performance parallel program for  identifying hub genes
#### 1.**Version of relevant software of test environment**

|     Name      | Version（linux） |        Version（windows）        |
| :-----------: | :--------------: | :------------------------------: |
|     cmake     |      3.13.4      |              3.26.3              |
|     cuda      |       10.2       |               10.2               |
| nvidia driver |    440.33.01     |              442.50              |
|    compile    |    g++(8.3.0)    | Visual Studio 2019、g++（9.2.0） |

#### 2.Python programming environment

|      Name       | Version |
| :-------------: | :-----: |
|     python      | 3.8.16  |
| matplotlib-base |  3.5.1  |
|    networkx     |  2.8.4  |
|      numpy      | 1.23.5  |
|     pandas      |  1.5.3  |

#### 4.The structure tree of this software package

```undefined
./LRcu/
└── LRCu1.0.0
    ├── calcKendall.py
    ├── calcNetwork.py
    ├── calcSIR.py
    ├── creatNetwork.py
    ├── LRcpu
    │   ├── code.cpp
    │   ├── operator.h
    │   ├── pearson.h
    │   ├── run_lr_cpu.py
    │   └── stringCut.h
    └── LRCu
        ├── CMakeLists.txt
        ├── run_lr_gpu.py
        └── src
            ├── main.cpp
            ├── operator.cu
            ├── operator.h
            └── strcut.h
```

* LRCu: This program can calculate the ranking of network nodes in the form of gene expression data or adjacency matrix through the weighted LeaderRank algorithm,and use GPU to accelerate.
* LRCpu: This program can calculate the ranking of network nodes in the form of gene expression data or adjacency matrix through the weighted LeaderRank algorithm, and only use CPU for calculation.
* calcKendall.py: This script is used to calculate the Kendall coefficients after normalization of two ranking files.
* calcNetwork.py: This script can calculate the basic topology parameters of the network, including: number of nodes, number of edges, network diameter, average cluster coefficient, average degree, and average shortest path. Eight network centrality can also be calculated, including: degree, closeness, betweenness, eigenvector, mnc, mcc, ec and rad. In addition, it can also generate network graphs and Degree distribution graphs
* calcSIR.py: This script can apply the SIR model to obtain the final node ranking.
* creatNetwork.py: This script can generate multiple types of random networks, including scale-free network, small worldnetworks and random networks

#### 5.Usage

#### 5.1 LRCu

We provide the script called `run_lr_gpu_win.py`​ and `run_lr_gpu_linux.py`​to complete the compilation and operation of the software.

```undefined
usage: run_lr_gpu.py [-h] [--input INPUT] [--type TYPE]
                     [--iteration ITERATION] [--times TIMES] [--diff DIFF]
                     [--func FUNC] [--output OUTPUT]

This program can calculate the ranking of network nodes in the form of gene expression 
data or adjacency matrix through the weighted LeaderRank algorithm,and use GPU to 
accelerate.

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         Please enter the path to the input file.
  --type TYPE           Please enter the type of the input file. 1 --
                        Adjacency matrix 2 -- Expression data. Default:2
  --iteration ITERATION
                        Please enter the type of the termination condition of
                        iteration. 1 -- Custom Times and Difference 2 -- Times
                        3 -- Difference. Default:3
  --times TIMES         If you need to control the number of iterations,
                        please modify this option. Default:100
  --diff DIFF           If you need to control the difference between two
                        iterations, please modify this option.
                        Default:0.000001
  --func FUNC           Whether it is necessary to process the correlation
                        matrix.1 -- Do not process 2 -- Co decrease model 3 --
                        Separate model 4 -- Co increase model. Default:1
  --coe COE             Whether it is necessary to output the weight matrix of
                        the edges. 1 -- Yes 2 -- No. Default:0
  --cut CUT             Whether it is necessary to output the network cut
                        according to threshold. If the input is not zero, set
                        the threshold to change and output. Default:0
  --cluster CLUSTER     Obtain local communities from a specified number of
                        top rankings. If necessary, please also set the cut.
                        Default:0
  --output OUTPUT       Please enter the path to the output file.
                        Default:../LRgpu_data/
```

If you do not want to use this script, you can compile it in the following way:

**Linux**  
1.Environment for configuring related software.  
2.Download the source file to the directory you want. `/home/liu/LRCu/`​  
3.Use the command to enter the directory of cmakelist,and compile LRCu with `cmake . -B ./build`​ ,enter the directory and use the command `make`​ to compile. After a successful compiling, LRCu can be seen in the directory `./bin/LRCu`​  
4.Add the file directory of LRCu to `~/.bashrc`​ `export PATH=/home/liu/LRCu/bin:$PATH`​, and use the commandsource `~/.bashrc`​ to activate the profile.  
5.run LRCu. `LRCu input.csv 2 3 100 0.000001 1 0 0 0 ./output.txt ​`​

**Windows**  
1.Environment for configuring related software.  
2.Download the source file to the directory you want. `D:\clash\LRCu1.0.0\LRCu`​  
3.Use the command to enter the directory of cmakelist,and compile LRCu with `cmake . -B ./build`​ ,and use the command `cmake --build ./build`​ to compile. After a successful compiling, LRCu can be seen in the directory `./bin/Debug/LRCu.exe`​  
5.run LRCu. `.\bin\Debug\LRCu.exe .\input_1000.csv 2 3 100 0.001 1 0 0 0 ./`​

Please note: Please enter all parameters even though you do not need to use them

‍

#### 5.2 LRCpu

We provide the script called `run_lr_cpu.py`​ to complete the compilation and operation of the software.

```undefined
usage: run_lr_cpu.py [-h] [--input INPUT] [--type TYPE]
                     [--iteration ITERATION] [--times TIMES] [--diff DIFF]
                     [--func FUNC] [--output OUTPUT]

This program can calculate the ranking of network nodes in the form of gene 
expression data or adjacency matrix through the weighted LeaderRank algorithm,
and only use CPU for calculation.

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         Please enter the path to the input file.
  --type TYPE           Please enter the type of the input file. 1 --
                        Adjacency matrix 2 -- Expression data. Default:2
  --iteration ITERATION
                        Please enter the type of the termination condition of
                        iteration. 1 -- Custom Times and Difference 2 -- Times
                        3 -- Difference. Default:3
  --times TIMES         If you need to control the number of iterations,
                        please modify this option. Default:100
  --diff DIFF           If you need to control the difference between two
                        iterations, please modify this option.
                        Default:0.000001
  --func FUNC           Whether it is necessary to process the correlation
                        matrix.1 -- Do not process 2 -- Co decrease model 3 --
                        Separate model 4 -- Co increase model. Default:1
  --coe COE             Whether it is necessary to output the weight matrix of
                        the edges. 1 -- Yes 2 -- No. Default:0
  --cut CUT             Whether it is necessary to output the network cut
                        according to threshold. If the input is not zero, set
                        the threshold to change and output. Default:0
  --cluster CLUSTER     Obtain local communities from a specified number of
                        top rankings. If necessary, please also set the cut.
                        Default:0
  --output OUTPUT       Please enter the path to the output file.
                        Default:../LRcpu_data/

```

If you do not want to use this script, you can compile it in the following way:

**Linux**  
1.Environment for configuring related software.  
2.Download the source file to the directory you want. `D:\clash\LRCu1.0.0\LRcpu`​  
3.Use the command to enter the directory of codes, and compile LRCu with `g++ code.cpp -o LRCpu,out`​ .  
4.run LRCu. `./LRcpu.out input.csv 2 3 100 0.000001 1 0 0 ./output.txt`​

**Windows**  
1.Environment for configuring related software.  
2.Download the source file to the directory you want. `/home/liu/LRCu/`​  
3.Use the command to enter the directory of codes, and compile LRCu with `g++ code.cpp -o LRCpu,out`​ .  
4.run LRCu. `./LRcpu.out input.csv 2 3 100 0.000001 1 0 0 ./output.txt`​

Please note: Please enter all parameters even though you do not need to use them

‍

#### 5.3 calcKendall.py

```undefined
usage: calcKendall.py [-h] [--inputA INPUTA] [--inputB INPUTB] [--output OUTPUT]

This script is used to calculate the Kendall coefficients after normalization of two ranking files.

optional arguments:
  -h, --help       show this help message and exit
  --inputA INPUTA  Please enter the path to the rank fileA.
  --inputB INPUTB  Please enter the path to the rank fileB.
  --output OUTPUT  Please enter the directory for the output file. Default:./Kendall/
```

#### 5.4 calcNetwork.py

```undefined
usage: calcNetwork.py [-h] [--input INPUT] [--picture PICTURE] [--attribution ATTRIBUTION]
                      [--centrality CENTRALITY] [--output OUTPUT]

This script can calculate the basic topology parameters of the network, including: number of nodes,
number of edges, network diameter, average cluster coefficient, average degree, and average shortest
path. Eight network centrality can also be calculated, including: degree, closeness, betweenness,
eigenvector, mnc, mcc, ec and rad. In addition, it can also generate network graphs and Degree
distribution graphs.

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         Please enter the path to the network file.
  --picture PICTURE     The network diagram and Degree distribution diagram will be generated. If you
                        want to turn off this function, please enter 0. Default: 1
  --attribution ATTRIBUTION
                        Network properties will be generated. If you want to turn off this feature,
                        please enter 0. Default: 1
  --centrality CENTRALITY
                        Network centrality will be generated. If you want to turn off this feature,
                        please enter 0. Default: 1
  --output OUTPUT       Please enter the directory for the output file. Default:./data/
```

#### 5.5 calcSIR.py

```undefined
usage: calcSIR.py [-h] [--input INPUT] [--gamma GAMMA] [--type TYPE] [--num NUM] [--output OUTPUT]

This script can apply the SIR model to obtain the final node ranking.

optional arguments:
  -h, --help       show this help message and exit
  --input INPUT    Please enter the path to the network file.
  --gamma GAMMA    Gamma parameters of SIR model. Default: 1
  --type TYPE      This parameter represents the type of network. If set to 1, it is an undirected
                   network, and if set to 2, it is a directed network. Default: 1
  --num NUM        This parameter represents the number of cycles in the SIR model. Default: 400
  --output OUTPUT  Please enter the directory for the output file. Default:./SIR/
```

#### 5.5 creatNetwork.py

```undefined
usage: creatNetwork.py [-h] [--node NODE] [--type TYPE] [--neighbor NEIGHBOR] [--rewiring REWIRING]
                       [--random_type RANDOM_TYPE] [--edge EDGE] [--connect CONNECT] [--output OUTPUT]

This script can generate multiple types of random networks, including scale-free network, small world
networks and random networks.

optional arguments:
  -h, --help            show this help message and exit
  --node NODE           Please enter the number of nodes included in the network.
  --type TYPE           Please enter the type of network to generate.Scale-free network:1 Small-world
                        networks:2 Random networks:3
  --neighbor NEIGHBOR   If generating a small world network, please enter the number of neighbors for
                        the node.Default: 0
  --rewiring REWIRING   If generating a small world network, please enter the reconnection
                        probability.Default: 0
  --random_type RANDOM_TYPE
                        If generating a random network, please enter 1 based on the number of edges and
                        2 based on the connection probability.Default: 0
  --edge EDGE           If generating a random network based on the number of edges, please enter the
                        number of edges. Default: 0
  --connect CONNECT     If generating a random network based on the connection probability, please enter
                        the probability. Default: 0
  --output OUTPUT       Please enter the directory for the output file. Default:./createNetwork/
```

‍

#### 6.Sample

#### 6.1 LRCu/LRCPu

<u>1.Sample of input</u>

1.1Adjacency matrix  
The first row and column are the names of the nodes, the rest are connections between nodes.

	,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15  
	1,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0  
	2,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0  
	3,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0  
	4,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0  
	5,1,0,0,1,1,1,0,1,0,0,0,0,0,0,0  
	6,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0  
	7,0,0,0,1,0,1,1,1,0,0,0,0,0,0,0  
	8,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0  
	9,0,0,1,0,0,0,0,1,1,1,0,1,1,0,0  
	10,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0  
	11,0,0,0,0,0,0,0,0,0,1,1,1,0,1,0  
	12,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1  
	13,0,0,0,0,0,0,0,0,1,0,0,1,1,0,1  
	14,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1  
	15,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1

1.2 Expression data  
The first row is the name of the node, and the rest is the obtained expression data,

	A,B,C,D,E,F,G,H,I,J  
	3.30105,1.85066,2.02519,4.47212,4.33654,7.11794,8.14456,2.45761,6.78099,5.69052  
	4.31783,1.8463,2.11336,5.26114,4.48297,8.42338,8.73852,3.54018,7.2457,6.11363  
	2.98749,2.14159,2.15384,4.45806,4.44503,6.24828,7.04447,2.02138,5.94896,6.49958  
	3.5481,1.83839,1.88753,5.72147,4.6213,6.79179,7.03643,2.38217,5.88869,5.04972  
	2.97383,2.37636,2.22671,5.18768,4.09481,6.96976,7.28209,1.83525,6.02336,4.9541  
	3.51183,1.80252,1.88364,4.73796,4.18046,6.20861,7.32149,1.79839,5.33305,5.83686  
	3.7338,1.8796,1.87758,5.15177,4.97488,6.39207,7.53039,1.97546,5.56711,6.36469  
	3.0558,2.1726,2.12081,5.59669,5.08431,6.28229,7.3642,2.16164,5.99548,6.36814  
	3.65471,1.80345,2.00478,4.71598,4.60058,6.42101,7.5093,2.09413,6.17371,5.16212  
	3.43433,1.82737,1.95566,5.15677,4.64041,5.88859,6.53288,2.02421,5.09121,5.77242  
	3.29431,1.84862,1.87844,5.17621,4.26306,6.11963,6.97762,1.76953,5.67645,5.33379  
	4.08833,1.81077,1.77065,4.46119,3.5042,6.71903,6.06804,1.66966,4.55219,4.94282  
	3.74363,1.85896,1.99058,4.4569,3.14414,5.71187,6.09579,1.60522,4.68492,5.18837  
	3.10381,1.71923,1.96344,5.44752,2.57226,7.09806,7.7557,2.90001,6.07892,5.31831  
	2.84823,1.76338,2.06948,5.064,4.38638,6.30277,7.62238,1.97735,6.1972,6.06222  
	4.05761,2.19248,2.2545,5.32474,5.62321,6.26306,6.83552,1.87527,5.22561,5.48593
	
	...

‍

<u>2.Sample of output</u>

2.1 LR Value

	I = 1.42418  
	G = 1.42404  
	F = 1.35382  
	H = 1.11365  
	D = 1.02921  
	E = 0.936206  
	C = 0.804893  
	B = 0.680489  
	J = 0.638708  
	A = 0.5948

2.2  coe Matirx 

,A,B,C,D,E,F,G,H,I,J  
A,1,0.0963213,2.72542e-05,0.0140918,0.0430247,0.282391,0.0950278,0.158223,0.0897797,0.204109  
B,0.0963213,1,0.424158,0.129355,0.285852,0.157206,0.112818,0.00288685,0.14411,0.0725324  
C,2.72542e-05,0.424158,1,0.250012,0.324944,0.231523,0.268875,0.0610025,0.24505,0.17259  
D,0.0140918,0.129355,0.250012,1,0.514133,0.393164,0.476561,0.564949,0.501143,0.0801207  
E,0.0430247,0.285852,0.324944,0.514133,1,0.249621,0.341763,0.327848,0.318342,0.166817  
F,0.282391,0.157206,0.231523,0.393164,0.249621,1,0.819836,0.68058,0.829543,0.0129403  
G,0.0950278,0.112818,0.268875,0.476561,0.341763,0.819836,1,0.66522,0.934273,0.261406  
H,0.158223,0.00288685,0.0610025,0.564949,0.327848,0.68058,0.66522,1,0.710572,0.0401101  
I,0.0897797,0.14411,0.24505,0.501143,0.318342,0.829543,0.934273,0.710572,1,0.197491  
J,0.204109,0.0725324,0.17259,0.0801207,0.166817,0.0129403,0.261406,0.0401101,0.197491,1

2.3 cut edge-edge

	F,G  
	F,I  
	G,I  
	H,I		

‍

2.4 cluser

	id1	id2	coe
	
	node1	node2	0.7834
	
	node1	node3	0.8334
	
	node2	node4	0.82332
	
	.....

‍

#### 6.2 calcKendall.py

<u>1.Sample of input</u>

	33=2.88392  
	0=2.73214  
	32=2.125  
	2=1.82143  
	1=1.66964  
	31=1.21429
	
	..

  

<u>2.Sample of output</u>

	name,file_a,file_b  
	0,0.9719182389937109,0.9375021103023106  
	1,0.5526100628930818,0.5000004117663046  
	2,0.853553459119497,0.562502419127039  
	3,0.46522012578616356,0.31250262501019127  
	4,0.1661635220125786,0.12500030882472837  
	5,0.19345911949685538,0.18750066912024485
	
	...

The Kendall is:0.6755793226381461

‍

#### 6.3 calcNetwork.py

<u>1.Sample of input</u>

	1,2  
	1,3  
	1,4  
	1,5  
	1,6  
	1,7
	
	..

<u>2.Sample of output</u>

2.1 result_centrality.txt

	deg_node	deg_val	col_node	col_val	bet_node	bet_val	eig_node	eig_val			mcc_node	mcc_val	mnc_node	mnc_val	rad_node	rad_val	ec_node	ec_val  
	1	29	1	0.5833333333333334	49	0.2296569891295954	1	0.3456386348035193	1	29	1	7338448	18	0.3333333333333333	1	5.396825396825397  
	3	27	3	0.5727272727272728	1	0.20089716941995484	3	0.3358560640869036	3	27	3	7338416	22	0.3333333333333333	3		5.365079365079365  
	7	22	25	0.5080645161290323	3	0.16427966506051503	7	0.2589137041021537	7	20	7	3709596	24	0.3333333333333333	25	5.142857142857143
	
	....

2.2 result_attribution.txt

	Total nodes:64  
	Total edges:243  
	Average degree:7.593750  
	Clustering coefficient:0.622325  
	Network diameter:6  
	Average shortest path length:2.690972

2.3 network.pdf

	network diagram

2.4 distribution.pdf

	Probability distribution diagram of node degree

#### 6.4 calcSIR.py

<u>1.Sample of input</u>	

	1,2  
	1,3  
	1,4  
	1,5  
	1,6  
	1,7
	
	..

<u>2.Sample of output</u>

	33=36.096  
	0=35.203  
	32=31.441  
	2=31.439  
	8=22.549  
	1=21.869  
	13=21.533  
	3=19.09
	
	...

‍

#### 6.4 creatNetwork.py

<u>1.Sample of input</u>

	`python creatNetwork.py --node 10 --type 1`​

<u>2.Sample of output</u>

2.1 ba_10_degree.txt

	0, 2  
	1, 7  
	2, 1  
	3, 2  
	4, 1  
	5, 1  
	6, 1  
	7, 1  
	8, 1  
	9, 1
	
	...

2.2 ba_10_edge.txt

	0, 1  
	0, 9  
	1, 2  
	1, 3  
	1, 4  
	1, 5  
	1, 6  
	1, 7  
	3, 8
	
	...

2.3 ba_10_matrix.txt

	,0,1,2,3,4,5,6,7,8,9  
	0,1.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0  
	1,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0  
	2,0.0,1.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0  
	3,0.0,1.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0  
	4,0.0,1.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0  
	5,0.0,1.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0  
	6,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0  
	7,0.0,1.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0  
	8,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0  
	9,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0

2.4 ba_10_network.pdf

	network diagram

‍
