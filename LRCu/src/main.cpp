#include "operator.h"
#include "strcut.h"


int main(int argc, char* argv[]) {
    // initialization
    const std::string inputPath = argv[1];
    const int typeId = std::stoi(std::string(argv[2]));
    const int funcId = std::stoi(std::string(argv[3]));
    const int iterTimes = std::stoi(std::string(argv[4]));
    const double iterDiff = std::stod(std::string(argv[5]));
    const int funcFlag = std::stod(std::string(argv[6]));
    const int coeFlag = std::stoi(std::string(argv[7]));
    const double cutFlag = std::stod(std::string(argv[8]));
    const std::string outPath = argv[9];
    double cutThreshold = cutFlag;


    std::cout << "inputPath:" << inputPath<< std::endl;
    std::cout << "typeId:" << typeId<< std::endl;
    std::cout << "funcId:" << funcId<< std::endl;
    std::cout << "iterTimes:" << iterTimes << std::endl;
    std::cout << "iterDiff:" << iterDiff << std::endl;
    std::cout << "funcFlag:" << funcFlag << std::endl;
    std::cout << "coeFlag:" << coeFlag << std::endl;
    std::cout << "cutFlag:" << cutFlag << std::endl;
    std::cout << "outPath:" << outPath << std::endl;
    
    Operator op(outPath, inputPath);
    clock_t timeStart, timeEnd, timeMid;
    op.menu(funcId,iterTimes,iterDiff); 
    
    
    if (typeId == 1) {
        std::cout << "Loding..." << std::endl;
        op.readFileDegree();
        //std::cout << op.myGenes.size() << std::endl;
        timeStart = clock();
        std::cout << "Computing LR..." << std::endl;
        op.calIteration(funcFlag,cutThreshold);
        op.calTransMatrixD();
        op.calLrValue();
        timeEnd = clock();
        double endtime = (double)(timeEnd - timeStart) / CLOCKS_PER_SEC;
        std::cout << "Total time:" << endtime << "s" << std::endl;
        std::cout << "Outputing..." << std::endl;
        op.outputFile(coeFlag,cutThreshold);
    }
    else
    {
        
        std::cout << "Loding Coe..." << std::endl;
        op.readFileCoe();
        timeStart = clock();
        std::cout << "Computing matrix by Pearson..." << std::endl;
        op.calPearson();
        timeMid = clock();
        std::cout << "Computing LR..." << std::endl;
        op.calIteration(funcFlag,cutThreshold);
        op.calTransMatrix();
        op.calLrValue();
        timeEnd = clock();
        double endtime = (double)(timeEnd - timeStart) / CLOCKS_PER_SEC;
        double endtime1 = (double)(timeEnd - timeMid) / CLOCKS_PER_SEC;
        double endtime2 = (double)(timeMid - timeStart) / CLOCKS_PER_SEC;
        std::cout << "Total time:" << endtime << "s" << std::endl;
        std::cout << "Pearson time:" << endtime2 << "s" << std::endl;
        std::cout << "LR time:" << endtime1 << "s" << std::endl;
        std::cout << "Outputing..." << std::endl;
        op.outputFile(coeFlag,cutThreshold);  
    }
}
