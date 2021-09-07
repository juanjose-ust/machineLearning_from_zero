import requests
import sys
import subprocess

headers={'content-type': 'application/json', 'Authorization': 'Basic cmFodWw4Ni4wOEBnbWFpbC5jb206TnNMdXpTVXZtNlk1QnlCTWlnZjk4QjZE'}
arg1=sys.argv[1]
projectID=""
queueID=""
d={}
dd={}
ddd={}



def get_jira_issue_key():
    process = subprocess.Popen(['git', 'log', '-1'],
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    



def list_issue(pID):
    url_issue="https://ust-test.atlassian.net/rest/servicedeskapi/servicedesk/" + pID + "/queue/" + qID + "issue"
    res_is=requests.get(url_issue, headers=headers)
    ddd={}
    ddd=res_is.json()
    for m in ddd:
        if m == 'values':
            for k in dd[m]:
                if 'All open tickets' == k['name']:
                   queueID = k['id']

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
                   list_issue(pID,queueID)


def list_projects()
   url_project="https://ust-test.atlassian.net/rest/servicedeskapi/servicedesk/"
   res=requests.get(url_project, headers=headers)
   d=res.json()
   for i in d:
       if i == 'values':
            for j in d[i]:
                if arg1 == j['projectName']:
                   projectID = j['id']
                   list_queue_components(projectID)


    







get_jira_issue_key
#list_projects()

