import requests
import sys
import subprocess
import time

from decimal import Decimal
import json
import boto3

## Supress Python Boto known Warning
import warnings
warnings.filterwarnings("ignore")


tt_url="https://ust-test.atlassian.net/rest/servicedeskapi/servicedesk/"
headers={'content-type': 'application/json', 'Authorization': 'Basic cmFodWw4Ni4wOEBnbWFpbC5jb206TnNMdXpTVXZtNlk1QnlCTWlnZjk4QjZE'}
endpoint_url="https://dynamodb.us-east-2.amazonaws.com"
table_name="finops"
projectID=""
queueID=""
d={}
dd={}
ddd={}


def create_temp_tag_file():
    filename="ticketdata.json"
    #"tag_file_" + time.strftime("%Y%m%d-%H%M%S")
    return filename

def write_tag_to_file(tkey,tvalue):
    file=open(create_temp_tag_file(), 'a')
    file.write(tkey + ":" + tvalue + "\n")
    file.close()

def list_issue2(pID,qID):
    url_issue=tt_url + pID + "/queue/" + qID + "/issue"
    res_is=requests.get(url_issue, headers=headers)
    ddd={}
    ddd=res_is.json()
    mm={}
    mmm=[]
    for m in ddd:
        if m == 'values':
            print("\nFound Tickets:")
            for k in ddd[m]:
                for z in k:
                    if z == 'fields':
                        if k[z]['reporter'] != None:
                             mm.update({'reporter': k[z]['reporter']['emailAddress']})
                          
                        if k[z]['assignee'] != None:
                                 mm.update({'assignee': k[z]['assignee']['emailAddress']})
                            
                        mm.update({'summary': k[z]['summary']})      
                    elif z == "self":
                        continue
                    elif z == "key":
                        print(k[z])
                        mm.update({z : k[z]})
                    else:
                        mm.update({z : k[z]})
                with open("jsondata.json", "w") as outfile:
                    json.dump(mm, outfile)
                with open("jsondata.json") as json_file:
                    data_list = json.load(json_file, parse_float=Decimal)
                    load_data(data_list)


def list_queue_components(pID):
    url_queue=tt_url + pID + "/queue"
    res_q=requests.get(url_queue, headers=headers)
    dd={}
    dd=res_q.json()
    for m in dd:
        if m == 'values':
            for k in dd[m]:
                if 'All open tickets' == k['name']:
                   queueID = k['id']
                   list_issue2(pID,queueID)


def list_projects():
   print("\nTicketing Tool URL - " + tt_url)
   arg1=raw_input("Enter the Project Name\n")
   res=requests.get(tt_url, headers=headers)
   d=res.json()
   for i in d:
       if i == 'values':
            for j in d[i]:
                if arg1 == j['projectName']:
                   projectID = j['id']
                   list_queue_components(projectID)
                #else:
                 #  print("Error - project not found. Exiting programe\n")
                  # sys.exit(1)


def load_data(data, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-east-2.amazonaws.com", region_name="us-east-2")

    table = dynamodb.Table(table_name)
    print("Database Endpoint - " + endpoint_url)
    print("Table Name - " + table_name)
    print("Adding entry to database")
    print( data)
    table.put_item(Item=data)




if __name__ == '__main__':
    
    list_projects()
   




