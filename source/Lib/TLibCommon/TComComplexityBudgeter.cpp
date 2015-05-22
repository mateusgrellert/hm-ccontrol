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
Int TComComplexityBudgeter::currPSet;
UInt TComComplexityBudgeter::picWidth;
UInt TComComplexityBudgeter::picHeight;
UInt TComComplexityBudgeter::maxCUDepth;
UInt TComComplexityBudgeter::maxTUDepth;
UInt TComComplexityBudgeter::maxNumRefPics;
Int TComComplexityBudgeter::searchRange;
Bool TComComplexityBudgeter::hadME;
Bool TComComplexityBudgeter::enFME;
Bool TComComplexityBudgeter::testAMP;
UInt TComComplexityBudgeter::currPoc;
UInt TComComplexityBudgeter::budgetAlgorithm;
unsigned int TComComplexityBudgeter::fixPSet; // for budget algorithm 4
Double TComComplexityBudgeter::frameBudget; 
Double TComComplexityBudgeter::estimatedTime;
std::ofstream TComComplexityBudgeter::budgetFile;

Void TComComplexityBudgeter::init(UInt w, UInt h, UInt gop){

    vector<double> tempHistRow;
    vector<config> tempConfigRow;
    config conf;
    
    estimatedTime = 0.0;
    gopSize = gop;
    maxCUDepth = 4;
    maxTUDepth = 3;
    maxNumRefPics = 4;
    picWidth = w;
    picHeight = h;
    hadME = 1;
    enFME = 1;
    testAMP = 1;
    searchRange = 64;
        
    currPSet = 0;

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

    maxCUDepth    = psetMap[x][y][0];
    maxTUDepth    = psetMap[x][y][1];
    testAMP       = psetMap[x][y][2];
    searchRange   = psetMap[x][y][3];
    hadME         = psetMap[x][y][4];
    maxNumRefPics = psetMap[x][y][5];
    enFME        = psetMap[x][y][6];
    // en_FME = configMap[x][y][6];
}

void TComComplexityBudgeter::resetConfig(TComDataCU*& cu){
    maxCUDepth = 4;
    maxTUDepth = 3;
    searchRange = 64;
    maxNumRefPics = 4;
    testAMP = 1;
    hadME = 1;
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


Void TComComplexityBudgeter::uniformEstimationBudget(){ 

    currPSet = 0;
    while( currPSet < NUM_PSETS -1 ){
        if (estimateCycleCount(currPSet) <= frameBudget){
            break;
        }
        currPSet ++;
    }



    for(int i = 0; i < ctuHistory.size(); i++){
        for(int j = 0; j < ctuHistory[0].size(); j++){
            if (ctuHistory[i][j] == -1)
                continue;
            setPSetToCTU(i,j,currPSet);
            updateEstimationAndStats(-1,currPSet);
        }
    }
    
       

}

Void TComComplexityBudgeter::uniformIncrementalBudget(){ 
   


    if(TComComplexityController::avgPV > 1.1*frameBudget)
        currPSet++;
    else if(TComComplexityController::avgPV < 0.90*frameBudget)
        currPSet--;
    
    currPSet = (currPSet > NUM_PSETS-1 ) ? NUM_PSETS-1 : currPSet;
    currPSet = (currPSet < 0) ? 0 : currPSet ;



    for(int i = 0; i < ctuHistory.size(); i++){
        for(int j = 0; j < ctuHistory[0].size(); j++){
            if (ctuHistory[i][j] == -1)
                continue;
            setPSetToCTU(i,j,currPSet);
                       
            updateEstimationAndStats(-1,currPSet);

        }
    }
       
    estimatedTime = estimateCycleCount(currPSet);

}



Void TComComplexityBudgeter::bottomUpBudget(){
    
  //  Int curr_depth = 3;
    UInt new_pset;
    
    
    // start by assigning PS20 to all
    for(int i = 0; i < ctuHistory.size(); i++){
        for(int j = 0; j < ctuHistory[0].size(); j++){
            if (ctuHistory[i][j] == -1) // sometimes the history table has more nodes than CTUs
                continue;

            setPSetToCTU(i,j,PS20);
            updateEstimationAndStats(-1,PS20);
        }
    }
    
    UInt promote_pset = PS20;
    
    while(promote_pset > PS100){ // maximum #iterations -- all PSETs are already set to PS100
        for(int i = 0; i < ctuHistory.size() and estimatedTime < frameBudget; i++){
            for(int j = 0; j < ctuHistory[0].size() and estimatedTime < frameBudget; j++){
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


Void TComComplexityBudgeter::ICIPBudget(){
    UInt new_pset;
    
    double time_step = (double)(maxCtuTime-minCtuTime)/NUM_PSETS;

    
    // first step - set HIGH and LOW configs and estimate cycle count
    for(int i = 0; i < ctuHistory.size(); i++){
        for(int j = 0; j < ctuHistory[0].size(); j++){
            if (ctuHistory[i][j] == -1)
                        continue;
            
            if(ctuHistory[i][j] >= minCtuTime and (ctuHistory[i][j] < minCtuTime + time_step)){
                setPSetToCTU(i,j,PS40);
                updateEstimationAndStats(-1,PS40);
            }
            
            else if(ctuHistory[i][j] >= minCtuTime + time_step and (ctuHistory[i][j] < minCtuTime + 2*time_step)){
                setPSetToCTU(i,j,PS40);
                updateEstimationAndStats(-1,PS40);
            }
            else if((ctuHistory[i][j] >= minCtuTime + 2*time_step) and (ctuHistory[i][j] < minCtuTime + 3*time_step)){
                setPSetToCTU(i,j,PS60);
                updateEstimationAndStats(-1,PS60);
            }
            else if((ctuHistory[i][j] >= minCtuTime + 3*time_step) and (ctuHistory[i][j] < minCtuTime + 4*time_step)){
                setPSetToCTU(i,j,PS80);
                updateEstimationAndStats(-1,PS80);
            }
            else{
                setPSetToCTU(i,j,PS100);
                updateEstimationAndStats(-1,PS100);
            }
        }
    }
    
           // second step - start demoting until available computation is reached
    

    
    UInt demote_pset = PS100;

    // second step - start demoting until available computation is reached
    while(demote_pset < PS20){ // maximum #iterations -- all PSETs are already set to PS20
        for(int i = 0; i < ctuHistory.size() and estimatedTime > frameBudget; i++){
            for(int j = 0; j < ctuHistory[0].size() and estimatedTime > frameBudget; j++){
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
    
    UInt promote_pset = PS20;
    
    while(promote_pset > PS100){ // maximum #iterations -- all PSETs are already set to PS100
        for(int i = 0; i < ctuHistory.size() and estimatedTime < frameBudget; i++){
            for(int j = 0; j < ctuHistory[0].size() and estimatedTime < frameBudget; j++){
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
    
    maxCtuTime = 0.0;
    minCtuTime = MAX_INT;
}




// conf 0 = low, 1 = medL, 2 = medH, 3 = high

void TComComplexityBudgeter::updateEstimationAndStats(Int old_pset, UInt new_pset){
    double nCU = (picHeight*picWidth)/(64.0*64.0);
   

    if (old_pset != -1)
        psetCounter[old_pset]--;
    psetCounter[new_pset]++;
       
    if (old_pset != -1)
        estimatedTime -= estimateCycleCount(old_pset)/nCU;
    estimatedTime += estimateCycleCount(new_pset)/nCU;
    
}

Void TComComplexityBudgeter::setPSetToCTU(UInt i, UInt j, UInt pset){
               
            psetMap[i][j][0] = PSET_TABLE[pset][0]; // Max CU Depth
            psetMap[i][j][1] = PSET_TABLE[pset][1]; // Max TU Depth
            psetMap[i][j][2] = PSET_TABLE[pset][2]; // AMP
            psetMap[i][j][3] = PSET_TABLE[pset][3]; // SR
            psetMap[i][j][4] = PSET_TABLE[pset][4]; // HAD ME
            psetMap[i][j][5] = PSET_TABLE[pset][5]; // Max Num Ref Pics
            psetMap[i][j][6] = PSET_TABLE[pset][6]; // FME
            psetMap[i][j][NUM_PARAMS] = pset;

}

Double TComComplexityBudgeter::estimateCycleCount(UInt conf){
    Double factor = 0.0;
    switch (conf){
        case PS100: factor = 1.0; break; //PS100
        case PS80: factor = 0.8; break; //PS80
        case PS60: factor = 0.6; break; //PS60
        case PS40: factor = 0.4; break; //PS40
        case PS20: factor = 0.2; break; //PS20
        default: factor = 1.0; break;
    }

    return TComComplexityController::avgPV*factor;
            
}

Void TComComplexityBudgeter::distributeBudget(){
    resetBudgetStats();

    switch(budgetAlgorithm){
        case 0: uniformEstimationBudget(); break;
        case 1: uniformIncrementalBudget(); break;
        case 2: bottomUpBudget(); break;
        case 3: ICIPBudget(); break;
        case 4: setPSetToAllCTUs(); break;
        default: uniformEstimationBudget(); break;
    }
    
    printBudgetStats();

}

Void TComComplexityBudgeter::resetBudgetStats(){

    for (int i = 0; i < NUM_PSETS; i++)
         psetCounter[i] = 0;
}

Void TComComplexityBudgeter::printBudgetStats(){
    
    if(!budgetFile.is_open()){
        budgetFile.open("budgetDistribution.csv",ofstream::out);
        budgetFile << "PS100\tPS80\tPS60\tPS40\tPS20" << endl;
    }

    Double total = 0.0;
    for (int i = 0; i < NUM_PSETS; i++)
        total += psetCounter[i];
    
    for (int i = 0; i < NUM_PSETS; i++)
        budgetFile << (Double) psetCounter[i]/total << "\t";

    budgetFile << endl;
}

Void TComComplexityBudgeter::setFrameBudget(Double budget){
    frameBudget = budget;
}




