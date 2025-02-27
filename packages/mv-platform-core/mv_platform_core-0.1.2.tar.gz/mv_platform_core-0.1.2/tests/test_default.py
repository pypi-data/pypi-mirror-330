import logging
import os
import tempfile
from unittest.mock import Mock
from datetime import datetime

import pytest

from mv_platform_core.readers import ReaderFactory
from mv_platform_core.writers import WriterFactory
from mv_platform_core.writers.base import DataWriter
from mv_platform_core.default import DefaultDataProcessing

from pyspark.sql import SparkSession

class TestDefaultTemplate:


    @pytest.fixture(autouse=True)
    def prepare_spark_session(self, spark_session: SparkSession):
        self.spark = spark_session

    @pytest.fixture(scope="function")
    def sample_data(self):
        data = [("1", "John", 30), ("2", "Jane", 25), ("3", "Bob", 35)]
        columns = ["id", "name", "age"]
        df = self.spark.createDataFrame(data, columns)
        df.createOrReplaceTempView("sample_table")
        self.temp_dir = tempfile.TemporaryDirectory().name
        self.spark.sql("DROP TABLE IF EXISTS below_thirty")
        self.spark.sql(f"""
            CREATE TABLE IF NOT EXISTS below_thirty 
                (ID STRING, NAME STRING, AGE LONG, as_of_date Date) 
                USING DELTA
                PARTITIONED BY (as_of_date)
                LOCATION '{self.temp_dir}/below_thirty'
        """)
        yield
        self.spark.catalog.dropTempView("sample_table")


    def test_read_data(self, sample_data):

        # Create a sample bronze_tables dictionary
        bronze_tables = {
            "sample": {
                "table_name": "sample_table",
                "primary_keys": ["id"],
                "filter_column": "age",
                "filter_condition": "age > 0"
            }
        }

        bronze_reader = ReaderFactory.create_reader("bronze", tables=bronze_tables)
        mock_data_writer = Mock(spec=DataWriter)
        # Initialize DefaultDataProcessing
        default_processing = DefaultDataProcessing(
            reader=bronze_reader,
            writer=mock_data_writer,
            spark=self.spark
        )

        # Call read_data method
        result = default_processing.read_data()

        # Assert the result
        assert result == "success"

        # Optionally, you can add more assertions here to check if the temp view was created correctly
        temp_view_data = self.spark.sql("SELECT * FROM temp_sample").collect()
        assert len(temp_view_data) == 3  # Assuming all rows meet the filter condition

    def test_transform_data(self, sample_data):
        # Create a sample bronze_tables dictionary
        bronze_tables = {
            "sample": {
                "table_name": "sample_table",
                "primary_keys": ["id"],
                "filter_column": "age",
                "filter_condition": "age > 0"
            }
        }

        bronze_reader = ReaderFactory.create_reader("bronze", tables=bronze_tables)
        mock_data_writer = Mock(spec=DataWriter)
        input = {
            "path": "./transformation.sql"
        }
        default_processing = DefaultDataProcessing(
            reader=bronze_reader,
            writer=mock_data_writer,
            configs=input,
            spark=self.spark
        )
        default_processing.read_data()

        result = default_processing.transform(input)
        assert result.count() == 1

    def test_write_scd_one(self, sample_data):
        bronze_tables = {
            "sample": {
                "table_name": "sample_table",
                "primary_keys": ["id"],
                "filter_column": "age",
                "filter_condition": "age > 0"
            }
        }

        bronze_reader = ReaderFactory.create_reader("bronze", tables=bronze_tables)

        as_of_date = datetime.now().strftime("%Y-%m-%d")
        scd_one_writer = WriterFactory.create_writer("scd_one",spark=self.spark, as_of_date=as_of_date, destination=f"{self.temp_dir}/below_thirty")
        input = {
            "path": "./transformation.sql"
        }
        default_processing = DefaultDataProcessing(
            reader=bronze_reader,
            writer=scd_one_writer,
            configs=input,
            spark=self.spark
        )
        default_processing.read_data()

        result = default_processing.transform(input)
        default_processing.write_output(result)

        assert self.spark.sql("select * from below_thirty").count() == 1

    def test_conversion(self, sample_data):
        # Create test data with spaces and hyphens
        data = [
            ("1", "  John-Doe  ", 30),
            ("2", "Jane-Smith  ", 25),
            ("3", "  Bob-Brown", 35)
        ]
        columns = ["id", "name", "age"]
        df = self.spark.createDataFrame(data, columns)
        df.createOrReplaceTempView("conversion_test_table")

        bronze_tables = {
            "sample": {
                "table_name": "conversion_test_table",
                "primary_keys": ["id"],
                "filter_column": "age",
                "filter_condition": "age > 0"
            }
        }

        bronze_reader = ReaderFactory.create_reader("bronze", tables=bronze_tables)
        mock_data_writer = Mock(spec=DataWriter)

        # Configure conversion operations
        configs = {
            "conversion_operations": {
                "RemoveTrailingWhitespace": ["name"],
                "RemoveHyphen": ["name"]
            }
        }

        # Initialize DefaultDataProcessing with conversion configs
        default_processing = DefaultDataProcessing(
            reader=bronze_reader,
            writer=mock_data_writer,
            configs=configs,
            spark=self.spark
        )

        # Read and convert data
        default_processing.read_data()
        df_result = default_processing.conversion(self.spark.sql("SELECT * FROM temp_sample"))

        # Verify results
        rows = df_result.collect()
        assert rows[0]["name"] == "JohnDoe"  # No spaces, no hyphen
        assert rows[1]["name"] == "JaneSmith"  # No spaces, no hyphen
        assert rows[2]["name"] == "BobBrown"  # No spaces, no hyphen

        # Clean up
        self.spark.catalog.dropTempView("conversion_test_table")
