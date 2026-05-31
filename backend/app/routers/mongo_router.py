"""
routers/mongo_router.py — Endpoints REST para MongoDB Atlas.
"""

from fastapi import APIRouter, HTTPException, Query

from app.db.mongo import get_db, ping_mongo
from app.utils.serializers import serialize_mongo_list, serialize_mongo_doc

router = APIRouter(prefix="/mongo", tags=["MongoDB"])


@router.get("/health")
def mongo_health():
    """Verifica la conexión a MongoDB Atlas."""
    return ping_mongo()


@router.get("/collections")
def list_collections():
    """Lista todas las colecciones de la base de datos."""
    try:
        db = get_db()
        return {"collections": db.list_collection_names()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/collection/{nombre}")
def get_documents(
    nombre: str,
    limit: int = Query(default=50, ge=1, le=500, description="Máximo de documentos a retornar"),
    skip: int = Query(default=0, ge=0, description="Documentos a saltear (paginación)"),
):
    """
    Retorna documentos de una colección con paginación.
    Todos los tipos BSON (ObjectId, fechas, Decimal128) son convertidos automáticamente.
    """
    try:
        db = get_db()
        cursor = db[nombre].find({}, limit=limit, skip=skip)
        docs = serialize_mongo_list(cursor)
        total = db[nombre].count_documents({})
        return {"total": total, "skip": skip, "limit": limit, "data": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/collection/{nombre}/{doc_id}")
def get_document_by_id(nombre: str, doc_id: str):
    """Busca un documento por su _id (string del ObjectId)."""
    try:
        from bson import ObjectId
        from bson.errors import InvalidId
        db = get_db()
        try:
            oid = ObjectId(doc_id)
        except InvalidId:
            raise HTTPException(status_code=400, detail="ID inválido")
        doc = db[nombre].find_one({"_id": oid})
        if doc is None:
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        return serialize_mongo_doc(doc)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
