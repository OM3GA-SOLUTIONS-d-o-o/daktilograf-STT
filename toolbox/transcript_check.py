#!/usr/bin/python

import sys, getopt, os, subprocess

csv_path = ""
model_dir = ""
model_path = ""
scorer_path = ""
threshold = 0.3
min_word_diff = 2
start_line = 3
   
def runScript():
	global csv_path, model_dir, model_path, scorer_path, threshold, min_word_diff, start_line

	try:
		opts, args = getopt.getopt(sys.argv[1:], [], ["input=", "model-dir=", "model=", "scorer=", "threshold=", "min-word-diff=", "start-line="])
	except getopt.GetoptError:
		print(os.path.basename(sys.argv[0]) + " --input <CSV path> --model-dir <dir> [--threshold <float>] [--min-word-diff <int>] [--start-line <int>]\n")
		print(os.path.basename(sys.argv[0]) + " --input <CSV path> --model <model> --alphabet <alphabet> --scorer <scorer> " + \
		"[--threshold <float>] [--min-word-diff <int>] [--start-line <int>]")
		print("\n--model-dir: Direktorijum sadrži jezički model i scorer")
		print("--threshold: Procentualna razlika između transkriptovanog i upisanog u trening da bi se racunao kao greška (default je 0.3)")
		print("--min-word-diff: Minimalna razlika u broju riječi između transkripta i treninga kako bi se računao kao greška (default je 2)")
		print("--start-line: Definisanje linije od koje se počinje transkript i upoređivanje. U našem trening fajlu prva linija počinje sa 2.")
		sys.exit(2)

	for opt, arg in opts:
		if opt == "-h":
			print(os.path.basename(sys.argv[0]) + " --input <CSV path> --model-dir <dir> [--threshold <float>] [--min-word-diff <int>] [--start-line <int>]\n")
			print(os.path.basename(sys.argv[0]) + " --input <CSV path> --model <model> --scorer <scorer> " + \
			"[--threshold <float>] [--min-word-diff <int>] [--start-line <int>]")
			print("\n--model-dir: Direktorijum sadrži jezički model i scorer")
			print("--threshold: Procentualna razlika između transkriptovanog i upisanog u trening da bi se racunao kao greška (default is 0.3)")
			print("--min-word-diff: Minimalna razlika u vbroju riječi između transkripta i treninga kako bi se računao kao greška (default is 2)")
			print("--start-line: Definisanje linije od koje se počinje transkript i upoređivanje. U našem trening fajlu prva linija počinje sa 2.")
			sys.exit()
		elif opt == "--input":
			csv_path = arg
		elif opt == "--model-dir":
			model_dir = arg
		elif opt == "--model":
			model_path = arg
		elif opt == "--scorer":
			scorer_path = arg
		elif opt == "--threshold":
			threshold = float(arg)
		elif opt == "--min-word-diff":
			min_word_diff = int(arg)
		elif opt == "--start-line":
			start_line = int(arg)
			if start_line <= 0:
				start_line = 1 

	if model_dir != "":
		# Pronađi fajlove u direktorijimu
		if scorer_path == "" and os.path.exists(os.path.join(model_dir,"scorer")):
			scorer_path = os.path.join(model_dir,"scorer")

		if model_path == "":
			model_path = firstFileWithExtension("pbmm",model_dir)

			# Koristi non-memory-mapped model ako postoji
			if model_path == "":
				model_path = firstFileWithExtension("pb",model_dir)

		
	# Provjera fajlova
	if not os.path.exists(scorer_path):
		print("Scorer nije pronađen")
		exit(1)

	if not os.path.exists(model_path):
		print("pbmm nije pronađen")
		exit(1)

	# Obrada CSV-a
	with open(csv_path) as f:
		line_no = 0			
		for line in f:
			line_no += 1
			if line_no < start_line:
				continue;
			
			components = line.split(",")

			if len(components) != 3:
				print("Greška u redu")
				continue
			
			if os.path.exists(components[0]):
				expected_transcript = components[2].strip()
				actual_transcript = transcribe(components[0]).strip()

				if not compareTranscripts(expected_transcript, actual_transcript):
					print("***")
					print("File: " + components[0])
					print("linija: " + str(line_no))
					print("Orginalni transkript: " + expected_transcript)
					print("Transkribovani file: " + actual_transcript)
					print("***")
		

def firstFileWithExtension(ext, folder):
	for root, dirs, files in os.walk(folder):
		for filename in files:
			if os.path.splitext(filename)[1].lower() == "." + ext.lower():
				return os.path.join(folder,filename)

	return ""

def transcribe(wav_path):
	global model_path, scorer_path

	return str(subprocess.check_output(["stt", "--model", model_path, "--scorer", scorer_path, \
 										"--audio", wav_path], stderr=subprocess.DEVNULL),"utf-8")

def compareTranscripts(expected, actual):
	global min_word_diff

	# Rezultati za pronađene fajlove zadatim parametrima
	expected_words = len(expected.split())	
	actual_words = len(actual.split())	

	if expected_words == 0 or actual_words == 0:
		return False

	if actual_words == expected_words:
		return True

	if actual_words > expected_words:
		if actual_words - expected_words < min_word_diff:
			return True

		return (actual_words - expected_words) / expected_words < threshold

	if expected_words - actual_words < min_word_diff:
		return True

	return (expected_words - actual_words) / expected_words < threshold


runScript()

