import requests
import sys
import subprocess
import time

from decimal import Decimal
import json, yaml
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

## Supress Python Boto known Warning
import warnings
warnings.filterwarnings("ignore")

#arg1=sys.argv[1]

##############################
## DynamoDB query ###########
##############################

def get_items(dynamodb=None):
   if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-east-2.amazonaws.com", region_name="us-east-2")
   table = dynamodb.Table('finops')
   response = table.scan()
   items = response['Items']
   # Prints Items line by line
   #for i, j in enumerate(items):
     #print(j['assignee'])
   cf_create_stack(items[0])
   #make_kv_from_args(items[0])


from urlparse import urlparse, parse_qs
def make_kv_from_args(tags):
    #nvs = parse_qs(tags)
    kv_pairs = []
    for key in tags:
        kv = {
            "Key":key,
            "Value":tags[key],
        }

        kv_pairs.append(kv)
    #print(kv_pairs)
    return kv_pairs


def cf_create_stack(tags):
   value = raw_input("Enter template location\n")
   # file must in the same dir as script
   #template_file_location = 'terraform-aws-ec2-instance-cf.yaml'
   stack_name = 'finops-rahul'

   # read entire file as yaml
   with open(value, 'r') as content_file:
       content = yaml.load(content_file)

   # convert yaml to json string
   content = json.dumps(content)
   cloud_formation_client = boto3.client('cloudformation')
   region="us-east-2"

   print("Creating CloudFormation Stack with name - {}".format(stack_name))
   response = cloud_formation_client.create_stack(
       StackName=stack_name,
       TemplateBody=content,
       Tags=make_kv_from_args(tags)
   )

def start():
   choice = raw_input("Enter 1 for CloudFormation.\nEnter 2 for Azure ARM.\nEnter 3 for Terraform\nEnter 4 for GCP:\n ")
   choice = int(choice)

   if choice == 1:
      get_items()
   elif choice == 2:
      print('Currently doesnt support. Back to main menu\n')
      start()
   elif choice == 3:
      print('Currently doesnt support. Back to main menu\n')
      start()
   elif choice == 4:
      print('Currently doesnt support. Back to main menu\n')
      start()
   else:
      print("Wrong Choice, back to main menu\n")
      start()


if __name__ == '__main__':

   start() 
   #cf_create_stack()
  #with open("terraform-aws-ec2-instance-cf.json") as f:
   # data = json.load(f)
    #data["tags"] = '{ env: production, application: java }'
    #json.dump(data, open("terraform-aws-ec2-instance-cf.json", "w"), indent = 4)



