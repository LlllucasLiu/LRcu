import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import math
import os
import argparse


class Centrality:
    def __init__(self):
        self.__G = nx.Graph()
        self.__num_nodes = 0
        self.__num_edges = 0
        self.__average_degree = 0
        self.__clustering_coefficient = 0
        self.__diameter = 0
        self.__avg_shortest_path_len = 0
        self.__degree_centrality = []
        self.__closeness_centrality = []
        self.__betweenness_centrality = []
        self.__eigenvector_centrality = []
        self.__mnc = []
        self.__mcc = []
        self.__ec = []
        self.__rad = []
        self.__input_name = ""

    def input_network(self, path):
        with open(path, 'r') as f:
            for line in f:
                temp_list = line.split(",")
                a = int(temp_list[0])
                b = int(temp_list[1].replace(r'\n', ''))
                self.__G.add_edge(a, b)
        self.__num_nodes = self.__G.number_of_nodes()
        self.__input_name = os.path.basename(path)

    def connected_component_subgraphs(self):
        for c in nx.connected_components(self.__G):
            yield self.__G.subgraph(c)

    def calc_mnc(self):
        result_mnc = {}
        for item in self.__G.adjacency():  # 遍历节点 得到的[0]为节点
            neighbor = self.__G[item[0]]
            induce_component = nx.induced_subgraph(self.__G, neighbor)
            largest = max(nx.connected_components(induce_component), key=len)
            largest_connected_subgraph = induce_component.subgraph(largest)
            result_mnc[item[0]] = largest_connected_subgraph.number_of_nodes()
        self.__mnc = sorted(result_mnc.items(), key=lambda x: x[1], reverse=True)

    def calc_mcc(self):
        result_mcc = {}
        for item in self.__G.nodes():
            mcc = 0
            result_mcc[item] = self.__G.degree(item)
            for c in nx.find_cliques(self.__G):
                if item in c:
                    mcc += math.factorial(len(c) - 1)
            if (mcc):
                result_mcc[item] = mcc
        self.__mcc = sorted(result_mcc.items(), key=lambda x: x[1], reverse=True)

    def calc_ec(self):
        result_ec = {}
        for item in self.__G.nodes():
            c_graph = nx.Graph()
            for g in self.connected_component_subgraphs():
                if item in g:
                    c_graph = g
            a = len(nx.node_connected_component(c_graph, item))
            b = a / self.__num_nodes
            c = b * (1 / nx.eccentricity(c_graph, v=item))
            result_ec[item] = c
        self.__ec = sorted(result_ec.items(), key=lambda x: x[1], reverse=True)

    def calc_rad(self):
        def return_sum(dict_tmp):
            sum_tmp = 0
            dq = dict_tmp.values()
            for i in dq:
                sum_tmp += i
            return sum_tmp
        result_rad = {}
        for item in self.__G.nodes():
            c_graph = nx.Graph()
            for g in self.connected_component_subgraphs():
                if item in g:
                    c_graph = g
            a = len(nx.node_connected_component(c_graph, item)) / self.__num_nodes
            num_nodes_sub = c_graph.number_of_nodes()
            b = num_nodes_sub * (nx.diameter(c_graph) + 1) - return_sum(
                nx.single_source_shortest_path_length(c_graph, item))
            c = b / (num_nodes_sub - 1)
            result_rad[item] = a * c
        self.__rad = sorted(result_rad.items(), key=lambda x: x[1], reverse=True)

    def calc_attribute(self):
        self.__num_edges = self.__G.number_of_edges()
        deg_tmp = dict(nx.degree(self.__G))
        self.__degree_centrality = sorted(deg_tmp.items(), key=lambda x: x[1], reverse=True)  # Degree Centrality 度中心度
        self.__average_degree = np.mean(list(deg_tmp.values()))
        self.__clustering_coefficient = nx.average_clustering(self.__G)
        self.__diameter = nx.diameter(self.__G)
        self.__avg_shortest_path_len = nx.average_shortest_path_length(self.__G)

    def calc_centrality(self):
        if self.__average_degree == 0:
            deg_tmp = dict(nx.degree(self.__G))
            self.__degree_centrality = sorted(deg_tmp.items(), key=lambda x: x[1], reverse=True)
        col_tmp = dict(nx.closeness_centrality(self.__G))
        bet_tmp = dict(nx.betweenness_centrality(self.__G))
        eig_tmp = dict(nx.eigenvector_centrality(self.__G))
        self.__closeness_centrality = sorted(col_tmp.items(), key=lambda x: x[1], reverse=True)
        self.__betweenness_centrality = sorted(bet_tmp.items(), key=lambda x: x[1], reverse=True)
        self.__eigenvector_centrality = sorted(eig_tmp.items(), key=lambda x: x[1], reverse=True)
        self.calc_mcc()
        self.calc_mnc()
        self.calc_rad()
        self.calc_ec()

    def output_centrality(self,out_path):
        save_path_dir = os.path.join(out_path,self.__input_name)
        if not os.path.exists(save_path_dir):
            os.makedirs(save_path_dir)
        w = open(os.path.join(save_path_dir,"result_centrality.txt"), "w")
        w.write("deg_node\tdeg_val\tcol_node\tcol_val\tbet_node\tbet_val\teig_node\teig_val\tmcc_node\tmcc_val\t"
                "mnc_node\tmnc_val\trad_node\trad_val\tec_node\tec_val")
        w.write("\n")
        for i in range(0,self.__num_nodes):
            w.write(str(self.__degree_centrality[i][0]))
            w.write("\t")
            w.write(str(self.__degree_centrality[i][1]))
            w.write("\t")
            w.write(str(self.__closeness_centrality[i][0]))
            w.write("\t")
            w.write(str(self.__closeness_centrality[i][1]))
            w.write("\t")
            w.write(str(self.__betweenness_centrality[i][0]))
            w.write("\t")
            w.write(str(self.__betweenness_centrality[i][1]))
            w.write("\t")
            w.write(str(self.__eigenvector_centrality[i][0]))
            w.write("\t")
            w.write(str(self.__eigenvector_centrality[i][1]))
            w.write("\t")
            w.write(str(self.__mnc[i][0]))
            w.write("\t")
            w.write(str(self.__mnc[i][1]))
            w.write("\t")
            w.write(str(self.__mcc[i][0]))
            w.write("\t")
            w.write(str(self.__mcc[i][1]))
            w.write("\t")
            w.write(str(self.__ec[i][0]))
            w.write("\t")
            w.write(str(self.__ec[i][1]))
            w.write("\t")
            w.write(str(self.__rad[i][0]))
            w.write("\t")
            w.write(str(self.__rad[i][1]))
            w.write("\n")
        w.close()

    def draw_pic(self,out_path):
        def draw_network(G, path):
            color_list = ['red', 'gray']
            pos = nx.spring_layout(G)
            with PdfPages(os.path.join(path,"network.pdf")) as pdf:
                nx.draw(G, pos=pos, node_size=300, node_color=color_list[0],
                        edge_color=color_list[1], with_labels=True)
                pdf.savefig()
                plt.close()

        def draw_distribution(G, path):
            d = dict(nx.degree(G))
            x = list(range(max(d.values()) + 1))
            y = [i / sum(nx.degree_histogram(G)) for i in nx.degree_histogram(G)]
            with PdfPages(os.path.join(path,"distribution.pdf")) as pdf:
                plt.bar(x, y, width=0.5, color="blue")
                plt.xlabel("$k$")
                plt.ylabel("$p_k$")
                pdf.savefig()
                plt.close()
        out_path = os.path.join(out_path,self.__input_name)
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        draw_network(self.__G, out_path)
        print()
        draw_distribution(self.__G, out_path)

    def output_attribution(self,out_path):
        out_path = os.path.join(out_path,self.__input_name)
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        w = open(os.path.join(out_path,"result_attribution.txt"), "w")
        w.write("Total nodes:%d\n" % self.__num_nodes)
        w.write("Total edges:%d\n" % self.__num_edges)
        w.write("Average degree:%f\n" % self.__average_degree)
        w.write("Clustering coefficient:%f\n" % self.__clustering_coefficient)
        w.write("Network diameter:%d\n" % self.__diameter)
        w.write("Average shortest path length:%f\n" % self.__avg_shortest_path_len)
        w.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description = 'This script can calculate the basic topology parameters of the network, \
    including: number of nodes, number of edges, network diameter, average cluster coefficient, average degree, and average shortest path. \
    Eight network centrality can also be calculated, including: degree, closeness, betweenness, eigenvector, mnc, mcc, ec and rad.\
    In addition, it can also generate network graphs and Degree distribution graphs'
    parser.add_argument('--input', type=str, help="Please enter the path to the network file.")
    parser.add_argument('--picture', type=int, default=1, help="The network diagram and Degree distribution diagram will be generated. If you want to turn off this function, please enter 0. Default: 1")
    parser.add_argument('--attribution', type=int, default=1, help="Network properties will be generated. If you want to turn off this feature, please enter 0. Default: 1")
    parser.add_argument('--centrality', type=int, default=1, help="Network centrality will be generated. If you want to turn off this feature, please enter 0. Default: 1")
    parser.add_argument('--output', type=str, default=os.getcwd()+"/data/", help="Please enter the directory for the output file. Default:./data/")
    args = parser.parse_args()
    if not os.path.exists(args.output):
            os.makedirs(args.output)
    G = Centrality()
    G.input_network(args.input)
    if args.picture:
        G.draw_pic(args.output)
    if args.attribution:
        G.calc_attribute()
        G.output_attribution(args.output)
    if args.centrality:
        G.calc_centrality()
        G.output_centrality(args.output)

