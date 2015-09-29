import platform


def buildTestSet(path):
	inputFile = open(path, 'r')
	binList = []
	paramList = []
	testNameList = []
	for line in inputFile.readlines():
		if '#' in line or len(line.split()) < 3 : continue

		line = line.split()
		name = line[0]
		bin = line[1]
		params = ' --'.join(line[2:])
		binList.append(bin)
		testNameList.append(name)
		if params:
			paramList.append(' --'+params)
		else:
			paramList.append(' ')
	inputFile.close()
	
	return [testNameList, binList, paramList]


gopStructureList = ['encoder_lowdelay_main']
sequenceList = [['BQSquare', 64],['BlowingBubbles', 64], \
				['Traffic', 64],['PeopleOnStreet', 64], \
				['BasketballDrive', 64],['ParkScene', 64], \
				['RaceHorsesC', 64],['BQMall', 64], \
				['ChinaSpeed', 64],['BasketballDrillText', 64], \
				['Johnny', 64],  ['FourPeople',64]]
sequenceList = [['BQMall', 320]]
qpList = ['22', '27', '32', '37']

targetComplexityList = xrange(10,100,10)

setPointList = {'Traffic' : {'22': 87.12, '27': 67.03, '32': 57.81, '37': 51.67}, \
				'PeopleOnStreet' : {'22': 130.71, '27': 105.42, '32': 86.63, '37': 77.12}, \
				'Nebuta' : {'22': 0.00, '27': 0.00, '32': 0.00, '37': 0.00}, \
				'SteamLocomotive' : {'22': 0.00, '27': 0.00, '32': 0.00, '37': 0.00}, \
				'Kimono' : {'22': 57.76, '27': 48.38, '32': 40.81, '37': 35.38}, \
				'ParkScene' : {'22': 49.72, '27': 38.04, '32': 31.88, '37': 28.34}, \
				'Cactus' : {'22': 52.27, '27': 37.54, '32': 31.75, '37': 28.41}, \
				'BasketballDrive' : {'22': 60.20, '27': 47.26, '32': 39.67, '37': 34.94}, \
				'BQTerrace' : {'22': 61.33, '27': 37.96, '32': 29.56, '37': 25.92}, \
				'BasketballDrill' : {'22': 0.00, '27': 0.00, '32': 0.00, '37': 0.00}, \
				'BQMall' : {'22': 9.79, '27': 7.81, '32': 6.59, '37': 5.79}, \
				'PartyScene' : {'22': 12.71, '27': 9.36, '32': 7.41, '37': 6.13}, \
				'RaceHorsesC' : {'22': 15.81, '27': 12.10, '32': 9.81, '37': 8.28}, \
				'BasketballPass' : {'22': 1.91, '27': 1.62, '32': 1.38, '37': 1.21}, \
				'BQSquare' : {'22': 2.39, '27': 1.71, '32': 1.30, '37': 1.09}, \
				'BlowingBubbles' : {'22': 2.19, '27': 1.65, '32': 1.32, '37': 1.12}, \
				'RaceHorses' : {'22': 4.69, '27': 4.25, '32': 3.66, '37': 3.10}, \
				'FourPeople' : {'22': 13.23, '27': 11.06, '32': 10.20, '37': 9.75}, \
				'Johnny' : {'22': 12.96, '27': 10.68, '32': 9.89, '37': 9.45}, \
				'KristenAndSara' : {'22': 0.00, '27': 0.00, '32': 0.00, '37': 0.00}, \
				'BasketballDrillText' : {'22': 9.44, '27': 7.69, '32': 6.42, '37': 5.61}, \
				'ChinaSpeed' : {'22': 23.04, '27': 19.47, '32': 16.01, '37': 13.34}, \
				'SlideEditing' : {'22': 9.48, '27': 9.37, '32': 9.25, '37': 9.20}, \
				'SlideShow' : {'22': 12.88, '27': 12.32, '32': 11.73, '37': 11.17}}

cfgPath = '../cfg'
if platform.system() == 'Darwin':
	sequencePath = '/Users/grellert/hm-cfgs/cropped'
else:
	sequencePath = '/home/grellert/hm-cfgs/cropped'
hmOutputPath = './hmoutput'  #ESSA PASTA PRECISA EXISTIR! IDEALMENTE TUDO MINUSCULO NESSE NOME!


pathToRefBin = '../bin/TAppEncoderStatic_original'
optParamsRef = ''

[testNameList, pathToTestBinList, optParamsTestList] = buildTestSet('Tests.inp')

N_TESTS = len(pathToTestBinList)
RUN_REFERENCE = True
RUN_TEST = True
RUN_PARALLEL = True
NUM_THREADS = 4
