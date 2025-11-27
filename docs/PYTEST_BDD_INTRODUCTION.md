# 🧪 Guía del Taller: Pytest + BDD + Buenas Prácticas
## 1. 📁 Organización y nomenclatura en pytest
Pytest detecta tests automáticamente basándose en un conjunto de convenciones. Esto ayuda a mantener los proyectos ordenados y a que los equipos sigan un estándar sencillo.
### 1.1 Nomenclatura de archivos
Pytest ejecuta cualquier archivo que cumpla el patrón:
```
test_*.py
*_test.py
```
Ejemplos válidos:
```
test_repository.py
service_test.py
test_integration_documents.py
```
### 1.2 Funciones de test
Dentro de esos archivos, pytest descubre funciones que comienzan por:
> def test_...

No hace falta heredar de unittest.TestCase, ni escribir clases, ni setUp/tearDown.

### 1.3 Estructura recomendada por tipo de test
```
├── tests
│   ├── unit
│   ├── integration
│   ├── e2e
│   ├── conftest.py        <-- fixtures compartidas
```

El conftest.py es un archivo especial que pytest carga automáticamente, sin necesidad de importarlo. Ahí se definen fixtures comunes.

## 2. 🔧 Fixtures

Los fixtures son probablemente la mejor característica de pytest. Permiten preparar el contexto de test de forma limpia, modular y reutilizable.

### 2.1 Qué son conceptualmente

Un fixture es:

- código reusable
- que prepara dependencias o entorno
- se ejecuta justo cuando un test lo necesita
- se inyecta por nombre

Ejemplo sencillo:
```python
@pytest.fixture
def sample_data():
    return {"id": 1, "name": "Javi"}
```
Uso:
```python
def test_data(sample_data):
    assert sample_data["id"] == 1
```

Pytest ve el nombre sample_data y ejecuta el fixture antes del test.

### 2.2 Scopes de un fixture

Los scopes controlan cada cuánto se instancia el fixture:

| Scope    | Ciclo de vida                 | Ejemplo                            |
|----------|-------------------------------|------------------------------------|
| function | una vez por test              | mocks, datos efímeros              |
| class    | una vez por clase             | costes moderados                   |
| module   | una vez por archivo           | cliente API real                   |
| package  | una vez por paquete           | entornos pesados                   |      
| session  | una vez por toda la ejecución | levantar docker-compose, clusters… |

```python
@pytest.fixture(scope="session")
def kafka_cluster():
    return start_fake_kafka()
```
Regla práctica:

- unit tests → function
- integration tests → module
- infra / e2e → session

### 2.3 Fixtures parametrizados

Puedes generar múltiples variantes de un fixture:
```python
@pytest.fixture(params=["sqlite", "mysql", "postgres"])
def db_engine(request):
    return setup_db_for(request.param)
```
Esto ejecutará los tests 3 veces, una por cada motor.

## 3. 🧪 Parametrize — Testear variantes sin repetir código

parametrize permite ejecutar un mismo test con distintas entradas y salidas esperadas.
```python
@pytest.mark.parametrize(
    "input,expected",
    [
        ("hola", "HOLA"),
        ("adios", "ADIOS"),
        ("python", "PYTHON"),
    ]
)
def test_upper(input, expected):
    assert input.upper() == expected
```
Usos típicos:

- múltiples casos borde
- validar errores y excepciones
- cubrir matrices de combinaciones (e.g. roles x permisos)

También se puede combinar con fixtures:
```python
@pytest.mark.parametrize("status", [200, 404, 500])
def test_api_responses(api_client, status):
```
## 4. 🎭 Mocking y Monkeypatching
### 4.1 Mock con unittest.mock
Parcheo temporal con patch (context manager)
from unittest.mock import patch
```python
def test_service():
    with patch("src.external.api_call", return_value={"ok": True}):
        assert my_service() == "success"
```
Parcheo como decorador
```python
@patch("src.external.api_call", return_value=42)
def test_value(mock_call):
    assert my_func() == 42
```
### 4.2 Mocking estilo pytest: monkeypatch
monkeypatch es un fixture built-in muy flexible.
```python
def test_env(monkeypatch):
    monkeypatch.setenv("API_KEY", "fake")

def test_attr(monkeypatch):
    monkeypatch.setattr(settings, "TIMEOUT", 0)
```
Usos típicos:
- simular variables de entorno
- reemplazar atributos en tiempo de ejecución
- desactivar funciones reales (e.g. requests.get)
## 5. 📊 Coverage — Medir líneas cubiertas

coverage.py integrado con pytest:

> pytest --cov=src

Mostrar líneas no cubiertas:
> pytest --cov=src --cov-report=term-missing

Report en HTML:
> pytest --cov=src --cov-report=html

Genera un informe navegable con colores que resalta líneas cubiertas y no cubiertas.

Buenas prácticas de coverage:

- No obsesionarse con 100%: cubrir casos de uso, no líneas
- Priorizar paths críticos, errores, casos borde

Tests de integración suben calidad aunque bajen coverage local

## 6. 📈 Reports 
### 6.1 JUnit (para CI/CD)
> pytest --junitxml=report.xml

Integración con GitLab CI, Jenkins o GitHub Actions.

### 7. 🔁 Steps reutilizables

En testing, sobre todo en BDD o test funcional, aparecen acciones repetidas. Pytest permite estructurarlas de varias formas.

## 7.1 Steps como funciones helper
```python
def create_user_and_login(client):
    user = client.create(...)
    token = client.login(...)
    return token
```
## 7.2 Steps via fixtures (pattern recomendado)
```python
@pytest.fixture
def step_create_user(db):
    def run(name):
        return db.add_user(name)
    return run
```
Uso:
```python
def test_user(step_create_user):
    user = step_create_user("pepe")
    assert user.name == "pepe"
```
## 7.3 Steps reutilizables en BDD

Con pybdd:
```python
@step("a valid user exists")
def create_user(context):
    context.user = UserMother.valid()
```
# 8. 🧱 Object Mother — Crear objetos de test complejos

El patrón Object Mother es una fábrica de objetos orientada a tests que permite generar entidades consistentes, completas y expresivas.

Ejemplo:
```python
class DocumentMother:
    @staticmethod
    def random():
        return Document(
            id=str(uuid4()),
            title=f"doc-{uuid4()}",
            content="lorem ipsum...",
            created_at=datetime.now(),
        )
    @staticmethod
    def titled(name):
        return Document(
            id=str(uuid4()),
            title=name,
            content="...",
            created_at=datetime.now(),
        )
```
Ventajas:

- test más expresivos
- evita duplicar datos de prueba
- facilita evolución del modelo DDD

# 9. 🧩 Inyección de contexto: repositorios, servicios, API clients
## 9.1 Via fixtures (más limpio)
```python
@pytest.fixture
def repo():
    return InMemoryDocumentRepository()

@pytest.fixture
def service(repo):
    return DocumentService(repo)
```
Pytest resuelve dependencias automáticamente.

## 9.2 Via monkeypatch (cuando quieres reemplazar implementaciones)
```python
def test_api(monkeypatch, client):
    monkeypatch.setattr(
        "src.services.repo",
        FakeRepo()
    )
```
## 9.3 Via factory fixtures (cuando necesitas configuraciones)
```python
@pytest.fixture
def service_factory():
    def build(url="http://mock"):
        return ApiService(url)
    return build
```
Uso:
```python
def test_api(service_factory):
    svc = service_factory(url="http://test")
```
# 10. 🐍 pybdd — BDD estilo Gherkin con pytest

PyBDD permite escribir escenarios estilo Given / When / Then integrados con pytest.

## 10.1 Decoradores principales
|Decorador|Significado|
|-|-|
|@given|estado inicial|
|@when|acción|
|@then|resultado esperado|
|@step|step genérico reutilizable|
|@scenario|enlaza un archivo Gherkin con su definición Python|

Ejemplo:
```gherkin
Feature: Document retrieval

  Scenario: Fetch existing document
    Given a document exists
    When I call GET /documents/{id}
    Then I receive the document
```
Código Python:
```python
@given("a document exists")
def _(context):
    context.doc = DocumentMother.random()
    context.repo.save(context.doc)

@when("I call GET /documents/{id}")
def _(context):
    context.response = context.client.get(f"/documents/{context.doc.id}")

@then("I receive the document")
def _(context):
    assert context.response.status_code == 200
    assert context.response.json()["id"] == context.doc.id
```
10.2 Contexto compartido

Cada escenario tiene su propio objeto context, similar a behave.