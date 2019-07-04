import boto3, botocore
from config import Config
from flask_login import current_user
import io
import os
import cv2
import numpy as np
from google.cloud import vision
from models.receipt import Receipt
from models.receipt_details import Receipt_details
# import braintree
# S3_KEY, S3_SECRET, S3_BUCKET

# gateway = braintree.BraintreeGateway(
#     braintree.Configuration(
#         braintree.Environment.Sandbox,
#         merchant_id=Config.MERCHANT_ID,
#         public_key=Config.PUBLIC_KEY,
#         private_key=Config.PRIVATE_KEY
#     )
# )

s3 = boto3.client(
   "s3",
   aws_access_key_id=Config.S3_KEY,
   aws_secret_access_key=Config.S3_SECRET
)


def upload_file_to_s3(file, bucket_name, acl="public-read"):

    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """

    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e

    return "{}-{}".format(Config.S3_LOCATION, file.filename)


# http://abe-next-clone-instagram.s3.amazonaws.com/up.png
# S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)


'''send image url to google vision AI and then put the text location and text in a database'''
# def detect_text_uri(uri, id):
def detect_text_uri(instance):
    #setting coords as a dictionary
    #need to pass in receipt_image_url for uri
    
    

    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = instance.receipt_image_url
    #need to define the url in above line

    response = client.text_detection(image=image)
    texts = response.text_annotations
    for text in texts:
        # Receipt_details.text = text.description
        #receipt_text is going to the database
        # print('\n"{}"'.format(text.description))
        
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])
        # only need the topleft and bottom right vertices
        topleft = tuple((text.bounding_poly.vertices[0].x, text.bounding_poly.vertices[0].y))
        
        bottomright = tuple((text.bounding_poly.vertices[2].x, text.bounding_poly.vertices[2].y))
        
        coords = tuple((topleft,bottomright))
        # Receipt_details.receipt_id = id
        if len(text.description) < 50:
            instance2 = Receipt_details(text = text.description, coords = coords, receipt = instance)
            instance2.save()
        # box is going to the database
        # receipt_coords is going to the database
        
        # print('bounds: {}'.format(','.join(vertices)))

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False