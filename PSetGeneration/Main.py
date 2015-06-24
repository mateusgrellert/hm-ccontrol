from Bjontegaard import *
from Utilities import *
import PSetBuilder
import Configuration
import os
#from joblib import Parallel, delayed  


for gopStructure in Configuration.gopStructureList:

	for [sequence, numFrames] in Configuration.sequenceList:

		refBDResults = []
		refTimeResults = []
		optParams = Configuration.optParamsRef
		pathToBin = Configuration.pathToRefBin

		if Configuration.RUN_REFERENCE:
			if Configuration.RUN_PARALLEL:
				Parallel(n_jobs=Configuration.NUM_THREADS)(delayed(runParallelSims)(sequence,numFrames, gopStructure, qp, pathToBin, optParams, 'ref') for qp in Configuration.qpList)
			else:
				for qp in Configuration.qpList:
					runParallelSims(sequence,numFrames, gopStructure, qp, pathToBin, optParams, 'ref') 


		for qp in Configuration.qpList:
			[gopPath, seqPath, resultsPath] = treatConfig(sequence, gopStructure, qp, 'ref')
			parsed = parseOutput(resultsPath)
			if parsed:
				[bd, time] = parsed
			else:
				[bd, time] = [['N/A'], 'N/A']

			refBDResults.append(bd)
			refTimeResults.append(time)

	currCfg = ''
	costList = PSetBuilder.BDRateCostList
	while not(PSetBuilder.allTargetsCovered(costList)):
		avgTimeSavings = 0.0
		avgBdrateIncY = 0.0

		testBDResults = []
		testTimeResults = []
		currCfg = PSetBuilder.getNextCfg(currCfg, costList)
		if not(currCfg):
			break
		testName = PSetBuilder.getCfgString(currCfg)
		
		for [sequence, numFrames] in Configuration.sequenceList:	
			timeSavings = 0.0
			bdrateIncY = 0.0
			pathToBin = Configuration.pathToRefBin

			if Configuration.RUN_TEST:
				if Configuration.RUN_PARALLEL:
					Parallel(n_jobs=Configuration.NUM_THREADS)(delayed(runParallelSims)(sequence,numFrames, gopStructure, qp, pathToBin, currCfg, 'test', testName) for qp in Configuration.qpList)	
				else:
					for qp in Configuration.qpList:
						runParallelSims(sequence,numFrames, gopStructure, qp, pathToBin, currCfg, 'test', testName)

			qpBDResults = []
			qpTimeResults = []
			for qp in Configuration.qpList:
				[gopPath, seqPath, resultsPath] = treatConfig(sequence, gopStructure, qp, 'test', testName)
				parsed = parseOutput(resultsPath)
				if parsed:
					[bd, time] = parsed
				else:
					[bd, time] = [['N/A'], 'N/A']
				qpBDResults.append(bd)
				qpTimeResults.append(time)
			
#			testBDResults.append(qpBDResults)
#			testTimeResults.append(qpTimeResults)
			testBDResults = qpBDResults
			testTimeResults = qpTimeResults

			timeSavings = 1.0-(sum(testTimeResults)/sum(refTimeResults))
			avgTimeSavings += timeSavings

			bdrateIncY = bdrate(refBDResults, testBDResults, 1)/100
			bdrateIncU = bdrate(refBDResults, testBDResults, 2)/100
			bdrateIncV = bdrate(refBDResults, testBDResults, 3)/100
			avgBdrateIncY += bdrateIncY


		avgTimeSavings /= len(Configuration.sequenceList)*1.0
		if avgTimeSavings < 0: avgTimeSavings = 0.0001
		avgBdrateIncY /= len(Configuration.sequenceList)*1.0
		RDCompCost = float(avgBdrateIncY/avgTimeSavings)
		costList[testName] = [avgBdrateIncY, avgTimeSavings, RDCompCost]
		print '%s: TS=%.2f, BD-BR=%.3f, RDCC=%.2f' % (testName, avgTimeSavings, avgBdrateIncY, RDCompCost)

	bdRateFile.close()
	rdValuesFile.close()
