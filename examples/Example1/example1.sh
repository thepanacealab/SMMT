#data acquisition
python ../../data_acquisition/search_generic.py -s "donald trump,coronavirus,cricket" -n 300

#data pre_processing
python ../../data_preprocessing/parse_json_lite.py "donald trump.json"
python ../../data_preprocessing/parse_json_lite.py coronavirus.json
python ../../data_preprocessing/parse_json_lite.py cricket.json

#data annotation
python ../../data_annotationANDstandardization/SMMT_NER_basic.py -i cricket.tsv -o annotated_cricket.tsv -d dict.tsv -f c
python ../../data_annotationANDstandardization/SMMT_NER_basic.py -i coronavirus.tsv -o annotated_coronavirus.tsv -d dict.tsv -f c
python ../../data_annotationANDstandardization/SMMT_NER_basic.py -i "donald trump.tsv" -o annotated_donaldtrump.tsv -d dict.tsv -f c