# Social Media Mining Toolkit (SMMT) main repository

This work was conceptualized for/and (mostly) carried out while at the [Biomedical Linked Annotation Hackathon 6](http://blah6.linkedannotation.org/) in Tokyo, Japan.

![BLAH](http://www.jmbanda.com/blah6.png)

We are very grateful for the support on this work.

# Proposed functionality of SMMT V1.0

![Architecture](http://www.jmbanda.com/SMMT-v1.png)

## Data Acquisition Tools:
1. **Twitter hydration tool** - This script will hydrate tweet ID’s provided by others. 
1. **Twitter gathering tool** - This script will allow users to specify hashtags and capture from the twitter faucet new tweets with the given hashtag.
1. **Reddit scraping tool** - This script will scrape reddit subgroups that are specified


## Data Preprocessing Tools: 
1. **Twitter JSON extraction tool** - While seemingly trivial, most biomedical researchers do not want to work with JSON objects. This tool will take the fields the researcher wants and output a simple to use CSV file created from the provided data. 

## Data Annotation and Standardization Tools: 
1. **Spacy dictionary-based annotation pipeline** This is the tool that will require the most work during the hackathon. This pipeline will be available as a service as well, with the user providing their dictionaries and feeding data directly.  
1. **Dictionary generation tool** This tool will transform ontologies or provided dictionary files into spacy compliant dictionaries to use with the previous pipeline.
1. **Manual annotation hooks to tools like brat annotation tools** 

# Dependencies and versions used

1. Python 3+

1. Spacy 

` pip install spacy `

1. Twarc

` pip install twarc `

1. Tweepy

` pip install tweepy `

# Usage

1. Clone repository
1. Each tool and their use is described on their individual pages 

# Everything below is a work in progress

Here is the documentation for the Social Media Mining

https://docs.google.com/document/d/1w49tIhvqxKTax47IwfKgaPSbnLImmSlPFozKrz_Efuw/edit?usp=sharing  . This is a draft version.

Related Repositories:
https://github.com/thepanacealab/InternetArchive-Pharmacovigilance-Tweets
