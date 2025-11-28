# 1. Desarrollo del taller

Introducción al TDD y breve explicación sobre Pytest y Pybdd. 

Puesta en práctica con un desarrollo y una adaptación del código.

Conclusiones y open-space para resolver dodas, y debatir sobre cómo abordar estrategias.

# 2. Descripción del proyecto y batería de test

## Cómo están estructurados los tests?

### Configuración general

Definida en el conftest. Aquí irán los fixtures de uso general, y los steps compartidos por diferentes features

Por cada sesión de test levantar infraestructura (MongoDB y S3)

```python
@pytest.fixture(scope="session", autouse=True)
def docker_infra():
    """
    Prepares docker infrastructure for tests
    """
    subprocess.run(["docker", "compose", "up", "-d"], check=True)
    time.sleep(3)
    yield
    subprocess.run(["docker", "compose", "down"], check=True)
```

Crear un TestClient para probar nuestra API:
```python
@pytest.fixture(scope="session")
def client():
    """
    Prepares a TestClient for testing fastAPI endpoints
    Returns:
        TestClient: A FastAPI API Rest Test client
    """
    return TestClient(app)
```
Antes de cada test limpiar la base de datos y el repo s3:
```python
@pytest.fixture(autouse=True,scope="function")
def clean_db_and_s3(mongo_repo: DocumentMongoRepository, s3_repo: S3Repository):
    """
    Drop application database for cleaning data between tests
    Args:
        mongo_repo (DocumentMongoRepository): Repository for Documents Collection
        s3_repo (S3Repository): Repository for S3 Storage
    """
    mongo_repo.client.drop_database(settings.mongodb_db)
    objects = s3_repo.client.list_objects_v2(Bucket=s3_repo.bucket)
    if "Contents" in objects:
        for obj in objects["Contents"]:
            s3_repo.client.delete_object(Bucket=s3_repo.bucket, Key=obj["Key"])
```
### Definición de los steps y escenarios

Ejemplo:

- La API está arrancada:
```python
@given("API is running")
def api_running(client):
    response = client.get("/docs")
    assert response.status_code == 200
```

```gherkin
    Given API is running
```

# 3. Encuentra y resuelve el error

Al ejecutar los tests con el siguiente comando

> make test/all

Puede observarse que falla un test. Encuentra y resuelve el error.

# 4. Ciclo del TDD -> Añadimos autenticación y autorización.

Vamos a hacer una modificación en la API para añadir autenticación y autorización. Lo vamos a hacer de forma obvia.
Sólo requeriremos que el usuario se haya logado en el sistema, y que por tanto las peticiones http nos lleguen con un bearer token válido. 
No vamos a persistir usuarios, pero, sí que vamos a tener una serie de lógica de negocio definido. 

Nuestro equipo funcional ha definido una serie de casos de uso, y sus criterios de aceptación:

Casos de uso:

  - Como usuario quiero crear un documento:
    - Escenario: Un usuario válido puede dar de alta un documento
      - Dado un usuario válido
      - Cuando inserto un documento
      - Entonces se crea correctamente
      - Y yo puedo consultarlo
      - Y otros usuario no puede consultarlo
  - Como usuario quiero consultar todos mis documentos
    - Escenario: Un usuario válido puede consultar sus documentos
      - Dado un usuario válido
      - Y existen documentos de diferentes usuarios
      - Cuando consulto todos los documentos
      - Enconces recupero una lista de documento
      - Y la lista sólo contiene mis documentos
  - Como usuario quiero consultar un documento
    - Escenario: Un usuario válido puede consultar un documento propio existente
      - Dado un usuario válido
      - Y existen un documento suyo
      - Cuando consulta su documento
      - Entonces recupera el documento
      - Y el documento es el esperado
    - Escenario: Un usuario válido no puede consultar un documento ajeno existente
      - Dado un usuario válido
      - Y existe al menos un documento ajeno
      - Cuando consulto el documento
      - Entonces la respuesta es 403
  - Como usuario quiero borrar un documento
    - Escenario: Un usuario válido puede borrar un documento propio existente
      - Dado un usuario valido
      - Y un documento existente
      - Cuando borro el documento
      - Este es borrado
      - Y no existe en el bucket
    - Escenario: Un usuario válido no puede borrar un documento ajeno existnete
      - Dado un usuario valido
      - Y un documento existente de otro usuario
      - Cuando borro el documento
      - Recibo un 403
      - Y este no ha sido borrado de la base de datos

Nuestra tarea va a consistir en implementarlos, aplicando metodología TDD y ayudándonos de pytest y pybdd

## Configuración de tests

Definimos los steps para inyectar token válido e inválido en el conftest.

Es importante definirlos en el conftest para que los steps se propagen en todos los archivos de test

```python
def create_test_token(user_id: str = "test-user") -> str:
    payload = {
        "sub": user_id,
        "exp": datetime.now() + timedelta(hours=1)
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


@given(parsers.parse("a valid JWT token for user {user_id}"))
def jwt_token_for_user(context, user_id: str):
    """
    Generates a valid token for specific username.
    """
    context["token"] = create_test_token(user_id=user_id)
    context["user_id"] = user_id


@given(parsers.parse("an invalid JWT token for user {user_id}"))
def jwt_invalid_token_for_user(context, user_id: str):
    """
    Generates an invalid token for specific username.
    """
    context["token"] = uuid.uuid4()
    context["user_id"] = user_id
```

A través del context podemos inyectar el token generado en las llamadas a las API's. En este caso, comenzaremos sobre la petición POST que nos genera los datos de prueba.

```python
 response = client.post(
            "/documents",
            data=create_document_request_factory().model_dump(),
            files={"file": ("file_name.txt", b"Document content", "text/plain")},
            headers={"Authorization": f'Bearer {context["token"]}'}
        )
```
De esta forma podemos definir los escenarios con la inyección de un usuario. 
```gherkin
  Scenario: GET /documents/document with existing documents
    Given API is running
    And an invalid JWT token for user John
    And Database contains documents
    When I get an existing document
    Then response is 200
    And response is the expected document
```
El siguiente paso, será modificar nuestra batería de pruebas para que haya documentos generados por diferentes usuarios. 

Para ello, vamos a definir un step parametrizable que recible una tabla de gherkin.
Además, como tendremos que realizar pruebas en cada uno de los endpoints en función de si tenemos autenticación y de si esta es válida,
vamos a crear un helper para crear los headers, y los steps de given que nos pemritirán generar token válidos e inválidos, de esta forma no repetiremos código. Este helper podemos añadirlo en el conftest o en un archivo de helpers.
```python
def create_test_token(user_id: str = "test-user") -> str:
    payload = {
        "sub": user_id,
        "exp": datetime.now() + timedelta(hours=1)
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


@given(parsers.parse("a valid JWT token for user {user_id}"))
def jwt_token_for_user(context, user_id: str):
    """
    Generates a valid token for specific username.
    """
    context["token"] = create_test_token(user_id=user_id)
    context["user_id"] = user_id


@given(parsers.parse("an invalid JWT token for user {user_id}"))
def jwt_invalid_token_for_user(context, user_id: str):
    """
    Generates an invalid token for specific username.
    """
    context["token"] = uuid.uuid4()
    context["user_id"] = user_id
```
Definimos el step que recibe la tabla:
```python
@given("documents owned by:")
def documents_owned_by(datatable, client, context):

    if not "documents" in context:
      context["documents"] = []

    for row in datatable:
        user_id = row[0]
        documents = int(row[1])
        for _ in range(documents):
            token = create_test_token(user_id=user_id)
            response = client.post(
                "/documents",
                data=create_document_request().model_dump(),
                files={"file": ("file_name.txt", b"Document content", "text/plain")},
                headers={"Authorization": f"Bearer {token}"}
            )

        assert response.status_code == 201
        context["documents"].append(Document.model_validate(response.json()))
```
Y a continuación, también deberemos modificar todos los steps que invocan a la API para incluir los headers mediante el helper (a excepción del swagger):
- Ejemplo:
```python
@when("I get all documents")
def get_documents(client, context):
    response = client.get("/documents",headers=get_auth_headers(context=context))
    context["response"] = response
```

Esto nos va a permitir definir en nuestro escenario un given en el que podremos parametrizar cuantos usuarios queremos, y cuantos documentos por usuario, haciéndolo super-flexible:

Vamos a definir, para comprobar que nuestra batería de tests funciona, un escenario en el que comprovamos que sin token la API debería devolver un 401
```gherkin
Scenario: An unauthenticated requests causes 401
    Given API is running
    And documents owned by:
        | Bob     | 1         |
        | John    | 1         |
        | Alice   | 1         |
    When I get an existing document
    Then response is 401
```

Si comprobamos el resultado, efectivamente vamos a tener un error, puesto que no hemos modificado la API para incluir la autenticación. 

```
FAILED test/steps/test_documents_steps.py::test_an_unauthenticated_requests_causes_401 - assert 200 == 401
```

Para seguir avanzando mediante el TDD, vamos a codificar a partir del caso de uso más básico (implementación obvia) los escenarios en base a sus criterios de aceptación, quedando el feature tal que así:

- **Como usuario quiero crear un documento**
```gherkin
Feature: As user I wan't to manage documents

  Scenario: An unauthenticated user can't create a document
    Given API is running
    When I create a document
    Then response is 401

  Scenario: A user with invalid token can't create a document
    Given API is running
    And an invalid JWT token for user John
    When I create a document
    Then response is 401

  Scenario: A valid user can create a document
    Given API is running
    And a valid JWT token for user John
    When I create a document
    Then response is 201   
```
De nuevo ejecutamos los tests, y efectivamente el resultado no va a ser el esperado, porque no hemos incluido la autenticación en los endpoints.

## Securización de la API

Vamos a configurar la API para recibir un bearer token.

Lo primero será añadir la variable jwt_secret que nos permitirá codificar y decodificar el token en el settings de la aplicación:

```python
    jwt_secret: str
```

Creamos un provider que nos entrega el sub del token: [oauth2_provider](../src/app/api/oauth2_provider.py)

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")  # tokenUrl solo se usa si hay login

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        return user_id
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
```

Y la inyectamos en cada endpoint:
- Ejemplo:
```python
@router.post("/", response_model=Document, status_code=HTTP_201_CREATED)
async def post_document(
        current_user: str = Depends(get_current_user),
        metadata: DocumentCreate = Depends(document_create_form),
        file: UploadFile = File(...),
        mongo_repo: DocumentMongoRepository = Depends(get_mongo_repo),
        s3_repo: S3Repository = Depends(get_s3_repo),
) -> Document:
```
Si volvemos a ejecutar los tests, ahora sí veremos que tenemos el resultado esperado. Por lo que ya podemos pasar a la siguiente fase

## Siguiente iteración, aplicación de criterios de aceptación

En este punto, tenemos nuestra API ya securizada, por lo que podemos seguir desarrollando casos de uso. Vamos a pasar al siguiente que nos parezca más fácil (implementación obvia)

- **Como usuario quiero consultar todos mis documentos**

Para ello vamos a definir los escenarios en base a los criterios de aceptación:

```gherkin
  Scenario: A valid user retrieves an empty list when there are no documents
    Given API is running
    And a valid JWT token for user John
    When I get all documents
    Then response is an empty list

  Scenario: A valid user can get their documents
    Given API is running
    And a valid JWT token for user John
    And documents owned by:
        | John | 5 |
        | Alice | 10 |
        | Bob   | 3  |
    When I get all documents
    Then response is 200
    And response contains only my documents

  Scenario: A valid user retrieves an empty list where he doesn't own documents
    Given API is running
    And a valid JWT token for user John
    And documents owned by:
        | Alice | 1 |
        | Bob   | 1 |
    When I get all documents
    Then response is 200
    And response is an empty list
```

Aquí, si intentaramos ejecutar, nos encontraremos dos errores, el primero debido a que no hemos definido un step *Then* para el criterio
de aceptación de que un usuario sólo puede recuperar sus documentos. El segundo, porque no hemos implementado la lógica de que un usuario
sólo puede consultar sus documentos. 

Siguiendo la filosofía del TDD, lo siguiente será crear el step para validar que la lista sólo contiene los documentos del usuario:

```python
@then("response contains only my documents")
def response_only_my_documents(context):
    docs : List[Document] = []
    [docs.append(Document.model_validate(element)) for element in context["response"].json()]
    assert not [doc for doc in docs if doc.owner_id != context["user_id"]]
```
Efectivamente, esto nos va a seguir fallando, porque no hemos implementado la lógica necesaria para que el documento tenga owner. Vamos a ello!

Modificamos el model:

```python
class Document(BaseModel):
    """
    Represents the metadata for accessing a Document
    Attributes:
        id (str): Unique document identifier
        title (str): Document title
        description (str): Document description
        key (str): The unique file name where the file resides
        file_path (str): The URL where the document can be accessed
    """

    id: str
    title: str
    description: str
    key: str
    file_path: Optional[str]
    owner_id: str
```

Y modificamos la creación del documento, primero en el repository. Añadimos el parametro current user y lo asignamos a la propiedad del model

```python
    async def create_document(self, document_create: DocumentCreate,current_user: str) -> Document:
        """
        Creates a new document
        Args:
            document (Document): The document to create
        Returns:
            id (str): The unique document identifier
        """
        LOG.debug(f"Create document {document_create}")
        url = quote(Path(document_create.title).name, safe="")
        document: Document = Document(
            id="",
            title=document_create.title,
            description=document_create.description,
            key=url,
            file_path=None,
            owner_id=current_user
        )
        data = document.model_dump(exclude={"id"})
        result = await self.collection.insert_one(data)
        document.id = str(result.inserted_id)
        return document
```
Después en la API:
```python
@router.post("/", response_model=Document, status_code=HTTP_201_CREATED)
async def post_document(
        current_user: str = Depends(get_current_user),
        metadata: DocumentCreate = Depends(document_create_form),
        file: UploadFile = File(...),
        mongo_repo: DocumentMongoRepository = Depends(get_mongo_repo),
        s3_repo: S3Repository = Depends(get_s3_repo),
) -> Document:
    """
    Post a document
    Args:
        metadata(DocumentCreate): The title and description of the document
        file(UploadFile): The file content in bytes
        mongo_repo(DocumentMongoRepository): The documents repository
        s3_repo(S3Repository): The S3 Bucket repository
    Returns:
        document (Document): The created document with a presigned url for downloading the file
    """
    content: bytes = await file.read()
    doc = await mongo_repo.create_document(document_create=metadata, current_user=current_user)
    s3_repo.upload_file(content, doc.key)
    doc.file_path = s3_repo.generate_presigned_url_for_get(doc.key)
    return doc
```
Añadimos el parámetro correspondiente en la creación del documento

En este punto, la lógica de creación estará bien, pero nos va a fallar el test, porque no hemos aplicado el filtro en la consulta,
así que modificaremos el GET para que incluya el filtro por owner id, primero en el repositorio, incluyendo parámetro y filtro en la query

```python
    async def list_documents(self,owner_id: str) -> List[Document]:
        """
        Returns the whole list of documents
        Returns:
            documents (List[Document])
        """
        cursor = self.collection.find({"owner_id":owner_id})
        docs = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            docs.append(Document(**doc))
        return docs
```

Y luego en la API:

```python
@router.get("/", response_model=List[Document])
async def list_documents(
        current_user: str = Depends(get_current_user),
        mongo_repo: DocumentMongoRepository = Depends(get_mongo_repo),
        s3_repo: S3Repository = Depends(get_s3_repo),
) -> List[Document]:
    """
    Get a List of Documents
    Args:
        mongo_repo (DocumentMongoRepository): MongoDB Repository for accessing metadata
        s3_repo (S3Repository): S3 Repository for accessing files
    Returns:
        documents (List[Document]): The whole list of existing documents
    """
    LOG.debug("Get the documents list")
    docs = await mongo_repo.list_documents(owner_id=current_user)
    LOG.debug(f"Document list has {len(docs)} elements")
    for doc in docs:
        doc.file_path = s3_repo.generate_presigned_url_for_get(doc.key)
    return docs
```
Una vez aplicada esta lógica, nuestros tests sí que funcionarán correctamente.

## Resto de iteraciones

El objetivo del taller no es el de finalizar la API, sino el de trabajar la dinámica TDD, e integrarla en pytest y pybdd

Por lo que lo dejaríamos aquí, y avanzaremos otros conceptos

## Cobertura

Vamos a ver un repaso a la cobertura realizada en estos tests, y repasar lo que hablamos al principio:
- No obsesionarse con el porcentaje
- Buscar cubrir comportamiento en lugar de líneas
- Intentar cubrir todas las ramas del código

## Mockear vs no mockear

En general, en la medida de lo posible, lo ideal es mockear lo minimo, pero cuando es necesario, pytest nos da las opciones.

# Bonus point

Si hemos llegado hasta aquí en tiempo, vamos a explorar las opciones de mocking y stubbing. Vamos a empezar aplicando una nueva funcionalidad.

Los usuarios, además de autenticados, deben existir en nuestra aplicación, para ello tenemos una API REST a la que llamaremos por usuario, y para ello nos definen los siguientes casos de uso, empezando por el alta de un documento:

```gherkin
    Scenario: An enrolled and authenticated user can create a document
      Given: API is running
      And: a valid JWT token for user John
      And: John is an enrolled user
      When: I create a document
      Then: Then response is 201
    Scenario: An non enrolled and authenticated user can create a document
      Given: API is running
      And: a valid JWT token for user John
      And: John is not an enrolled user
      When: I create a document
      Then: Then response is 403
```

Para codificar la funcionalidad creamos un repositorio http:

Primero añadimos la depdendencia de requests al proyecto:

```toml
    "requests==2.32.5"
```
Y creamos el repository
```python
class UserRepository:
    """
    A repository for accessing enrolled users
    Args:
        base_url(str): base url for endpoint
        timeout(str): timeout limit, default 5.0 seconds
    """
    def __init__(self, base_url: str, timeout: float = 5.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def exists(self, user_id: str) -> bool:
        """
        Validate if user is enrolled
        Args:
            user_id(str): The user id
        Returns:
            boolean: True if user exists, false if user doesn't exist
        Raises:
            HTTPException with 500 status
        """
        url = f"{self.base_url}/users/{user_id}"
        response = requests.get(url, timeout=self.timeout)

        if response.status_code == 200:
            return True

        if response.status_code == 404:
            return False

        raise HTTPException(status_code=500,detail="Internal server error")
```
Modificaremos el model settings para incluir el base url que inyectaremos:
```python
class Settings(BaseSettings):
    mongodb_uri: str
    mongodb_db: str
    s3_endpoint_url: str
    s3_access_key: str
    s3_secret_key: str
    s3_bucket: str
    oauth2_authorization_url: str = "https://auth-server.example.com/auth/realms/myrealm/protocol/openid-connect/token"
    jwt_secret: str = "example"
    users_base_url: str

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "forbid",
        "case_sensitive": False,
    }


settings = Settings()  # type: ignore[call-arg]
```
El archivo unittest.env para inyectar una url base:
```
USERS_BASE_URL=http://example.com
```
Con estos cambios, podemos comprobar ejecutando los tests que la configuración que hemos realizado es correcta

Ahora el siguiente paso será desarrollar los steps que necesitamos para acceder a la API, y, dado que no podremos acceder de forma
real, lo que haremos es mockear el resultado

Lo primero será, en el conftest, mockear el repositorio, que mockearemos con pytest-mock

Añadimos la dependencia en dev
```
    "pytest-mock==3.15.1",
```
Y creamos el fixture para mockear la API:
```python
@pytest.fixture(scope="function")
def mock_users_rest_repository(mocker):
    return mocker.Mock(spec=UsersRestRepository)
```
También tendremos que modificar el fixture del client para probar la API para incluir el mock y hacer override de la dependencia del repository:
```python
@pytest.fixture(scope="function")
def client(mock_users_rest_repository):
    """
    Prepares a TestClient for testing fastAPI endpoints
    Returns:
        TestClient: A FastAPI API Rest Test client
    """
    app.dependency_overrides[create_users_repository] = lambda: mock_users_rest_repository
    yield TestClient(app)
    app.dependency_overrides.clear()
```
A continuación creamos los steps
```python
@given(parsers.parse("{user_id} is an enrolled user"))
def user_is_enrolled(mock_users_rest_repository,user_id: str):
    mock_users_rest_repository.exists.return_value = True

@given(parsers.parse("{user_id} is not an enrolled user"))
def user_is_not_enrolled(mock_users_rest_repository,user_id: str):
    mock_users_rest_repository.exists.return_value = False
```
En este punto aún no hemos creado la lógica, pero el siguiente paso sería adaptar los escenarios existentes a la nueva funcionalidad:
```gherkin
  Scenario: A valid user can create a document
    Given API is running
    And a valid JWT token for user John
    And John is an enrolled user
    When I create a document
    Then response is 201

  Scenario: A valid user retrieves an empty list when there are no documents
    Given API is running
    And a valid JWT token for user John
    And John is an enrolled user
    When I get all documents
    Then response is an empty list

  Scenario: A valid user can get their documents
    Given API is running
    And a valid JWT token for user John
    And John is an enrolled user
    And documents owned by:
        | John | 5 |
        | Alice | 10 |
        | Bob   | 3  |
    When I get all documents
    Then response is 200
    And response contains only my documents

  Scenario: A valid user retrieves an empty list where he doesn't own documents
    Given API is running
    And a valid JWT token for user John
    And John is an enrolled user
    And documents owned by:
        | Alice | 1 |
        | Bob   | 1 |
    When I get all documents
    Then response is 200
    And response is an empty list
```
En este punto, deberíamos de poder ejecutar los tests sin errores

Y ahora, siguiendo con la filosofía del TDD, crearemos el escenario que impide que un usuario no enrolado cree un documento:
```gherkin
  Scenario: A non enrolled valid user can't create a document
    Given API is running
    And a valid JWT token for user John
    And John is not an enrolled user
    When I create a document
    Then response is 403
```
Si ejecutamos los tests, este último va a fallar, ya que no codificamos la lógica. Procedemos a ello. 
```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")  # tokenUrl solo se usa si hay login
users_rest_repository = UsersRestRepository(base_url=settings.users_base_url)

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        if not users_rest_repository.exists(user_id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return user_id
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
```
## Conclusiones

Hemos incluido una nueva funcionalidad que no podíamos reproducir con infraestructura local y hemos podido probar la lógica de negocio

Pero... no hemos podido probar el código que realmente invoca a la API 

Esto nos lleva a unas reflexiones sobre TDD, BDD y cobertura de código: 

- Calidad de los tests es más importante que la cobertura
- Tests basados en comportamientos
- Probar comportamiento
