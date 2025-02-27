import os
import shutil
import sys
import tempfile

import findspark
import pytest

from pyspark.sql import SparkSession

from .dbx_test_settings import JARS_PACKAGES

# Add src directory to PYTHONPATH
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
sys.path.insert(0, src_dir)

findspark.init()

def removeMetastore(temp_dir: str):
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

@pytest.fixture(scope="session")
def spark_session(request) -> SparkSession:  # type: ignore
    """Create a PySpark SparkSession."""

    with tempfile.TemporaryDirectory() as temp_dir:
        warehouse_location = f"{temp_dir}/spark-warehouse"
        print(f"\n----------> Warehouse location: {warehouse_location}")
        spark = (
            SparkSession.builder.master("local[*]")
            .appName("prx-dwh-lib-test")
            .config("spark.sql.warehouse.dir", warehouse_location)
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
            .config("spark.jars.packages", JARS_PACKAGES)
            .getOrCreate()
        )
        request.addfinalizer(lambda: spark.stop())

        yield spark
        spark.stop()
        removeMetastore(temp_dir)
