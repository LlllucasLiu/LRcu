import os
import argparse

def compile_lr_gpu():
    now_path = os.getcwd() 
    file_path = os.path.split(os.path.realpath(__file__))[0]
    os.system("cmake {} -B {}".format(file_path,os.path.join(file_path,"build")))
    os.chdir(os.path.join(file_path,"build"))
    os.system("make")

def get_parameter():
    parser = argparse.ArgumentParser()
    parser.description = 'This program can calculate the ranking of network nodes in the form of gene expression data or adjacency matrix through the weighted LeaderRank algorithm,and use GPU to accelerate.'
    parser.add_argument('--input', type=str, 
    help="Please enter the path to the input file.")
    parser.add_argument('--type', type=int, default=2,
    help="Please enter the type of the input file. 1 -- Adjacency matrix 2 -- Expression data. Default:2 ")
    parser.add_argument('--iteration', type=int, default=3,
    help="Please enter the type of the termination condition of iteration. 1 -- Custom Times and Difference 2 -- Times 3 -- Difference. Default:3 ")
    parser.add_argument('--times', type=int, default=100,
    help="If you need to control the number of iterations, please modify this option. Default:100")
    parser.add_argument('--diff', type=float, default=0.000001,
    help="If you need to control the difference between two iterations, please modify this option. Default:0.000001")
    parser.add_argument('--func', type=int, default=1,
    help="Whether it is necessary to process the correlation matrix.1 -- Do not process 2 -- Co decrease model 3 -- Separate model 4 -- Co increase model. Default:1")
    parser.add_argument('--coe', type=int, default=0,
    help="Whether it is necessary to output the weight matrix of the edges. 1 -- Yes 2 -- No. Default:0")
    parser.add_argument('--cut', type=float, default=0,
    help="Whether it is necessary to output the network cut according to threshold. If the input is not zero, set the threshold to change and output. Default:0")
    out_path = os.path.split(os.path.realpath(__file__))[0]
    out_path = os.path.dirname(out_path)
    parser.add_argument('--output', type=str, default=out_path,
    help="Please enter the path to the output file. Default:../LRgpu_data/")
    return parser.parse_args()


def run_lr_gpu(args,run_path):
    file_name = os.path.splitext(os.path.basename(args.input))[0]
    args.output = os.path.join(args.output,"LRgpu_data")
    if not os.path.exists(args.output):
            os.makedirs(args.output)
    out_path = os.path.join(args.output,file_name)
    os.system("{} {} {} {} {} {} {} {} {} {}".format(run_path,args.input,args.type,args.iteration,args.times,args.diff,args.func,args.coe,args.cut,out_path))


if __name__ == "__main__":
    args = get_parameter() 
    run_file = os.path.split(os.path.realpath(__file__))[0]
    run_file = os.path.join(run_file,"bin","LRCu")
    if not os.path.exists(run_file):
      compile_lr_gpu()
    run_lr_gpu(args,run_file)