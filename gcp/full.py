import boto3
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
  for i in tags:
      print(i + ": " + tags[i])
  
# [UPDATING FILE]
  with open(template_path, 'r') as content_file:
       template = json.load(content_file)
# 
#  print("\n\nUpdating template...\n")
#  with open(template_path,'r+') as file:
#    file_data = json.load(file)
#    file_data["labels"].append(new_data)
#    file.seek(0)
#    json.dump(file_data, file, indent = 4)
#  
#  addlabels = { tags }
#  write_json(addlabels)
  

  config = template

  return compute.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()

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
    instances = list_instances()
    print('Instances in project %s and zone %s:' % (project, zone))
    for instance in instances:
        print(' - ' + instance['name'])
