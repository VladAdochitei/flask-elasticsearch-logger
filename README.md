# flask-elasticsearch-logger
Flask Logger with ElasticSearch functionality.

## Application Context
I have developed a very simple flask application which resembles a web server written in python. this code is present in app.py. The web application has 2 routes, the `/` and `/operation` routes, which are defined to log different information on the request, request's source IP and the log category (ERROR, INFO, WARNING, etc.). 

In this scenario, the purpose of the logger is to identify unauthorized requests on the routes, so we can Identify if an external entity is trying to sniff the web server's routes in order to find an attack vector.

The application's logs can be found in `/logs/app.log` file, and are standardised.

## Simulation context
In order to simulate a bunch of requests to our application we should run the `requestor.script.sh` which is a simple shell script that will perform a bunch of requests on our web application. this is useful because it will generate a log of logging data which will then be used by our ElasticSearch application