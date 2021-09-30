import requests
import sys
import subprocess
import time
from decimal import Decimal
import json, yaml
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
import warnings
import os.path
import json
from azure.common.credentials import ServicePrincipalCredentials
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import DeploymentMode
from azure.mgmt.resource.resources.models import DeploymentProperties
from azure.mgmt.resource.resources.models import Deployment


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
   stack_name = raw_input("i\nEnter STACK Name\n")

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
           print("\nUpdating CloudFormation Stack - {}".format(stack_name))
           response = client.update_stack(
           StackName=stack_name.strip(),
           TemplateBody=content,
           Tags=make_kv_from_args(tags)
        )
           #for resource in response['StackResources']:
            #  print resource['PhysicalResourceId']



def azure_new_deploy():
        template_path = raw_input("Enter template location\n")
        deployment_name = raw_input("\nEnter Deployment Name\n")
        resourcegroup_name = raw_input("\nEnter Resource-group Name\n")
        location = raw_input("\nEnter Location/Region\n")

        subscription_id = os.environ.get('AZURE_SUBSCRIPTION_ID', '11111111-1111-1111-1111-111111111111') # your Azure Subscription Id

        credentials = ServicePrincipalCredentials(
            client_id=os.environ['AZURE_CLIENT_ID'],
            secret=os.environ['AZURE_CLIENT_SECRET'],
            tenant=os.environ['AZURE_TENANT_ID']
        )

        credential = DefaultAzureCredential()

        client = ResourceManagementClient(credential, subscription_id)

        client.resource_groups.create_or_update(
           resource_group,
            {
                'location': location
            }
         )

        #template_path = os.path.join(os.path.dirname(__file__), 'templates', 'template.json')
        with open(template_path, 'r') as template_file_fd:
            template = json.load(template_file_fd)
        

        for i in template: 
            if i == 'parameters':
                template['parameters']['resourceTags']={"type": "object", "defaultValue": { 
            "Environment": "Dev",
            "Project": "Tutorial"}
            }

        for i in template:
            if i == 'resources':
               L=len(template['resources'])
               #L=L-1
               for k in range(0, L):
                  template[i][k]['tags']="[parameters('resourceTags')]"

        #print(template)


        parameters = {
        "location": {
            "value": "eastus"
        },
        "networkInterfaceName": {
            "value": "rahul-test-machine537-test"
        },
        "enableAcceleratedNetworking": {
            "value": "true"
        },
        "networkSecurityGroupName": {
            "value": "rahul-test-machine-nsg-test"
        },
        "networkSecurityGroupRules": {
            "value": [
                {
                    "name": "SSH",
                    "properties": {
                        "priority": 300,
                        "protocol": "TCP",
                        "access": "Allow",
                        "direction": "Inbound",
                        "sourceAddressPrefix": "*",
                        "sourcePortRange": "*",
                        "destinationAddressPrefix": "*",
                        "destinationPortRange": "22"
                    }
                }
            ]
        },
        "subnetName": {
            "value": "default"
        },
        "virtualNetworkName": {
            "value": "Test1-vnet"
        },
        "addressPrefixes": {
            "value": [
                "172.21.0.0/16"
            ]
        },
        "subnets": {
            "value": [
                {
                    "name": "default",
                    "properties": {
                        "addressPrefix": "172.21.0.0/24"
                    }
                }
            ]
        },
        "publicIpAddressName": {
            "value": "rahul-test-machine-ip-test"
        },
        "publicIpAddressType": {
            "value": "Static"
        },
        "publicIpAddressSku": {
            "value": "Standard"
        },
        "virtualMachineName": {
            "value": "rahul-test-machine-1-test"
        },
        "virtualMachineComputerName": {
            "value": "rahul-test-machine-1-test"
        },
        "virtualMachineRG": {
            "value": "Test1"
        },
        "osDiskType": {
            "value": "StandardSSD_LRS"
        },
        "virtualMachineSize": {
            "value": "Standard_DS1_v2"
        },
        "adminUsername": {
            "value": "test123"
        },
        "adminPassword": {
            "value": "1A2s3d4f5g6h7j@"
        },
        "zone": {
            "value": "1"
        }
    }

        deployment_properties = DeploymentProperties(mode=DeploymentMode.incremental, template=template, parameters=parameters)

        deployment_async_operation = client.deployments.begin_create_or_update(
            resourcegroup_name,
            deployment_name,
            Deployment(properties=deployment_properties)
        )
        deployment_async_operation.wait()


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
      choice_az = raw_input("Enter 'a' for New Stack.\nEnter 'b' for existig Stack.\n")
      choice_az = str(choice_az)
      if choice_az == 'a':
           azure_new_deploy()
      elif choice_cf == 'b':
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



## Starting point
if __name__ == '__main__':

   start()


