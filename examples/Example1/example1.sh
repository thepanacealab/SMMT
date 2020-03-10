#data acquisition
python ../../data_acquisition/search_generic.py -s "donald trump,coronavirus,cricket" -n 300

#data pre_processing
python ../../data_preprocessing/parse_json_lite.py "donald trump.json"
python ../../data_preprocessing/parse_json_lite.py coronavirus.json
python ../../data_preprocessing/parse_json_lite.py cricket.json
