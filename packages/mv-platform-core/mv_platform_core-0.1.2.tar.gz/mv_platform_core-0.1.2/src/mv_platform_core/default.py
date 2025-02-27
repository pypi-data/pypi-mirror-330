"""
This class idealy needs to be moved to the library where it will be used to lokup transformations etc
"""

from pyspark.sql import DataFrame, SparkSession

from . import DataProcessingTemplate, DataReader, DataWriter
from .conversion import AbstractConversionOperations
from .conversion.base import load_class


class DefaultDataProcessing(DataProcessingTemplate):

    def __init__(self,
                 reader: DataReader,
                 writer: DataWriter,
                 configs: dict = None,
                 spark: SparkSession = None):
        super().__init__(reader, writer, spark)
        self.configs = configs #FIXME this should be not dict but pydantic class

    def transform(self, input) -> DataFrame:
        sql_query = self._load_sql_from_file(self.configs.get("path"))
        df = self.spark.sql(sql_query).drop("rnum").selectExpr("*",  "current_date() as as_of_date")
        return df

    def conversion(self, df: DataFrame) -> DataFrame:
        conversion_items: dict  = self.configs.get("conversion_operations")
        for operation_name, columns in conversion_items.items():
            class_path = f"mv_platform_core.conversion.base.{operation_name}" #FIXME replace with plugins
            operation_class = load_class(class_path)
            operation: AbstractConversionOperations = operation_class()
            df = operation.convert(df, columns)
        return df

    def _load_sql_from_file(self, file_path):
        try:
            with open(file_path, "r") as file:
                soql_query = file.read()
            return soql_query
        except Exception as e:
            raise e
