import importlib
from abc import ABC, abstractmethod
from typing import Dict, List, Type, Any

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, regexp_replace, trim


class AbstractConversionOperations(ABC):
    @abstractmethod
    def convert(self, df: DataFrame, columns: List) -> DataFrame:
        """
        Transform the input DataFrame.

        Parameters:
        df (DataFrame): The input DataFrame.
        columns (List): List of columns

        Returns:
        DataFrame: The transformed DataFrame.
        """
        pass


class RemoveTrailingWhitespace(AbstractConversionOperations):
    """
    Remove trailing white spaces.
    """

    def convert(self, df: DataFrame, columns: List) -> DataFrame:
        """
        Transform the input DataFrame by removing trailing spaces from given columns.

        Parameters:
        df (DataFrame): The input DataFrame.
        columns (List): List of columns

        Returns:
        DataFrame : The transformed DataFrame
        """
        for column in columns:
            df = df.withColumn(column, trim(col(column)))
        return df


class RemoveHyphen(AbstractConversionOperations):
    """
    Remove hyphens from given columns.
    """

    def convert(self, df: DataFrame, columns: List) -> DataFrame:
        """
        Transform the input DataFrame by removing hyphen from given columns.

        Parameters:
        df (DataFrame): The input DataFrame.
        columns (List): List of columns

        Returns:
        DataFrame : The transformed DataFrame
        """
        for column in columns:
            df = df.withColumn(column, regexp_replace(col(column), "-", ""))
        return df


class ModifyDataType(AbstractConversionOperations):
    """
    Modify the data type of specified DataFrame columns.
    """

    def convert(self, df: DataFrame, data_type_change: Dict) -> DataFrame:
        """
        Change the data type of specified DataFrame columns.

        Parameters:
        df(DataFrame): The DataFrame with the columns you want to change the datatype of.
        data_type_change(Dict): A dictionary where the key is the target data type, and the value is a list of column names.

        Returns:
        DataFrame: The DataFrame with modified column data types.
        """
        for data_type, columns in data_type_change.items():
            for column in columns:
                df = df.withColumn(column, col(column).cast(data_type))
        return df


class DropNullRecords(AbstractConversionOperations):
    """
    Drop rows from a DataFrame with null values in any or specified columns.
    """

    def convert(self, df: DataFrame, columns: List[str] = None) -> DataFrame:
        """
        Transform the input DataFrame by dropping rows from any or specified columns having null value.

        Parameters:
        df (DataFrame): The input DataFrame.
        columns (List[str]): List of columns

        Returns:
        DataFrame: The transformed DataFrame
        """

        # If columns list is not provided or is empty, drop any row that has at least one null value
        if not columns:
            return df.na.drop(how="any")

        # Check if columns exist in df
        missing_cols = set(columns) - set(df.columns)
        if df and missing_cols:
            raise ValueError(f"These columns '{', '.join(missing_cols)}' do not exist in the DataFrame")

        return df.na.drop(subset=columns)


def load_class(class_path: str) -> Type[Any]:
    """
    Load a class from a string path.

    Args:
        class_path: Full path to the class (e.g., 'mv_platform_core.conversion.base.RemoveHyphen')

    Returns:
        The class type specified by the path

    Raises:
        ValueError: If class_path is empty or invalid format
        ImportError: If module or class cannot be found
    """
    if not class_path or '.' not in class_path:
        raise ValueError("Invalid class path format. Expected 'module.path.ClassName'")

    try:
        module_path, class_name = class_path.rsplit('.', 1)
        module = importlib.import_module(module_path)
        class_type = getattr(module, class_name)

        # Verify it's actually a class
        if not isinstance(class_type, type):
            raise TypeError(f"{class_path} is not a class")

        return class_type
    except ImportError as e:
        raise ImportError(f"Could not import module '{module_path}': {str(e)}")
    except AttributeError:
        raise ImportError(f"Could not find class '{class_name}' in module '{module_path}'")
