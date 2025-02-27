"""Factory methods for creating conversion operations."""

import importlib
from typing import Type, TypeVar, Any

from .base import AbstractConversionOperations

T = TypeVar('T', bound=AbstractConversionOperations)

class ConversionFactory:
    """Factory class for creating conversion operations."""

    @staticmethod
    def create(cls: Type[T]) -> T:
        """
        Create an instance of the specified conversion operation class.

        Args:
            cls: The class type of the conversion operation to create.

        Returns:
            An instance of the specified conversion operation class.
        """
        return cls()

    @staticmethod
    def load_class(class_path: str) -> Type[AbstractConversionOperations]:
        """
        Dynamically load a class from a string path.

        Args:
            class_path: Full path to the class (e.g., 'mv_platform_core.conversion.base.RemoveHyphen')

        Returns:
            The class type specified by the path.

        Raises:
            ImportError: If the module or class cannot be found.
            AttributeError: If the class does not exist in the module.
        """
        try:
            module_path, class_name = class_path.rsplit('.', 1)
            module = importlib.import_module(module_path)
            return getattr(module, class_name)
        except (ImportError, AttributeError) as e:
            raise ImportError(f"Could not load class '{class_path}': {str(e)}")

    @classmethod
    def create_from_string(cls, class_path: str) -> AbstractConversionOperations:
        """
        Create an instance of a conversion operation from a string path.

        Args:
            class_path: Full path to the class (e.g., 'mv_platform_core.conversion.base.RemoveHyphen')

        Returns:
            An instance of the specified conversion operation class.

        Example:
            >>> factory = ConversionFactory()
            >>> operation = factory.create_from_string('mv_platform_core.conversion.base.RemoveHyphen')
            >>> df = operation.convert(df, columns)
        """
        operation_class = cls.load_class(class_path)
        return cls.create(operation_class)
