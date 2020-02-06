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

# Twitter Keys
**This is a very important step, if you do not have any Twitter API keys, none of the software that uses Twitter will work without it**

Make sure you create a copy of copy_auth.py and call it auth.py, replacing the corresponding text inside with the proper keys.

# Dependencies and versions used

1. Python 3+

1. Spacy
``` 
pip install spacy 
python -m spacy download en
python -m spacy download en_core_web_sm
```
1. Twarc
` pip install twarc `

1. Tweepy
` pip install tweepy `

1. argparse
` pip install argparse `

1. xtract
` pip install xtract `

**NOTE:** If you are using the scraping utility, install the following dependencies.

1. Xvfb
` sudo yum install Xvfb `

1. Firefox
` sudo yum install firefox `

1. selenium
` pip install -U selenium `

1. pyvirtualdisplay
` pip install pyvirtualdisplay `

1. GeckoDriver
` sudo yum install jq `

and then use the provided utility:

` bash SMMT/data_acquisition/geckoDriverInstall.sh `

If you still have issues or the Firefox window is popping up through your X11, follow this:
https://www.tienle.com/2016/09-20/run-selenium-firefox-browser-centos.html


# Usage

1. Clone repository
1. Each tool and their usage is described on their individual pages 

# Everything below is a work in progress

Here is the documentation for the Social Media Mining

https://docs.google.com/document/d/1w49tIhvqxKTax47IwfKgaPSbnLImmSlPFozKrz_Efuw/edit?usp=sharing  . This is a draft version.

Related Repositories:
https://github.com/thepanacealab/InternetArchive-Pharmacovigilance-Tweets
