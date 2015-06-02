import operator

TARGET_POINTS = [float(x)/10 for x in range(9,0,-1)]

def getNextCfg(optParams, BDRateCostList, target, currBDBRInc):
	sortedBD = sorted(BDRateCostList.items(), key=lambda x: x[1][0]) # sort by [1][0] -- BD-BR INC, [1][1] -- TIME SAVINGS
	bestCost = 100.0
	bestSavings = 0.0
	bestParam = ''
	currCfg = getCfgString(optParams)
	
	# find param closest to target
	i = 0
	for param, timeandbdinc in sortedBD:
		[bdInc, timeSavings] = timeandbdinc
		if timeSavings <= target:
			bestCost = bdInc
			bestParam = param
			bestSavings = timeSavings
			bestIdx = i
		elif timeSavings > target:
			nextCost = bdInc
			nextParam = param
			nextSavings = timeSavings
			nextIdx = i
			break
		i += 1
	
	i = 0
	while bestParam in currCfg and i < bestIdx:
		bestParam = sortedBD[i][0]
		i+=1


	if bestParam in currCfg or (currBDBRInc > nextCost): #flush current CFG
		currCfg = ''
		bestParam = nextParam

	return joinConfigs(currCfg, bestParam)
	
def removeParamIfExists(currCfg, param):
	[p,val] = param.split('=')
	currParams = currCfg.split('_')
	for currP in currParams:
		if p in currP:
			currParams.remove(currP)
	return '_'.join(currParams)


def joinConfigs(cfg, param):
	cfg = removeParamIfExists(cfg, param)
	currParams = cfg.split('_')
	if currParams != ['']:
		jointParams = sorted(currParams+ [param])
		return (' --'+' --'.join(jointParams))
	else:
		return ' --'+param

def getCfgString(optParams):
	return '_'.join([x.strip('--') for x in optParams.split()])


#  PARAM: [BD-BR INC, TIME SAVINGS]
BDRateCostList = {'SearchRange=32': [ 0.03 ,  1.34 ], 'QuadtreeTUMaxDepthInter=2': [ 0.33 ,  12.97 ], 'TestRect=0': [ 2.1 ,  36.25 ],\
				  'QuadtreeTUMaxDepthInter=1': [ 1.53 ,  23.09 ], 'AMP=0': [ 0.97 ,  13.63 ], 'SearchRange=8': [ 0.3 ,  2.29 ], 'HadamardME=0': [ 1.06 ,  5.72 ], \
				  'MaxPartitionDepth=3': [ 5.79 ,  24.31 ], 'FME=1': [ 4.38 ,  16.69 ], 'RefFrames=1': [ 8.99 ,  31.05 ], 'RefFrames=2': [ 7.42 ,  20.24 ], \
				  'MaxPartitionDepth=2': [ 24.68 ,  56.71 ], 'FME=0': [ 15.9 ,  29.5 ], 'MaxPartitionDepth=1': [ 63.63 ,  78.04 ], 'SearchRange=0': [ 3.69 ,  3.82 ], 'FME=2': [ 16.18 ,  13.68 ]}
#visited = {'SearchRange=32': False, 'QuadtreeTUMaxDepthInter=2': False, 'TestRect=0': False, 'QuadtreeTUMaxDepthInter=1': False, 'AMP=0': False, 'SearchRange=8': False, 'HadamardME=0': False, 'MaxPartitionDepth=3': False, 'FME=1': False, 'RefFrames=1': False, 'RefFrames=2': False, 'MaxPartitionDepth=2': False, 'FME=0': False, 'MaxPartitionDepth=1': False, 'SearchRange=0': False, 'FME=2': False}

while True:
	target = float(raw_input('Target: '))
	optParams = ''
	currSavings = 0.0
	currBDBRInc = 0.0
	while currSavings < target:
		optParams = getNextCfg(optParams, BDRateCostList, target, currBDBRInc)
		print optParams
		currSavings = float(raw_input('Savings: '))
		currBDBRInc = float(raw_input('BDBR: '))
