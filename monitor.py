import random
import urllib
import re
import boto3
import botocore

sns = boto3.client('sns')

def monitor_angrychair(event, context):

    url = "http://shop.angrychairbrewing.com/product-category/beers/"
    snsUrn = 'arn:aws:sns:us-east-1:619096257283:monitor-angrychair'
    bucket_name = "your-bucket"
    file_name =  "angrychair.txt"

    myfile = ""
    myfile = urllib.urlopen(url).read()

    myfile = myfile[:50000]
    encoded_string = myfile.encode("utf-8")

    s3_path = file_name
    try:
        client = boto3.client('s3')
        lastpage_content = ""
        lastpage = client.get_object(Bucket=bucket_name, Key=s3_path)
        lastpage_content = lastpage['Body'].read()
    except botocore.exceptions.ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "NoSuchKey":
            lastpage_content = "file did not exist"
            client.Bucket(bucket_name).put_object(Key=s3_path, Body=lastpage_content)

    try:
        if lastpage_content == encoded_string:
            returnvalue = "This is the same"
        else:
            returnvalue = "This has changed."
            s3 = boto3.resource("s3")
            s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_string)
            s3.Bucket(bucket_name).put_object(Key="last-" + s3_path, Body=lastpage_content)
            print("notifying sns")
            sns.publish(
                TargetArn=snsUrn,
                Message=(
                    url + ' has changed.'
                )
            )
    except e:
        returnvalue = "failed to get content" + e

    response = {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': returnvalue
            }
        }
    }

    return response
