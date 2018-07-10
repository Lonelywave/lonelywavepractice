import numpy as np

insiderGetFilesNumber = 0

# Insider initial, DLP, Oral, Terminate, Not Caught
def runI():
	print ('I State')
	randomNumber = (np.random.choice(5, 1, p=[0, 0.2, 0.8, 0, 0]))[0]
	if randomNumber == 1:
		return 'D'
	elif randomNumber == 2:
		return 'O' 
	else:
		AssertionError()
		
def runD():
	print ('D State')
	randomNumber = (np.random.choice(5, 1, p=[1, 0, 0, 0, 0]))[0]
	if randomNumber == 0:
		return 'I'
	else:
		AssertionError()
		
def runO():
	print ('O State')
	randomNumber = (np.random.choice(5, 1, p=[0, 0, 0, 0.20, 0.80]))[0]
	if randomNumber == 3:
		return 'C'
	elif randomNumber == 4:
		return 'N'
	else:
		AssertionError()

# gameover or not
def gameoverChecker(nextState):
	global insiderGetFilesNumber
	# determine if is it gameover or not
	if nextState == 'C':
		return 'gameover'
	elif nextState == 'N':
		insiderGetFilesNumber = insiderGetFilesNumber + 2
		if insiderGetFilesNumber >= 200:
			insiderGetFilesNumber = 200
			return 'gameover'
		else:
			# Not caught so back to initial state
			return 'notcaught'
	elif nextState == 'N':
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
	stateList = ['I', 'D', 'O', 'C', 'N']
	whichround = 1
	while True:
		
		nextState = ''
		# in different state, run different random function
		if currentstate == 'I':
			nextState = runI()
		elif currentstate == 'D':
			nextState = runD()
		elif currentstate == 'O':
			nextState = runO()
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
	#print ('Inisder Get ' + str(insiderGetFilesNumber) + ' Files')
	with open('DLP_2000times_200files.csv', 'a') as the_file:
		the_file.write( str(index+1) + ', ' + str(TOTALFILES) + ', ' + str(insiderGetFilesNumber) + ', ' + str(whichround) + '\n')
	
for index in range(2000):
	main(index)

