import requests
import sys
import subprocess
import time

from decimal import Decimal
import json
import boto3


headers={'content-type': 'application/json', 'Authorization': 'Basic cmFodWw4Ni4wOEBnbWFpbC5jb206TnNMdXpTVXZtNlk1QnlCTWlnZjk4QjZE'}
arg1=sys.argv[1]
projectID=""
queueID=""
d={}
dd={}
ddd={}


def create_temp_tag_file():
    filename="ticketdata.json"
    #"tag_file_" + time.strftime("%Y%m%d-%H%M%S")
    return filename


def git_log():
    process = subprocess.Popen(['git', 'log', '-1'],
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    get_issue_key(stdout)


def get_issue_key(stdout):
    l=[]
    l=stdout.split('  ')
    iss_k=l[-1].split(':')[0]
    list_issue(iss_k)


def list_issue(issueKey):
    url_issue="https://ust-test.atlassian.net/rest/api/2/issue/" + issueKey 
    res_is=requests.get(url_issue, headers=headers)
    ddd={}
    ddd=res_is.json()
    for m in ddd['fields']:
        if m == 'project':
            tag_key='Project'
            tag_value=ddd['fields'][m]['name']
            write_tag_to_file(tag_key,tag_value)
    
    for m in ddd['fields']:
        if m == 'priority':
            tag_key='Priority'
            tag_value=ddd['fields'][m]['id']
            write_tag_to_file(tag_key,tag_value)
    
    #for m in ddd['fields']:
    #    if m == 'labels':
    #        tag_key='Labels'
    #        tag_value=ddd['fields'][m]
    #        write_tag_to_file(tag_key,tag_value)
    
    for m in ddd['fields']:
        if m == 'creator':
            tag_key='Creator'
            tag_value=ddd['fields'][m]['emailAddress']
            write_tag_to_file(tag_key,tag_value)
        
    tag_key="IssueKey"
    tag_value=issueKey
    write_tag_to_file(tag_key,tag_value)


def write_tag_to_file(tkey,tvalue):
    file=open(create_temp_tag_file(), 'a')
    file.write(tkey + ":" + tvalue + "\n")
    file.close()

def list_issue2(pID,qID):
    url_issue="https://ust-test.atlassian.net/rest/servicedeskapi/servicedesk/" + pID + "/queue/" + qID + "/issue"
    res_is=requests.get(url_issue, headers=headers)
    ddd={}
    ddd=res_is.json()
    mm={}
    mmm=[]
    for m in ddd:
        if m == 'values':
            for k in ddd[m]:
                for z in k:
                    if z == 'fields':
                        if k[z]['reporter'] != None:
                            #write_tag_to_file("reporter",str(k[z]['reporter']['emailAddress']))
                             mm.update({'reporter': k[z]['reporter']['emailAddress']})
                            #print "reporter: " + str(k[z]['reporter']['emailAddress'])
                          
                        if k[z]['assignee'] != None:
                                # write_tag_to_file("assignee",str(k[z]['assignee']['emailAddress']))
                                 mm.update({'assignee': k[z]['assignee']['emailAddress']})
                                 #print "assignee: " + str(k[z]['assignee']['emailAddress'])
                            
                        #write_tag_to_file("summary",str(k[z]['summary']))     
                        mm.update({'summary': k[z]['summary']})      
                            #print "description: " + str(k[z]['summary'])
                    elif z == "self":
                        continue
                    else:
                        mm.update({z : k[z]})
                        #write_tag_to_file(z,k[z])
                        #print z + ": " + str(k[z])
                #prepare_load()
                #json_object = json.dumps(mm, indent = 4)
                #print(json_object)
                with open("jsondata.json", "w") as outfile:
                    json.dump(mm, outfile)
                with open("jsondata.json") as json_file:
                    data_list = json.load(json_file, parse_float=Decimal)
                    load_data(data_list)
                    #print(data_list)


def list_queue_components(pID):
    url_queue="https://ust-test.atlassian.net/rest/servicedeskapi/servicedesk/" + pID + "/queue"
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
   url_project="https://ust-test.atlassian.net/rest/servicedeskapi/servicedesk/"
   res=requests.get(url_project, headers=headers)
   d=res.json()
   for i in d:
       if i == 'values':
            for j in d[i]:
                if arg1 == j['projectName']:
                   projectID = j['id']
                   list_queue_components(projectID)


    




##############################
## DynamoDB upload ###########
##############################

def load_data(data, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-east-2.amazonaws.com", region_name="us-east-2")

    table = dynamodb.Table('finops')
    #for d in data:
     #   issueid = int(d['id'])
      #  issuekey = d['key']
       # issuetitle = d['summary']
        #reporter = d['reporter']
        #assignee = d['assignee']
        #print("Adding item:", issueid, issuekey, issuetitle, reporter, assignee)
    print(data)
    table.put_item(Item=data)


#def prepare_load():
    # json_object = json.dumps(dictionary, indent = 4) 
    # print(json_object)




if __name__ == '__main__':
    list_projects()
   



#git_log()
#list_projects()

