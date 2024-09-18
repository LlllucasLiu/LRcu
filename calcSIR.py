import random
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import argparse
import sys,time,os

class SIR:
    def __init__(self):
        self.__G = nx.Graph()
        self.__Index = []
    
    def update_node_status(self,beta,gamma):
        for node in self.__G:
            if self.__G.nodes[node]['status'] == 'I':
                neighbors = list(self.__G.neighbors(node))
                for neighbor in neighbors:
                    if(self.__G.nodes[neighbor]['status'] == 'R'):
                        continue
                    p = random.random()
                    if p < beta:
                        self.__G.nodes[neighbor]['status'] = 'I'
                p2 = random.random()
                if p2 < gamma:
                    self.__G.nodes[node]['status'] = 'R'
    
    def count_node(self,r_num):
        i_num = 0
        for node in self.__G:
            if self.__G.nodes[node]['status'] == 'I':
                i_num += 1
            elif self.__G.nodes[node]['status'] == 'R':
                r_num += 1
        return i_num, r_num
    
    def ini(self):
        for node in self.__G:
            self.__G.nodes[node]['status'] = 'S' 
    
    def sir_network(self,beta,gamma):
        svlist = []
        for index in self.__G.nodes():
            self.ini()
            r = 0
            self.__G.nodes[index]['status'] = 'I' 
            i = 1
            while i != 0:
                self.update_node_status(beta, gamma)
                i, r = self.count_node(r)
            svlist.append(r)
        return np.array(svlist)
    
    def input_network(self,flag,input_path):
        if flag==1:
            self.__G = nx.Graph() 
        else:
            self.__G = nx.DiGraph()  
        with open(input_path, 'r') as f:
            for line in f:
                list = line.split(",")
                a = int(list[0]) 
                b = int(list[1].replace(r'\n', '')) 
                self.__G.add_edge(a, b)
        for index in self.__G.nodes():
            self.__Index.append(index)
        

    def run_output_network(self,output_path,num_cir,gamma):
        d = dict(nx.degree(self.__G))
        k = sum(d.values())/len(self.__G.nodes)
        a = list(d.values())
        a = np.array(a)
        k2 = sum(a ** 2)/len(self.__G.nodes)
        beta = k/(k2-k)
        a = self.sir_network(beta, gamma)
        for j in range(2, num_cir):
            a = a + self.sir_network(beta, gamma)
            print(f"Current progress:{(j/num_cir)*100}%", end="\n")
            sys.stdout.flush()
            time.sleep(0.05)
        print(f"Current progress:100%", end="\n")
        a = a / num_cir
        dict1 = dict(zip(self.__Index,a.tolist()))
        dict1 = sorted(dict1.items(), key=lambda item: item[1], reverse=True)
        with open(output_path, "w+") as f:
            for key, value in dict1:
                f.write(str(key) + '=' + str(value) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description = "This script can apply the SIR model to obtain the final node ranking."
    parser.add_argument('--input', type=str, help="Please enter the path to the network file.")
    parser.add_argument('--gamma', type=float, default=1, help="Gamma parameters of SIR model. Default: 1")
    parser.add_argument('--type', type=int, default=1, help="This parameter represents the type of network. If set to 1, it is an undirected network, and if set to 2, it is a directed network. Default: 1")
    parser.add_argument('--num', type=int, default=400, help="This parameter represents the number of cycles in the SIR model. Default: 400")
    parser.add_argument('--output', type=str, default=os.getcwd()+"/SIR/", help="Please enter the directory for the output file. Default:./SIR/")
    args = parser.parse_args()
    if not os.path.exists(args.output):
            os.makedirs(args.output)
    G = SIR()
    G.input_network(args.type,args.input)
    out_path = os.path.join(args.output,os.path.basename(args.input)+".result")
    G.run_output_network(out_path,args.num,args.gamma)
