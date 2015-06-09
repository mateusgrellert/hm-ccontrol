from Bjontegaard import *
from Utilities import *
import Configuration
import os
from joblib import Parallel, delayed  
import multiprocessing

for gopStructure in Configuration.gopStructureList:
	bdRateFile = makeBDRateFile(gopStructure)
	rdValuesFile = makeRDValuesFile(gopStructure)
	for [sequence, numFrames] in Configuration.sequenceList:
		print >> bdRateFile, sequence,

		refBDResults = []
		refTimeResults = []
		optParams = Configuration.optParamsRef
		pathToBin = Configuration.pathToRefBin
		rdFileLine = {}
		if Configuration.RUN_REFERENCE:
			Parallel(n_jobs=Configuration.NUM_THREADS)(delayed(runParallelSims)(sequence,numFrames, gopStructure, qp, pathToBin, optParams, 'ref') for qp in Configuration.qpList)


		for qp in Configuration.qpList:
			[gopPath, seqPath, resultsPath] = treatConfig(sequence, gopStructure, qp, 'ref')
			[bd, time] = parseOutput(resultsPath)
			rdFileLine[qp] = '\t'.join([str(x) for x in [sequence]+[qp]+bd+[time]]) + '\t'

			refBDResults.append(bd)
			refTimeResults.append(time)
	for target in PSetBuilder.TARGET_POINTS:
		currCfg = ''
		avgTimeSavings = 0.0
		avgBdrateIncY = 0.0
		while avgTimeSavings < target:
			for [sequence, numFrames] in Configuration.sequenceList:	
				testBDResults = []
				testTimeResults = []
				timeSavings = 0.0
				bdrateIncY = 0.0

				currCfg = PSetBuilder.getNextCfg(currCfg, BDRateCostList, target, timeSavings)
				testName = PSetBuilder.getCfgName(currCfg)
				pathToBin = Configuration.pathToRefBin

				if Configuration.RUN_TEST:
					Parallel(n_jobs=Configuration.NUM_THREADS)(delayed(runParallelSims)(sequence,numFrames, gopStructure, qp, pathToBin, currCfg, 'test', testName) for qp in Configuration.qpList)	

				for qp in Configuration.qpList:
					[gopPath, seqPath, resultsPath] = treatConfig(sequence, gopStructure, qp, 'test', testName)
					[bd, time] = parseOutput(resultsPath)
					rdFileLine[qp] += '\t'.join([str(x) for x in bd+[time]]) + '\t'
					testBDResults.append(bd)
					testTimeResults.append(time)

				timeSavings = 1.0-(sum(testTimeResults)/sum(refTimeResults))
				avgTimeSavings += timeSavings

				bdrateIncY = bdrate(refBDResults, testBDResults, 1)/100
				bdrateIncU = bdrate(refBDResults, testBDResults, 2)/100
				bdrateIncV = bdrate(refBDResults, testBDResults, 3)/100
				avgBdrateIncY += bdrateIncY

				bdRates = '\t'.join(["%.2f" % (x) for x in [bdrateIncY]])

				
			for qp in Configuration.qpList:
				print >> rdValuesFile, rdFileLine[qp]

			print >> bdRateFile, '\n',

	bdRateFile.close()
	rdValuesFile.close()
