# Social Media Mining Toolkit - Examples

## Example 1

### Search for specific terms (donald trump, coronavirus, cricket) using the data acquisition tools. Preprocess the data using the data preprocessing tools. Annotate the tweets using the Data_annotation tools and finally classify the tweets. 

1. Set up all the requirements required for Social Media Mining Toolkit (https://github.com/thepanacealab/SMMT)
2. You will need Twitter API keys for using any of the data acquisition tools. Please apply for a twitter developer account and obtain keys. Place the keys in auth.py using the format of copy_api_keys.sample.
3. You can execute the whole script by this command.

```
sh example1.sh

```

4. In this documentation, we explain what each command does. First, we search for 3 different terms and obtain 300 tweets per term. 

```
python search_generic.py -s "donald trump,coronavirus,cricket" -n 300

```


5. The output format we need after preprocessing the obtained json files is TweetId TAB TweetText. So first, we need to edit the fields.py. Open fields.py and keep only the following two fields.

```
fields =[ 
	'id_str', 
	'text', 
	]

```

6. The parse_json_lite.py will now only use fields from step 5 and create a tab separated file (file) with only two values per line. The output of this will be "donaldtrump.tsv ; coronavirus.tsv ; cricket.tsv"

```
python parse_json_lite.py donald trump.json
python parse_json_lite.py coronavirus.json
python parse_json_lite.py cricket.json

```

7. Annotate the tab separate data. The output of this program is a file with format - TweetText TAB Annotation. First, we need a dictionary to annotate. So use an existing dictionary or create a new one using the create_dictionary.py. Since, for this example, we used 3 distinct terms, i manually created a dictionary with 3 different terms of the format ID TAB term. The dictionary is available in this folder. The dictionary (dict.tsv) looks like this

```
cui term
1   coronavirus
2   cricket
3   donald trump
```


8. Before you annotate, please verify the tsv files. You should have one tweet per line files after step 7. Sometimes, tweets come in multiple lines. Additional preprocessing might be required. To annotate the tweets using a dictionary, use the following commands;

```
python SMMT_NER_basic.py -i cricket.tsv -o annotated_cricket.tsv -d dict.tsv -f b
python SMMT_NER_basic.py -i coronavirus.tsv -o annotated_coronavirus.tsv -d dict.tsv -f b
python SMMT_NER_basic.py -i donald trump.tsv -o annotated_donaldtrump.tsv -d dict -f b
```

9. Open https://colab.research.google.com/drive/1c_5JBJ7diMDeUVVxZG95_25bZ-u8ZIDZ (Google Colab) and use the output files obtained from Annotation. The google colab has instructions on proceeding at each step.

10. Uplaod the annotated files on Step 1 og colab notebook and execute each step. 

11. Change the dataset names to the annotated tsv files on Step 3 of the google colab

12. At the end, you can find the classified tweets, metrics and classification report. If the notebook runs succesfully, you will be able to view metrics like the image below.

![Colab notebook example](notebook_colab.png)
