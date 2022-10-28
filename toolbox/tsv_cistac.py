#!/usr/bin/python

import sys, getopt, os
   
def runScript():
	ulazni_fajl = ""
	izlazni_fajl = ""
	cistac_fajl = ""
	cistac_lista = []
	broj_ociscenih = 0

	try:
		opts, args = getopt.getopt(sys.argv[1:], "u:i:c", ["ulaz=", "izlaz=", "cistac-lista="])
	except getopt.GetoptError:
		print(os.path.basename(sys.argv[0]) + " --ulaz <ulazni TSV fajl> --izlaz <izlazni TSV fajl> --cistac-lista <txt ili TSV ili naziv fajlova za ciscenje>")
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print(os.path.basename(sys.argv[0]) + " --ulaz <ulazni TSV fajl> --izlaz <izlazni TSV fajl> --cistac-lista <txt ili TSV ili naziv fajlova za ciscenje>")
			sys.exit()
		elif opt in ("-u", "--ulaz"):
			ulazni_fajl = arg
		elif opt in ("-i", "--izlaz"):
			izlazni_fajl = arg
		elif opt in ("-c", "--cistac-lista"):
			cistac_fajl = arg

	# Keširanje fajlova za brisanje u listi
	with open(cistac_fajl) as f:  			
		for line in f:
			items = line.split("    ")

			if len(items) > 0 and len(items[0].strip()) > 0:
				cistac_lista.append(items[0].strip().lower())

		f.close()

	# Otvaranje izlaznog TSV-a
	f_out = open(izlazni_fajl,"w")

	# Loop kroz ulazni TSV
	with open(ulazni_fajl) as f:  			
		for line in f:
			items = line.split('\t')
			
			if len(items) != 11:
				print("Pogrešan fajl")
				continue

			file_path = items[1].strip().lower()

			if file_path in cistac_lista:
				broj_ociscenih += 1
				continue
			
			# Upoređivanje naziva fajlova
			file_name = os.path.basename(file_path)

			if file_name in cistac_lista:
				broj_ociscenih += 1
				continue
			
			# Ako nema podudarnosti
			f_out.write(line)

		f.close()
	
	f_out.close()

	print("{} linija očišćen{}".format(broj_ociscenih,"o" if broj_ociscenih != 1 else "a"))
	
runScript()

