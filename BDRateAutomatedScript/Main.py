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
		

		for testIdx in range(Configuration.N_TESTS):
			testBDResults = []
			testTimeResults = []
			optParams = Configuration.optParamsTestList[testIdx]
			pathToBin = Configuration.pathToTestBinList[testIdx]

			if Configuration.RUN_TEST:
				Parallel(n_jobs=Configuration.NUM_THREADS)(delayed(runParallelSims)(sequence,numFrames, gopStructure, qp, pathToBin, optParams, 'test', testIdx) for qp in Configuration.qpList)	

			for qp in Configuration.qpList:
				[gopPath, seqPath, resultsPath] = treatConfig(sequence, gopStructure, qp, 'test', testIdx)
				[bd, time] = parseOutput(resultsPath)
				rdFileLine[qp] += '\t'.join([str(x) for x in bd+[time]]) + '\t'
				testBDResults.append(bd)
				testTimeResults.append(time)

			timeSavings = 1.0-(sum(testTimeResults)/sum(refTimeResults))
			bdRates = '\t'.join(["%.2f" % (bdrate(refBDResults, testBDResults, i)) for i in range(1,2)])
			print >> bdRateFile, '\t%s\t%.3f' % (bdRates, timeSavings),
		for qp in Configuration.qpList:
			print >> rdValuesFile, rdFileLine[qp]

		print >> bdRateFile, '\n',

	bdRateFile.close()
	rdValuesFile.close()