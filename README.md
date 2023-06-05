# Take-home-project

### Application code to return all users details from json file

##### Explanation:

1) Flask is used as application framework.
2) `/api` endpoint is giving the result in json.
3) `/healthcheck` endpoint is returning the health of application with http code 200, it also tells from which webserver is serving the request.
3) `/addtosql` endpoint is loading the csv in mysql if mysql table in already empty.
4) Using pymysql library to connect to mysql.


`/api` endpoint result
```
$ curl http://122.201.9.1/api
[{"NAME": "Duane Adams", "STREET": "Hojzi Path", "CITY": "Zurmubku", "STATE": "NY", "USER_DATE": "08/08/43"}, {"NAME": "Ruby Hampton", "STREET": "Seime Plaza", "CITY": "Ikduju", "STATE": "KS", "USER_DATE": "16/09/86"}, {"NAME": "Carl Johnson", "STREET": "Zopwe Drive", "CITY": "Ehazeru", "STATE": "RI", "USER_DATE": "27/11/64"}]

[output truncated]
```

`/healthcheck` endpoint result
```
$ curl http://122.201.9.1/healthcheck
all good from webserver1
```

PS: `122.201.9.1` is not actual IP of application as the app is not public.

##### Docker is used to host application

Dockerfile has been added in the repository. Using centos7 OS to host the application where installing required python modules and copying the application file and data csv in the image.
Also adding application startup during the container run itself.

Below is used to build image and run it on a virtual machine in AWS EC2.

```
# cd app #[change directory to file where Dockerfile and other files are present]
# docker build -t local/app .
# docker run -p 8888:8888 -itd local/app
```

### Load balancer configuration

##### HAPROXY has been used as load balancer for the application

Haproxy backend has two servers added in it where it checks if application is running on port 8888, where `172.31.3.200`[**webserver1**] is primary server and `172.31.15.189`[**webserver2**] is secondary server, request will only go to secondary server only when **webserver1** is down.

**`haproxy.cfg`** is added in the repo. Port 80 has been configured in the haproxy to make the application accesible, haproxy also has port 8080 configured where we can see application http stats and do its monitoring.

AWS EC2 virtual machine has been used to host the load balancer.

### Database server configuration

AWS RDS mysql has been used as database which is configured to run in master and read replica mode, all the read requests are going to read replica.
Master and replica are in sync as per the design of AWS RDS.

Have enabled snapshotting in RDS to take the backup, if RDS gets deleted or data gets wiped out it can be restored from snapshot.

Used below AWS doc to get the restoration testing done.
https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Tutorials.RestoringFromSnapshot.html

### Monitoring of application using Site 24X7

[site24x7](https://www.site24x7.com) has been used monitor the application where have whitelisted its Public IPs in the aws security group to monitor the application securely.

Added endpoint `http://122.201.9.1/healthcheck` URL check in site24x7 dashboard.
