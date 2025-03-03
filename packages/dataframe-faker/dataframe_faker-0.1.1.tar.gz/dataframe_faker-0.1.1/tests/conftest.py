from typing import Generator, cast

import pytest
from faker import Faker
from pyspark.sql import SparkSession


@pytest.fixture(scope="module")
def spark() -> Generator[SparkSession, None, None]:
    builder = cast(SparkSession.Builder, SparkSession.builder)
    builder.appName("unit-testing").master("local[4]")

    yield builder.getOrCreate()


@pytest.fixture(scope="module")
def fake() -> Faker:
    return Faker()
