#include "cuda_runtime.h"
#include "device_launch_parameters.h"
#include <thrust/transform_reduce.h>
#include <thrust/functional.h>
#include <thrust/device_vector.h>
#include <thrust/host_vector.h>
#include <thrust/fill.h>
#include <cuda.h>
#include "operator.h"
#include "strcut.h"
#include "cublas_v2.h"

__device__ double getPearson(double* d_dataList, int row, int col, int conNum)
{
    int num = 0;
    double mulE = 0, yDataE = 0, xDataE = 0;
    for (int i = 0; i < conNum; i++) {
        if (d_dataList[row * conNum + i] == 0 || d_dataList[col * conNum + i] == 0) {
            num++;
            continue;
        }
        mulE += d_dataList[row * conNum + i] * d_dataList[col * conNum + i];
        xDataE += d_dataList[row * conNum + i];
        yDataE += d_dataList[col * conNum + i];
    }
    double numerator = mulE - (xDataE * yDataE / (conNum - num));
    num = 0;
    double	xDataSquareAdd = 0, xDataAdd = 0, yDataSquareAdd = 0, yDataAdd = 0;
    for (int i = 0; i < conNum; i++) {
        if (d_dataList[row * conNum + i] == 0 || d_dataList[col * conNum + i] == 0) {
            num++;
            continue;
        }
        xDataSquareAdd += d_dataList[row * conNum + i] * d_dataList[row * conNum + i];
        xDataAdd += d_dataList[row * conNum + i];
        yDataSquareAdd += d_dataList[col * conNum + i] * d_dataList[col * conNum + i];
        yDataAdd += d_dataList[col * conNum + i];
    }
    double denominator = sqrt((xDataSquareAdd - xDataAdd * xDataAdd / (conNum - num)) * (yDataSquareAdd - yDataAdd * yDataAdd / (conNum - num)));
    return  fabs(numerator / denominator);
}

__global__ void kernelPearson(double* d_dataList, double* d_coeMatrix, int num, int conNum)
{
    int index = threadIdx.x + blockIdx.x * blockDim.x;
    if (index > num * num)
        return;
    int row = index / num;
    int col = index % num;
    if (row > col)
        return;
    double pearson = getPearson(d_dataList, row, col, conNum);
    d_coeMatrix[row * num + col] = pearson;
    d_coeMatrix[col * num + row] = pearson;

}

__global__ void kernelTransMatrix(double* d_coeMatrix, double* d_coeSum, double* d_transMatrix, int num, int highNum, int* d_numList) {
    int index = threadIdx.x + blockIdx.x * blockDim.x;
    if (index > num * num)
        return;
    int row = index / num;
    int col = index % num;
    if (col == num - 1) {
        d_transMatrix[index] = 1.0 / d_coeSum[row];
    }
    else if (row == num - 1)
    {
        d_transMatrix[index] = double(d_numList[col]) / highNum;
    }
    else {
        d_transMatrix[index] = d_coeMatrix[row * (num - 1) + col] / d_coeSum[row];
    }
    if (row == col)
        d_transMatrix[index] = 0.0;
}

__global__ void kernelLrValue(double* d_lrValue, double* d_transMatrix, double* d_nextLrValue, int num, double* d_error) {
    int index = threadIdx.x + blockIdx.x * blockDim.x;
    if (index > num)
        return;
    d_nextLrValue[index] = 0;
    for (int i = 0; i < num; i++)
    {
        d_nextLrValue[index] += d_lrValue[i] * d_transMatrix[i * num + index];
    }
    d_error[index] = abs(d_nextLrValue[index] - d_lrValue[index]);
}

__global__ void kernelLrValueEq(double* d_lrValue, double* d_nextLrValue, int num) {
    int index = threadIdx.x + blockIdx.x * blockDim.x;
    if (index > num)
        return;
    d_lrValue[index] = d_nextLrValue[index];
}

__global__ void kernelLrValueEq2(double* d_lrValue, double* d_nextLrValue, int num, double* d_error) {
    int index = threadIdx.x + blockIdx.x * blockDim.x;
    if (index > num)
        return;
    d_error[index] = abs(d_nextLrValue[index] - d_lrValue[index]);
    d_lrValue[index] = d_nextLrValue[index];
}

__global__ void kernelLrValueShare(double* d_lrValue, int num) {
    int index = threadIdx.x + blockIdx.x * blockDim.x;
    if (index > num - 1)
        return;
    d_lrValue[index] += d_lrValue[num - 1] / (num - 1);
}

__global__ void kernelFunction1(double* d_coeMatrix, int num) {
    int index = threadIdx.x + blockIdx.x * blockDim.x;
    if (index > num * num)
        return;
    if (index % num != index / num)
        d_coeMatrix[index] = d_coeMatrix[index] * d_coeMatrix[index] * d_coeMatrix[index];
}

__global__ void kernelFunction2(double* d_coeMatrix, int num) {
    int index = threadIdx.x + blockIdx.x * blockDim.x;
    if (index > num * num)
        return;
    if (index % num != index / num)
        d_coeMatrix[index] = d_coeMatrix[index] * (d_coeMatrix[index] + 0.5);
}

__global__ void kernelFunction3(double* d_coeMatrix, int num) {
    int index = threadIdx.x + blockIdx.x * blockDim.x;
    if (index > num * num)
        return;
    if (index % num != index / num)
        d_coeMatrix[index] = d_coeMatrix[index] * (d_coeMatrix[index] + 1.0);
}

__global__ void kernelPearsonCut(double* d_coeMatrix, int num, double cutThreshold) {
    int index = threadIdx.x + blockIdx.x * blockDim.x;
    if (index > num * num)
        return;
    if (d_coeMatrix[index] > cutThreshold)
    {
        d_coeMatrix[index] = 1;
    }
    else
    {
        d_coeMatrix[index] = 0;
    }
}

__global__ void kernelGround(double* d_corMatrix, int num, int* d_numList)
{
    int index = threadIdx.x + blockIdx.x * blockDim.x;
    if (index > num)
        return;
    int highCoeNum = 1;
    for (int i = 0; i < num; i++)
    {
        if (d_corMatrix[index * num + i] > 0.8)
            highCoeNum++;
    }
    d_numList[index] = highCoeNum;
}

__global__ void kernelTransMatrixD(double* d_coeMatrix, double* d_coeSum, double* d_transMatrix, int num) {
    int index = threadIdx.x + blockIdx.x * blockDim.x;
    if (index > num * num)
        return;
    int row = index / num;
    int col = index % num;
    if (col == num - 1) {
        d_transMatrix[index] = 1.0 / d_coeSum[row];
    }
    else if (row == num - 1)
    {
        d_transMatrix[index] = 1.0 / (num - 1);
    }
    else {
        d_transMatrix[index] = d_coeMatrix[row * (num - 1) + col] / d_coeSum[row];
    }
    if (row == col)
        d_transMatrix[index] = 0.0;
}


Operator::Operator(const std::string outPath, const std::string inputPath) : outPath(outPath), inputPath(inputPath)
{
}

Operator::~Operator() {
    cudaFree(d_transMatrix);
    cudaFree(d_coeMatrix);
    delete[]lrValue;
}

void Operator::quickSort(int low, int high, int array[], double* res)
{
    int Low, High, temp;
    if (low < high) {
        Low = low;
        High = high;
        temp = array[low];
        while (Low < High) {
            while (Low < High && res[array[High]] >= res[temp]) {
                High--;
            }
            if (Low < High) {
                array[Low] = array[High];
                Low++;
            }
            while (Low < High && res[array[Low]] <= res[temp]) {
                Low++;
            }
            if (Low < High) {
                array[High] = array[Low];
                High--;
            }
        }
        array[Low] = temp;
        quickSort(low, Low - 1, array, res);
        quickSort(Low + 1, high, array, res);
    }
}


void Operator::printMyGenes() {
    int num = myGenes.size();
    for (unsigned int i = 0; i < myGenes.size(); i++)
    {
        std::cout << myGenes[i].name << ",";
    }
    std::cout << std::endl;
    /*for (int i = 0; i < num*conNum; i++)
    {
        if (i % conNum == 0)
            std::cout << std::endl;
        std::cout << dataList[i] << " ";
    }*/

}

void Operator::printCoeMatrix() {
    int num = myGenes.size();
    std::string outPathCoe = outPath + "_coe.txt";
    std::ofstream outFile(outPathCoe, std::ios::ate);
    for(int i = 0; i < num; i++)
    {
     outFile << "," << myGenes[i].name;
    }
    int id=0; 
    for (int i = 0; i < num * num; i++)
    {
        if (i % num == 0){
          outFile << "\n";
          outFile << myGenes[id++].name;
        }
        //std::cout<< coeMatrix[i];
        outFile  << "," << coeMatrix[i];
    }
}

void Operator::cutAndOut() {
    int num = myGenes.size();
    std::string outPathCoe = outPath + "_cut.txt";
    std::ofstream outFile(outPathCoe, std::ios::ate);

    for (int i = 0; i < num * num; i++)
    {   
        int j = i / num;
        int k = i % num;
        if (k<=j)
            continue;
        if (coeMatrix[i]){
          outFile << myGenes[j].name << "," << myGenes[k].name << "\n";
          }
    }
}


void Operator::outputFile(const int coeFlag,double cutThreshold) {
    int num = myGenes.size() - 1;
    std::string outPathLr = outPath + "_lr.txt";
    std::ofstream outFile(outPathLr, std::ios::ate);
    if (!outFile)
    {
        std::cout << "Error!" << std::endl;
        exit(1);
    }
    int* mediate = new int[num];
    for (int i = 0; i <= num; i++) {
        mediate[i] = i;
    }
    double* res = lrValue;
    quickSort(0, num, mediate, lrValue);
    int flag = 0;
    for (int i = num; i >= 0; i--)
    {
        outFile << myGenes[mediate[i]].name << " = " << res[mediate[i]] << std::endl;
        if (flag < 15)
        {
            idList.push_back(mediate[i]);
            flag++;
        }
    }
    outFile.close();
    if(coeFlag){
        num = myGenes.size();
        coeMatrix = new double[num * num]();
        cudaMemcpy(coeMatrix, d_coeMatrix, num * num * sizeof(double), cudaMemcpyDeviceToHost);
        printCoeMatrix();
    }
    if(cutThreshold){
        dim3 blockSize(256);
        dim3 gridSize((num * num + blockSize.x - 1) / blockSize.x);
        kernelPearsonCut << <gridSize, blockSize >> > (d_coeMatrix, num, cutT);
        num = myGenes.size();
        coeMatrix = new double[num * num]();
        cudaMemcpy(coeMatrix, d_coeMatrix, num * num * sizeof(double), cudaMemcpyDeviceToHost);
        cutAndOut();
    }

}

void Operator::printTransMatrix() {
    int num = myGenes.size() + 1;
    for (int i = 0; i < num; i++)
    {
        double sum = 0;
        for (int j = 0; j < num; j++)
        {
            sum += transMatrix[i * num + j];
        }
        std::cout << i << ":" << sum << std::endl;
    }
    for (int i = 0; i < num; i++)
    {
        for (int j = 0; j < num; j++)
        {
            std::cout << transMatrix[i * num + j] << " ";
        }
        std::cout << std::endl;
    }
}

void Operator::readFileCoe() {
    int num;
    std::ifstream fp(inputPath);
    std::string strLine;
    int a = -1;
    while (std::getline(fp, strLine))
    {
        a++;
    }
    conNum = a;
    fp.clear();
    fp.seekg(std::ios::beg);

    int index = -1;
    while (std::getline(fp, strLine)) {
        std::vector<std::string> values;
        splitStr(strLine, ",", values);
        if (index == -1)
        {
            for (unsigned int k = 0; k < values.size(); ++k)
            {
                geneNode item;
                item.id = k;
                item.name = values[k];
                myGenes.push_back(item);
            }
            num = myGenes.size();
            dataList = new double[num * conNum]();
        }
        else
        {
            for (unsigned int k = 0; k < values.size(); ++k)
            {
                auto fvalue = atof(values[k].c_str());
                dataList[k * conNum + index] = fvalue;
            }
        }
        index++;
    }
    lrValue = new double[num + 1];
    for (int i = 0; i < num + 1; i++)
    {
        lrValue[i] = 1.0;
    }
    lrValue[num] = 0.0;
    fp.close();
    int len = myGenes[num-1].name.length();
    myGenes[num-1].name=myGenes[num-1].name.substr(0,len-1);
    cudaMalloc(&d_dataList, num * conNum * sizeof(double));
    cudaMemcpy(d_dataList, dataList, num * conNum * sizeof(double), cudaMemcpyHostToDevice);
    delete[]dataList;
    std::cout<<num<<std::endl;
}

void Operator::readFileDegree() {
    std::ifstream fp(inputPath);
    std::string strLine;
    int index = -1;
    int num;
    while (std::getline(fp, strLine)) {
        std::vector<double> item;
        std::vector<std::string> values;
        splitStr(strLine, ",", values);
        if (index == -1)
        {
            for (unsigned int k = 0; k < values.size(); ++k)
            {
                geneNode item;
                item.id = k;
                item.name = values[k];
                if(k==values.size()-1)
                {
                  item.name = values[k].substr(0,values[k].length()-1);
                }
                myGenes.push_back(item);
            }
            num = myGenes.size();
            coeMatrix = new double[num * num]();
        }
        else
        {
            for (unsigned int k = 1; k < values.size(); ++k)
            {
                double fvalue = atof(values[k].c_str());
                coeMatrix[index * num + k - 1] = fvalue;
            }
        }
        index++;
    }
    lrValue = new double[num + 1]();
    for (int i = 0; i < num; i++)
    {
        lrValue[i] = 1.0;
    }
    fp.close();
    cudaMalloc(&d_coeMatrix, num * num * sizeof(double));
    cudaMemcpy(d_coeMatrix, coeMatrix, num * num * sizeof(double), cudaMemcpyHostToDevice);
}

void Operator::calPearson() {

    int num = myGenes.size();
    cudaMalloc(&d_coeMatrix, num * num * sizeof(double));
    dim3 blockSize(256);
    dim3 gridSize((num * num + blockSize.x - 1) / blockSize.x);
    kernelPearson << <gridSize, blockSize >> > (d_dataList, d_coeMatrix, num, conNum);
    cudaFree(d_dataList);
}

void Operator::calTransMatrix()
{
    int num = myGenes.size();
    double* coeSum = new double[num + 1]();
    for (int i = 0; i < num; ++i)
    {
        double* d_rowSum;
        cudaMalloc(&d_rowSum, num * sizeof(double));
        int nBegin = i * num;
        cudaMemcpy(d_rowSum, d_coeMatrix + nBegin, sizeof(double) * num, cudaMemcpyDeviceToDevice);
        thrust::device_ptr<double> dev_ptr(d_rowSum);
        double row_sum = thrust::reduce(dev_ptr, dev_ptr + num);
        cudaFree(d_rowSum);
        coeSum[i] = row_sum;
    }
    coeSum[num] = 1;
    double* d_coeSum;
    cudaMalloc(&d_coeSum, (num + 1) * sizeof(double));
    cudaMemcpy(d_coeSum, coeSum, (num + 1) * sizeof(double), cudaMemcpyHostToDevice);
    num++;
    transMatrix = new double[num * num];
    cudaMalloc(&d_transMatrix, num * num * sizeof(double));
    dim3 blockSize(256);
    dim3 gridSize((num * num + blockSize.x - 1) / blockSize.x);
    kernelTransMatrix << <gridSize, blockSize >> > (d_coeMatrix, d_coeSum, d_transMatrix, num, highNum, d_numList);
    cudaMemcpy(transMatrix, d_transMatrix, num * num * sizeof(double), cudaMemcpyDeviceToHost);
    delete[]coeSum;
    cudaFree(d_coeSum);
    cudaFree(d_numList);
}

void Operator::calTransMatrixD()
{
    int num = myGenes.size();
    double* coeSum = new double[num]();
    for (int i = 0; i < num; ++i)
    {
        double* d_rowSum;
        cudaMalloc(&d_rowSum, num * sizeof(double));
        int nBegin = i * num;
        cudaMemcpy(d_rowSum, d_coeMatrix + nBegin, sizeof(double) * num, cudaMemcpyDeviceToDevice);
        thrust::device_ptr<double> dev_ptr(d_rowSum);
        double row_sum = thrust::reduce(dev_ptr, dev_ptr + num);
        cudaFree(d_rowSum);
        coeSum[i] = row_sum;
    }
    double* d_coeSum;
    cudaMalloc(&d_coeSum, num * sizeof(double));
    cudaMemcpy(d_coeSum, coeSum, num * sizeof(double), cudaMemcpyHostToDevice);
    num++;
    transMatrix = new double[num * num];
    cudaMalloc(&d_transMatrix, num * num * sizeof(double));
    dim3 blockSize(256);
    dim3 gridSize((num * num + blockSize.x - 1) / blockSize.x);
    kernelTransMatrixD << <gridSize, blockSize >> > (d_coeMatrix, d_coeSum, d_transMatrix, num);
    cudaMemcpy(transMatrix, d_transMatrix, num * num * sizeof(double), cudaMemcpyDeviceToHost);
    delete[]coeSum;
    cudaFree(d_coeSum);
}

void Operator::calLrValue()
{
    int num = myGenes.size() + 1;
    int numIter = 1;
    double error;
    double* d_error;
    double* d_nextLrValue;
    double* d_lrValue;
    cudaMalloc(&d_error, num * sizeof(double));
    cudaMalloc(&d_lrValue, num * sizeof(double));
    cudaMalloc(&d_nextLrValue, num * sizeof(double));
    cudaMemcpy(d_lrValue, lrValue, num * sizeof(double), cudaMemcpyHostToDevice);
    dim3 blockSize(256);
    dim3 gridSize((num + blockSize.x - 1) / blockSize.x);
    do
    {
        kernelLrValue << <gridSize, blockSize >> > (d_lrValue, d_transMatrix, d_nextLrValue, num, d_error);
        thrust::device_ptr<double> dev_ptr(d_error);
        error = thrust::reduce(dev_ptr, dev_ptr + num);
        kernelLrValueEq << <gridSize, blockSize >> > (d_lrValue, d_nextLrValue, num);
        //std::cout << numIter++ << std::endl;
        //std::cout << error << std::endl;
    } while (error > minError || numIter < maxNum);
    kernelLrValueShare << <gridSize, blockSize >> > (d_lrValue, num);
    cudaMemcpy(lrValue, d_lrValue, num * sizeof(double), cudaMemcpyDeviceToHost);
    /*
    num = num -1;
    coeMatrix = new double[num * num]();
    cudaMemcpy(coeMatrix, d_coeMatrix, num * num * sizeof(double), cudaMemcpyDeviceToHost);
    */
    cudaFree(d_lrValue);
    cudaFree(d_nextLrValue);
    cudaFree(d_error);
}


void Operator::calIteration(int modId,double cutThreshold) {
    int num = myGenes.size();
    cudaMalloc(&d_numList, num * sizeof(int));
    dim3 blockSize(256);
    dim3 gridSize2((num + blockSize.x - 1) / blockSize.x);
    kernelGround << <gridSize2, blockSize >> > (d_coeMatrix, num, d_numList);
    thrust::device_ptr<int> dev_ptr2(d_numList);
    highNum = thrust::reduce(dev_ptr2, dev_ptr2 + num);
    dim3 gridSize((num * num + blockSize.x - 1) / blockSize.x);
    switch (modId)
    {
    case 1:
        cutT = cutThreshold;
        return;
    case 2:
        cutT = cutThreshold * cutThreshold *cutThreshold;
        kernelFunction1 << <gridSize, blockSize >> > (d_coeMatrix, num);
        break;
    case 3:
        cutT = cutThreshold * (cutThreshold + 0.5);
        kernelFunction2 << <gridSize, blockSize >> > (d_coeMatrix, num);
        break;
    case 4:
        cutT = cutThreshold * (cutThreshold+1.0);
        kernelFunction3 << <gridSize, blockSize >> > (d_coeMatrix, num);
        break;
    }
}

void Operator::menu(const int funcId, const int iterTimes,const double iterDiff) {
    
    if (funcId == 1)
    {
        maxNum = iterTimes;
        minError = iterDiff;
    }
    if (funcId == 2)
    {
        maxNum = iterTimes;
        minError = 99999;
    }

    if (funcId == 3)
    {
        maxNum = 0;
        minError = iterDiff;
    }
    
}