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
Modify the `network.host:` entry to read `network.host: localhost`

# Start Elasticsearch
```sudo service elasticsearch restart```

```sudo update-rc.d elasticsearch defaults 95 10```

# Install Kibana
```echo "deb http://packages.elastic.co/kibana/4.5/debian stable main" | sudo tee -a /etc/apt/sources.list.d/kibana-4.5.x.list```

```sudo apt-get update```

```sudo apt-get -y install kibana```

# Edit Kibana Config
```sudo nano /opt/kibana/config/kibana/yml```

## Changes
Modify `server.host` to specify `server.host: "localhost"`

# Start Kibana

```sudo update-rc.d kibana defaults 96 9```

```sudo service kibana start```

# Install nginx

```sudo apt-get install nginx apache2-utils```

## Configure nginx
### Create kibana user
```sudo htpasswd -c /etc/nginx/htpasswd.users [USERNAME]```
Remeber the details used here as they are required to access the kibana interface.

### Edit kibana config
```sudo nano /etc/nginx/sites-available/default```
Replace the existing content with:

```
server {
    listen 80;

    server_name example.com;

    auth_basic "Restricted Access";
    auth_basic_user_file /etc/nginx/htpasswd.users;

    location / {
        proxy_pass http://localhost:5601;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;        
    }
}
```

```sudo service nginx restart```

# Install logstash
```echo 'deb http://packages.elastic.co/logstash/2.2/debian stable main' | sudo tee /etc/apt/sources.list.d/logstash-2.2.x.list```

```sudo apt-get update```

```sudo apt-get install logstash```

## Generate SSL certificates
```sudo mkdir -p /etc/pki/tls/certs```
```sudo mkdir /etc/pki/tls/private```
### Configure SSL / TLS to use IP addressess

### Configure SSL / TLS to use DNS



