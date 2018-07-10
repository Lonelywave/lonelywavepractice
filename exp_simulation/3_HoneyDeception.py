import numpy as np

insiderGetFilesNumber = 0
	
# Insider initial, DLP, Oral, Detection, DLP Fail, Not Caught, Caught, Not Caught
def runI():
	print ('I State')
	randomNumber = (np.random.choice(8, 1, p=[0, 0.8, 0.2, 0, 0, 0, 0, 0]))[0]
	if randomNumber == 1:
		return 'DW'
	elif randomNumber == 2:
		return 'O'
	else:
		AssertionError()
		
def runDW():
	print ('DW State')
	randomNumber = (np.random.choice(8, 1, p=[0.8, 0, 0, 0, 0.2, 0, 0, 0]))[0]
	if randomNumber == 0:
		return 'I'
	elif randomNumber == 4:
		return 'DT'
	else:
		AssertionError()
		
def runO():
	print ('O State')
	randomNumber = (np.random.choice(8, 1, p=[0, 0, 0, 0, 0, 0.80, 0.20, 0]))[0]
	if randomNumber == 5:
		return 'NC2'
	elif randomNumber == 6:
		return 'C'
	else:
		AssertionError()

def runDS():
	print ('DS State')
	randomNumber = (np.random.choice(8, 1, p=[0, 0, 0, 0, 0, 0, 0.80, 0.20]))[0]
	if randomNumber == 6:
		return 'C'
	elif randomNumber == 7:
		return 'NC5'
	else:
		AssertionError()

def runDT():
	print ('DT State')
	randomNumber = (np.random.choice(8, 1, p=[0, 0, 0, 1, 0, 0, 0, 0]))[0]
	if randomNumber == 3:
		return 'DS'
	else:
		AssertionError()
		
# gameover or not
def gameoverChecker(nextState):
	global insiderGetFilesNumber
	# determine if is it gameover or not
	if nextState == 'C':
		return 'gameover'
	elif nextState == 'NC2':
		insiderGetFilesNumber = insiderGetFilesNumber + 2
		if insiderGetFilesNumber >= 200:
			insiderGetFilesNumber = 200
			return 'gameover'
		else:
			# Not caught so back to initial state
			return 'notcaught'
	elif nextState == 'NC5':
		insiderGetFilesNumber = insiderGetFilesNumber + 5
		if insiderGetFilesNumber >= 200:
			insiderGetFilesNumber = 200
			return 'gameover'
		else:
			# Not caught so back to initial state
			return 'notcaught'
	else:
		return 'donext' 
		
def main(index):
	global insiderGetFilesNumber
	# initial variable
	TOTALFILES = 200
	insiderGetFilesNumber = 0
	currentstate = 'I'
	stateList = ['I', 'DW', 'O', 'DS', 'DT', 'NC2', 'C', 'NC5']
	whichround = 1
	while True:
		nextState = ''
		# in different state, run different random function
		if currentstate == 'I':
			nextState = runI()
		elif currentstate == 'DW':
			nextState = runDW()
		elif currentstate == 'O':
			nextState = runO()
		elif currentstate == 'DS':
			nextState = runDS()
		elif currentstate == 'DT':
			nextState = runDT()
		else:
			AssertionError()
			
		print ('next' + nextState)
		
		result = gameoverChecker(nextState)
		if result == 'gameover':
			break
		elif result == 'notcaught':
			currentstate = 'I'
			whichround = whichround + 1
		else:
			currentstate = nextState
			
	# Final Result
	#print (str(index+1) + ', ' + str(TOTALFILES) + ', ' + str(insiderGetFilesNumber) + ', ' + str(whichround) + '\n')
	with open('Our_new2000times_200files.csv', 'a') as the_file:
		the_file.write( str(index+1) + ', ' + str(TOTALFILES) + ', ' + str(insiderGetFilesNumber) + ', ' + str(whichround) + '\n')
	
for index in range(2000):
	main(index)