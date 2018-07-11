import numpy as np
import pandas as pd 

def valueR(allow_probablilty, deny_probability):
	A = np.matrix([
	#A B C
	[deny_probability,allow_probablilty,0],#A
	[0.08,0,0.92],#B
	[0,0.80,0.20], #C
	])
	return A

def valueD(allow_probablilty, deny_probability):
	A = np.matrix([
	#A B C
	[deny_probability,allow_probablilty,0],#A
	[0.80,0,0.20],#B
	[0,0.08,0.92], #C
	])
	return A
	
def run(matrix):
	B = [1,0,0]
	C = B * matrix
	for i in range(60):
		C = C * matrix
	print ('C')
	print (C)
	itemindex = C[0:1, 2:3]
	print ('itemindex')
	print (itemindex.item(0))
	return itemindex.item(0)
	
def main():
		allow_probablilty = 0.00
		deny_probability = 1.00
		a = np.asarray([0])
		while (deny_probability >= 0):
			ans = run(valueR(allow_probablilty, deny_probability))
			#ans = run(valueD(allow_probablilty, deny_probability))
			allow_probablilty += 0.05
			deny_probability = 1.00 - allow_probablilty
			a = np.append(a, [ans])
		df = pd.DataFrame(a)
		with open('lonelyR.csv', 'a') as f:
			df.to_csv(f, header=False)
main()
