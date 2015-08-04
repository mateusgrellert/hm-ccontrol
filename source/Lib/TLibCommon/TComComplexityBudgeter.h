/* 
 * File:   TComComplexityBudgeter.h
 * Author: mateusgrellert
 *
 * Created on November 27, 2012, 5:14 PM
 */

#ifndef TCOMCOMPLEXITYBUDGETER_H
#define	TCOMCOMPLEXITYBUDGETER_H

#include "TComComplexityManagement.h"

#define BUDGET_UPDATE_PERIOD 10

using namespace std;

typedef vector<unsigned int> config;

class TComComplexityBudgeter {
    
public:
    static vector<vector <config> > psetMap;
    static vector<vector <double> > ctuHistory; //stores either depth or ctu time or anything that can be used to classify a ctu

    static long initCtuTime, endCtuTime;
    static double maxCtuTime, minCtuTime;
    static double frameBudget,estFrameTime;
    static unsigned int gopSize;
    static int psetCounter[NUM_PSETS], budgetCount;
    
    static unsigned int picWidth;
    static unsigned int picHeight;
    static unsigned int intraPeriod;

    static unsigned int currPoc;
    static unsigned int budgetAlgorithm;
    static unsigned int fixPSet;
    static int currPredSavings;
    
    static int searchRange, bipredSR;
    static bool hadME;
    static Int enFME;
    static bool testAMP;
    static unsigned int testSMP;
    static bool enRDOQ;
    static unsigned int maxNumRefPics;
    static unsigned int maxCUDepth;
    static unsigned int maxTUDepth;
    
    static ofstream budgetFile;
    
    
    TComComplexityBudgeter();
    
    static Void init(UInt, UInt, UInt);

    static Void printBudgetStats();
    static Void resetBudgetStats();
    
    static UInt promote(UInt, UInt);
    static UInt demote(UInt, UInt);
    
    static Void uniformBudget();
    static Void uniformEstimationBudget();
    static Void uniformIncrementalBudget();
    static Void bottomUpBudget();
    static Void priorityBasedBudget();
    static Void setPSetToAllCTUs();
    
    static Void distributeBudget();
    static void updateEstimationAndStats(Int old, UInt neww);

    static Void setDepthHistory(TComDataCU *&, UInt);
    static Void setTimeHistory(TComDataCU *&);
    
    static Void setFrameBudget(Double);
    static Double estimateTime(UInt);
    static Void updateConfig(TComDataCU*& cu);
    static Void resetConfig();
    static Void setPSetToCTU(UInt i, UInt j, UInt prof);

};


#endif	/* TCOMCOMPLEXITYBUDGETER_H */

