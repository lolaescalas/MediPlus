"""
db/neo4j.py — Conexión singleton a Neo4j Aura.

Uso:
    from app.db.neo4j_db import get_driver, run_query, ping_neo4j

    records = run_query("MATCH (n) RETURN n LIMIT 5")
"""

from contextlib import contextmanager

from neo4j import GraphDatabase, Driver
from neo4j.exceptions import AuthError, ServiceUnavailable

from app.config import settings

_driver: Driver | None = None


def get_driver() -> Driver:
    """Retorna el driver Neo4j (singleton)."""
    global _driver
    if _driver is None:
        _driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password),
        )
    return _driver


@contextmanager
def get_session():
    """Context manager que abre y cierra una sesión Neo4j automáticamente."""
    driver = get_driver()
    session = driver.session()
    try:
        yield session
    finally:
        session.close()


def run_query(cypher: str, params: dict | None = None) -> list[dict]:
    """
    Ejecuta una query Cypher y retorna los resultados como lista de dicts.

    Ejemplo:
        run_query("MATCH (n:Persona) RETURN n.nombre AS nombre LIMIT 10")
    """
    with get_session() as session:
        result = session.run(cypher, params or {})
        return [record.data() for record in result]


def ping_neo4j() -> dict:
    """
    Verifica la conexión a Aura.
    Retorna {"status": "ok", "version": "..."} o {"status": "error", "detail": "..."}.
    """
    try:
        driver = get_driver()
        driver.verify_connectivity()
        with get_session() as session:
            result = session.run("CALL dbms.components() YIELD name, versions WHERE name = 'Neo4j Kernel' RETURN versions[0] AS version")
            record = result.single()
            version = record["version"] if record else "desconocida"
        return {"status": "ok", "version": version}
    except AuthError:
        return {"status": "error", "detail": "Credenciales inválidas (usuario o contraseña)"}
    except ServiceUnavailable as e:
        return {"status": "error", "detail": f"Servicio no disponible: {e}"}


def close_neo4j():
    """Cierra el driver (llamar al apagar la app)."""
    global _driver
    if _driver:
        _driver.close()
        _driver = None
