from Bjontegaard import *
from Utilities import *
import PSetBuilder
import Configuration
import os
#from joblib import Parallel, delayed  


for gopStructure in Configuration.gopStructureList:
	bdRateFile = makeBDRateFile(gopStructure)

	for [sequence, numFrames] in Configuration.sequenceList:
		print >> bdRateFile, sequence,

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


	for target in PSetBuilder.TARGET_POINTS:
		currCfg = ''
		avgTimeSavings = 0.0
		avgBdrateIncY = 0.0
		while avgTimeSavings < target:
			testBDResults = []
			testTimeResults = []
			for [sequence, numFrames] in Configuration.sequenceList:	

				timeSavings = 0.0
				bdrateIncY = 0.0

				currCfg = PSetBuilder.getNextCfg(currCfg, target, timeSavings)
				testName = PSetBuilder.getCfgName(currCfg)
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
				
				testBDResults.append(qpBDResults)
				testTimeResults.append(qpTimeResults)

				timeSavings = 1.0-(sum(testTimeResults)/sum(refTimeResults))
				avgTimeSavings += timeSavings

				bdrateIncY = bdrate(refBDResults, testBDResults, 1)/100
				bdrateIncU = bdrate(refBDResults, testBDResults, 2)/100
				bdrateIncV = bdrate(refBDResults, testBDResults, 3)/100
				avgBdrateIncY += bdrateIncY

				bdRates = '\t'.join(["%.2f" % (x) for x in [bdrateIncY]])

			avgTimeSavings /= len(Configuration.sequenceList)
			for i,j,k in zip(testTimeResults,testBDResults, Configuration.sequenceList):
				print >> bdRateFile, k,		
				calcAndPrintBDRate(refTimeResults,refBDResults,i,j, bdRateFile)
				print >> bdRateFile, '\n',		


	bdRateFile.close()
	rdValuesFile.close()
