import boto3 
import os
import re
import shutil 

REGION = '<enter region>'
ACCESS_KEY_ID = '<enter access key id' 
SECRET_ACCESS_KEY = '<enter secret access key' 
BUCKET_NAME = '<enter bucket name>' 
pattern = re.compile(r'^date=\d{4}-\d{2}-\d{2}$')
dir = os.listdir('<enter dir name path>')

for file in dir:
   if re.match(pattern, file):
    FILE_PATH = 'airline_data/' + file + '/flights.csv' 
    ARCHIVE_PATH = 'airline_data_archive/' + file
    KEY = 'daily_raw/' + file + '/flights.csv' # file path in S3 
    print("Wait while uploading...")
    s3_resource = boto3.resource(
        's3', 
        region_name = REGION, 
        aws_access_key_id = ACCESS_KEY_ID,
        aws_secret_access_key = SECRET_ACCESS_KEY
    ) 
    s3_resource.Bucket(BUCKET_NAME).put_object(
        Key = KEY, 
        Body = open(FILE_PATH, 'rb')
    )
    print("Successfully uploaded {}".format(file))
    shutil.move('airline_data/' + file, ARCHIVE_PATH, copy_function = shutil.copytree)
    print("Successfully archived {}".format(file))


