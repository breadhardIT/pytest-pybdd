import logging
import subprocess
import time

import pytest
from botocore.exceptions import ClientError
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings
from app.main import app
from app.repository.document_mongo_repository import DocumentMongoRepository
from app.repository.document_s3_repository import S3Repository

logging.basicConfig(
    level=logging.INFO,  # mostrar INFO y superiores
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logging.getLogger("httpx").setLevel(logging.WARNING)


@pytest.fixture(scope="session", autouse=True)
def docker_infra():
    """
    Prepares docker infrastructure for tests
    """
    subprocess.run(["docker", "compose", "up", "-d"], check=True)
    time.sleep(3)
    yield
    subprocess.run(["docker", "compose", "down"], check=True)


@pytest.fixture(scope="session")
def client():
    """
    Prepares a TestClient for testing fastAPI endpoints
    Returns:
        TestClient: A FastAPI API Rest Test client
    """
    return TestClient(app)


@pytest.fixture(scope="session")
def mongo_repo() -> DocumentMongoRepository:
    """
    Prepares a mongo client for manipulating database content during tests
    Returns:
        DocumentMongoRepository: A MongoDB Repository for Document model
    """
    client = AsyncIOMotorClient(settings.mongodb_uri)
    return DocumentMongoRepository(client=client, db_name=settings.mongodb_db)


@pytest.fixture(scope="session")
def s3_repo() -> S3Repository:
    """
    Prepares S3 Repository for manipulating bucket during tests
    Returns:
        S3Repository: The S3 repository for Document model
    """
    repository: S3Repository = S3Repository(
        endpoint_url=settings.s3_endpoint_url,
        access_key=settings.s3_access_key,
        secret_key=settings.s3_secret_key,
        bucket=settings.s3_bucket,
    )
    try:
        repository.client.head_bucket(Bucket=settings.s3_bucket)
    except ClientError:
        repository.client.create_bucket(Bucket=settings.s3_bucket)
    return repository


@pytest.fixture(autouse=True)
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
    yield


@pytest.fixture
def context():
    return {}
