def build_envelope(*, success: bool, message: str = "", data=None, errors=None):
    return {
        "success": success,
        "message": message,
        "data": data,
        "errors": errors,
    }
