import boto3
from config import Config
from botocore.exceptions import ClientError

class AWSUtils:
    @staticmethod
    def get_s3_client():
        """Retorna cliente configurado para S3"""
        return boto3.client(
            's3',
            aws_access_key_id=Config.AWS_ACCESS_KEY,
            aws_secret_access_key=Config.AWS_SECRET_KEY,
            region_name=Config.AWS_REGION
        )

    @staticmethod
    def get_ses_client():
        """Retorna cliente configurado para SES"""
        return boto3.client(
            'ses',
            aws_access_key_id=Config.AWS_ACCESS_KEY,
            aws_secret_access_key=Config.AWS_SECRET_KEY,
            region_name=Config.AWS_REGION
        )

    @staticmethod
    def upload_to_s3(bucket_name, file_key, file_data):
        """Sube archivos a S3"""
        try:
            s3 = AWSUtils.get_s3_client()
            s3.put_object(
                Bucket=bucket_name,
                Key=file_key,
                Body=file_data
            )
            return True
        except ClientError as e:
            raise Exception(f"Error al subir a S3: {str(e)}")

    @staticmethod
    def send_ses_email(to_email, subject, body):
        """Envía emails a través de SES"""
        try:
            ses = AWSUtils.get_ses_client()
            response = ses.send_email(
                Source=Config.SES_SENDER_EMAIL,
                Destination={'ToAddresses': [to_email]},
                Message={
                    'Subject': {'Data': subject},
                    'Body': {'Text': {'Data': body}}
                }
            )
            return response
        except ClientError as e:
            raise Exception(f"Error al enviar email: {str(e)}")