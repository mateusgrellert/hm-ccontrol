/* 
 * File:   TComComplexityManagement.h
 * Author: mateusgrellert
 *
 * Created on December 6, 2012, 6:15 PM
 */

#ifndef TCOMCOMPLEXITYMANAGEMENT_H
#define	TCOMCOMPLEXITYMANAGEMENT_H

#define TEST_RECT_GOP 8
#define TILE_LEVEL_TEST_RECT 0

#define EN_COMPLEXITY_MANAGING 0
#define NUM_RD_FRAMES 5
#define DISPLAY_VERBOSE 1

#define CONTROL_ERROR 0.05  // 5% error

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
#define PS100 10
// bipred sr, sr, testrect, tu depth, amp, had me, num refs, rdoq, fme, cu depth, 
const int PSET_TABLE[NUM_PSETS][NUM_PARAMS] = {
  // BI | SR | RCT | TU | AMP | HAD | RFS | RDQ | FME | CUD
    {4,   64,  10,   3,   1,    1,    4,    1,     3,    4},  //0%
    //{2,    8,   0,   1,   0,    0,    2,    0,     1,    3},  //10%
    {2,   64,  10,   2,   1,    1,    4,    1,     3,    4},  //10%
    {0,   32,   9,   2,   1,    1,    4,    1,     3,    4},  //20%
    {2,    8,   7,   2,   1,    1,    4,    1,     3,    4},  //30%
    {2,   64,   3,   2,   1,    1,    4,    1,     3,    4},  //40%
    {4,   64,   0,   2,   1,    1,    4,    1,     3,    4},  //50%
    {2,    8,   1,   2,   0,    1,    4,    1,     3,    4},  //60%
    {0,   32,   0,   2,   0,    1,    3,    1,     3,    4},  //70%
    {0,   32,   0,   1,   0,    0,    3,    0,     3,    4},  //80%
    {2,    8,   0,   1,   0,    0,    2,    0,     1,    3},  //90%
    //{2,    1,   0,   1,   0,    0,    1,    0,     1,    3},  //100%
};

#include <fstream>
#include "TComMotionInfo.h"
#include "TComDataCU.h"
#include "TLibEncoder/TEncCfg.h"
#include "TComSlice.h"
#include "TLibEncoder/TEncSearch.h"
#include "TypeDef.h"
#include <string>

#endif	/* TCOMCOMPLEXITYMANAGEMENT_H */

