import pandas as pd
import re as re

dataset = pd.read_csv ('1-reportMarch2021-April2021.csv', sep= ',',quotechar='"', encoding='utf8',engine="python",error_bad_lines=False)
new_df = pd.DataFrame(dataset, columns = ["Text for Training","Language"])
#df.drop(df[df['Language'] < "English" | df['Language'] < "english" ].index, inplace = True)
# for x in new_df.index:
#   if new_df.loc[x, "Language"] == "Spanish" or new_df.loc[x, "Language"] == "German" or  new_df.loc[x, "Language"] == "german" or new_df.loc[x, "Language"] == "french" or new_df.loc[x, "Language"] == "French" :
#     new_df.drop(x, inplace = True)

# for x in new_df.index:
#   if new_df.loc[x, "Language"] != "English" and new_df.loc[x, "Language"] != "english" :
#     new_df.drop(x, inplace = True)
# new_df.to_csv('test_1.csv', sep= ',',quotechar='"', encoding='utf8')
def find_nonalpha(text):
    result = re.findall("[^A-Za-z0-9 ]",text)
    return result
new_df ['nonalpha']=new_df ['Text for Training'].apply(lambda x: find_nonalpha(x))
print("\Extracting only non alphanumeric characters from company_code:")
sr = pd.Series(new_df ['nonalpha'])
print(sr)
sr.to_csv('test_2.csv', sep= ',')
print(new_df.to_string())