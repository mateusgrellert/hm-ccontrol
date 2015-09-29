from sys import argv
import os

# Control: SP = line[3]    PV = line[4]    AVG PV = line[6]    PID = line[7]
# Budget: 

def parseControlOutput(fileLines):
	control = []
	budget = []
	avg_Pv = 0.0
	leng = 0
	for line in fileLines:
		if '@control' in line and 'SP' not in line:
			line = line.split('\t')
			[sp, pv, gopPv, avgPv, pid] = line[3:8]
			controlStr = '%s\t%s' % (sp, avgPv)
			avg_Pv += float(pv)
			leng += 1
			control.append(controlStr)

		elif '@budget' in line and 'PS' not in line:
			line = line.split('\t')
			budgets = line[1:-1]
			budgetStr = '%s\t' % ('/'.join(budgets))
			budget.append(budgetStr)

	control.append(('\t%f' % (avg_Pv/leng)))
	budget.append('\t\t')
	return [control, budget]






if len(argv) < 4:
	print  'USAGE: python parseControlResults.py [hmOutputPath] [sequence] [numFrames]'
	exit()

resultsPath = argv[1]
sequence = argv[2]
numFrames = int(argv[3])

foutC = open('parsedControl_'+sequence+'.csv','w')
foutB = open('parsedBudget_'+sequence+'.csv','w')

qps = ['22','27','32','37']
#qps=['22']

for qp in qps:
	print >> foutC, 'QP=', qp
	print >> foutB, 'QP=', qp
	controlVet = [None]*(numFrames+2)
	budgetVet = [None]*(numFrames+2)

	for p in os.listdir(resultsPath):
		if sequence.lower() in p.lower() and qp in p.lower() and '_ref' not in p.lower():
			heading = p.split(qp+'_')[1].split('.')[0]
			heading = (heading.replace('pct', '% '))+'\t'
			if controlVet[0]:
				controlVet[0].append(heading)
				controlVet[1].append('SP\tPV')
			else:
				controlVet[0] = [heading]
				controlVet[1] = ['SP\tPV']


			if budgetVet[0]:
				budgetVet[0].append(heading)
				budgetVet[1].append('BudgetString\t')

			else:
				budgetVet[0] = [heading]
				budgetVet[1] = ['BudgetString\t']


			rawFile = open(resultsPath+p, 'r')
			[controlOut, budgetOut] = parseControlOutput(rawFile.readlines())
			rawFile.close()
			
			i = 2
			for x,y in zip(controlOut, budgetOut):
				if controlVet[i]:
					controlVet[i].append(x)
				else:
					controlVet[i] = [x]

				if budgetVet[i]:
					budgetVet[i].append(y)
				else:
					budgetVet[i] = [y]
				i += 1
	for c, b in zip(controlVet, budgetVet):
		if not c: break
		print >> foutC, '\t'.join(c)
		print >> foutB, '\t'.join(b)

foutC.close()
foutB.close()

