# -*- coding: utf-8 -*-
"""Unit tests for logging import from pyjstat."""

# Dependencies
import logging
import unittest

# Class to be tested
from pyjstat import pyjstat


class TestPyjstat(unittest.TestCase):
    """Unit tests for logging import from pyjstat."""

    def setUp(self):
        """
        Set up test environment.

        Remove all handlers associated with the root logger object
        and set default log level.
        """
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        logging.basicConfig(level=logging.ERROR)

    def test_import(self):
        """Check log level for root and child logger instances."""
        self.assertEqual(
            logging.getLogger('pyjstat.pyjstat').getEffectiveLevel(),
            logging.INFO
            )
        self.assertEqual(
            logging.getLogger().getEffectiveLevel(),
            logging.ERROR)
