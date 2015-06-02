from operator import itemgetter

def getNextCfg(optParams, BDRateCostList, target):
	sortedBD = (sorted(BDRateCostList.items(), key=lambda x: x[1][0])) # sort by time savings
	print sortedBD
	currCfg = getCfgString(optParams)

	bestCost = 10.0
	bestCfg = ''
	currSavings = 0.0
	if optParams:
		currSavings = BDRateCostList[currCfg][0]

	while bestCfg == '':
		for cfg, timeandbdinc in sortedBD:
			if any(x in currCfg for x in cfg.split('_')): continue

			[timeSavings, bdInc] = timeandbdinc
			if (timeSavings+currSavings) <= target:
				bdTimeCost = bdInc / timeSavings
				if bdTimeCost < bestCost:
					bestCost = bdTimeCost
					bestCfg = cfg
					currSavings = timeSavings+currSavings
		currCfg = '_'.join(currCfg.split('_')[1:])

	return joinConfigs(currCfg, bestCfg)


def joinConfigs(cfg1, cfg2):
	params1 = cfg1.split('_')
	params2 = cfg2.split('_')
	if params1 != ['']:
		jointParams = sorted(params1+params2)
	else:
		jointParams = sorted(params2)
	return (' --'+' --'.join(jointParams))

def getCfgString(optParams):
	return '_'.join([x.strip('--') for x in optParams.split()])

BDRateCostList = {'CUD': [0.2,0.15], 'TUD': [0.1,0.1], 'AMP': [0.2,0.2], 'SR': [0.15,0.1], 'HAD': [0.3,0.35], 'FME': [0.5,0.5], 'REFS': [0.3,0.2], 'RDOQ': [0.15,0.2], 'RECT': [0.2,0.1]}
TARGET_POINTS = [float(x)/10 for x in range(9,0,-1)]
config = ''
for target in TARGET_POINTS:
	print 'Target :', target, ' ',
	config = getNextCfg(config, BDRateCostList, 0.1)
	print config