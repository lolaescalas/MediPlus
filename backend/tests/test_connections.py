"""
tests/test_connections.py — Verifica que las conexiones a Atlas y Aura funcionen.

Ejecutar desde /backend con:
    python -m pytest tests/test_connections.py -v

O directamente:
    python tests/test_connections.py
"""

import sys
import os

# Permite ejecutar directamente sin instalar el paquete
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_mongo_connection():
    """Verifica conexión a MongoDB Atlas."""
    from app.db.mongo import ping_mongo
    result = ping_mongo()
    print(f"\n  MongoDB Atlas → {result}")
    assert result["status"] == "ok", f"Falló: {result.get('detail')}"


def test_neo4j_connection():
    """Verifica conexión a Neo4j Aura."""
    from app.db.neo4j_db import ping_neo4j
    result = ping_neo4j()
    print(f"\n  Neo4j Aura   → {result}")
    assert result["status"] == "ok", f"Falló: {result.get('detail')}"


if __name__ == "__main__":
    print("=" * 50)
    print("  Test de conexiones")
    print("=" * 50)

    mongo_ok = False
    neo4j_ok = False

    try:
        test_mongo_connection()
        print("  ✅ MongoDB Atlas: OK")
        mongo_ok = True
    except Exception as e:
        print(f"  ❌ MongoDB Atlas: {e}")

    try:
        test_neo4j_connection()
        print("  ✅ Neo4j Aura: OK")
        neo4j_ok = True
    except Exception as e:
        print(f"  ❌ Neo4j Aura: {e}")

    print("=" * 50)
    if mongo_ok and neo4j_ok:
        print("  Todo OK — podés levantar la API con uvicorn")
    else:
        print("  Revisá tu archivo .env y las credenciales")
    print("=" * 50)
