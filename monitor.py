import random
import urllib
import re
import boto3

sns = boto3.client('sns')

def monitor_angrychair(event, context):

    blog = "shop.angrychairbrewing.com/product-category/beers/"
    
    
    link = "http://" + blog 
    myfile = ""
    myfile = urllib.urlopen(link).read()
    
    myfile = myfile[:50000]
    encoded_string = myfile.encode("utf-8")
    
    bucket_name = "bdsmlr-tracker"
    file_name =  "angrychair.txt"
    s3_path = file_name
    try:
        client = boto3.client('s3')
        lastpage_content = ""
        lastpage = client.get_object(Bucket=bucket_name, Key=s3_path)
        lastpage_content = lastpage['Body'].read()
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "NoSuchKey":
            lastpage_content = "file did not exist"
            client.Bucket(bucket_name).put_object(Key=s3_path, Body=lastpage_content)
        
    try:
        #encoded_string = re.sub(r'(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})', '', encoded_string)
        #encoded_string = re.sub(r'ey[a-zA-Z0-9=]+', '', encoded_string)
        #encoded_string = re.sub(r'span.*\/span', '', encoded_string)
        #for line in encoded_string.split('\n'):
            #if 'class="post_content' in line:
                #encoded_string = line
        if lastpage_content == encoded_string:
            returnvalue = "This is the same"
        else:
            returnvalue = "This has changed."
            s3 = boto3.resource("s3")
            s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_string)
            s3.Bucket(bucket_name).put_object(Key="last-" + s3_path, Body=lastpage_content)
            print("notifying sns")
            sns.publish(
                TargetArn='arn:aws:sns:us-east-1:619096257283:monitor-angrychair',
                Message=(
                    'https://' + blog + ' has changed.'
                )
            )
    except:
        returnvalue = "failed to get content"

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

