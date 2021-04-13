import pandas as pd
import re as re

dataset = pd.read_csv ('test_11.csv', sep= ',',quotechar='"', encoding='utf8',engine="python",error_bad_lines=False)
new_df = pd.DataFrame(dataset, columns = ["Text for Training","Language"])
#df.drop(df[df['Language'] < "English" | df['Language'] < "english" ].index, inplace = True)
# for x in new_df.index:
#   if new_df.loc[x, "Language"] == "Spanish" or new_df.loc[x, "Language"] == "German" or  new_df.loc[x, "Language"] == "german" or new_df.loc[x, "Language"] == "french" or new_df.loc[x, "Language"] == "French" :
#     new_df.drop(x, inplace = True)

# for x in new_df.index:
#   if new_df.loc[x, "Language"] != "English" and new_df.loc[x, "Language"] != "english" :
#     new_df.drop(x, inplace = True)
# new_df.to_csv('test_1.csv', sep= ',',quotechar='"', encoding='utf8')
print(new_df.to_string())