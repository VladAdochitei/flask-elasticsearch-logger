# flask-elasticsearch-logger
Flask Logger with ElasticSearch functionality.

<br>

---------------------------------------------------
## Contents:
- [1. Application context](#1-application-context)
- [2. Simulation context](#2-simulation-context)
- [3. ElasticSearch context](#3-elasticsearch-context)
- [4. How to use the application](#4-how-to-use-the-application)
- [5. How to integrate ElasticSearch with the logs](#5-how-to-integrate-elasticsearch-with-the-logs)
---------------------------------------------------

<br>

## 1. Application Context
I have developed a very simple flask application which resembles a web server written in python. this code is present in app.py. The web application has 2 routes, the `/` and `/operation` routes, which are defined to log different information on the request, request's source IP and the log category (ERROR, INFO, WARNING, etc.). 

In this scenario, the purpose of the logger is to identify unauthorized requests on the routes, so we can Identify if an external entity is trying to sniff the web server's routes in order to find an attack vector.

The application's logs can be found in `/logs/app.log` file, and are standardised.

<br>


## 2. Simulation context
In order to simulate a bunch of requests to our application we should run the `requestor.script.sh` which is a simple shell script that will perform a bunch of requests on our web application. this is useful because it will generate a log of logging data which will then be used by our ElasticSearch application.

<br>

## 3. ElasticSearch context
ElasticSearch will be used to visualize the data and categorise requests based on log level severity and pages accessed.


<br>

## 4. How to use the application:

1. Start the application:

```sh
python3 app.py
```

2. Run the requestor script:

```sh
./requestor_script.sh
```

3. Look into the logs of the application:
```sh
# This should return the logs
cat ./logs/app.log
```

## 5. How to integrate ElasticSearch with the logs

TBD...