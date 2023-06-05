FROM centos:7

COPY app.py /opt/app.py

COPY requirements.txt /tmp/requirements.txt

COPY data.csv /opt/data_new.csv

RUN yum install python3-pip -y && \
    pip3 install -r /tmp/requirements.txt

CMD ["python3", "/opt/app.py"]
