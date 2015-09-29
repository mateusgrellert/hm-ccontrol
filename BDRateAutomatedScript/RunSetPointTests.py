from Bjontegaard import *
from Utilities import *
import Configuration
import os
from joblib import Parallel, delayed  


for gopStructure in Configuration.gopStructureList:
	bdRateFile = makeBDRateFile(gopStructure, 'set point')
	rdValuesFile = makeRDValuesFile(gopStructure)
	for [sequence, numFrames] in Configuration.sequenceList:
		print >> bdRateFile, sequence,

		refBDResults = []
		refTimeResults = []
		optParams = Configuration.optParamsRef
		pathToBin = Configuration.pathToRefBin
		rdFileLine = {}
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
				[bd, time] = parseOutput(resultsPath)
			else:
				[bd, time] = [['N/A'], 'N/A']
			rdFileLine[qp] = '\t'.join([str(x) for x in [sequence]+[qp]+bd+[time]]) + '\t'

			refBDResults.append(bd)
			refTimeResults.append(time)
		

		for savings in Configuration.targetComplexityList:
		#for savings in xrange(20,50,10):


			testBDResults = []
			testTimeResults = []
			pathToBin = '../bin/TAppEncoderStatic'
			testName = str(savings) + 'pct savings'

			if Configuration.RUN_TEST:
				if Configuration.RUN_PARALLEL:
					Parallel(n_jobs=Configuration.NUM_THREADS)(delayed(runSetPointSims)(sequence,numFrames, gopStructure, qp, pathToBin, optParams, 'set point', refTimeResults,savings) for qp in Configuration.qpList)
				else:
					for qp in Configuration.qpList:
						runSetPointSims(sequence,numFrames, gopStructure, qp, pathToBin, optParams, 'set point', refTimeResults,savings)

			for qp in Configuration.qpList:
				[gopPath, seqPath, resultsPath] = treatConfig(sequence, gopStructure, qp, 'set point', savings)
				parsed = parseOutput(resultsPath)
				if parsed:
					[bd, time] = parseOutput(resultsPath)
				else:
					[bd, time] = [['N/A'], 'N/A']
				rdFileLine[qp] += '\t'.join([str(x) for x in bd+[time]]) + '\t'
				testBDResults.append(bd)
				testTimeResults.append(time)

			calcAndPrintBDRate(refTimeResults,refBDResults,testTimeResults,testBDResults, bdRateFile)
		for qp in Configuration.qpList:
			print >> rdValuesFile, rdFileLine[qp]

		print >> bdRateFile, '\n',

	bdRateFile.close()
	rdValuesFile.close()
