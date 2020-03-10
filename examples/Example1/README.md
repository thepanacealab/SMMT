# Social Media Mining Toolkit - Examples

## Example 1

### Search for specific terms (donald trump, coronavirus, cricket) using the data acquisition tools. Preprocess the data using the data preprocessing tools. Annotate the tweets using the Data_annotation tools and finally classify the tweets. 

1. Set up all the requirements required for Social Media Mining Toolkit (https://github.com/thepanacealab/SMMT)
2. You will need Twitter API keys for using any of the data acquisition tools. Please apply for a twitter developer account and obtain keys. Place the keys in auth.py using the format of copy_api_keys.sample.
3. You can execute the whole script by this command.

```
sh example1.sh

```

4. In this document, we explain what each command does. First, we search for 3 different terms and obtain 300 tweets per term. 

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

7. Open https://colab.research.google.com/drive/1-KfCxmk476HsKEx4yDIV7whLqDsp51W6 (Google Colab) and use the output files obtained from Annotation. The Google Colab has instructions on proceeding at each step.

8. Upload the tsv files on Step 1 and execute each step. 

9. Change the dataset and target names to the tsv files on Step 3 of the Google Colab

10. At the end, you can find the classified tweets, metrics and classification report. If the notebook runs successfully, you will be able to view metrics like the image below.

![Colab notebook example](notebook_colab.PNG)
