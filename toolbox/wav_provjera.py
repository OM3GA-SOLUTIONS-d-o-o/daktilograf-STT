#!/usr/bin/python

import sys, os, subprocess
   
def runScript():
	if len(sys.argv) != 2:
			print('wav_provjera.py <direktorijum za skeniranje>')
			sys.exit(2)

	dir = sys.argv[1]

	# Detekcija fajlova u folderu - Walk
	for root_dir, subdir_list, file_list in os.walk(dir):
		for file_name in file_list:
			# Samo WAV fajlovi
			if os.path.splitext(file_name)[1].lower() == '.wav':
				full_path = os.path.join(root_dir,file_name)
				success = checkWAV(full_path)
				
				if success:
					print(full_path + ' - OK')
				else:
					print(full_path + ' - GREŠKA', file=sys.stderr)

def checkWAV(file_path):
	# Čitaj file od početka do kraja uz NULL pipeline
	process = subprocess.run(['ffmpeg','-i',file_path,'-f','null','-'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

	# Koristi ffmpeg povratni kod
	return (process.returncode == 0)
	
runScript()

