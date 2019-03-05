import boto3
import datetime

s3 = boto3.resource('s3')


def create_bucket(bucket_name_input):
    print("Creating a Bucket")
    time=datetime.datetime.now()
    bucket_name = bucket_name_input+'-'+str(time.microsecond)

    try:
        response = s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
        print("Created a bucket" + str(response))
        return bucket_name
    except Exception as error:
        print(error)


def upload_existing_img(bucket_name):
    print("Uploading image to the bucket")
    try:
        response = s3.Object(bucket_name, 'image_for_bucket.jpg').put(ACL='public-read', ContentType='image/jpeg',
                                                                      Body=open('image_for_bucket.jpg', 'rb'))
        print(response)
        print("Upload Successful")
    except Exception as error:
        print(error)


