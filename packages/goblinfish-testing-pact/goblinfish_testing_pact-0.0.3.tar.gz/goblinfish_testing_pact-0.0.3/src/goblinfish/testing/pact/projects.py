#!/usr/bin/env python3.11
"""
Provides classes and functionality to seek out and verify the presence
of test-modules that directly correspond, by name, with souorce modules
in a Python project.

Environment:
------------
PACT_LOG_LEVEL : The logging-level to

Logging:
--------
"""

from __future__ import annotations

# Built-In Imports
import os
import sys
import unittest

from collections import namedtuple
from pathlib import Path

# Third-Party Imports

# Path Manipulations (avoid these!) and "Local" Imports
from goblinfish.testing.pact.abcs import HasSourceAndTestEntities
from goblinfish.testing.pact.pact_logging import logger

# Module "Constants" and Other Attributes
ProjectRootFiles = namedtuple('ProjectRootFiles', ['Pipenv', 'PyProject'])(
    Pipenv=set(['Pipfile', 'Pipfile.lock']),
    PyProject=set(['pyproject.toml']),
)

# Module Exceptions

# Module Functions

# Module Metaclasses


# Module Abstract Base Classes
class ExaminesProjectModules(HasSourceAndTestEntities):
    """
    A mix-in "abstract" class that provides a test-method that tests for
    test-modules that correlate on a one-to-one basis with modules in a
    project's source directory.

    Class Variables/Attributes:
    ---------------------------
    SOURCE_DIR : Path [fragment, defaults to Path('src')]
        The path under the project root where the project's source
        modules and packages are located.
    TEST_DIR : Path [fragment, defaults to Path('tests') / 'unit']
        The path under the project root where the project's unit test
        suite is located.
    TEST_PREFIX : str [defaults to 'test_']
        The string that is used to prefix all test-module names in the
        test suite that the test-case class lives in.
    """

    SOURCE_DIR = Path('src')
    TEST_DIR = Path('tests') / 'unit'
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
    def project_root(self) -> Path:
        f"""
        Gets and caches the project root directory that the parent class
        lives in, by looking for known file-names by project type:
        {ProjectRootFiles}
        """
        # If we've already found the project root, return it
        if getattr(self, '_project_root', None) is not None:
            return self._project_root

        # Otherwise go looking for it
        local_file = sys.modules[self.__class__.__module__].__file__
        current_path = Path(local_file).parent
        root = current_path.root

        # Walk from the file that the class lives in up the file-system,
        # looking for matching files from ProjectRootFiles
        project_files_items = ProjectRootFiles._asdict().items()
        while str(current_path) != str(root):
            logger.debug(f'Checking {current_path}')
            current_files = set([f.name for f in current_path.glob('*')])
            logger.debug(current_files)
            for name, files in project_files_items:
                if files.intersection(current_files) == files:
                    logger.info(
                        f'Found {name} project structure files '
                        f'{tuple(files)} at {current_path}: '
                        'Assuming that is project root'
                    )
                    self._project_root = current_path
                    return self._project_root
            current_path = current_path.parent
        raise RuntimeError(
            f'{self.__class__.__name__}.project_root could not find a '
            'project root directory using the expected files in '
            f'{ProjectRootFiles}'
        )

    @property
    def source_dir(self) -> Path:
        """
        Gets the source directory
        """
        return self.project_root / self.SOURCE_DIR

    @property
    def source_entities(self) -> set[str]:
        """
        Gets the actual entities present in the source target
        """
        source_dir = str(self.source_dir)
        return set(
            [
                str(f)[len(source_dir) + 1:]
                for f in self.source_dir.glob('**/*.py')
            ]
        )

    @property
    def test_dir(self) -> Path:
        """
        Gets the test directory
        """
        return self.project_root / self.TEST_DIR

    @property
    def test_entities(self) -> set[str]:
        """
        Gets the actual entities present in the test target
        """
        test_dir = str(self.test_dir)
        return set(
            [
                str(f)[len(test_dir) + 1:]
                for f in self.test_dir.glob('**/*.py')
            ]
        )

    def test_source_modules_have_test_modules(self):
        """Test that source modules have corresponding test-modules"""
        logger.debug(f'Source directory ... {self.source_dir}')
        logger.debug(f'Test directory ..... {self.test_dir}')
        logger.debug(f'Source modules ..... {self.source_entities}')
        logger.debug(f'Test modules ....... {self.test_entities}')
        logger.debug(f'Expected tests ..... {self.expected_test_entities}')
        assert isinstance(self, unittest.TestCase), (
            f'{self.__class__.__name__}.test_source_modules_have_test_modules '
            f'cannot execute because {self.__class__.__name__} is not a '
            f'unittest.TestCase class {self.__class__.__mro__}'
        )
        for expected in self.expected_test_entities:
            with self.subTest(msg=f'Expecting {expected} test-module'):
                expected_path = self.test_dir / expected
                self.assertTrue(
                    expected_path.exists(),
                    f'The expected test-module at {expected} does not exist'
                )


# Code to run if the module is executed directly
if __name__ == '__main__':
    pass
