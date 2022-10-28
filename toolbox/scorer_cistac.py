veliki_dokument = 'output-all-07-11.txt'
cisit_generisani = 'output-clean-11-11.txt'
recnik_dozvoljenih = 'words-11-11.txt'
recnik_rijeci = set(x[:-1].lower() for x in open(recnik_dozvoljenih).readlines())

def lines_with_only_recnik_rijeci(veliki_dokument):
    with open(veliki_dokument) as fin:
        for line in fin:
            for w in line.split():
                if w.lower() not in recnik_rijeci:
                    break
            else:
                yield line

with open(cisit_generisani, 'w') as fout:
    fout.writelines(lines_with_only_recnik_rijeci(veliki_dokument))