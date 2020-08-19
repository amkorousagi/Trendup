# Trendup
OIDC2020

## How to use Trendup?
go to http://49.50.164.37:6002/ !

## Where source code?
1. front end: https://github.com/amkorousagi/trendup_front
2. back end: https://github.com/amkorousagi/trendup_back
3. data collection and machine learning: this repository!

## CAUTION
1. replace Authentication key(GCP api key, service json in youtube_*.py) with yours.
2. Do not operate youtube_*.py too many times, it  only works 5~7 times because of Google API call limit for Free user.



## For Youtube Containers

### master container 

### youtube_data container 

### youtube_map container 


## For Web Crawling Containers

### n_shopping container

### c_shopping container

### _11_shopping container

### keyword_rank container

## For Machine Learning Containers

### AI_male container

### AI_female container

### AI_predict_male container

### AI_prefict_female container




### before run youtube_data container
plz update your authentication information (API_KEY, service account json) 

### before run master.py
plz update your server's private IP by "hostname -I"

## Network graph
![image](https://user-images.githubusercontent.com/39821875/89766357-fc8a6f00-db32-11ea-8b98-fca5f822e6aa.png)

## Architecture graph
![image](https://user-images.githubusercontent.com/39821875/89766416-15932000-db33-11ea-9df4-eaa18d0cba2d.png)
