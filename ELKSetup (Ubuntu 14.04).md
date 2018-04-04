# Install Java
```
sudo add-apt-repository -y ppa:webupd8team/java
sudo apt-get update
sudo apt-get -y install oracle-java8-installer
```

# Install Elasticsearch
```
wget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
echo "deb http://packages.elastic.co/elasticsearch/2.x/debian stable main" | sudo tee -a /etc/apt/sources.list.d/elasticsearch-2.x.list
sudo apt-get update
sudo apt-get -y install elasticsearch
```

# Edit Elasticsearch config
```sudo nano /etc/elasticsearch/elasticsearch.yml```

## Assumptions
You want to restrict access to Elasticsearch to prevent external users reading data or shutting down the system.

## Changes
Modify the `network.host:` entry to read `network.host: localhost`

# Start Elasticsearch
```
sudo service elasticsearch restart
sudo update-rc.d elasticsearch defaults 95 10
```

# Install Kibana
```
echo "deb http://packages.elastic.co/kibana/4.5/debian stable main" | sudo tee -a /etc/apt/sources.list.d/kibana-4.5.x.list
sudo apt-get update
sudo apt-get -y install kibana
```

# Edit Kibana Config
```sudo nano /opt/kibana/config/kibana/yml```

## Changes
Modify `server.host` to specify `server.host: "localhost"`

# Start Kibana

```
sudo update-rc.d kibana defaults 96 9
sudo service kibana start
```

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
Then
```sudo service nginx restart```

# Install logstash
```
echo 'deb http://packages.elastic.co/logstash/2.2/debian stable main' | sudo tee /etc/apt/sources.list.d/logstash-2.2.x.list
sudo apt-get update
sudo apt-get install logstash
```

## Generate SSL certificates
```sudo mkdir -p /etc/pki/tls/certs```

```sudo mkdir /etc/pki/tls/private```

Two options - 1 configure SSL to use IP or configure SSL to use DNS.

### Configure SSL / TLS to use IP addressess
```sudo nano /etc/ssl/openssl.cnf```

Find the [ v3_ca ] section of the file and add the following underneath:

```subjectAltName = IP: {use the private IP of the ELK server}```

Now generate SSL cert and private key in the appropriate locations (/etc/pki/tls/)

```
cd /etc/pki/tls
sudo openssl req -config /etc/ssl/openssl.cnf -x509 -days 3650 -batch -nodes -newkey rsa:2048 -keyout private/logstash-forwarder.key -out certs/logstash-forwarder.crt
```

Copy the logstash-forwarder.crt to all servers that will send logs to logstash. 

### Configure SSL / TLS to use DNS
If you have a DNS setup with your private internetz, create an A record that contains the ELK box's private IP address. This will be used as the domain name to generate the servers perivat cert - marked as {ELK Server Domain Name} below. 
An alternative is to use an A record that points to the server's public IP address. 
Ensure that the log source servers will be able to resolve the domain name to ELKserver.

```
cd /etc/pki/tls
sudo openssl req -subj '/CN={ELK Server Domain Name}' -x509 -days 3650 -batch -nodes -newkey rsa:2048 -keyout private/logstash-forwarder.key -out certs/logstash-forwarder.crt
```
## Configure Logstash
Configuration files are in JSON format and stored in /etc/logstash/conf.d.
There are three sections
* inputs
* filters
* outputs

### Example INPUT config
```
input {
    sniff {
        port => 4040
        ssl => true
        ssl_certificate => "/etc/pki/tls/certs/logstash-forwarder.crt"
        ssl_key => "/etc/pki/tls/private/logstash-forwarder.key"
    }
}
```
This specifies a `sniff` input that will listen on TCP port `4040` and will use the previously generated SSL certificate.

**Note**: Firewall changes may be required to allow this traffic. For example:

- Iptables: `sudo iptables -A INPUT -p tcp --dport 4040 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT`
- UFW: `sudo ufw allow 4040`
- etc.

### Example FILTER config
```
filter {
  if [type] == "syslog" {
    grok {
      match => { "message" => "%{SYSLOGTIMESTAMP:syslog_timestamp} %{SYSLOGHOST:syslog_hostname} %{DATA:syslog_program}(?:\[%{POSINT:syslog_pid}\])?: %{GREEDYDATA:syslog_message}" }
      add_field => [ "received_at", "%{@timestamp}" ]
      add_field => [ "received_from", "%{host}" ]
    }
    syslog_pri { }
    date {
      match => [ "syslog_timestamp", "MMM  d HH:mm:ss", "MMM dd HH:mm:ss" ]
    }
  }
}
```

### Example OUTPUT config
```
output {
  elasticsearch {
    hosts => ["localhost:9200"]
    sniffing => true
    manage_template => false
    index => "%{[@metadata][sniff]}-%{+YYYY.MM.dd}"
    document_type => "%{[@metadata][type]}"
  }
}
```

## Test and Restart

Test the logstash config:
```
sudo /opt/logstash/bin/logstash --configtest -f /etc/logstash/conf.d/
```

Restart logstash
```
sudo systemctl restart logstash
sudo systemctl enable logstash
```

# Load Kibana Dashboards

There are Kibana dashboards provided with Elastic to get things started quickly. Here the plan is to install them so the index patterns can be reused.

(Beats Dashboards 1.2.2 is for Kibana4 and the most suitable version at the time of writing)

```
curl -L -O https://download.elastic.co/beats/dashboards/beats-dashboards-1.2.2.zip
unzip beats-dashboards-*.zip
cd beats-dashboards-*
./load.sh
```

