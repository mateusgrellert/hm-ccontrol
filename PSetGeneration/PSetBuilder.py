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


#  PARAM: [BD-BR INC, TIME SAVINGS, RDCCost]
BDRateCostList = {'SearchRange=32' : [0.033,0.000,0.014],'BipredSearchRange=2' : [0.052,0.001,0.022],'QuadtreeTUMaxDepthInter=2' : [0.098,0.003,0.031],'TestRect=0' : [0.435,0.021,0.049],'BipredSearchRange=0' : [0.069,0.005,0.066],'SearchRange=8' : [0.056,0.004,0.066],'QuadtreeTUMaxDepthInter=1' : [0.161,0.013,0.081],'AMP=0' : [0.103,0.010,0.098],'RefFrames=3' : [0.157,0.019,0.119],'HadamardME=0' : [0.088,0.013,0.151],'RefFrames=2' : [0.309,0.048,0.155],'FME=1' : [0.243,0.039,0.160],'MaxPartitionDepth=3' : [0.228,0.057,0.248],'RefFrames=1' : [0.451,0.125,0.278],'FME=0' : [0.409,0.141,0.345],'SearchRange=0' : [0.090,0.038,0.419],'RDOQ=0' : [0.074,0.032,0.427],'MaxPartitionDepth=2' : [0.559,0.246,0.440],'FME=2' : [0.188,0.152,0.809],'MaxPartitionDepth=1' : [0.770,0.650,0.845]}

#visited = {'SearchRange=32': False, 'QuadtreeTUMaxDepthInter=2': False, 'TestRect=0': False, 'QuadtreeTUMaxDepthInter=1': False, 'AMP=0': False, 'SearchRange=8': False, 'HadamardME=0': False, 'MaxPartitionDepth=3': False, 'FME=1': False, 'RefFrames=1': False, 'RefFrames=2': False, 'MaxPartitionDepth=2': False, 'FME=0': False, 'MaxPartitionDepth=1': False, 'SearchRange=0': False, 'FME=2': False}
