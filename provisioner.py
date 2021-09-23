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
   #cf_create_stack(items[0])
   return items[0]

from urlparse import urlparse, parse_qs
def make_kv_from_args(tags):
    kv_pairs = []
    for key in tags:
        kv = {
            "Key":key,
            "Value":tags[key],
        }

        kv_pairs.append(kv)
    return kv_pairs


def cf_create_stack():
   value = raw_input("Enter template location\n")
   stack_name = raw_input("Enter STACK Name\n")

   # read entire file as yaml
   with open(value, 'r') as content_file:
       content = yaml.load(content_file)

   # convert yaml to json string
   content = json.dumps(content)
   cloud_formation_client = boto3.client('cloudformation')
   region="us-east-2"

   tags=get_items()
   print("Creating CloudFormation Stack with name - {}".format(stack_name))
   response = cloud_formation_client.create_stack(
       StackName=stack_name,
       TemplateBody=content,
       Tags=make_kv_from_args(tags)
   )


def cf_update_stack():
   
   value1=raw_input("Enter file location containing STACK Names\n")
   value = raw_input("Enter template location\n")

   # read entire file as yaml
   with open(value, 'r') as content_file:
       content = yaml.load(content_file)

   # convert yaml to json string
   content = json.dumps(content)

   file=open(value1, 'r')
   lines=file.readlines()

   client = boto3.client('cloudformation')
   tags=get_items()

   if lines:
        for stack_name in lines:
           print("Updating CloudFormation Stack - {}".format(stack_name))
           response = client.update_stack(
           StackName=stack_name.strip(),
           TemplateBody=content,
           Tags=make_kv_from_args(tags)
        )
           #for resource in response['StackResources']:
            #  print resource['PhysicalResourceId']


def start():
   choice = raw_input("Enter 1 for CloudFormation.\nEnter 2 for Azure ARM.\nEnter 3 for Terraform\nEnter 4 for GCP:\n ")
   choice = int(choice)

   if choice == 1:
      choice_cf = raw_input("Enter 'a' for New Stack.\nEnter 'b' for existig Stack.\n")
      choice_cf = str(choice_cf)
      if choice_cf == 'a':
           cf_create_stack()
      elif choice_cf == 'b': 
           cf_update_stack()
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



