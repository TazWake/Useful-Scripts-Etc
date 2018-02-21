# Install Java
```sudo add-apt-repository -y ppa:webupd8team/java```

```sudo apt-get update```

```sudo apt-get -y install oracle-java8-installer```

# Install Elasticsearch
```wget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -```

```echo "deb http://packages.elastic.co/elasticsearch/2.x/debian stable main" | sudo tee -a /etc/apt/sources.list.d/elasticsearch-2.x.list```

```sudo apt-get update```

```sudo apt-get -y install elasticsearch```

# Edit Elasticsearch config
```sudo nano /etc/elasticsearch/elasticsearch.yml```

## Assumptions
You want to restrict access to Elasticsearch to prevent external users reading data or shutting down the system.

## Changes
Modify the 'network.host:' entry to read 'network.host: localhost'

# Start Elasticsearch
```sudo service elasticsearch restart```

```sudo update-rc.d elasticsearch defaults 95 10```

# Install Kibana
```echo "deb http://packages.elastic.co/kibana/4.5/debian stable main" | sudo tee -a /etc/apt/sources.list.d/kibana-4.5.x.list```




