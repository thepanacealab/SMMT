import pandas as pd
import argparse

parser = argparse.ArgumentParser()
   
parser.add_argument("-o", "--outputfile", help="Output file name with extension", required=True)
parser.add_argument("-i", "--inputfile", help="Input file name with extension", required=True)

args = parser.parse_args()
input_file = args.inputfile
output_file = args.outputfile

data = pd.read_csv(input_file, sep = "\t", encoding="utf-8")

data['term'] = data.term.astype(str).str.lower()
data['cui'] = data.cui.astype(str).str.lower()

#print(data['term'])
#print(data['cui'])

header = ["cui", "term"]

data.to_csv(output_file, columns = header, sep = "\t", encoding="utf-8", index=False)