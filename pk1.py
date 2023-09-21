import boto3
import datetime
import csv

# Function to get the daily cost for a given AWS account
def get_daily_cost_for_account(account_id, start_date, end_date):
    # Initialize a Boto2 Cost Explorer client
    cost_explorer = boto3.client('ce')

    # Define the time period for the cost report
    time_period = {
        'Start': start_date.strftime('%Y-%m-%d'),
        'End': end_date.strftime('%Y-%m-%d')
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

# Define the AWS account IDs you want to calculate the daily cost for
account_ids = ['690940206480', '971986416690', '859756588904']  # Replace with your AWS account IDs

# Define the start and end dates for the cost report (typically, one day)
start_date = datetime.datetime(2023, 9, 7)  # Replace with your desired start date
end_date = datetime.datetime(2023, 9, 8)    # Replace with your desired end date

# Create a list to store daily cost data
daily_cost_data = []

# Calculate the daily cost for each account and store it in the list
for account_id in account_ids:
    daily_costs = get_daily_cost_for_account(account_id, start_date, end_date)
    for data_point in daily_costs:
        date = data_point['TimePeriod']['Start']
        cost = float(data_point['Total']['BlendedCost']['Amount'])
        daily_cost_data.append({'Account ID': account_id, 'Date': date, 'Cost': cost})

# Define the output file path (e.g., CSV file)
output_file = 'daily_costs.csv'

# Write the daily cost data to the CSV file
with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ['Account ID', 'Date', 'Cost']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in daily_cost_data:
        writer.writerow(row)

# Print a message to confirm the file was written
print(f"Daily costs saved to {output_file}")

