import random
import urllib2
import re
import boto3
import botocore

sns = boto3.client('sns')

def monitor_angrychair(event, context):

    url = "https://shop.angrychairbrewing.com/product-category/beers/feed/"
    clickable_link = "https://shop.angrychairbrewing.com/product-category/beers/"
    snsUrn = 'arn:aws:sns:us-east-1:619096257283:monitor-angrychair'
    bucket_name = "your-tracker"
    file_name =  "angrychair.txt"

    req = urllib2.Request(url)
    myfile = ""
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0")
    myfile = urllib2.urlopen(req).read()

    myfile = myfile[:50000]
    encoded_string = myfile.encode("utf-8")
    encoded_string = re.sub("lastBuildDate.*\/lastBuildDate", "", encoded_string.rstrip())
    
    s3_path = file_name
    try:
        client = boto3.client('s3')
        lastpage_content = ""
        lastpage = client.get_object(Bucket=bucket_name, Key=s3_path)
        lastpage_content = lastpage['Body'].read()
        
        lastpage_content = re.sub("lastBuildDate.*\/lastBuildDate", "", lastpage_content.rstrip())
        
    except botocore.exceptions.ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "NoSuchKey":
            lastpage_content = "file did not exist"
            client.Bucket(bucket_name).put_object(Key=s3_path, Body=lastpage_content)

    try:
        if lastpage_content == encoded_string:
            returnvalue = "This is the same. " + myfile[:100]
        else:
            returnvalue = "This has changed."
            s3 = boto3.resource("s3")
            s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_string)
            print("notifying sns")
            sns.publish(
                TargetArn=snsUrn,
                Message=(
                    clickable_link + ' has changed.'
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
