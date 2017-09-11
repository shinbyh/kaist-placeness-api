# kaist-placeness-api
KAIST Placeness API

## Project
Development of Placeness-based Data Mining Core Technologies for Real-time Intelligent Information Recommendation Services in Smart Spaces (MSIP, South Korea)

## Prerequisites
### Common
* Python 3.x
* Flask ($ sudo pip install flask)
* Flask-Restful ($ sudo pip install flask-restful)
* Flask-API ($ sudo pip install flask-api)
* OpenJDK 7 ($ sudo add-apt-repository ppa:openjdk-r/ppa; sudo apt-get update; sudo apt-get install openjdk-7) 

### For hotspot placeness
* Firebase ($ sudo pip install python-firebase)
* Dependencies for konlpy ($ sudo apt-get install g++ openjdk-7-jdk python-dev python3-dev)
* konlpy ($ sudo pip install konlpy)

### For relationship extraction
* gensim ($ sudo pip install gensim)

### For relationship extraction
* networkx ($ sudo pip install networkx)

### Or if you want to install all at once...
You can use "requirements.txt" in the repository.
```
$ virtualenv -p python3 venv
$ ./venv/bin/activate
(venv)$ pip install -r requirements.txt
```


## How to run
Just simply run "main.py".
```
$ python main.py
```
Or, if you want to specify the access permissions by the host address and the port number,
```
$ python main.py [HOST_IP] [PORT]
```
Note: If the port number is below 1024, you need a root permission. (8080 or others recommended)
