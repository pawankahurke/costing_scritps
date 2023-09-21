import boto3
import datetime
import csv

# Function to get the daily cost for a given AWS account on a specific date
def get_daily_cost_for_account(account_id, date):
    # Initialize a Boto3 Cost Explorer client
    cost_explorer = boto3.client('ce')

    # Define the time period for the cost report (single day)
    time_period = {
        'Start': date.strftime('%Y-%m-%d'),
        'End': date.strftime('%Y-%m-%d')
    }

    # Define the granularity (DAILY) and metrics (BlendedCost)
    granularity = 'DAILY'
    metrics = ['BlendedCost']

    # Query the AWS Cost Explorer API to get the cost data
    response = cost_explorer.get_cost_and_usage(
        TimePeriod=time_period,
        Granularity=granularity,
        Metrics=metrics,
        Filter={
            "Dimensions": {
                "Key": "LINKED_ACCOUNT",
                "Values": [account_id]
            }
        }
    )

    # Extract the daily cost data
    daily_costs = response['ResultsByTime']

    return daily_costs

# Function to get the account alias (name) for a given AWS account ID
def get_account_alias(account_id):
    # Initialize a Boto3 IAM client
    iam_client = boto3.client('iam')

    try:
        # Get the account alias
        response = iam_client.list_account_aliases()
        if 'AccountAliases' in response:
            return response['AccountAliases'][0]
    except Exception as e:
        print(f"Error fetching account alias for {account_id}: {str(e)}")

    return "N/A"

# Define the AWS account IDs you want to calculate the daily cost for
account_ids = ['690940206480', '971986416690', '859756588904']  # Replace with your AWS account IDs

# Define the date range for which you want to calculate the cost
start_date = datetime.datetime(2023, 9, 6)  # Replace with your desired start date
end_date = datetime.datetime(2023, 9, 6)    # Replace with your desired end date

# Create a list to store daily cost data
daily_cost_data = []

# Iterate through the date range and calculate the daily cost for each account
current_date = start_date
while current_date <= end_date:
    for account_id in account_ids:
        daily_costs = get_daily_cost_for_account(account_id, current_date)
        account_alias = get_account_alias(account_id)

        for data_point in daily_costs:
            date = data_point['TimePeriod']['Start']
            cost = float(data_point['Total']['BlendedCost']['Amount'])
            daily_cost_data.append({'Account ID': account_id, 'Alias Name': account_alias, 'Date': date, 'Cost': cost})

    # Move to the next day
    current_date += datetime.timedelta(days=1)

# Define the output file path (e.g., CSV file)
output_file = 'daily_costs_datewise.csv'

# Write the daily cost data to the CSV file
with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ['Account ID', 'Alias Name', 'Date', 'Cost']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in daily_cost_data:
        writer.writerow(row)

# Print a message to confirm the file was written
print(f"Daily costs saved to {output_file}")
