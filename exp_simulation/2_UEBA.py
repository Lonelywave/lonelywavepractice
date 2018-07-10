import numpy as np

insiderGetFilesNumber = 0
	
# Insider initial, Transmit out, Oral, UEBA, Not Caught, Caught, Not Caught
def runI():
	print ('I State')
	randomNumber = (np.random.choice(7, 1, p=[0, 0.8, 0.2, 0, 0, 0, 0]))[0]
	if randomNumber == 1:
		return 'T'
	elif randomNumber == 2:
		return 'O' 
	else:
		AssertionError()
		
def runT():
	print ('T State')
	randomNumber = (np.random.choice(7, 1, p=[0, 0, 0, 1, 0, 0, 0]))[0]
	if randomNumber == 3:
		return 'U'
	else:
		AssertionError()
		
def runO():
	print ('O State')
	randomNumber = (np.random.choice(7, 1, p=[0, 0, 0, 0, 0.80, 0.20, 0]))[0]
	if randomNumber == 4:
		return 'NC2'
	elif randomNumber == 5:
		return 'C'
	else:
		AssertionError()

def runU():
	print ('U State')
	randomNumber = (np.random.choice(7, 1, p=[0, 0, 0, 0, 0, 0.08, 0.92]))[0]
	if randomNumber == 5:
		return 'C'
	elif randomNumber == 6:
		return 'NC5'
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
	stateList = ['I', 'T', 'O', 'U', 'NC2', 'C', 'NC5']
	whichround = 1
	while True:
		nextState = ''
		# in different state, run different random function
		if currentstate == 'I':
			nextState = runI()
		elif currentstate == 'T':
			nextState = runT()
		elif currentstate == 'O':
			nextState = runO()
		elif currentstate == 'U':
			nextState = runU()
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
	print ('Inisder Get ' + str(insiderGetFilesNumber) + ' Files')
	with open('UEBA_2000times_200files.csv', 'a') as the_file:
		the_file.write( str(index+1) + ', ' + str(TOTALFILES) + ', ' + str(insiderGetFilesNumber) + ', ' + str(whichround) + '\n')
	
for index in range(2000):
	main(index)