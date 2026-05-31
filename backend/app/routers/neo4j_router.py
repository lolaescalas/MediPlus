"""
routers/neo4j_router.py — Endpoints REST para Neo4j Aura.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.db.neo4j_db import run_query, ping_neo4j
from app.utils.serializers import serialize_neo4j_results

router = APIRouter(prefix="/neo4j", tags=["Neo4j"])


class CypherRequest(BaseModel):
    query: str
    params: dict = {}


@router.get("/health")
def neo4j_health():
    """Verifica la conexión a Neo4j Aura."""
    return ping_neo4j()


@router.get("/labels")
def list_labels():
    """Lista todos los labels (tipos de nodos) disponibles."""
    try:
        records = run_query("CALL db.labels() YIELD label RETURN label ORDER BY label")
        return {"labels": [r["label"] for r in records]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/relationship-types")
def list_relationship_types():
    """Lista todos los tipos de relaciones disponibles."""
    try:
        records = run_query("CALL db.relationshipTypes() YIELD relationshipType RETURN relationshipType")
        return {"types": [r["relationshipType"] for r in records]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/nodes/{label}")
def get_nodes_by_label(
    label: str,
    limit: int = Query(default=50, ge=1, le=500),
    skip: int = Query(default=0, ge=0),
):
    """
    Retorna nodos de un label dado con paginación.
    Los tipos Neo4j (Node, DateTime, Duration) son serializados automáticamente.
    """
    try:
        # Nota: los labels no pueden parametrizarse con $param en Cypher
        # Se valida que solo contenga caracteres alfanuméricos y guion bajo
        if not label.replace("_", "").isalnum():
            raise HTTPException(status_code=400, detail="Label inválido")
        records = run_query(
            f"MATCH (n:`{label}`) RETURN n SKIP $skip LIMIT $limit",
            {"skip": skip, "limit": limit},
        )
        return {"label": label, "skip": skip, "limit": limit, "data": serialize_neo4j_results(records)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query")
def execute_cypher(body: CypherRequest):
    """
    Ejecuta una query Cypher personalizada (solo lectura recomendado).
    Útil para el WinForms: enviá tu Cypher desde C# y recibís los resultados serializados.
    """
    try:
        records = run_query(body.query, body.params)
        return {"data": serialize_neo4j_results(records), "count": len(records)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
