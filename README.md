# 📄 Document Management API

API de documentos construida con **FastAPI**, **MongoDB**, y **S3**, para gestión de documentos con metadata y archivos. Pensada para ser usada en un taller práctico.

La documentación para el taller se encuentra en:

1. [Breve introducción al TDD i BDD](docs/TDD_INTRODUCTION.md)
2. [Introducción a Pytest y BDD](docs/PYTEST_BDD_INTRODUCTION.md)
3. [Guía del taller](docs/WORKSHOP_GUIDE.md)

Antes de iniciar el taller, seguir las instrucciones descritas a continuación, y leer la documentación sobre el funcionamiento de la API

---

## 🚀 Requisitos y dependencias

### 🔧 Dependencias del sistema
- Python 3.10+
- Docker
- Docker Compose
- [uv](https://pypi.org/project/uv/): gestor ultra rápido de Python

Instalación de uv:

```bash
pip install uv
```
## 📦 Servicios necesarios

- MongoDB: guarda metadata de documentos.
- MinIO/S3: almacena archivos.
- Levantar los servicios con Docker Compose:

```bash
docker compose up -d
```

## ▶️ Ejecutar la API en local

```bash
make run/local
```

Esto arranca FastAPI en: http://localhost:8000/docs desde donde puedes probar la API usando Swagger.  

## 🧱 Arquitectura mínima

### Repositorios

- DocumentMongoRepository: gestiona metadata de documentos en MongoDB.
- S3Repository: gestiona ficheros en S3/MinIO y genera URLs presignadas.

### Modelos

- Document:
```python
    id: str
    title: str
    description: str
    key: str
    file_path: Optional[str]
```
- DocumentCreate:
```python
    title: str
    description: str
```
## 🧵 Endpoints
### GET /documents/
Devuelve la lista de documentos. Cada documento incluye una URL presignada para descargar el fichero.
### POST /documents/
Sube un nuevo documento:
 - Metadata (title, description)
 - Archivo (UploadFile)
Flujo:
 1. Guardar metadata en MongoDB.
 2. Subir archivo a S3.
 3. Devolver el documento con la URL prefirmada.
### GET /documents/{document_id}
Obtiene un documento específico.
Si no existe → 404
### DELETE /documents/{document_id}
Elimina el documento:
- Archivo en S3
- Metadata en MongoDB
Documento inexistente → 404
Documento eliminado correctamente → 204

## 🧪 Tests

Tests escritos en pytest + pytest-bdd.

### Cobertura:

- Obtener todos los documentos
- Obtener documentos vacíos
- Obtener documento existente
- Obtener documento inexistente
- Borrar documento existente
- Borrar documento inexistente

Integración Mongo + S3

Ejecutar tests:

> make test/all

Genera:

- report.html (informe de tests)
- htmlcov/ (cobertura de código)

## 👀 Nota

Hay un error intencionado en uno de los tests. Parte del taller consiste en bucear para descubrir por qué falla: puede ser por la base de datos, IDs de documentos o la lógica programada.

📁 Estructura del proyecto
```
├── app/
│   ├── main.py
│   ├── config.py
│   ├── models/document.py
│   ├── controllers/document_controller.py
│   └── repository/
│       ├── document_mongo_repository.py
│       └── document_s3_repository.py
├── tests/
│   ├── features/
│   ├── steps/
│   └── fixtures/
├── docker-compose.yml
├── Makefile
└── README.md
```
