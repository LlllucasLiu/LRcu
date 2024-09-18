import numpy as np
import pandas as pd
import os
import argparse

def inputFile(file_a,file_b,out_path):
    dic_A = {}
    list_A = []
    list_name_A = []
    dic_B = {}
    list_B = []
    list_name_B = []
    with open(file_a, 'r') as f:
        for line in f:
            list = line.split("=")
            list_A.append(float(list[1]))
            list_name_A.append(int(list[0]))
        np_A = np.array(list_A)
        list_A = (np_A-np.min(np_A))/(np.max(np_A)-np.min(np_A))
    for i in range(0, len(list_name_A)):
        a = {list_name_A[i]: list_A[i]}
        dic_A.update(a)
    dic_A = sorted(dic_A.items(), key=lambda x: x[0])

    with open(file_b, 'r') as f:
        for line in f:
            list = line.split("=")
            list_B.append(float(list[1]))
            list_name_B.append(int(list[0]))
        np_B = np.array(list_B)
        list_B = (np_B-np.min(np_B))/(np.max(np_B)-np.min(np_B))
    for i in range(0, len(list_name_B)):
        a = {list_name_B[i]:list_B[i]}
        dic_B.update(a)
    dic_B = sorted(dic_B.items(), key=lambda x: x[0])
    df = pd.DataFrame(dic_B)
    df.columns = ['name',"file_a"]
    df2 = pd.DataFrame(dic_A)
    df2.columns = ['name', "file_b"]
    df=pd.merge(df,df2,on='name')
    out_path = os.path.join(out_path,os.path.basename(file_a)+os.path.basename(file_b)+".csv")
    df.to_csv(out_path, index=False)
    listA = []
    for item in dic_A:
        listA.append(item[1])
    listB = []  
    for item in dic_B:
        listB.append(item[1])
    return listA,listB

def kendall(a, b):
    L = len(a)
    count = 0
    for i in range(L - 1):
        for j in range(i + 1, L):
            count = count + np.sign(a[i] - a[j]) * np.sign(b[i] - b[j])
    kendall_tau = count / (L * (L - 1) / 2)

    return kendall_tau



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description = "This script is used to calculate the Kendall coefficients after normalization of two ranking files."
    parser.add_argument('--inputA', type=str, help="Please enter the path to the rank fileA.")
    parser.add_argument('--inputB', type=str, help="Please enter the path to the rank fileB.")
    parser.add_argument('--output', type=str, default=os.getcwd()+"/Kendall/", help="Please enter the directory for the output file. Default:./Kendall/")
    args = parser.parse_args()
    if not os.path.exists(args.output):
            os.makedirs(args.output)
    a, b = inputFile(args.inputA,args.inputB,args.output)
    f = open(os.path.join(args.output,os.path.basename(args.inputA)+os.path.basename(args.inputB)+".csv"), 'a')
    f.write("The Kendall is:"+str(kendall(a, b)))
    f.flush()
    f.close()