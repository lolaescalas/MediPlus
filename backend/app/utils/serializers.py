"""
utils/serializers.py — Conversión de tipos nativos de MongoDB y Neo4j a JSON serializable.

MongoDB devuelve tipos BSON que Python no puede serializar directamente a JSON:
  - ObjectId      → str
  - datetime      → str ISO 8601
  - Decimal128    → float
  - bytes         → str base64

Neo4j devuelve tipos propios del driver:
  - Node          → dict con id, labels, properties
  - Relationship  → dict con id, type, start, end, properties
  - Path          → lista de nodos y relaciones
  - Date/DateTime → str ISO 8601
  - Duration      → str
"""

import base64
from datetime import datetime, date
from decimal import Decimal

from bson import ObjectId, Decimal128
from bson.binary import Binary

from neo4j.graph import Node, Relationship, Path
from neo4j.time import (
    Date as Neo4jDate,
    DateTime as Neo4jDateTime,
    Time as Neo4jTime,
    Duration as Neo4jDuration,
)


# ─────────────────────────────────────────────────────────────
#  MongoDB / BSON
# ─────────────────────────────────────────────────────────────

def serialize_mongo_value(value):
    """Convierte un valor BSON individual a tipo Python serializable."""
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, Decimal128):
        return float(str(value))
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, Binary):
        return base64.b64encode(value).decode("utf-8")
    if isinstance(value, bytes):
        return base64.b64encode(value).decode("utf-8")
    if isinstance(value, dict):
        return serialize_mongo_doc(value)
    if isinstance(value, list):
        return [serialize_mongo_value(v) for v in value]
    return value


def serialize_mongo_doc(doc: dict) -> dict:
    """Convierte un documento MongoDB completo a dict JSON-serializable."""
    return {k: serialize_mongo_value(v) for k, v in doc.items()}


def serialize_mongo_list(docs) -> list[dict]:
    """Convierte un cursor o lista de documentos MongoDB."""
    return [serialize_mongo_doc(doc) for doc in docs]


# ─────────────────────────────────────────────────────────────
#  Neo4j
# ─────────────────────────────────────────────────────────────

def serialize_neo4j_value(value):
    """Convierte un valor Neo4j individual a tipo Python serializable."""
    if isinstance(value, Node):
        return {
            "_id": value.element_id,
            "_labels": list(value.labels),
            **{k: serialize_neo4j_value(v) for k, v in dict(value).items()},
        }
    if isinstance(value, Relationship):
        return {
            "_id": value.element_id,
            "_type": value.type,
            "_start": value.start_node.element_id,
            "_end": value.end_node.element_id,
            **{k: serialize_neo4j_value(v) for k, v in dict(value).items()},
        }
    if isinstance(value, Path):
        return {
            "nodes": [serialize_neo4j_value(n) for n in value.nodes],
            "relationships": [serialize_neo4j_value(r) for r in value.relationships],
        }
    if isinstance(value, (Neo4jDate, Neo4jDateTime, Neo4jTime)):
        return value.iso_format()
    if isinstance(value, Neo4jDuration):
        return str(value)
    if isinstance(value, dict):
        return {k: serialize_neo4j_value(v) for k, v in value.items()}
    if isinstance(value, list):
        return [serialize_neo4j_value(v) for v in value]
    return value


def serialize_neo4j_record(record: dict) -> dict:
    """Convierte un record Neo4j (dict de valores) a JSON-serializable."""
    return {k: serialize_neo4j_value(v) for k, v in record.items()}


def serialize_neo4j_results(records: list[dict]) -> list[dict]:
    """Convierte una lista de records Neo4j."""
    return [serialize_neo4j_record(r) for r in records]
