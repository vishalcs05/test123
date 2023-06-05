from flask import Flask, abort
import csv
import json
import logging
import sys
import os
import pymysql
import socket

app = Flask(__name__)

def check_sql():
    query2 = "SELECT * FROM TBL_USER LIMIT 1"
    cursor.execute(query2)
    print(cursor.fetchall())
    if cursor.rowcount == 0:
        pass
    else:
        print("SQL TABLE is not empty")
        return 1

@app.route('/addtosql',methods = ['GET'])
def add_to_sql():
    result4 = check_sql()
    if result4 == 1:
        return "SQL TABLE is not empty\n"
    try:
        with open ("/data/app/data_new.csv") as newfile:
            reader = csv.reader(newfile)
            for row in reader:
                if row[0] == "name":
                    pass
                else:
                    query = "INSERT INTO TBL_USER (NAME,STREET,CITY,STATE,USER_DATE) VALUES (%s, %s, %s, %s, %s)"
                    #print("name " + row[0], "street " + row[1], "city " + row[2], "state " + row[3], "date " + row[4])
                    val = (row[0], row[1], row[2], row[3], row[4])
                    try:
                        cursor.execute(query, val)
                        db.commit()
                    except Exception as w:
                        print(w)
                        return "sql error\n", 500
        return "Inserted in sql\n"
    except Exception as e:
        print(e)

def convert_to_json():
    data = {}
    try:
        query1 = "SELECT * FROM TBL_USER"
        cursor = db.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query1)
        result_query = cursor.fetchall()
        result = json.dumps(result_query)
        return result
    except Exception as e:
        print(e)

@app.route('/api',methods = ['GET'])
def return_json():
    try:
        to_return = convert_to_json()
        return to_return
    except Exception as error:
        print(error)

@app.route('/healthcheck',methods = ['GET'])
def check_health():
    ip = socket.gethostbyname(socket.gethostname())
    if ip == "172.31.3.200":
        server = "webserver1"
    else:
        server = "webserver2"
    string1 = "all good from " + server + "\n"
    return string1
    return abort(500)


db = pymysql.connect(
    host="testdb.jidpzbzqfdicy.ap-south-1.rds.amazonaws.com",
    user="admin",
    password="testing123",
    database="USERS" )

cursor = db.cursor()
app.run(host="0.0.0.0",port=8888)
