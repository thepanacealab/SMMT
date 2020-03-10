# Social Media Mining Toolkit (SMMT) main repository

The set of tools collected and presented here are designed with the purpose of facilitating the acquisition, preprocessing, and initial exploration of social media data (mostly Twitter for now). This centralized repository depends on other widely available libraries that need to be installed. 

We separated this toolkit in three categories (each one on an individual folder):

1. Data Acquisition Tools: Utilities to gather data from social media sites.
1. Data Preprocessing  Tools: Utilities to parse social media 'raw' data and to separate by terms
1. Data Annotation and Standardization Tools: Utilities to make automatic NER annotations on preprocessed tweets, plugins to use popular annotation tools and NER systems.

# Usage

1. Install dependencies (below)
1. Clone repository
1. Make sure you have your Twitter API keys handy if you are gathering any Twitter Data
1. Each tool and their usage is described on the README file on each category of tools folder.

# Dependencies and versions used

1. Python 3+

1. [Spacy v2.2](https://spacy.io/usage)
``` 
pip install spacy 
python -m spacy download en
python -m spacy download en_core_web_sm
```
1. [Twarc](https://github.com/DocNow/twarc)
` pip install twarc `

1. [Tweepy v3.8.0](http://docs.tweepy.org/en/latest/)
` pip install tweepy `

1. [argparse - v3.2](https://docs.python.org/3/library/argparse.html)
` pip install argparse `

1. [xtract - v0.1a3](https://pypi.org/project/xtract/)
` pip install xtract `

**NOTE:** If you are using the scraping utility, install the following dependencies. These dependencies are needed for the headless browsing automation tasks (no need to have a screen open for them). Configuration of these items is very finicky but there is plenty of documentation online.

1. [Xvf](https://linux.die.net/man/1/xvfb)
` sudo yum install Xvfb `

1. [Firefox](https://www.mozilla.org/en-US/firefox/linux/)
` sudo yum install firefox `

1. [selenium](https://selenium.dev/)
` pip install -U selenium `

1. [pyvirtualdisplay - v0.25](https://pypi.org/project/PyVirtualDisplay/)
` pip install pyvirtualdisplay `

1. [GeckoDriver - v0.26.0](https://github.com/mozilla/geckodriver/releases)
` sudo yum install jq `

and then use the provided utility:

` bash SMMT/data_acquisition/geckoDriverInstall.sh `

If you still have issues or the Firefox window is popping up through your X11, follow this:
https://www.tienle.com/2016/09-20/run-selenium-firefox-browser-centos.html

# Twitter Keys
**This is a very important step, if you do not have any Twitter API keys, none of the software that uses Twitter API will work without it**

# Social Media Mining Toolkit (SMMT) Extra Information

![SMMT](http://www.jmbanda.com/sMMT_smalllogo.png)

## Data Acquisition Tools:
1. **Twitter hydration tool** - This script will hydrate tweet ID’s provided by others. 
1. **Twitter gathering tool** - This script will allow users to specify hashtags and capture from the twitter faucet new tweets with the given hashtag.

## Data Preprocessing Tools: 
1. **Twitter JSON extraction tool** - While seemingly trivial, most biomedical researchers do not want to work with JSON objects. This tool will take the fields the researcher wants and output a simple to use CSV file created from the provided data. 

## Data Annotation and Standardization Tools: 
1. **Spacy dictionary-based annotation pipeline** This is the tool that will require the most work during the hackathon. This pipeline will be available as a service as well, with the user providing their dictionaries and feeding data directly.  
1. **Dictionary generation tool** This tool will transform ontologies or provided dictionary files into spacy compliant dictionaries to use with the previous pipeline.
1. **Manual annotation hooks to tools like brat annotation tools** 


This work was conceptualized for/and (mostly) carried out while at the [Biomedical Linked Annotation Hackathon 6](http://blah6.linkedannotation.org/) in Tokyo, Japan.

![BLAH](http://www.jmbanda.com/blah6.png)

We are very grateful for the support on this work.

# Proposed functionality of SMMT V1.0

![Architecture](http://www.jmbanda.com/SMMT-v1.png)
