import os.path
import json
from azure.common.credentials import ServicePrincipalCredentials
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import DeploymentMode
from azure.mgmt.resource.resources.models import DeploymentProperties
from azure.mgmt.resource.resources.models import Deployment

## Supress Python Boto known Warning
import warnings



def deploy():
        warnings.filterwarnings("ignore")
        subscription_id = os.environ.get('AZURE_SUBSCRIPTION_ID', '11111111-1111-1111-1111-111111111111')   # your Azure Subscription Id
        resource_group = 'Test2'            # the resource group for deployment

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
                'location':'eastus'
            }
         )

        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'template.json')
        with open(template_path, 'r') as template_file_fd:
            template = json.load(template_file_fd)
        

        for i in template: 
            if i == 'parameters':
                template['parameters']['resourceTags']={"type": "object", "defaultValue": { 
            "Environment": "Dev",
            "Project": "Tutorial"}
            }
            #print("\n")
            #print("\n")
            #print(template[i])
        #print(template['parameters'])

        for i in template:
            if i == 'resources':
               L=len(template['resources'])
               #L=L-1
               for k in range(0, L):
                  template[i][k]['tags']="[parameters('resourceTags')]"
                  print(template[i][k])
                  print("\n")
                  print("\n")

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

        #deployment_properties = DeploymentProperties(mode=DeploymentMode.incremental, template=template, parameters=parameters)

        #deployment_async_operation = client.deployments.begin_create_or_update(
         #   resource_group,
           # 'rahul-azure-test',
            #Deployment(properties=deployment_properties)
        #)
        #deployment_async_operation.wait()



deploy()
