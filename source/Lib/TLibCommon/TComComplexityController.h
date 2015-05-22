/* 
 * File:   TComComplexityController.h
 * Author: mateusgrellert
 *
 * Created on November 27, 2012, 5:14 PM
 */

#include "TComComplexityManagement.h"

#ifndef TCOMCOMPLEXITYCONTROLLER_H
#define	TCOMCOMPLEXITYCONTROLLER_H

class TComComplexityController {

public:
    static double targetSavings;
    static double SP;
    static double PV, accumPV, avgPV, gopPV;
    static double kp, ki, kd;
    static double error, prevError, accumError;
    static double controlOutput;
    static double frameTime;
    static unsigned int frameCount;
    static unsigned int trainingPeriod;
    static int gopSize, currPoc;
    static clock_t tBegin;
    static std::ofstream pidFile;

    
    static bool controlActive;
    
    TComComplexityController();
    
    static void init(int gop);
    static void updateSP();
    static void updatePV();

    static double calcPID();
    
    static void beginFrameTimer();
    static void endFrameTimer();
    
    static bool activateControl(int poc);
    static void openPidFile();
    static void printControlStats(double estimatedTime);



};

#endif	/* TCOMCOMPLEXITYCONTROLLER_H */

