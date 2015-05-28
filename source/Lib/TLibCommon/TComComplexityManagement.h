/* 
 * File:   TComComplexityManagement.h
 * Author: mateusgrellert
 *
 * Created on December 6, 2012, 6:15 PM
 */

#ifndef TCOMCOMPLEXITYMANAGEMENT_H
#define	TCOMCOMPLEXITYMANAGEMENT_H


#define EN_COMPLEXITY_MANAGING 0
#define NUM_RD_FRAMES 5

#define NUM_PARAMS 7 // cu depth, tu depth, AMP, SE, HAD ME, num ref frames, FME
#define NUM_PSETS 5
#define PS100 0
#define PS80 1
#define PS60 2
#define PS40 3
#define PS20 4

const int PSET_TABLE[NUM_PSETS][NUM_PARAMS] = {
    {4,3,1,64,1,4,1}, //100%
    {4,3,0,64,1,3,1}, //80%
    {4,1,0,64,0,4,1}, //60%
    {3,1,0,64,0,4,1}, //40%
    {2,1,0,64,0,2,1}  //20%
};

//    {2,1,0,64,0,1,1}  //20%
#include <fstream>
#include "TComMotionInfo.h"
#include "TComDataCU.h"
#include "TypeDef.h"


#endif	/* TCOMCOMPLEXITYMANAGEMENT_H */

