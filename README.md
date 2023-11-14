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
    - [5.1. Running ElasticSearchwith systemd](#51-running-elasticsearch-with-systemd)
    - [5.2. Ensure ElasticSearch is running](#52-ensure-elasticsearch-is-running)
- [6. Using ElasticSearch](#6-using-elasticsearch)
    - [6.1. Indexing the logs](#61-indexing-the-logs)
    - [6.2. Querying the logs](#62-querying-the-logs)
    
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

> Reference link: https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html

Installed the elasticsearch engine manually:

```sh
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.11.1-amd64.deb
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.11.1-amd64.deb.sha512
shasum -a 512 -c elasticsearch-8.11.1-amd64.deb.sha512 
sudo dpkg -i elasticsearch-8.11.1-amd64.deb
```

Installation output:

```
--------------------------- Security autoconfiguration information ------------------------------

Authentication and authorization are enabled.
TLS for the transport and HTTP layers is enabled and configured.

The generated password for the elastic built-in superuser is : 2GpaWu*RYcvAq7TxuXvk

If this node should join an existing cluster, you can reconfigure this with
'/usr/share/elasticsearch/bin/elasticsearch-reconfigure-node --enrollment-token <token-here>'
after creating an enrollment token on your existing cluster.

You can complete the following actions at any time:

Reset the password of the elastic built-in superuser with 
'/usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic'.

Generate an enrollment token for Kibana instances with 
 '/usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana'.

Generate an enrollment token for Elasticsearch nodes with 
'/usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s node'.

-------------------------------------------------------------------------------------------------
### NOT starting on installation, please execute the following statements to configure elasticsearch service to start automatically using systemd
 sudo systemctl daemon-reload
 sudo systemctl enable elasticsearch.service
### You can start elasticsearch service by executing
 sudo systemctl start elasticsearch.service

```

Export the elastic password:

```sh
export ELASTIC_PASSWORD="your_password" # The password is visible in thefirst installation of Elastic as clear text output.
```

### 5.1. Running ElasticSearch with systemd
Configure Elasticsearch daemon to start at boot time:
```sh
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable elasticsearch.service
```

Start/Stop the elasticsearch service:

```sh
sudo systemctl start elasticsearch.service
sudo systemctl stop elasticsearch.service
```

### 5.2. Ensure ElasticSearch is running
Prior to this command ensure the `ELASTIC_PASSWORD` environment variable is configured.

```sh
sudo curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200
```

The output of this command should look something like this:

```json
{
  "name" : "ThiccPadX",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "GdfxbztCQ5OKGDNguw1zGw",
  "version" : {
    "number" : "8.11.1",
    "build_flavor" : "default",
    "build_type" : "deb",
    "build_hash" : "6f9ff581fbcde658e6f69d6ce03050f060d1fd0c",
    "build_date" : "2023-11-11T10:05:59.421038163Z",
    "build_snapshot" : false,
    "lucene_version" : "9.8.0",
    "minimum_wire_compatibility_version" : "7.17.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "You Know, for Search"
}
```

Now we know that the ElasticSearch server is running.


## 6. Using ElasticSearch
To analyze these logs using Elasticsearch, you need to:
1. Index the logs: Ingest these logs into Elasticsearch. Elasticsearch uses indices to store and search data.
2. Query the indexed logs: Once the logs are indexed, you can query Elasticsearch to retrieve specific information.

### 6.1. Indexing the logs
Assuming the ElasticSearch instance is already running and accessible, `curl` will be used to index the logs from the `app.log` file:

```sh
curl -XPOST -u elastic:$ELASTIC_PASSWORD -H "Content-Type: application/json" https://localhost:9200/my_logs/_doc -d '
{
  "timestamp": "2023-11-07T14:07:57.503",
  "level": "INFO",
  "message": "GET request on operation page - IP:127.0.0.1"
  // Add other log fields similarly...
}
'
```

Now, this only has demonstration purposes, the actual log exporter will be another Python script that will look through the whole app.log file, parse everyline and generate a similar `JSON` document thta will be loaded into the ElasticSearch engine.

Running the script:

```sh
sudo python3 log_exporter.py
```

The output of that script should look something like this:

```
...
{...
index":"my_logs","_id":"IDX6zIsBrvfmCB4eB_hX","_version":1,"result":"created","_shards":{"total":2,"successful":1,"failed":0},"_seq_no":1633,"_primary_term":1}{"_index":"my_logs","_id":"ITX6zIsBrvfmCB4eB_iP","_version":1,"result":"created","_shards":{"total":2,"successful":1,"failed":0},"_seq_no":1634,"_primary_term":1}{"_index":"my_logs","_id":"IjX6zIsBrvfmCB4eB_jD","_version":1,"result":"created","_shards":{"total":2,"successful":1,"failed":0},"_seq_no":1635,"_primary_term":1}{"_index":"my_logs","_id":"IzX6zIsBrvfmCB4eCPgS","_version":1,"result":"created","_shards":{"total":2,"successful":1,"failed":0},"_seq_no":1636,"_primary_term":1}{"_index":"my_logs","_id":"JDX6zIsBrvfmCB4eCPhK","_version":1,"result":"created","_shards":{"total":2,"successful":1,"failed":0},"_seq_no":1637,"_primary_term":1}{"_index":"my_logs","_id":"JTX6zIsBrvfmCB4eCPh9","_version":1,"result":"created","_shards":{"total":2,"successful":1,"failed":0},"_seq_no":1638,"_primary_term":1}{"_index":"my_logs","_id":"JjX6zIsBrvfmCB4eCPjA","_version":1,"result":"created","_shards":{"total":2,"successful":1,"failed":0},"_seq_no":1639,"_primary_term":1}{"_index":"my_logs","_id":"JzX6zIsBrvfmCB4eCPjq","_version":1,"result":"created","_shards":{"total":2,"successful":1,"failed":0},"_seq_no":1640,"_primary_term":1}{"_index":"my_logs","_id":"KDX6zIsBrvfmCB4eCfge","_version":1,"result":"created","_shards":{"total":2,"successful":1,"failed":0},"_seq_no":1641,"_primary_term":1}{"_index":"my_logs","_id":"KTX6zIsBrvfmCB4eCfha","_version":1,"result":"created","_shards":{"total":2,"successful":1,"failed":0},"_seq_no":1642,"_primary_term":1}{"_index":"my_logs","_id":"KjX6zIsBrvfmCB4eCfiK","_version":1,"result":"created","_shards":{"total":2,"successfu
...
}

...
```

ElasticSearch indexed log format:

```json
{
  "_index": "my_logs",
  "_id": "IDX6zIsBrvfmCB4eB_hX",
  "_version": 1,
  "result": "created",
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 1633,
  "_primary_term": 1
}
```

### 6.2. Querying the logs
Once indexed, you can perform queries to retrieve specific information. For example, to get all logs that contain "Unauthorized" or errors, you could use a query like this:

```bash

curl -XGET -u elastic:$ELASTIC_PASSWORD -H "Content-Type: application/json" https://localhost:9200/my_logs/_search -d '
{
  "query": {
    "match": {
      "message": "Unauthorized"
    }
  }
}
'
```

That same command is dome in a more programmatic way thorough the `log_query.py` file:

```sh
sudo python3 log_query.py 
```

The output of the command should look something like this: 

```
Request successful!
{"took":74,"timed_out":false,"_shards":{"total":1,"successful":1,"skipped":0,"failed":0},"hits":{"total":{"value":396,"relation":"eq"},"max_score":1.4005797,"hits":[{"_index":"my_logs","_id":"bDX4zIsBrvfmCB4e1PJT","_score":1.4005797,"_source":{"timestamp": "2023-11-14 10:23:05,128", "loglevel": "WARNING", "message": "Unauthorized - POST request - at the index page", "ip_address": "127.0.0.1"}},{"_index":"my_logs","_id":"cDX4zIsBrvfmCB4e1fIb","_score":1.4005797,"_source":{"timestamp": "2023-11-14 10:23:05,215", "loglevel": "WARNING", "message": "Unauthorized - POST request - at the index page", "ip_address": "127.0.0.1"}},{"_index":"my_logs","_id":"cjX4zIsBrvfmCB4e1fJ9","_score":1.4005797,"_source":{"timestamp": "2023-11-14 10:23:05,238", "loglevel": "WARNING", "message": "Unauthorized - PUT request - at the index page", "ip_address": "127.0.0.1"}},{"_index":"my_logs","_id":"dDX4zIsBrvfmCB4e1fLb","_score":1.4005797,"_source":{"timestamp": "2023-11-14 10:23:05,261", "loglevel": "ERROR", "message": "Unauthorized - PUT request - on the operation page", "ip_address": "127.0.0.1"}},{"_index":"my_logs","_id":"djX4zIsBrvfmCB4e1vJG","_score":1.4005797,"_source":{"timestamp": "2023-11-14 10:23:05,291", "loglevel": "WARNING", "message": "Unauthorized - PUT request - at the index page", "ip_address": "127.0.0.1"}},{"_index":"my_logs","_id":"ejX4zIsBrvfmCB4e1_IJ","_score":1.4005797,"_source":{"timestamp": "2023-11-14 10:23:05,319", "loglevel": "WARNING", "message": "Unauthorized - POST request - at the index page", "ip_address": "127.0.0.1"}},{"_index":"my_logs","_id":"QzX4zIsBrvfmCB4ey_KC","_score":1.4005797,"_source":{"timestamp": "2023-11-14 10:23:04,534", "loglevel": "ERROR", "message": "Unauthorized - PUT request - on the operation page", "ip_address": "127.0.0.1"}},{"_index":"my_logs","_id":"TDX4zIsBrvfmCB4ezfKm","_score":1.4005797,"_source":{"timestamp": "2023-11-14 10:23:04,705", "loglevel": "WARNING", "message": "Unauthorized - POST request - at the index page", "ip_address": "127.0.0.1"}},{"_index":"my_logs","_id":"UDX4zIsBrvfmCB4ezvJx","_score":1.4005797,"_source":{"timestamp": "2023-11-14 10:23:04,741", "loglevel": "WARNING", "message": "Unauthorized - POST request - at the index page", "ip_address": "127.0.0.1"}},{"_index":"my_logs","_id":"UjX4zIsBrvfmCB4ezvLZ","_score":1.4005797,"_source":{"timestamp": "2023-11-14 10:23:04,749", "loglevel": "WARNING", "message": "Unauthorized - PUT request - at the index page", "ip_address": "127.0.0.1"}}]}}
```

END.


P.S. - I know it's best not to store passwords in clear text but in this project the passwor's presence doesn't affect anything, in an ideal scenario it would havebeen stored in an Environment Variable and grabbed with python's os library, `os.getenv('ELASTIC_PASSWORD')`...