import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import pandas as pd
import os
import argparse

class CreateNet:
    def __init__(self):
        self.__nodes_num = 0
        self.__edges_num = 0
        self.__num_neighbors = 0
        self.__rewiring_p = 0
        self.__connect_p = 0
        self.__random_type = 0


    def get_init(self, num_nodes, num_neighbors, rewiring_p, num_edges, connect_p, random_type):
        self.__nodes_num = num_nodes
        self.__edges_num = num_edges
        self.__num_neighbors = num_neighbors
        self.__rewiring_p = rewiring_p
        self.__connect_p = connect_p
        self.__random_type = random_type

    def edge2matrix(self, edge_path, matrix_path):
        matrix = np.zeros((self.__nodes_num, self.__nodes_num))
        with open(edge_path, 'r') as f:
            for line in f:
                list1 = line.split(",")
                a = int(list1[0])
                b = int(list1[1].replace(r'\n', ''))
                matrix[a, b] = 1
                matrix[b, a] = 1
        for i in range(0, self.__nodes_num):
            matrix[i, i] = 1
        pd.DataFrame(matrix).to_csv(matrix_path)

    def create_ba(self, out_path):
        ba_network = nx.barabasi_albert_graph(self.__nodes_num, 1)
        a = list(ba_network.degree)
        degree_path = os.path.join(out_path, "ba_"+str(self.__nodes_num)+ "_degree.txt")
        with open(degree_path, 'w') as f:
            for item in a:
                f.write(str(item).replace('(', '').replace(')', '') + "\n")
        a = list(ba_network.edges)
        edge_path = os.path.join(out_path, "ba_"+str(self.__nodes_num)+ "_edge.txt")
        with open(edge_path, 'w') as f:
            for item in a:
                f.write(str(item).replace('(', '').replace(')', '') + "\n")
        draw_path = os.path.join(out_path, "ba_"+str(self.__nodes_num)+ "_network.pdf")
        with PdfPages(draw_path) as pdf:
            ps = nx.spring_layout(ba_network)
            nx.draw(ba_network, ps, with_labels=True, font_weight='bold')
            pdf.savefig()
            plt.close()
        matrix_path = os.path.join(out_path, "ba_"+str(self.__nodes_num)+ "_matrix.txt")
        self.edge2matrix(edge_path, matrix_path)

    def create_ws(self, out_path):
        ws_network = nx.watts_strogatz_graph(self.__nodes_num,self.__num_neighbors, self.__rewiring_p)
        a = list(ws_network.degree)
        degree_path = os.path.join(out_path, "ws_"+str(self.__nodes_num)+"_"+str(self.__num_neighbors)+"_"+str(self.__rewiring_p)+"_degree.txt")
        with open(degree_path, 'w') as f:
            for item in a:
                f.write(str(item).replace('(', '').replace(')', '') + "\n")
        a = list(ws_network.edges)
        edge_path = os.path.join(out_path, "ws_"+str(self.__nodes_num)+"_"+str(self.__num_neighbors)+"_"+str(self.__rewiring_p)+"_edge.txt")
        with open(edge_path, 'w') as f:
            for item in a:
                f.write(str(item).replace('(', '').replace(')', '') + "\n")
        draw_path = os.path.join(out_path, "ws_"+str(self.__nodes_num)+"_"+str(self.__num_neighbors)+"_"+str(self.__rewiring_p)+"_network.pdf")
        with PdfPages(draw_path) as pdf:
            ps = nx.circular_layout(ws_network)
            nx.draw(ws_network, ps, with_labels=True, font_weight='bold')
            pdf.savefig()
            plt.close()
        matrix_path = os.path.join(out_path,"ws_"+str(self.__nodes_num)+"_"+str(self.__num_neighbors)+"_"+str(self.__rewiring_p)+"_matrix.txt")
        self.edge2matrix(edge_path, matrix_path)

    def create_random(self,out_path):
        if self.__random_type == 1:
            network = nx.gnm_random_graph(self.__nodes_num, self.__edges_num)  # 根据连边数，确定随机网络
        if self.__random_type == 2:
            network = nx.gnp_random_graph(self.__nodes_num, self.__connect_p)  # 根据连边概率，确定随机网络
        a = list(network.degree)
        degree_path = os.path.join(out_path, "rd_"+str(self.__nodes_num)+ "_"+str(self.__edges_num)+"_"+str(self.__connect_p)+"_degree.txt")
        with open(degree_path, 'w') as f:
            for item in a:
                f.write(str(item).replace('(', '').replace(')', '') + "\n")
        a = list(network.edges)
        edge_path = os.path.join(out_path,"rd_"+str(self.__nodes_num)+ "_"+str(self.__edges_num)+"_"+str(self.__connect_p)+ "_edge.txt")
        with open(edge_path, 'w') as f:
            for item in a:
                f.write(str(item).replace('(', '').replace(')', '') + "\n")
        draw_path = os.path.join(out_path,"rd_"+str(self.__nodes_num)+ "_"+str(self.__edges_num)+"_"+str(self.__connect_p)+ "_network.pdf")
        with PdfPages(draw_path) as pdf:
            ps = nx.spring_layout(network)
            nx.draw(network, ps, with_labels=True, font_weight='bold')
            pdf.savefig()
            plt.close()
        matrix_path = os.path.join(out_path, "rd_"+str(self.__nodes_num)+ "_"+str(self.__edges_num)+"_"+str(self.__connect_p)+  "_matrix.txt")
        self.edge2matrix(edge_path, matrix_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description = "This script can generate multiple types of random networks, including scale-free network, small world networks and random networks"
    parser.add_argument('--node', type=int,
                        help="Please enter the number of nodes included in the network.")
    parser.add_argument('--type', type=int,
                        help="Please enter the type of network to generate.Scale-free network:1 Small-world networks:2 Random networks:3")
    parser.add_argument('--neighbor', type=int, default=0,
                        help="If generating a small world network, please enter the number of neighbors for the node.Default: 0")
    parser.add_argument('--rewiring', type=float, default=0,
                        help="If generating a small world network, please enter the reconnection probability.Default: 0")
    parser.add_argument('--random_type', type=int,default=0,
                        help="If generating a random network, please enter 1 based on the number of edges and 2 based on the connection probability.Default: 0")
    parser.add_argument('--edge', type=int, default=0,
                        help="If generating a random network based on the number of edges, please enter the number of edges. Default: 0")
    parser.add_argument('--connect', type=float, default=0,
                        help="If generating a random network based on the connection probability, please enter the probability. Default: 0")
    parser.add_argument('--output', type=str, default=os.getcwd() + "/createNetwork/",
                        help="Please enter the directory for the output file. Default:./createNetwork/")
    args = parser.parse_args()
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    network = CreateNet()
    network.get_init(args.node,args.neighbor,args.rewiring,args.edge,args.connect,args.random_type)
    if args.type==1:
        network.create_ba(args.output)
    if args.type==2:
        network.create_ws(args.output)
    if args.type==3:
        network.create_random(args.output)
