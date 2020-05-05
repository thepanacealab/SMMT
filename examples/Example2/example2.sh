#data acquisition
python ../../data_acquisition/search_generic.py -s "covid,olympics" -n 300
#data pre_processing
python ../../data_preprocessing/parse_json_lite.py covid.json
python ../../data_preprocessing/parse_json_lite.py olympics.json
#data annotation
python ../../data_annotationANDstandardization/SMMT_NER_basic.py -i olympics.tsv -o annotated_olympics.tsv -d dict.tsv 
python ../../data_annotationANDstandardization/SMMT_NER_basic.py -i covid.tsv -o annotated_covid.tsv -d dict.tsv