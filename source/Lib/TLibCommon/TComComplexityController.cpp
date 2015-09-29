#include "TComComplexityController.h"

double TComComplexityController::SP;
double TComComplexityController::PV;
double TComComplexityController::avgPV;
double TComComplexityController::gopPV;
double TComComplexityController::accumPV;
double TComComplexityController::error;
double TComComplexityController::prevError;
double TComComplexityController::accumError;
double TComComplexityController::controlOutput;
double TComComplexityController::kd;
double TComComplexityController::ki;
double TComComplexityController::kp;
double TComComplexityController::targetSavings;
unsigned int TComComplexityController::trainingPeriod;
int TComComplexityController::gopSize;
int TComComplexityController::currPoc;
double TComComplexityController::frameTime;
clock_t TComComplexityController::tBegin;
unsigned int TComComplexityController::frameCount;
std::ofstream TComComplexityController::pidFile;
bool TComComplexityController::controlActive;

void TComComplexityController::init(int gop){
    gopSize = gop;
    
    frameCount = 0;
    frameTime = 0.0;
    
    error = 0.0;
    prevError = 0.0;
    accumError = 0.0;    
    controlOutput = 0.0;
    controlActive = false;
    accumPV = 0.0;
    avgPV = 0.0;
    gopPV = 0.0;
}


void TComComplexityController::updateSP(){
    if(trainingPeriod > 0)
        SP = avgPV*targetSavings;

}

void TComComplexityController::updatePV(){
    PV = frameTime;
    accumPV += PV;
    if(frameCount % gopSize == 0)
        gopPV = PV;
    else
        gopPV += PV;
    
    frameCount++;
    

    
    avgPV = accumPV/frameCount;
}

double TComComplexityController::calcPID(){

    double PIDOutput;
    
    prevError = error;
    error = SP - PV;
    
    accumError += error;           

    PIDOutput = kp*error + ki*accumError+ kd*(error - prevError);
    controlOutput = (PV + PIDOutput);

    return controlOutput;
    
}

void TComComplexityController::beginFrameTimer(){
    tBegin = clock();
}

void TComComplexityController::endFrameTimer(){
    clock_t tAfter = clock();
    frameTime = (double) (tAfter - tBegin)/ CLOCKS_PER_SEC;
}

void TComComplexityController::printControlStats(double estimatedTime){
    openPidFile();
    pidFile << currPoc;
    pidFile << "\t" << controlActive << "\t" <<  SP << "\t" << PV << "\t" << gopPV/gopSize << "\t" << avgPV << "\t" << controlOutput;
    pidFile << "\t" << estimatedTime << "\t\t\t" << kp*error << "\t" << ki*accumError << "\t" <<  kd*(error - prevError) << endl;
    
#if DISPLAY_VERBOSE
    cout << "@control\tPOC\tControl Active\tSP\tPV\tGOP PV\tAVG PV\tPID\tEST\t\t\te\tSe\tde\n";
    cout << "@control\t\t" << controlActive << "\t" <<  SP << "\t" << PV << "\t" << gopPV/gopSize << "\t" << avgPV << "\t" << controlOutput;
    cout << "\t" << estimatedTime << "\t\t\t" << kp*error << "\t" << ki*accumError << "\t" <<  kd*(error - prevError) << endl;
#endif

}


bool TComComplexityController::activateControl(int poc){
    currPoc = poc;
    controlActive = (poc >= (NUM_RD_FRAMES + trainingPeriod));
    updateSP();
    return controlActive;
}

Void TComComplexityController::openPidFile(){ 
    if(!pidFile.is_open()){
        pidFile.open("controlOut.csv",ofstream::out);
        pidFile << "POC\tControl Active\tSP\tPV\tGOP PV\tAVG PV\tPID\tEST\t\t\te\tSe\tde\n";
    }
}