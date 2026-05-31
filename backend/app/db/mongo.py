"""
db/mongo.py — Conexión singleton a MongoDB Atlas.

Uso:
    from app.db.mongo import get_db, ping_mongo

    db = get_db()
    coleccion = db["nombre_coleccion"]
"""

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConnectionFailure, ConfigurationError

from app.config import settings

_client: MongoClient | None = None


def get_client() -> MongoClient:
    """Retorna el cliente MongoDB (singleton)."""
    global _client
    if _client is None:
        _client = MongoClient(
            settings.mongo_uri,
            serverSelectionTimeoutMS=5000,  # 5 seg de timeout
            connectTimeoutMS=5000,
        )
    return _client


def get_db() -> Database:
    """Retorna la base de datos configurada en MONGO_DB_NAME."""
    return get_client()[settings.mongo_db_name]


def ping_mongo() -> dict:
    """
    Verifica la conexión a Atlas.
    Retorna {"status": "ok", "host": "..."} o {"status": "error", "detail": "..."}.
    """
    try:
        client = get_client()
        client.admin.command("ping")
        info = client.server_info()
        return {
            "status": "ok",
            "version": info.get("version", "desconocida"),
            "host": settings.mongo_uri.split("@")[-1].split("/")[0],  # oculta credenciales
        }
    except ConnectionFailure as e:
        return {"status": "error", "detail": f"No se pudo conectar: {e}"}
    except ConfigurationError as e:
        return {"status": "error", "detail": f"URI inválida: {e}"}


def close_mongo():
    """Cierra la conexión (llamar al apagar la app)."""
    global _client
    if _client:
        _client.close()
        _client = None
