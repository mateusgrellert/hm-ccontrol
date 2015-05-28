TARGET_POINTS = [float(x)/10 for x in range(9,0,-1)]

def getNextCfg(optParams, BDRateCostList, target):
	sortedBD = sorted(BDRateCostList.items(), key=operator.itemgetter(1)[0]) # sort by time savings
	bestCost = 1.0
	currCfg = getCfgString(optParams)

	for cfg, timeandbdinc in sortedBD.items():
		if any(x in currCfg for x in cfg.split('_')): continue

		[timeSavings, bdInc] = timeandbdinc
		if timeSavings <= target:
			bdTimeCost = bdinc / timeSavings
			if bdTimeCost < bestCost:
				bestCost = bdTimeCost
				bestCfg = cfg
	return joinConfigs(currCfg, bestCfg)

def joinConfigs(cfg1, cfg2):
	params1 = cfg1.split('_')
	params2 = cfg2.split('_')
	jointParams = sorted(params1+params2)
	return (' --'+' --'.join(jointParams))

def getCfgString(optParams):
	return '_'.join([x.strip('--') for x in optParams.split()])
