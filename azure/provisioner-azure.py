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

        #parameter_path =  os.path.join(os.path.dirname(__file__), 'parameters', 'parameter.json')
        #with open(parameter_path, 'r') as parameter_file_fd:
           # parameters = json.load(parameter_file_fd)
        
        #print(parameters)
        deployment_properties = DeploymentProperties(mode=DeploymentMode.incremental, template=template, parameters_link='file:///root/machineLearning_from_zero/azure/parameters/parameter.json')
        

        deployment_async_operation = client.deployments.begin_create_or_update(
            resource_group,
            'rahul-azure-test',
            Deployment(properties=deployment_properties)
        )
        deployment_async_operation.wait()



deploy()
