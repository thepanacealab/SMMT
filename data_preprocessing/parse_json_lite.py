import pandas as pd
import numpy as np
import json
import sys
import string
import re
# This will load the fields list
import fields


fieldsFilter = fields.fields

fileN = sys.argv[1]

with open(fileN, "r") as read_file:
    data = json.load(read_file)

tweet_df = pd.json_normalize(data)
tweet_df = tweet_df.loc[:, tweet_df.columns.isin(fieldsFilter)]

with open(fileN[:-5]+".tsv",'w') as write_tsv:
    write_tsv.write(tweet_df.to_csv(sep='\t', index=False))
