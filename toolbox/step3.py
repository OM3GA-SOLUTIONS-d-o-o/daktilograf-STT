input_filename = 'output-all.txt'
output_filename = 'output-clean.txt'
dictionary_filename = 'words.txt'
english_words = set(x[:-1].lower() for x in open(dictionary_filename).readlines())

def lines_with_only_english_words(input_filename):
    with open(input_filename) as fin:
        for line in fin:
            for w in line.split():
                if w.lower() not in english_words:
                    break
            else:
                yield line

with open(output_filename, 'w') as fout:
    fout.writelines(lines_with_only_english_words(input_filename))