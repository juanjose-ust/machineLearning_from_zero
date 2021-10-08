from pathlib import Path
import boto3
import sys
import json
import yaml
import os
import time
import warnings
import googleapiclient.discovery
from google.oauth2 import service_account

## Supress Python Boto known Warning
warnings.filterwarnings("ignore")

## DynamoDB query ###########
def get_items(dynamodb=None):
   if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-east-2.amazonaws.com", region_name="us-east-2")
   table = dynamodb.Table('finops')
   response = table.scan()
   items = response['Items']
   #cf_create_stack(items[0])
   return items[0]


def create_instance():

# [TEMPLATE INPUT]
  template_path = input("Enter template location\n")

# [GET TAGS]
  print("\nFetching metadata...\n")
  tags=get_items()
  print("done")
  print("\n(Metadata) =")

  orig_stdout = sys.stdout
  f = open('out.txt', 'w')
  sys.stdout = f

  for i in tags:
      print(i + ": " + tags[i])
      
  sys.stdout = orig_stdout
  f.close()
 
  with open('out.txt', 'r') as file:
    d = file.read()
    file.close()
    m = d.split("\n")
    s = "\n".join(m[:-1])
  
  with open('out.txt', 'w') as file:
    for i in range(len(s)):
      file.write(s[i])
    file.close()

  data = {'labels': {}}
# [UPDATING FILE]
  with open('template.yaml', 'r') as file:
    data2 = file.read()
    substring = 'properties'
    count = data2.count(substring)
  check = 0
  while check < count: 
    with open(template_path, 'r') as yamlfile:
         cur_yaml = yaml.safe_load(yamlfile)
         cur_yaml['resources'][check]['properties'].update(data)
         d = {}
         f = open('out.txt', 'r')
         for line in f.readlines():
             key,value = line.split(":")
             key = key.replace('@','-')
             value = value.replace('@','-')
             key = key.replace('.','-')
             value = value.replace('\n','')
             value = value.replace('.','-')
             value = value.replace(' ','')
             d[key.lower()] = value.lower()
         cur_yaml['resources'][check]['properties']['labels'].update(d)
         check += 1

    if cur_yaml:
         with open(template_path,'w') as yamlfile:
           yaml.safe_dump(cur_yaml, yamlfile) # Also note the safe_dump 

    print(cur_yaml)
    config = cur_yaml

#  return compute.instances().insert(
#        project=project,
#        zone=zone,
#        body=config).execute()

# [START list_instances]
def list_instances():
  result = compute.instances().list(project=project, zone=zone).execute()
  return result['items'] if 'items' in result else None
# [END list_instances]


if __name__ == '__main__':
    project = 'ust-edgeops-dagility-dev'
    zone = 'us-central1-a'
    credentials = service_account.Credentials.from_service_account_file(
      filename='cred.json',
        scopes=['https://www.googleapis.com/auth/cloud-platform'])
    compute = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)
    create_instance()
#    instances = list_instances()
    print('Instances in project %s and zone %s:' % (project, zone))
    for instance in instances:
        print(' - ' + instance['name'])
    text = Path("out.txt").read_text()
    print(text)
