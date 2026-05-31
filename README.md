# 📊 DataViz Dashboard — MongoDB Atlas + Neo4j Aura

Interfaz visual WinForms (.NET 8 / C#) con backend FastAPI (Python) para visualizar datos de MongoDB Atlas y Neo4j Aura.

## 🏗️ Arquitectura

```
WinForms (C#)  ──HTTP──▶  FastAPI (Python)  ──▶  MongoDB Atlas
                                             ──▶  Neo4j Aura
```

## 📁 Estructura del repositorio

```
/
├── backend/                  # API Python (FastAPI)
│   ├── app/
│   │   ├── main.py           # Entrypoint FastAPI
│   │   ├── config.py         # Variables de entorno
│   │   ├── db/
│   │   │   ├── mongo.py      # Conexión MongoDB Atlas
│   │   │   └── neo4j.py      # Conexión Neo4j Aura
│   │   ├── routers/
│   │   │   ├── mongo_router.py
│   │   │   └── neo4j_router.py
│   │   ├── models/           # Schemas Pydantic
│   │   └── utils/
│   │       └── serializers.py  # Conversión de tipos BSON / Neo4j
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
├── frontend/                 # WinForms C# (.NET 8)
│   └── DataVizApp/
├── docs/
│   └── SETUP.md
├── .gitignore
└── README.md
```

## 🚀 Inicio rápido

### 1. Clonar el repo
```bash
git clone https://github.com/TU_USUARIO/TU_REPO.git
cd TU_REPO
```

### 2. Configurar el backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env         # Completar con tus credenciales
```

### 3. Levantar la API
```bash
uvicorn app.main:app --reload --port 8000
```

### 4. Abrir el frontend
Abrir `frontend/DataVizApp/DataVizApp.sln` en Visual Studio 2022 y ejecutar.

## 🔐 Variables de entorno

Ver [`.env.example`](backend/.env.example) — **nunca commitear el `.env` real**.

## 📚 Documentación adicional

- [Guía de setup detallada](docs/SETUP.md)
- API docs interactiva: `http://localhost:8000/docs` (Swagger UI)
