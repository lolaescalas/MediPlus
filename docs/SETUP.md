# Guía de Setup Detallada

## 1. Clonar y preparar el repositorio

```bash
git clone https://github.com/TU_USUARIO/TU_REPO.git
cd TU_REPO
```

---

## 2. Obtener credenciales de MongoDB Atlas

1. Entrá a [cloud.mongodb.com](https://cloud.mongodb.com)
2. Creá una cuenta gratuita (o iniciá sesión)
3. Creá un **Free Cluster** (M0 — gratis para siempre)
4. En el cluster → **Connect** → **Drivers**
5. Copiá la URI con formato:
   ```
   mongodb+srv://usuario:password@cluster0.XXXXX.mongodb.net/
   ```
6. En **Database Access** → creá un usuario con contraseña
7. En **Network Access** → agregá tu IP (o `0.0.0.0/0` para desarrollo)

---

## 3. Obtener credenciales de Neo4j Aura

1. Entrá a [console.neo4j.io](https://console.neo4j.io)
2. Creá una cuenta gratuita
3. Creá una instancia **AuraDB Free**
4. Al crearla, **descargá el archivo de credenciales** (solo se muestra una vez)
5. Los datos que necesitás:
   - **Connection URI**: `neo4j+s://XXXXXXXX.databases.neo4j.io`
   - **Username**: `neo4j`
   - **Password**: la generada automáticamente

---

## 4. Configurar el archivo .env

```bash
cd backend
copy .env.example .env    # Windows CMD
# o
cp .env.example .env      # PowerShell / Git Bash
```

Editá `.env` con tus credenciales reales.

---

## 5. Instalar dependencias Python

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 6. Verificar conexiones

```bash
python tests/test_connections.py
```

Deberías ver:
```
✅ MongoDB Atlas: OK
✅ Neo4j Aura: OK
```

---

## 7. Levantar la API

```bash
uvicorn app.main:app --reload --port 8000
```

Abrí en el navegador:
- **Swagger UI**: http://localhost:8000/docs
- **Health check**: http://localhost:8000/health

---

## 8. Abrir el frontend WinForms

Abrir `frontend/DataVizApp/DataVizApp.sln` en **Visual Studio 2022** y ejecutar con F5.

---

## 9. Setup del repositorio GitHub (primera vez)

```bash
# Desde la raíz del proyecto
git init
git add .
git commit -m "feat: estructura inicial del proyecto"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

> ⚠️ Verificá que `.env` esté en `.gitignore` **antes** del primer push.
