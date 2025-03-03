# from pymongo import MongoClient
# import ssl
# import boto3
# import logging
from tinydb import TinyDB

# def db_connection(url=None, timeout=None, pool_size=None):
#     if url:
#         client = MongoClient(
#             url,
#             maxPoolSize=pool_size,
#             waitQueueTimeoutMS=timeout,
#             ssl_cert_reqs=ssl.CERT_NONE
#         )
#         # print("Connected successfully!!!")
#         return client
#     else:
#         print("please provide the URL")
#         raise ValueError

def tiny_db_connection(db_path=None):
    collection=TinyDB(db_path)
    return collection

# def minio_connection(endpoint_url, aws_access_key_id, aws_secret_access_key, region_name):
#     try:
#
#         botosession = boto3.session.Session(aws_access_key_id=aws_access_key_id,
#                                             aws_secret_access_key=aws_secret_access_key,
#                                             region_name=region_name)
#
#         botoclient = botosession.client(service_name="s3", use_ssl=False, verify=False,
#                                         endpoint_url=endpoint_url)
#
#         return botoclient
#     except Exception:
#         logging.info("Minio Connection not established")
#         return None