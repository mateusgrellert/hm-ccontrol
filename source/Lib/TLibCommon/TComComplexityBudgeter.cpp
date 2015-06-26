#include "TComComplexityBudgeter.h"
#include "TComComplexityController.h"
#include "TComCABACTables.h"
#include <cmath>

using namespace std;

int TComComplexityBudgeter::psetCounter[NUM_PSETS];
long TComComplexityBudgeter::initCtuTime;
long TComComplexityBudgeter::endCtuTime;
double TComComplexityBudgeter::maxCtuTime;
double TComComplexityBudgeter::minCtuTime;
vector<vector <double> > TComComplexityBudgeter::ctuHistory;
vector<vector <config> > TComComplexityBudgeter::psetMap;
UInt TComComplexityBudgeter::gopSize;
Int TComComplexityBudgeter::currPredSavings;
UInt TComComplexityBudgeter::picWidth;
UInt TComComplexityBudgeter::picHeight;
UInt TComComplexityBudgeter::maxCUDepth;
UInt TComComplexityBudgeter::maxTUDepth;
UInt TComComplexityBudgeter::maxNumRefPics;
Int TComComplexityBudgeter::searchRange;
Int TComComplexityBudgeter::bipredSR;
Bool TComComplexityBudgeter::hadME;
Int TComComplexityBudgeter::enFME;
Bool TComComplexityBudgeter::enRDOQ;
Bool TComComplexityBudgeter::testAMP;
UInt TComComplexityBudgeter::testSMP;
UInt TComComplexityBudgeter::currPoc;
UInt TComComplexityBudgeter::budgetAlgorithm;
unsigned int TComComplexityBudgeter::fixPSet; // for budget algorithm 4
Double TComComplexityBudgeter::frameBudget; 
Double TComComplexityBudgeter::estFrameTime;
std::ofstream TComComplexityBudgeter::budgetFile;


Void TComComplexityBudgeter::init(UInt w, UInt h, UInt gop){

    vector<double> tempHistRow;
    vector<config> tempConfigRow;
    config conf;
    
    estFrameTime = 0.0;
    gopSize = gop;
    
    picWidth = w;
    picHeight = h;
            
    currPredSavings = PS0;

    maxCtuTime = 0.0;
    minCtuTime = MAX_INT;

    
    for(int i = 0; i < (w >> 6) + 1; i++){
        tempHistRow.clear();
        tempConfigRow.clear();
        for(int j = 0; j < (h >> 6) + 1; j++){
            conf.clear();
            tempHistRow.push_back(-1);

            // for config map
            for(int k = 0; k < NUM_PARAMS+1; k++){
                conf.push_back(-1);
            }
            tempConfigRow.push_back(conf);
        }
        ctuHistory.push_back(tempHistRow);
        psetMap.push_back(tempConfigRow);
    }
}



void TComComplexityBudgeter::setDepthHistory(TComDataCU *&pcCU, UInt pu_idx){
    
    unsigned int x = pcCU->getCUPelX();
    unsigned int y = pcCU->getCUPelY();
    ctuHistory[x >> 6][y >> 6] = pcCU->getDepth(pu_idx);

}

void TComComplexityBudgeter::setTimeHistory(TComDataCU *&pcCU){
    
    UInt x = pcCU->getCUPelX();
    UInt y = pcCU->getCUPelY();

    double ctu_time = (double)(endCtuTime - initCtuTime)*1.0/CLOCKS_PER_SEC*1.0;
    ctuHistory[x >> 6][y >> 6] = ctu_time;
    
    if (ctu_time > maxCtuTime)
        maxCtuTime = ctu_time;
    else if(ctu_time < minCtuTime)
        minCtuTime = ctu_time;
    
}

void TComComplexityBudgeter::updateConfig(TComDataCU*& cu){
    Int x = cu->getCUPelX() >> 6;
    Int y = cu->getCUPelY() >> 6;
      // bipred sr, sr, testrect, tu depth, amp, had me, num refs, rdoq, cu depth, 

    bipredSR      = psetMap[x][y][0];
    searchRange   = psetMap[x][y][1];
    testSMP       = psetMap[x][y][2];
    maxTUDepth    = psetMap[x][y][3];
    testAMP       = psetMap[x][y][4];
    hadME         = psetMap[x][y][5];
    maxNumRefPics = psetMap[x][y][6];
    enRDOQ        = psetMap[x][y][7];
    enFME         = psetMap[x][y][8];
    maxCUDepth    = psetMap[x][y][9];
}

void TComComplexityBudgeter::resetConfig(TComDataCU*& cu){
  
      // bipred sr, sr, testrect, tu depth, amp, had me, num refs, rdoq, cu depth, 

    bipredSR      = 4;
    searchRange   = 64;
    testSMP       = 10;
    maxTUDepth    = 3;
    testAMP       = 1;
    hadME         = 1;
    maxNumRefPics = 4;
    enRDOQ        = 1;
    maxCUDepth    = 4;
    enFME = 3;
}



UInt TComComplexityBudgeter::promote(UInt ctux, UInt ctuy){
    UInt new_pset = psetMap[ctux][ctuy][NUM_PARAMS]-1; // upgrading pset
    setPSetToCTU(ctux,ctuy,new_pset);
    return new_pset;
}

UInt TComComplexityBudgeter::demote(UInt ctux, UInt ctuy){
    UInt new_pset = psetMap[ctux][ctuy][NUM_PARAMS]+1; // downgrading pset
    setPSetToCTU(ctux,ctuy,new_pset);
    return new_pset;
}

Void TComComplexityBudgeter::uniformBudget(){ 
    
    int predSav = (int) ((1-(frameBudget/TComComplexityController::avgPV))*10);
    predSav = predSav < 0 ? 0 : predSav;
    predSav = predSav >= NUM_PSETS ? NUM_PSETS-1 : predSav;
    currPredSavings += predSav;
    currPredSavings = currPredSavings < 0 ? 0 : currPredSavings;
    currPredSavings = currPredSavings >= NUM_PSETS ? NUM_PSETS-1 : currPredSavings;           
    
    for(int i = 0; i < ctuHistory.size(); i++){
        for(int j = 0; j < ctuHistory[0].size(); j++){
            if (ctuHistory[i][j] == -1)
                continue;
            setPSetToCTU(i,j,currPredSavings);
            updateEstimationAndStats(-1,currPredSavings);

        }
    }
}


Void TComComplexityBudgeter::uniformEstimationBudget(){ 

    currPredSavings = PS0;
    while( currPredSavings < NUM_PSETS ){
        if (estimateTime(currPredSavings) <= frameBudget){
            break;
        }
        currPredSavings++;
    }



    for(int i = 0; i < ctuHistory.size(); i++){
        for(int j = 0; j < ctuHistory[0].size(); j++){
            if (ctuHistory[i][j] == -1)
                continue;
            setPSetToCTU(i,j,currPredSavings);
            updateEstimationAndStats(-1,currPredSavings);
        }
    }
    
       

}

Void TComComplexityBudgeter::uniformIncrementalBudget(){ 
   
    if(TComComplexityController::avgPV > 1.1*frameBudget)
        currPredSavings++;
    else if(TComComplexityController::avgPV < 0.90*frameBudget)
        currPredSavings--;
    
    currPredSavings = (currPredSavings > NUM_PSETS-1 ) ? NUM_PSETS-1 : currPredSavings;
    currPredSavings = (currPredSavings < 0) ? 0 : currPredSavings ;



    for(int i = 0; i < ctuHistory.size(); i++){
        for(int j = 0; j < ctuHistory[0].size(); j++){
            if (ctuHistory[i][j] == -1)
                continue;
            setPSetToCTU(i,j,currPredSavings);
                       
            updateEstimationAndStats(-1,currPredSavings);

        }
    }
       
    estFrameTime = estimateTime(currPredSavings);

}



Void TComComplexityBudgeter::bottomUpBudget(){
    
  //  Int curr_depth = 3;
    UInt new_pset;
    
    
    // start by assigning PS90 to all
    for(int i = 0; i < ctuHistory.size(); i++){
        for(int j = 0; j < ctuHistory[0].size(); j++){
            if (ctuHistory[i][j] == -1) // sometimes the history table has more nodes than CTUs
                continue;

            setPSetToCTU(i,j,PS90);
            updateEstimationAndStats(-1,PS90);
        }
    }
    
    UInt promote_pset = PS90;
    
    while(promote_pset > PS0){ // maximum #iterations -- all PSETs are already set to PS100
        for(int i = 0; i < ctuHistory.size() and estFrameTime < frameBudget; i++){
            for(int j = 0; j < ctuHistory[0].size() and estFrameTime < frameBudget; j++){
                if (ctuHistory[i][j] == -1) // sometimes the history table has more nodes than CTUs
                    continue;

                    if(psetMap[i][j][NUM_PARAMS] == promote_pset){
                        new_pset = promote(i,j);
                        updateEstimationAndStats(promote_pset,new_pset);
                    }
            }
        }
        promote_pset--;
    }
}


        

Void TComComplexityBudgeter::setPSetToAllCTUs() {
     for(int i = 0; i < ctuHistory.size(); i++){
        for(int j = 0; j < ctuHistory[0].size(); j++){
            if (ctuHistory[i][j] == -1)
                        continue;
            setPSetToCTU(i,j,fixPSet);
                       
            updateEstimationAndStats(-1,fixPSet);

        }
     }
}


Void TComComplexityBudgeter::priorityBasedBudget(){
    UInt new_pset;
    
    double time_step = (double)(maxCtuTime-minCtuTime)/NUM_PSETS;

    
    // first step - set PSavings according to the previous CTU Time
    for(int i = 0; i < ctuHistory.size(); i++){
        for(int j = 0; j < ctuHistory[0].size(); j++){
            if (ctuHistory[i][j] == -1)
                        continue;
            
            for(UInt psav=PS0; psav < NUM_PSETS; psav++){
                if(ctuHistory[i][j] >= (1-time_step*(psav-1))*maxCtuTime){
                    setPSetToCTU(i,j, psav);
                    updateEstimationAndStats(-1, psav);
                    break;
                }
            }
            
        }
    }
    
           // second step - start demoting until available computation is reached
        
    UInt demote_pset = PS0;

    // second step - start demoting until available computation is reached
    while(demote_pset < PS90){ // maximum #iterations -- all PSETs are already set to PS20
        for(int i = 0; i < ctuHistory.size() and estFrameTime > frameBudget; i++){
            for(int j = 0; j < ctuHistory[0].size() and estFrameTime > frameBudget; j++){
                if (ctuHistory[i][j] == -1) // sometimes the history table has more nodes than CTUs
                    continue;

                    if(psetMap[i][j][NUM_PARAMS] == demote_pset){
                        new_pset = demote(i,j);
                        updateEstimationAndStats(demote_pset,new_pset);
                    }
            }
        }          
        demote_pset++;
    }
    
    UInt promote_pset = PS90;
    
    while(promote_pset > PS0){ // maximum #iterations -- all PSETs are already set to PS100
        for(int i = 0; i < ctuHistory.size() and estFrameTime < frameBudget; i++){
            for(int j = 0; j < ctuHistory[0].size() and estFrameTime < frameBudget; j++){
                if (ctuHistory[i][j] == -1) // sometimes the history table has more nodes than CTUs
                    continue;
                
                if(psetMap[i][j][NUM_PARAMS] == promote_pset){
                    new_pset = promote(i,j);
                    updateEstimationAndStats(promote_pset,new_pset);
                }
            }
        }
        promote_pset--;
    }
    
}


// conf 0 = low, 1 = medL, 2 = medH, 3 = high

void TComComplexityBudgeter::updateEstimationAndStats(Int old_pset, UInt new_pset){
    double nCU = (picHeight*picWidth)/(64.0*64.0);
   

    if (old_pset != -1)
        psetCounter[old_pset]--;
    psetCounter[new_pset]++;
       
    if (old_pset != -1)
        estFrameTime -= estimateTime(old_pset)/nCU;
    estFrameTime += estimateTime(new_pset)/nCU;
    
}

Void TComComplexityBudgeter::setPSetToCTU(UInt i, UInt j, UInt pset){
      // bipred sr, sr, testrect, tu depth, amp, had me, num refs, rdoq, en fme,  cu depth, 
         
            psetMap[i][j][0] = PSET_TABLE[pset][0]; // bipred SR
            psetMap[i][j][1] = PSET_TABLE[pset][1]; // SR
            psetMap[i][j][2] = PSET_TABLE[pset][2]; // TestRect
            psetMap[i][j][3] = PSET_TABLE[pset][3]; // TU Depth
            psetMap[i][j][4] = PSET_TABLE[pset][4]; // AMP
            psetMap[i][j][5] = PSET_TABLE[pset][5]; // HAD ME
            psetMap[i][j][6] = PSET_TABLE[pset][6]; // Max Num Ref Pics
            psetMap[i][j][7] = PSET_TABLE[pset][7]; // rdoq
            psetMap[i][j][8] = PSET_TABLE[pset][8]; // EN FME
            psetMap[i][j][9] = PSET_TABLE[pset][9]; // cu depth
            psetMap[i][j][NUM_PARAMS] = pset;

}

Double TComComplexityBudgeter::estimateTime(UInt predSavings){
    Double factor = double (predSavings)/10.0; // get percentage predicted savings
    
    return TComComplexityController::avgPV*(1-factor);
            
}

Void TComComplexityBudgeter::distributeBudget(){
    resetBudgetStats();

    switch(budgetAlgorithm){
        case 0:  uniformBudget(); break;
        case 1:  uniformEstimationBudget(); break;
        case 2:  uniformIncrementalBudget(); break;
        case 3:  bottomUpBudget(); break;
        case 4:  priorityBasedBudget(); break;
        default: uniformEstimationBudget(); break;
    }
    
    printBudgetStats();
    maxCtuTime = 0.0;
    minCtuTime = MAX_INT;
}

Void TComComplexityBudgeter::resetBudgetStats(){

    for (int i = 0; i < NUM_PSETS; i++)
         psetCounter[i] = 0;
}

Void TComComplexityBudgeter::printBudgetStats(){
    
    if(!budgetFile.is_open()){
        budgetFile.open("budgetDistribution.csv",ofstream::out);
        int inc = 100/NUM_PSETS;
        int num = 0;
        for (int i = 0; i < NUM_PSETS; i++){
            budgetFile << "PS" << num << "\t";
            num += inc;
        }
       budgetFile << endl;

    }

    Double total = 0.0;

    for (int i = 0; i < NUM_PSETS; i++){
        total += psetCounter[i];
    }
    
    for (int i = 0; i < NUM_PSETS; i++)
        budgetFile << (Double) psetCounter[i]/total << "\t";

    budgetFile << endl;
}

Void TComComplexityBudgeter::setFrameBudget(Double budget){
    frameBudget = budget;
}




