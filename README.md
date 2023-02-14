# stream
This repository contains three implementations for i) fetching data from tweeter and receive a json file; ii) creating a tweeter stream socket, and iii) creating an IoT socket.

i) fetching data from tweeter:

  git the file.
  
  !pip install tweepy
  !pip install tweet-preprocessor
  
  import streamous
  
  api_key='put your key'
  api_secrets='put your key'
  access_token ='put your key'
  access_secret='put your key'
  
  api, result = streamous.authenticate(api_key, api_secrets, access_token, access_secret)
  QueryTopic = 'covid19' #send your own keyword
  if result:
      jsonResult = checkTweets(api,QueryTopic)

ii) creating a tweeter stream socket
  
  !pip install tweepy
  !pip install tweet-preprocessor
  
  bearer = 'put your key'
  search_terms = ["python","spark"] # add your keyword
  create_stream(search_terms,bearer) #the default values for host and port are '127.0.0.1' and 5555 respectively.

iii) creating an IoT socket
  # download the related csv file from 
  getVibrationReadings('put your own path/fault_stream.csv') # the structure is like : "DateTime":"26\\/12\\/2020 14:51","Value":0.4796875
