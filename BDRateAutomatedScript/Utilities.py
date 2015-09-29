from Bjontegaard import *
import Configuration
import re
import os
from joblib import Parallel, delayed  


def treatConfig(sequence, gopStructure, qp, mode, complement = 0):
	gopStructure = gopStructure.split('.cfg')[0]
	sequence = sequence.split('.cfg')[0]
	cfgPath = Configuration.cfgPath.rstrip('/')
	hmOutputPath = Configuration.hmOutputPath.rstrip('/').lower()
	sequencePath = Configuration.sequencePath.rstrip('/')

	gopPath = cfgPath + '/' + gopStructure + '.cfg'
	seqPath = sequencePath + '/' + sequence + '.cfg'
	
	if mode == 'ref':
		resultsPath = '/hmOut_%s_%s_QP%s_REF.txt' % (sequence, gopStructure, qp)
	elif mode == 'set point':
		resultsPath = '/hmOut_%s_%s_QP%s_%dpctSavings.txt' % (sequence, gopStructure, qp, complement)
	else:
		resultsPath = '/hmOut_%s_%s_QP%s_%s.txt' % (sequence, gopStructure, qp, Configuration.testNameList[complement])
	
	resultsPath = hmOutputPath+ (resultsPath.lower())

	return [gopPath, seqPath, resultsPath]

def parseOutput(resultsPath):
	hmResults = open(resultsPath, 'r').read()
	rd_pattern = '\s+\d+\s+a\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+).*'
	#time_pattern = 'Total\s+Time\:\s+(\d+\.\d+)\s+.*'
	time_pattern = '\[ET\s+(\d+\.\d+)\s+\]'

	rd = re.compile(rd_pattern, re.S)
	time = re.compile(time_pattern, re.S)
	try:
		rd_result = rd.findall(hmResults)[0]
		time_result = sum([ float(x) for x in time.findall(hmResults)][4:])
		return [[float(x) for x in rd_result], time_result]
	except:
		print 'Could not parse results for ', resultsPath, '. Skipping this test.'
		return False

def makeBDRateFile(gopStructure, mode='other'):
	bdRateFile = open('BDResults_' + gopStructure + '.csv', 'w')
	if mode == 'set point':
		print >> bdRateFile, '\t'+'\t\t'.join([str(x) + 'pct savings' for x in Configuration.targetComplexityList])
	else:
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
	if os.path.isfile(resultsPath) or os.path.isfile(resultsPath.lower()) :
		return
	if numFrames:
		optParams += ' -f ' + str(numFrames)

	cmdLine = '%s -c %s -c %s -q %s %s > %s 2> /dev/null ' % (pathToBin, gopPath, seqPath, qp, optParams, resultsPath)	
	#cmdLine = '%s -c %s -c %s -q %s %s > %s ' % (pathToBin, gopPath, seqPath, qp, optParams, resultsPath)
	#print cmdLine
	os.system(cmdLine)

def runSetPointSims(sequence,numFrames, gopStructure, qp, pathToBin, optParams, mode, refTimeResults, savings=0):
	#sp = float(Configuration.setPointList[sequence][qp])*(1.0-(savings*1.0/100))
	sp = float(refTimeResults[Configuration.qpList.index(qp)])*((100.0-savings)/100.0)/numFrames
	optParams = ' --SP=%f --KP=1.0 --KI=0 --KD=0 -balg 0' % (sp)
	runParallelSims(sequence,numFrames, gopStructure, qp, pathToBin, optParams, mode, savings)

def calcAndPrintBDRate(refTimeResults,refBDResults,testTimeResults,testBDResults, bdRateFile):
	if any('N/A' == x for x in testTimeResults + refTimeResults) or any('N/A' == x for x in testBDResults + refBDResults):
		timeSavings = 'N/A'
		bdRates = 'N/A'
		print >> bdRateFile, '\t%s\t%s' % (bdRates, timeSavings),
	else:
		timeSavings = 1.0-(sum(testTimeResults)/sum(refTimeResults))
		bdRates = '\t'.join(["%.5f" % (bdrate(refBDResults, testBDResults, i)/100.0) for i in range(1,2)])
		print >> bdRateFile, '\t%s\t%.3f' % (bdRates, timeSavings),


