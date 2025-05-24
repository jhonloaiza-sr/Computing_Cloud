# services/email_service.py

import boto3
from config import Config
from botocore.exceptions import ClientError


class EmailService:
    def __init__(self):
        self.ses = boto3.client(
            'ses',
            region_name=Config.AWS_REGION,
            aws_access_key_id=Config.AWS_ACCESS_KEY,
            aws_secret_access_key=Config.AWS_SECRET_KEY
        )

    def send_confirmation_email(self, to_email, appointment_details):
        """Envía email de confirmación de cita"""
        try:
            response = self.ses.send_email(
                Source=Config.SES_SENDER_EMAIL,
                Destination={'ToAddresses': [to_email]},
                Message={
                    'Subject': {'Data': 'Confirmación de Cita Médica'},
                    'Body': {
                        'Text': {
                            'Data': (
                                f"Hola,\n\n"
                                f"Tu cita ha sido agendada con éxito:\n"
                                f"Fecha: {appointment_details['date']}\n"
                                f"Hora: {appointment_details['time']}\n"
                                f"Estado: {appointment_details['status']}\n\n"
                                "Gracias por usar nuestro servicio."
                            )
                        }
                    }
                }
            )
            print(f"✅ Correo enviado a {to_email}")
            return response
        except ClientError as e:
            raise Exception(f"Error al enviar email: {e.response['Error']['Message']}")

    def send_cancellation_notice(self, to_email, appointment_id, reason):
        """Envía notificación de cancelación"""
        # Implementación similar a send_confirmation_email
        pass