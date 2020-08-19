# Trendup
OIDC2020

## How to use Trendup?
go to http://49.50.164.37:6002/ !

## Where source code?
1. front end: https://github.com/amkorousagi/trendup_front
2. back end: https://github.com/amkorousagi/trendup_back
3. data collection and machine learning: this repository!

## CAUTION
1. replace Authentication key(GCP api key, service json in youtube_*.py) with yours. (other containers not require Authentication key)
2. Do not operate youtube_*.py too many times, it  only works 5~7 times on each day because of Google API call limit for Free user.(If you want to update several timme, plz convert youtube_* func in tcp.py to comment). also you need to command  GOOGLE_APPLICATION_CREDENTIALS="*.json" and to convert "~/api_key.txt" in tcp.py for running youtube_* containers
3. If you operate containers on other public IP, only chage MASTER_PUBLIC_IP in tcp.py.
4. Do not change port for each container, every port is fixed
5. According to your environment, can occur errors. then, try converting all print* to comment. for DB, convert character set = utf8mb4 

## For Youtube Containers
1. docker build -t youtube_image -f Dockerfile_youtube
2. follow commands below

### master container

2. docker run -it -p 5001:5001 --name master_container youtube_image /bin/bash
3. hostname -I
4. in tcp.py, replace MASTER_PRIVATE_IP ="172.0.0.4" with MASTER_PRIVATE_IP = "<above result>"
5. python3 master.py
6. wait other all container connected
  
### youtube_data container 

2. docker run -it -p 5002:5002 --name youtube_data_container youtube_data_image /bin/bash
4. python3 youtube_data1.py
5. wait other all container connected


### youtube_map container 

2. docker run -it -p 5003:5003 --name youtube_map_container youtube_image /bin/bash
4. python3 youtube_map.py
5. wait other all container connected

## For Web Crawling Containers
1. docker build -t webcrawling_image -f Dockerfille_webcrawling .
2. follow commands below

### n_shopping container

1. docker run -it -p 5004:5004 --name n_shopping_container webcrawling_image /bin/bash
2. python3 n_shopping.py
3. wait other all container connected

### c_shopping container
1. docker run -it -p 5005:5005 --name c_shopping_container webcrawling_image /bin/bash
2. python3 c_shopping.py
3. wait other all container connected

### _11_shopping container
1. docker run -it -p 5006:5006 --name _11_shopping_container webcrawling_image /bin/bash
2. python3 _11_shopping.py
3. wait other all container connected

### keyword_rank container
1. docker run -it -p 5007:5007 --name keyword_rank_container webcrawling_image /bin/bash
2. python3 keyword_rank.py
3. wait other all container connected

## For Machine Learning Containers
1. docker build -t ml_image -f Dockerfile_AI_male .
2. follow commands below

### ML_male container
1. docker run -it -p 5008:5008 --name ml_male_container ml_image /bin/bash
2. python3 "AI(machine_learning)_male.py"
3. wait other all container connected

### ML_female container
1. docker run -it -p 5009:5009 --name ml_female_container ml_image /bin/bash
2. python3 "AI(machine_learning)_female.py"
3. wait other all container connected

### ML_predict_male container
1. docker run -it -p 5010:5010 --name ml_predict_male_container ml_image /bin/bash
2. python3 AI_predict_male.py
3. wait other all container connected

### ML_prefict_female container
1. docker run -it -p 5011:5011 --name ml_predict_female_container ml_image /bin/bash
2. python3 AI_predict_female.py
3. wait other all container connected

## Web

### Front end
go to https://github.com/amkorousagi/trendup_front

### Back end
go to https://github.com/amkorousagi/trendup_back

## Network graph
![image](https://user-images.githubusercontent.com/39821875/89766357-fc8a6f00-db32-11ea-8b98-fca5f822e6aa.png)

## Architecture graph
![image](https://user-images.githubusercontent.com/39821875/89766416-15932000-db33-11ea-9df4-eaa18d0cba2d.png)



#### when having problem, whenever contacting  me (hasmi5452@gmail.com)
