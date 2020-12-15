import logging
from botocore.exceptions import ClientError
import boto3


def upload_obj_to_pdf_bucket(pdf_file_object, object_name):
    s3_client = boto3.client('s3', region_name='eu-central-1')

    try:
        response = s3_client.upload_fileobj(pdf_file_object, 'paeda-menu-pdf', object_name)
    except ClientError as error:
        logging.error(error)
        return 'ERROR'
    return 'SUCCESS'
