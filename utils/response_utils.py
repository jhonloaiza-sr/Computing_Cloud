from flask import jsonify

# Cambia los nombres de las funciones:
def success(data=None, message="Operación exitosa", status_code=200):
    """Formato estándar para respuestas exitosas"""
    response = {
        'success': True,
        'message': message,
        'data': data
    }
    return jsonify(response), status_code

def error(message="Error en la operación", status_code=400, details=None):
    """Formato estándar para errores"""
    response = {
        'success': False,
        'error': {
            'code': status_code,
            'message': message,
            'details': details
        }
    }
    return jsonify(response), status_code

# Mantén esta función igual
def handle_database_error(e):
    """Manejo específico para errores de base de datos"""
    return error(
        message="Error en la base de datos",
        status_code=500,
        details=str(e)
    )