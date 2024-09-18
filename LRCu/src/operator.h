#pragma once
#ifndef OPERATOR_H
#define OPERATOR_H

#include <vector>
#include <string>
#include <stdio.h>
#include <iostream>
#include <cmath>
#include <fstream>
#include <ctime>
#include <algorithm>


struct geneNode {
    std::string name;
    int id;
};


class Operator
{
public:
    Operator(const std::string outPath, const std::string inputPath);
    ~Operator();

public:
    void readFileCoe();
    void readFileDegree();
    void calPearson();
    void calTransMatrix();
    void calTransMatrixD();
    void calLrValue();
    void calLrValue2();
    void quickSort(int low, int high, int array[], double* res);
    void outputFile(const int coeFlag,double cutThreshold);
    void calIteration(int modId,double cutThreshold);
    void menu(const int funcId, const int iterTimes,const double iterDiff);


public:
    void printMyGenes();
    void printCoeMatrix();
    void printTransMatrix();
    void cutAndOut();



protected:
    std::vector<geneNode> myGenes;
    unsigned int conNum;
    
    const std::string outPath;
    const std::string inputPath;
    
    double* dataList;
    double* coeMatrix;
    double* transMatrix;
    double* lrValue;
    int maxNum;
    int highNum;
    double minError;

    double* d_dataList;
    double* d_coeMatrix;
    double* d_transMatrix;
    int* d_numList;

    std::vector<int> idList;
    std::vector<int> bigList;
    const char* outPath1 = "../data/outputcluster.txt";

    double cutT;

};

#endif