import boto3
import datetime

# Function to get the daily cost for a given AWS account
def get_daily_cost_for_account(account_id, start_date, end_date):
    # Initialize a Boto3 Cost Explorer client
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

    # Extract the daily cost from the response
    daily_cost = sum(float(data_point['Total']['BlendedCost']['Amount']) for data_point in response['ResultsByTime'])

    return daily_cost

# Define the AWS account IDs you want to calculate the daily cost for
account_ids = ['690940206480', '971986416690']  # Replace with your AWS account IDs

# Define the start and end dates for the cost report (typically, one day)
start_date = datetime.datetime(2023, 9, 1)  # Replace with your desired start date
end_date = datetime.datetime(2023, 9, 5)    # Replace with your desired end date

# Calculate the daily cost for each account and sum them up
total_daily_cost = sum(get_daily_cost_for_account(account_id, start_date, end_date) for account_id in account_ids)

# Print the total daily cost
print(f"Total Daily Cost: ${total_daily_cost:.2f}")
