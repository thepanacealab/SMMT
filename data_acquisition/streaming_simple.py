from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import oauth2 
import twitter
import csv

#Variables that contains the user credentials to access Twitter API 
consumer_key="6m23Sb281bnbQc45EJOLptTof"
consumer_secret="YWS12KIRaBd7btOByPhXcvKRWbAdHBBl4ktJr5lXo31Kf4mNQC"
access_token="1173363240027508737-2wGuqHB7w6c6XPhi3wXukOBFSA2aKe"
access_token_secret="UZjIqWw21h7pf4du9vTAovGFEligJwGMf2KxBNaF9qrQT"

#Very simple (non-production) Twitter stream example
#1. Download / install python and tweepy (pip install tweepy)
#2. Fill in information in auth.py
#3. Run as: python streaming_simple.py
#4. It will keep running until the user presses ctrl+c to exit
#All output stored to output.json (one tweet  per line)
#Text of tweets also printed as recieved (see note about not doing this in production (final) code

class StdOutListener(StreamListener):
	
	#This function gets called every time a new tweet is received on the stream
	def on_data(self, data):
		#Just write data to one line in the file
		fhOut.write(data)
		
		#Convert the data to a json object (shouldn't do this in production; might slow down and miss tweets)
		j=json.loads(data)

		#See Twitter reference for what fields are included -- https://dev.twitter.com/docs/platform-objects/tweets
		text=j["text"]
		id = j["id_str"] #The text of the tweet
		print(id +"\t" + text) #Print it out

	def on_error(self, status):
		print("ERROR")
		print(status)

if __name__ == '__main__':
	try:
		#Create a file to store output. "a" means append (add on to previous file)
		fhOut = open("output.json","a")

		#Create the listener
		l = StdOutListener()
		auth = OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)

		drugsList=[]
		with open("drug_dict_singlestr.csv") as f:
			reader = csv.reader(f, delimiter=",", quotechar="\"")
			next(reader)
			for drugRow in reader:
				drugsList.append(drugRow[1].lower())
		#Connect to the Twitter stream
		stream = Stream(auth, l)	

		#Terms to track
		for drug in drugsList:
			stream.filter(track=drug,languages=["en"])
		
		#Alternatively, location box  for geotagged tweets
		#stream.filter(locations=[-0.530, 51.322, 0.231, 51.707])

	except KeyboardInterrupt:
		#User pressed ctrl+c -- get ready to exit the program
		pass

	#Close the 
	fhOut.close()



