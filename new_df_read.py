import pandas as pd
import chardet
import csv
import math
with open('/home/syeda.zeenat/Downloads/5-reportJune2019-Jan2020.csv', 'r') as file:
    reader = csv.reader(file)
    df = pd.DataFrame(reader)
    print(df)
    # for row in reader:
    #     df = pd.DataFrame(row)
    #     print(df)
NUMBER_OF_SPLITS = 3
fileOpens = [open(f"out{i}.csv","w") for i in range(NUMBER_OF_SPLITS)]
fileWriters = [csv.writer(v, lineterminator='\n') for v in fileOpens]
for i,row in df.iterrows():
    fileWriters[math.floor((i/df.shape[0])*NUMBER_OF_SPLITS)].writerow(row.tolist())
for file in fileOpens:
    file.close()


# with open('out0.csv', 'r') as file:
#     reader = csv.reader(file)
#     df = pd.DataFrame(reader)
#     print(df)