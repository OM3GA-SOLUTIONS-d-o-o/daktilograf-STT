
import os
import csv

with open('/home/omega/trening/B14/clips/train-all-B14-f.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        print(row[0])
        exists = os.path.isfile(row[0])
        if exists:
            temp=1
        else:
            print("Does not exist:" + row[0])