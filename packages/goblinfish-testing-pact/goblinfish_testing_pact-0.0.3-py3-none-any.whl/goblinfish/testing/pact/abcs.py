#!/usr/bin/env python3.11
"""
Provides classes and functionality that allow common properties and
methods to be required by other package entities.
"""

from __future__ import annotations

# Built-In Imports
import abc


# Module Abstract Base Classes
class HasSourceAndTestEntities(abc.ABC):
    """
    Provides baseline functionality, interface requirements, and type-
    identity for objects that can retrieve source- and test-code entities.
    """

    @property
    @abc.abstractmethod
    def source_entities(self) -> set[str]:
        """
        Gets the actual entities present in the source target
        """
        raise NotImplementedError(
            f'{self.__class__.__name__}.source_entities is not implemented '
            'as required by goblinfish.testing.pact.abcs.'
            'HasSourceAndTestEntities'
        )

    @property
    @abc.abstractmethod
    def test_entities(self) -> set[str]:
        """
        Gets the actual entities present in the test target
        """
        raise NotImplementedError(
            f'{self.__class__.__name__}.test_entities is not implemented '
            'as required by goblinfish.testing.pact.abcs.'
            'HasSourceAndTestEntities'
        )


# Code to run if the module is executed directly
if __name__ == '__main__':
    pass
