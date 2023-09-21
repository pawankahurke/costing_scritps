import boto3
import datetime

# Initialize the AWS Cost Explorer client
ce = boto3.client('ce', region_name='us-east-1')  # Replace with your region

# Get the current date
today = datetime.date.today()

# Calculate the start and end date for the report (one day ago)
start_date = today - datetime.timedelta(days=1)
end_date = today

# Define the granularity for the report (DAILY)
granularity = 'DAILY'

# Query the Cost Explorer API for the daily cost
response = ce.get_cost_and_usage(
    TimePeriod={
        'Start': start_date.strftime('%Y-%m-%d'),
        'End': end_date.strftime('%Y-%m-%d')
    },
    Granularity=granularity,
    Metrics=['UnblendedCost'],  # You can customize metrics as needed
)

# Extract and calculate the daily cost
daily_cost = float(response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount'])

# Print the daily cost
print(f'Daily AWS Cost on {start_date}: ${daily_cost:.2f}')

