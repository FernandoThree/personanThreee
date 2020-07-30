from hashlib import sha256
from datetime import datetime

def autenticar(username: str, password: str) -> bool:
    return username == "aalvarez" and password == "aalvarez"

def generar_fecha_sha256(fecha: datetime = datetime.utcnow().date()) -> str:
    hoy = str(fecha).encode()
    auth = sha256()
    auth.update(hoy)
    return auth.hexdigest()

def autenticar_fecha_sha256(token: str) -> bool:
    fecha = datetime.utcnow().date()
    return True if generar_fecha_sha256(fecha) == token else False