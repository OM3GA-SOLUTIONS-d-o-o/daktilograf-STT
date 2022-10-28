#!/usr/bin/python

import sys, os, subprocess

broj_fajlova = 0
ukupna_velicina = 0
ukupno_trajanje = 0
bez_predpostavke = False

def runScript():
	global broj_fajlova, ukupna_velicina, ukupno_trajanje, bez_predpostavke

	if len(sys.argv) < 2:
		print('clip_stats.py [--bez-predpostavke] <direktorijum za skeniranje ili CSV fajl>')
		sys.exit(2)

	if "--bez-predpostavke" in sys.argv:
		bez_predpostavke = True

	dir = sys.argv[-1]
	split_ext = os.path.splitext(dir)

	if len(split_ext) > 0 and split_ext[1].lower() == '.csv':
		# Obrada CSV-a
		with open(dir) as f:  			
			for line in f:
				components = line.split(",")

				if len(components) != 3:
					print("Greška na liniji")
					continue
				
				if os.path.exists(components[0]):
					checkFile(components[0])
	else:
		# Detekcija fajlova u folderu - Walk
		for root_dir, subdir_list, file_list in os.walk(dir):
			for file_name in file_list:
				# Samo WAV fajlovi
				if os.path.splitext(file_name)[1].lower() == '.wav':
					full_path = os.path.join(root_dir,file_name)				
					checkFile(full_path)

	# Ispis kalkulacije svih fajlova
	print("Pronđeno {0} fajlova, {1:.2f} MB, {2:.2f} sati".format(broj_fajlova,ukupna_velicina,(ukupno_trajanje/60/60)))

def getDuration(file_path):
	global bez_predpostavke

	if not bez_predpostavke:
		# Brza kalkulacija za nas dataset WAV 16-bit, 16000 Hz mono
		file_size = os.path.getsize(file_path)
		return file_size/(2*16000)
	else:
		# Stvarna kalkulacija WAV fajlova
		return float(str(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',file_path]),"utf-8"))

def checkFile(file_path):
	global broj_fajlova, ukupna_velicina, ukupno_trajanje

	broj_fajlova += 1
	ukupno_trajanje += getDuration(file_path)
	ukupna_velicina += os.path.getsize(file_path)/1024/1024

	print("Pronađeno {0} fajlova, {1:.2f} MB, {2:.2f} sati".format(broj_fajlova,ukupna_velicina,(ukupno_trajanje/60/60)), end="\r")

	
runScript()

