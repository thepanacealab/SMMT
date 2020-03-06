# Social Media Mining Toolkit - Examples

## Example 1

### Search for specific terms (donald trump, coronavirus, cricket) using the data acquisition tools. Preprocess the data using the data preprocessing tools. Annotate the tweets using the Data_annotation tools and finally classify the tweets. 

1. Set up all the requirements required for Social Media Mining Toolkit (https://github.com/thepanacealab/SMMT)
2. You will need Twitter API keys for using any of the data acquisition tools. Please apply for a twitter developer account and obtain keys. Place the keys in auth.py using the format of copy_api_keys.sample.
3. In this example, we search for 3 different terms and obtain 300 tweets per term. 

```
cd SMMT/data_acquisition
python search_generic.py -s "donald trump,coronavirus,cricket" -n 300

```
4. Move the obtained json files to data_preprocessing folder .

```
mv donald trump.json SMMT/data_preprocessing
mv coronavirus.json SMMT/data_preprocessing
mv cricket.json SMMT/data_preprocessing
cd SMMT/data_preprocessing

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

7. Move the obtained tsv files to data_annotationANDstandardization

``` 
mv donald trump.tsv SMMT/data_annotationANDstandardization
mv coronavirus.tsv SMMT/data_annotationANDstandardization
mv cricket.tsv SMMT/data_annotationANDstandardization
cd SMMT/data_annotationANDstandardization

```

8. Annotate the tab separate data. The output of this program is a file with format - TweetText TAB Annotation. First, we need a dictionary to annotate. So use an existing dictionary or create a new one using the create_dictionary.py. Since, for this example, we used 3 distinct terms, i manually created a dictionary with 3 different terms of the format ID TAB term. The dictionary (dict.tsv) looks like this

```
cui term
1   coronavirus
2   cricket
3   donald trump
```

11. Since the output needs TweetText TAB Annotation format; edit the bratFormat method in line 45. Remove the current fO.write (fO.write("T" + str(i) + "\t" + str(ent.label_) + "\t" + str(ent.start_char) + "\t" + str(ent.end_char) + "\t" + str(ent.text) + "\n")) and add the following line

```
fO.write(str(description) + "\t" + str(ent.text) + "\n")
```
10. To annotate the tweets using a dictionary, use the following commands;

```
python SMMT_NER_basic.py -i cricket.tsv -o annotated_cricket.tsv -d dict.tsv -f b
python SMMT_NER_basic.py -i coronavirus.tsv -o annotated_coronavirus.tsv -d dict.tsv -f b
python SMMT_NER_basic.py -i donald trump.tsv -o annotated_donaldtrump.tsv -d dict -f b
```

11. Open https://colab.research.google.com/drive/1c_5JBJ7diMDeUVVxZG95_25bZ-u8ZIDZ (Google Colab) and use the output files obtained from Annotation. The google colab has instructions on proceeding at each step.