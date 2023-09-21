import boto3
import os
import json
from datetime import datetime, timedelta
from botocore.exceptions import ClientError


def send_sns_notification(daily_cost, monthly_cost):
    sns = boto3.client('sns')
    topic_arn = os.environ['SNS_TOPIC_ARN']

    message = f"Today's AWS bill: ${daily_cost:.2f}\nTotal bill for the month: ${monthly_cost:.2f}"
    try:
        response = sns.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject='AWS Billing Update'
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print(f"Message sent to SNS topic {topic_arn}")

def lambda_handler(event, context):
    ce = boto3.client('ce')

    end = datetime.today().date().strftime('%Y-%m-%d')
    start_month = datetime.today().date().replace(day=1).strftime('%Y-%m-%d')
    start_day = (datetime.today() - timedelta(days=1)).date().strftime('%Y-%m-%d')

    print("The start date is ", start_month)
    print("The end date is ", end)

    response = ce.get_cost_and_usage(
        TimePeriod={
            'Start': start_month,
            'End': end
        },
        Granularity='DAILY',
        Metrics=['UnblendedCost'],
        GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
    )
    print(response)

    daily_cost = sum(float(res['Metrics']['UnblendedCost']['Amount']) for res in response['ResultsByTime'][-1]['Groups'])
    print("The daily cost is ", daily_cost)
    monthly_cost = sum(float(res['Metrics']['UnblendedCost']['Amount']) for day in response['ResultsByTime'] for res in day['Groups'])
    print("The monthly cost is ", monthly_cost)

    send_sns_notification(daily_cost, monthly_cost)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'daily_cost': daily_cost,
            'monthly_cost': monthly_cost
        })
    }
