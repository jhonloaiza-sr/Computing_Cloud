from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

def error_response(status_code, message=None):
    payload = {
        'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error'),
        'status_code': status_code
    }
    if message:
        payload['message'] = message
    return jsonify(payload), status_code

def handle_404(e):
    return error_response(404, "Recurso no encontrado")

def handle_500(e):
    return error_response(500, "Error interno del servidor")

def register_error_handlers(app):
    app.register_error_handler(404, handle_404)
    app.register_error_handler(500, handle_500)