#To calculate the daily cost of multiple cloud providers like AWS, Azure, and GCP and generate a daily report as an external file with account ID, date, and cost for each account, you'll need to use the respective SDKs for each cloud provider (Boto3 for AWS, Azure SDK for Azure, and Google Cloud SDK for GCP) and then combine the data into a single report.




import boto3
from azure.identity import DefaultAzureCredential
from azure.mgmt.consumption import ConsumptionManagementClient
from google.cloud import billing_v1

import datetime
import csv

# Function to get the daily cost for an AWS account
def get_aws_daily_cost(account_id, account_name):
    ce = boto3.client('ce')
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=1)
    response = ce.get_cost_and_usage(
        TimePeriod={
            'Start': start_date.strftime('%Y-%m-%d'),
            'End': end_date.strftime('%Y-%m-%d')
        },
        Granularity='DAILY',
        Metrics=['UnblendedCost'],
        Filter={
            'Dimensions': {
                'AccountId': [account_id]
            }
        }
    )
    cost = float(response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount'])
    return cost

# Function to get the daily cost for an Azure account
def get_azure_daily_cost(subscription_id):
    credentials = DefaultAzureCredential()
    consumption_client = ConsumptionManagementClient(credentials, subscription_id)
    usage_list = consumption_client.usage_details.list(
        filter=f"usageStart ge {datetime.datetime.now() - datetime.timedelta(days=1)} and usageEnd le {datetime.datetime.now()}"
    )
    total_cost = sum(usage.total_cost for usage in usage_list)
    return total_cost

# Function to get the daily cost for a GCP account
def get_gcp_daily_cost(project_id):
    client = billing_v1.CloudBillingClient()
    billing_account_name = f"billingAccounts/{project_id}/billingAccount"
    billing_account = client.get_billing_account(name=billing_account_name)
    cost = client.list_project_billing_info(name=billing_account_name, pageSize=1).next().spend
    return cost

# Define your cloud provider accounts and account names
aws_accounts = [
    {'id': '690940206480', 'name': 'pk'},
    {'id': 'AWS_ACCOUNT_ID_2', 'name': 'AWS Account 2'},
]

azure_subscription_ids = [
    'AZURE_SUBSCRIPTION_ID_1',
    'AZURE_SUBSCRIPTION_ID_2',
]

gcp_project_ids = [
    'GCP_PROJECT_ID_1',
    'GCP_PROJECT_ID_2',
]

# Get the current date
current_date = datetime.date.today()
current_date_str = current_date.strftime('%Y-%m-%d')

# Create a unique filename based on the current date
output_file = f'daily_costs_{current_date_str}.csv'

# Calculate and store the daily costs for each account
daily_costs = []

# AWS
for aws_account in aws_accounts:
    aws_cost = get_aws_daily_cost(aws_account['id'], aws_account['name'])
    daily_costs.append({'AccountType': 'AWS', 'AccountID': aws_account['id'], 'AccountName': aws_account['name'], 'Date': current_date_str, 'Cost': aws_cost})

# Azure
for azure_subscription_id in azure_subscription_ids:
    azure_cost = get_azure_daily_cost(azure_subscription_id)
    daily_costs.append({'AccountType': 'Azure', 'AccountID': azure_subscription_id, 'Date': current_date_str, 'Cost': azure_cost})

# GCP
for gcp_project_id in gcp_project_ids:
    gcp_cost = get_gcp_daily_cost(gcp_project_id)
    daily_costs.append({'AccountType': 'GCP', 'AccountID': gcp_project_id, 'Date': current_date_str, 'Cost': gcp_cost})

# Write the data to an external CSV file
with open(output_file, mode='w', newline='') as csv_file:
    fieldnames = ['AccountType', 'AccountID', 'AccountName', 'Date', 'Cost']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for cost_data in daily_costs:
        writer.writerow(cost_data)

print(f'Daily costs saved to {output_file}')


#This script combines AWS, Azure, and GCP cost data and generates a daily report in a CSV file with the specified columns. Make sure to replace the placeholder values ('AWS_ACCOUNT_ID_1', 'AZURE_SUBSCRIPTION_ID_1', 'GCP_PROJECT_ID_1', etc.) with your actual account IDs or subscription IDs.
