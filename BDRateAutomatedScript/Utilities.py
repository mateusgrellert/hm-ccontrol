from Bjontegaard import *
import Configuration
import re
import os
from joblib import Parallel, delayed  
import multiprocessing

def treatConfig(sequence, gopStructure, qp, mode, testIdx = 0):
	gopStructure = gopStructure.split('.cfg')[0]
	sequence = sequence.split('.cfg')[0]
	cfgPath = Configuration.cfgPath.rstrip('/')
	hmOutputPath = Configuration.hmOutputPath.rstrip('/')
	sequencePath = Configuration.sequencePath.rstrip('/')

	gopPath = cfgPath + '/' + gopStructure + '.cfg'
	seqPath = sequencePath + '/' + sequence + '.cfg'
	
	if mode == 'ref':
		resultsPath = hmOutputPath+'/hmOut_%s_%s_QP%s_REF.txt' % (sequence, gopStructure, qp)
	else:
		resultsPath = hmOutputPath+'/hmOut_%s_%s_QP%s_%s.txt' % (sequence, gopStructure, qp, Configuration.testNameList[testIdx])

	return [gopPath, seqPath, resultsPath]

def parseOutput(resultsPath):
	hmResults = open(resultsPath, 'r').read()
	rd_pattern = '\s+\d+\s+a\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+).*'
	time_pattern = 'Total\s+Time\:\s+(\d+\.\d+)\s+.*'
	p = re.compile(rd_pattern + time_pattern, re.S)
	try:
		result = p.findall(hmResults)[0]
		return [[float(x) for x in result[:-1]], float(result[-1])]
	except:
		print 'Could not parse results for ', resultsPath, '. Skipping this test.'
		return False

def makeBDRateFile(gopStructure):
	bdRateFile = open('BDResults_' + gopStructure + '.csv', 'w')
	print >> bdRateFile, '\t'+'\t\t'.join(Configuration.testNameList)
	print >> bdRateFile, 'Sequence\t' + '\t'.join(['BD-BR Y\tTime Savings']*Configuration.N_TESTS)
	return bdRateFile

def makeRDValuesFile(gopStructure):
	rdRateFile = open('RDResults_' + gopStructure + '.csv', 'w')
	print >> rdRateFile, '\t\t'+'\t\t\t\t\t'.join(['Reference'] + Configuration.testNameList)
	print >> rdRateFile, 'Sequence\tQP\t' + '\t'.join(['Bitrate\tPSNR-Y\tPSNR-U\tPSNR-V\tEnc. Time']*(Configuration.N_TESTS+1))
	return rdRateFile



def runParallelSims(sequence,numFrames, gopStructure, qp, pathToBin, optParams, mode, testIdx=0):
	[gopPath, seqPath, resultsPath] = treatConfig(sequence, gopStructure, qp, mode, testIdx)
	if os.path.isfile(resultsPath):
		return
	cmdLine = '%s -c %s -c %s -q %s %s > %s 2> %s_warn.txt' % (pathToBin, gopPath, seqPath, qp, optParams, resultsPath, resultsPath)
	if numFrames:
		cmdLine += ' -f ' + str(numFrames)
	os.system(cmdLine)

def calcAndPrintBDRate(refTimeResults,refBDResults,testTimeResults,testBDResults, bdRateFile):
	if any('N/A' == x for x in testTimeResults + refTimeResults) or any('N/A' == x for x in testBDResults + refBDResults):
		timeSavings = 'N/A'
		bdRates = 'N/A'
		print >> bdRateFile, '\t%s\t%s' % (bdRates, timeSavings),
	else:
		timeSavings = 1.0-(sum(testTimeResults)/sum(refTimeResults))
		bdRates = '\t'.join(["%.2f" % (bdrate(refBDResults, testBDResults, i)) for i in range(1,2)])
		print >> bdRateFile, '\t%s\t%.3f' % (bdRates, timeSavings),