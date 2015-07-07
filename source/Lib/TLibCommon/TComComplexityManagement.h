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

#define NUM_PARAMS 10 
#define NUM_PSETS 10
#define PS0 0
#define PS10 1
#define PS20 2
#define PS30 3
#define PS40 4
#define PS50 5
#define PS60 6
#define PS70 7
#define PS80 8
#define PS90 9
// bipred sr, sr, testrect, tu depth, amp, had me, num refs, rdoq, fme, cu depth, 
const int PSET_TABLE[NUM_PSETS][NUM_PARAMS] = {
  // BI | SR | RCT | TU | AMP | HAD | RFS | RDQ | FME | CUD
    {4,   64,  10,   3,   1,    1,    4,    1,     3,    4},  //0%
    {2,   32,   9,   3,   1,    1,    4,    1,     3,    4},  //10%
    {2,    8,   9 ,  2,   1,    1,    4,    1,     3,    4},  //20%
    {2,   32,   6 ,  2,   1,    1,    4,    1,     3,    4},  //30%
    {2,   32,   7 ,  1,   0,    1,    4,    1,     3,    4},  //40%
    {0,   32,   9 ,  1,   0,    0,    4,    1,     3,    3},  //50%
    {0,    8,   3 ,  2,   0,    0,    4,    1,     3,    3},  //60%
    {2,    8,   0 ,  2,   0,    0,    4,    1,     3,    3},  //70%
    {0,   32,   0 ,  2,   0,    0,    4,    1,     1,    3},  //80%
    {2,   32,   1 ,  1,   0,    0,    4,    1,     1,    1},  //90%
};

#include <fstream>
#include "TComMotionInfo.h"
#include "TComDataCU.h"
#include "TypeDef.h"


#endif	/* TCOMCOMPLEXITYMANAGEMENT_H */

