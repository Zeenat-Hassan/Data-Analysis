import pandas as pd
import re as re

dataset = pd.read_csv ('test_11.csv', sep= ',',quotechar='"', encoding='utf8',engine="python",error_bad_lines=False)
new_df = pd.DataFrame(dataset, columns = ["Text for Training","Language"])
def find_nonalpha(text):
    result = re.findall("[^A-Za-z0-9 ]",text)
    return result
new_df ['nonalpha']=new_df ['Text for Training'].apply(lambda x: find_nonalpha(x))
print("\Extracting only non alphanumeric characters from company_code:")
sr = pd.Series(new_df ['nonalpha'])
print(sr)
sr.to_csv('test_2.csv', sep= ',')
#print(new_df.to_string())