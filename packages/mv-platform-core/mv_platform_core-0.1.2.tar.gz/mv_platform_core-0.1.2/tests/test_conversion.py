import pytest
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

import mv_platform_core.conversion.base as conversion_base
from mv_platform_core.conversion.base import AbstractConversionOperations
from mv_platform_core.conversion import ConversionFactory


class TestConversionFactory:
    """Test suite for ConversionFactory and its operations."""

    @pytest.fixture(autouse=True)
    def prepare_spark_session(self, spark_session: SparkSession):
        """Initialize SparkSession for all tests."""
        self.spark = spark_session

    def test_factory_creates_instances(self):
        """Test that factory creates instances of all conversion operations."""
        test_cases = [
            (conversion_base.RemoveTrailingWhitespace, "RemoveTrailingWhitespace"),
            (conversion_base.RemoveHyphen, "RemoveHyphen"),
            (conversion_base.ModifyDataType, "ModifyDataType"),
            (conversion_base.DropNullRecords, "DropNullRecords"),
        ]

        for cls, name in test_cases:
            operation = ConversionFactory.create(cls)
            assert isinstance(operation, cls), f"Failed to create {name} instance"
            assert isinstance(operation, AbstractConversionOperations), f"{name} is not an AbstractConversionOperations"

    def test_factory_creates_instances_from_string(self):
        """Test that factory creates instances from string paths."""
        test_cases = [
            ("mv_platform_core.conversion.base.RemoveTrailingWhitespace", conversion_base.RemoveTrailingWhitespace),
            ("mv_platform_core.conversion.base.RemoveHyphen", conversion_base.RemoveHyphen),
            ("mv_platform_core.conversion.base.ModifyDataType", conversion_base.ModifyDataType),
            ("mv_platform_core.conversion.base.DropNullRecords", conversion_base.DropNullRecords),
        ]

        for class_path, expected_type in test_cases:
            operation = ConversionFactory.create_from_string(class_path)
            assert isinstance(operation, expected_type), f"Failed to create instance from {class_path}"
            assert isinstance(operation, AbstractConversionOperations), f"Instance from {class_path} is not an AbstractConversionOperations"

    def test_factory_load_class_invalid_path(self):
        """Test that factory raises appropriate error for invalid class paths."""
        with pytest.raises(ImportError):
            ConversionFactory.load_class("invalid.module.path.Class")

        with pytest.raises(ImportError):
            ConversionFactory.load_class("mv_platform_core.conversion.base.NonExistentClass")

    def test_remove_trailing_whitespace_transformation(self):
        """Test RemoveTrailingWhitespace operation functionality."""
        # Create test DataFrame
        data = [("  test  ",), ("value  ",)]
        df = self.spark.createDataFrame(data, ["col1"])

        # Apply transformation
        operation = ConversionFactory.create(conversion_base.RemoveTrailingWhitespace)
        result = operation.convert(df, ["col1"])

        # Verify results
        rows = result.collect()
        assert rows[0]["col1"] == "test"
        assert rows[1]["col1"] == "value"

    def test_remove_hyphen_transformation(self):
        """Test RemoveHyphen operation functionality."""
        # Create test DataFrame
        data = [("test-value",), ("another-test",)]
        df = self.spark.createDataFrame(data, ["col1"])

        # Apply transformation
        operation = ConversionFactory.create(conversion_base.RemoveHyphen)
        result = operation.convert(df, ["col1"])

        # Verify results
        rows = result.collect()
        assert rows[0]["col1"] == "testvalue"
        assert rows[1]["col1"] == "anothertest"

    def test_modify_data_type_transformation(self):
        """Test ModifyDataType operation functionality."""
        # Create test DataFrame with schema
        schema = StructType([
            StructField("col1", StringType(), True)
        ])
        data = [("123",), ("456",)]
        df = self.spark.createDataFrame(data, schema)

        # Apply transformation
        operation = ConversionFactory.create(conversion_base.ModifyDataType)
        result = operation.convert(df, {"integer": ["col1"]})

        # Verify results
        assert result.schema["col1"].dataType == IntegerType()
        rows = result.collect()
        assert rows[0]["col1"] == 123
        assert rows[1]["col1"] == 456

    def test_drop_null_records_transformation(self):
        """Test DropNullRecords operation functionality."""
        # Create test DataFrame
        data = [("test", None), (None, "value"), ("data", "value")]
        df = self.spark.createDataFrame(data, ["col1", "col2"])

        # Apply transformation
        operation = ConversionFactory.create(conversion_base.DropNullRecords)
        result = operation.convert(df, ["col1", "col2"])

        # Verify results
        rows = result.collect()
        assert len(rows) == 1
        assert rows[0]["col1"] == "data"
        assert rows[0]["col2"] == "value"
