# cosmic_sdk/secrets/aws.py
import boto3
import json
import os

#TODO: List all available if the manager is initialized
class SecretsManager:
    def __init__(self, region: str = "us-west-2"):
        self.client = boto3.client('secretsmanager', region_name=region)
        self.env = os.getenv('COSMIC_ENV', 'dev')
        
    def get_secrets(self, org_id: str, connector_type: str) -> dict:
        """
        Get secrets for an org's connector
        Usage: secrets.get_secret('org_id', 'posthog')
        """
        path = f"{self.env}/orgs/{org_id}/connectors/{connector_type}"
        try:
            response = self.client.get_secret_value(SecretId=path)
            return json.loads(response['SecretString'])
        except Exception as e:
            print(f"Error getting secret: {str(e)}")
            return {}