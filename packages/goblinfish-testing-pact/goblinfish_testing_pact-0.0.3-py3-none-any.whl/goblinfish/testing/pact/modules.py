#!/usr/bin/env python3.11
"""
Provides a class and related functionality that executes tests requiring
test-case classes to be defined for all classes and functions within a
source module, and that those test-cases are of an appropriate type.
"""

from __future__ import annotations

# Built-In Imports
import inspect
import os
import sys
import unittest

from importlib import import_module
from types import ModuleType

# Third-Party Imports

# Path Manipulations (avoid these!) and "Local" Imports
from goblinfish.testing.pact.abcs import HasSourceAndTestEntities
from goblinfish.testing.pact.module_members import \
    ExaminesSourceClass, ExaminesSourceFunction
from goblinfish.testing.pact.pact_logging import logger

# Module "Constants" and Other Attributes

# Module Exceptions


# Module Functions

# Module Metaclasses


# Module Abstract Base Classes
class ExaminesModuleMembers(HasSourceAndTestEntities):
    """
    Mix-in class that tests for expected test-case types for each
    callable member in a specified source module.


    Class Variables/Attributes:
    ---------------------------
    TARGET_MODULE : str
        The resolvable Python namespace to the source module that is
        being tested.
        MUST BE DEFINED ON EACH DERIVED CLASS
        Examples:
            goblinfish.testing.pact.modules
            goblinfish.testing.pact.projects
    TEST_PREFIX : str [defaults to 'test_']
        The string that is used to prefix all expected test-case names
        in the test module that the test-case class lives in.
    """

    TARGET_MODULE = ''
    TEST_PREFIX = 'test_'

    @property
    def expected_test_entities(self) -> set[str]:
        """
        Constructs and returns a set of expected test-module path-fragments
        from the source_entitites that the instance is concerned with.

        Note:
        -----
        Calculation of test-entity names, both directories and modules,
        will make an effort to assure that no more than two concurrent
        underscore characters will exist in the name, but that is currently
        limited to one pass replacing '___' with '__' in those names.
        """
        return set(
            [
                os.sep.join(
                    [
                        f'{self.TEST_PREFIX}{segment}'.replace('___', '__')
                        for segment in path.split(os.sep)
                    ]
                )
                for path in self.source_entities
            ]
        )

    @property
    def source_entities(self) -> set[str]:
        """
        Gets the actual entities present in the source target
        """
        logger.debug(f'Getting callables in {self.TARGET_MODULE}')
        return set(
            [
                name for name, member
                in inspect.getmembers(self.target_module, callable)
                if hasattr(member, '__module__')
                and sys.modules[member.__module__] == self.target_module
            ]
        )

    @property
    def target_module(self) -> ModuleType:
        """
        Gets, caches, and returns the actual module specified by the
        namespace in the class' TARGET_MODULE attribute, importing it
        locally if needed in the process.
        """
        assert self.TARGET_MODULE, (
            f'{self.__class__.__name__}.TARGET_MODULE does not have a '
            'module namespace specified in it: '
            f'"{self.TARGET_MODULE}" ({type(self.TARGET_MODULE).__name__})'
        )
        # If it's already cached, return it
        if getattr(self, '_target_module', None) is not None:
            return self._target_module

        # If it's already imported, but not cached, cache it and return it
        if self.TARGET_MODULE in sys.modules:
            self._target_module = sys.modules[self.TARGET_MODULE]
            logger.debug(f'Caching {self.TARGET_MODULE}: already imported.')
            return self._target_module

        # Import it, cache it, and return it
        namespace_segments = self.TARGET_MODULE.split('.')
        if len(namespace_segments) > 1:
            name = namespace_segments[-1]
            package = '.'.join(namespace_segments[:-1])
            logger.debug(f'Trying to import {name} from package {package}')
            self._target_module = import_module(name, package)
        else:
            logger.debug(
                f'Trying to import {self.TARGET_MODULE} from package {package}'
            )
            self._target_module = import_module(self.TARGET_MODULE)
        logger.debug(f'Imported {self.TARGET_MODULE} as {self._target_module}')
        return self._target_module

    @property
    def test_entities(self) -> set[str]:
        """
        Gets the actual test-entities present in the test module.

        Note:
        -----
        This is not actually used by the processes here, but in the
        interests of keeping a consistent interface, and because it's
        expected to be useful later, it was kept in play.
        """
        return set(
            [
                name for name, member
                in inspect.getmembers(self.test_module, inspect.isclass)
                if inspect.isclass(member)
                and issubclass(member, unittest.TestCase)
            ]
        )

    @property
    def test_module(self) -> ModuleType:
        """
        Gets the test-module that the class lives in
        """
        return sys.modules[self.__class__.__module__]

    def test_source_entities_have_test_cases(self):
        logger.debug(f'Source entities .... {self.source_entities}')
        logger.debug(f'Test entities ...... {self.test_entities}')
        logger.debug(f'Target module ...... {self.target_module}')
        logger.debug(f'Test module ........ {self.test_module}')
        logger.debug(f'Test entities ...... {self.test_entities}')
        logger.debug(f'Expected tests ..... {self.expected_test_entities}')
        assert isinstance(self, unittest.TestCase), (
            f'{self.__class__.__name__}.test_source_entities_have_test_cases '
            f'cannot execute because {self.__class__.__name__} is not a '
            f'unittest.TestCase class {self.__class__.__mro__}'
        )
        for test_entity in self.expected_test_entities:
            with self.subTest(msg=f'checking {test_entity}'):

                # Check that it exists in the first place
                test_case = getattr(self.test_module, test_entity, None)
                self.assertTrue(
                    test_case is not None,
                    f'No test-case class named {test_entity} is defined in '
                    f'{self.test_module.__file__.split(os.sep)[-1]}'
                )

                # Check that it's a unittest.TestCase
                self.assertTrue(
                    issubclass(test_case, unittest.TestCase),
                    f'The {test_case.__name__} class is exepcted to be a '
                    'subclass of unittest.TestCase, but is not: '
                    f'{test_case.__mro__}'
                )

                # Check that it's the appropriate pact test-type
                source_name = test_entity[len(self.TEST_PREFIX):]
                source_entity = getattr(self.target_module, source_name, None)
                if inspect.isclass(source_entity):
                    pact_type = ExaminesSourceClass
                else:
                    pact_type = ExaminesSourceFunction
                self.assertTrue(
                    issubclass(test_case, pact_type),
                    f'The {test_case.__name__} class is exepcted to be a '
                    f'subclass of {pact_type.__name__}, but is not: '
                    f'{test_case.__mro__}'
                )


# Module Concrete Classes

# Code to run if the module is executed directly
if __name__ == '__main__':
    pass

    class test_pact_projects_temp(ExaminesModuleMembers, unittest.TestCase):
        TARGET_MODULE = 'goblinfish.testing.pact.projects'

    class test_ExaminesProjectModules(unittest.TestCase, ExaminesSourceClass):
        pass

    class test_temp_function(unittest.TestCase, ExaminesSourceFunction):
        pass

    inst = test_pact_projects_temp()
    inst.test_source_entities_have_test_cases()
