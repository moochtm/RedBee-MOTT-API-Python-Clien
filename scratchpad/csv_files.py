import csv

csv_fp = "/Users/home/Downloads/DTC RED BEE SCHEDULE.csv"

with open(csv_fp, newline='') as csvfile:
    print(csvfile.readline())
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        print(', '.join(row))