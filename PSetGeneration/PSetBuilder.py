import operator

def getNextCfg(currCmd, costList):
	sortedBD = sorted(costList.items(), key=lambda x: x[1][2]) # sort by [1][0] -- BD-BR INC, [1][1] -- TIME SAVINGS, [1][2] -- RDCCost
	currCfgStr = getCfgString(currCmd)
	if not currCfgStr:
		currCfgStr = sortedBD[1][0]

	for cfg, time_bdinc_rdccost in sortedBD:
		[bdInc, timeSavings, rdccost] = time_bdinc_rdccost
		jointCfg = joinConfigs(currCfgStr, cfg)
		if jointCfg not in costList.keys():
			return getCmdString(jointCfg)

			
	return False

	
def removeParamIfExists(currCfg, param):
	if param:
		[p,val] = param.split('=')
		currParams = currCfg.split('_')
		for currP_Val in currParams:
			currP = currP_Val.split('=')[0]
			if p == currP:
				currParams.remove(currP_Val)
		return '_'.join(currParams)
	else: return currCfg


def joinConfigs(cfg, params):
	for param in params.split('_'):
		cfg = removeParamIfExists(cfg, param)
	currParams = sorted(cfg.split('_') + params.split('_'))
	return ('_'.join([x for x in currParams if x]))
	
def getCfgString(commandLine):
	return '_'.join([x.strip('--') for x in sorted(commandLine.split())])

def getCmdString(cfg):
	return ' --'+(' --'.join(cfg.split('_')))

def allTargetsCovered(costList):
	TARGET_POINTS = [float(x)/10 for x in range(9,0,-1)]
	sortedBD = sorted(costList.items(), key=lambda x: x[1][2]) # sort by [1][0] -- BD-BR INC, [1][1] -- TIME SAVINGS, [1][2] -- RDCCost
	error = 0.05
	for target in TARGET_POINTS:
		covered = False
		for cfg, time_bdinc_rdccost in sortedBD:
			[bdInc, timeSavings, rdccost] = time_bdinc_rdccost
			if ((1.0-error)*timeSavings <= target and target <= (1.0+error)*timeSavings):
				covered = True

		if not(covered): return False
	return True

#  PARAM: [BD-BR INC, TIME SAVINGS, RDCCost]
BDRateCostList = {'': [0, 0, 0], 'SearchRange=32': [0.01, 0.0327, 0.0005], 'BipredSearchRange=2': [0.02, 0.0516, 0.0011], 'QuadtreeTUMaxDepthInter=2': [0.03, 0.0980, 0.0030], 'TestRect=0.9': [0.04, 0.0502, 0.0018], 'TestRect=0.7': [0.04, 0.1339, 0.0055], 'TestRect=0.8': [0.04, 0.0939, 0.0039], 'TestRect=0.3': [0.04, 0.3139, 0.0135], 'TestRect=0.2': [0.05, 0.3527, 0.0167], 'TestRect=0.6': [0.05, 0.1788, 0.0085], 'TestRect=0.1': [0.05, 0.3952, 0.0190], 'TestRect=0': [0.05, 0.4346, 0.0213], 'TestRect=0.4': [0.05, 0.2652, 0.0133], 'TestRect=0.5': [0.06, 0.2213, 0.0123], 'BipredSearchRange=0': [0.07, 0.0689, 0.0045], 'SearchRange=8': [0.07, 0.0560, 0.0037], 'QuadtreeTUMaxDepthInter=1': [0.08, 0.1611, 0.0131], 'AMP=0': [0.10, 0.1029, 0.0100], 'RefFrames=3': [0.12, 0.1573, 0.0188], 'HadamardME=0': [0.15, 0.0882, 0.0133], 'RefFrames=2': [0.16, 0.3094, 0.0480], 'FME=1': [0.16, 0.2427, 0.0389], 'MaxPartitionDepth=3': [0.25, 0.2281, 0.0567], 'RefFrames=1': [0.28, 0.4511, 0.1253], 'FME=0': [0.35, 0.4085, 0.1410], 'SearchRange=0': [0.42, 0.0903, 0.0378], 'RDOQ=0': [0.43, 0.0740, 0.0316], 'MaxPartitionDepth=2': [0.44, 0.5594, 0.2460], 'FME=2': [0.81, 0.1878, 0.1520], 'MaxPartitionDepth=1': [0.85, 0.7695, 0.6504]}

