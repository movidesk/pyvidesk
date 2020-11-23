import unittest

from pyvidesk.exceptions import (
    PyvideskPropertyNotValidError,
    PyvideskPropertyWithWrongType,
    PyvideskWrongKwargError,
)

from pyvidesk.tickets import Tickets
from tests.config import TOKEN


class TestEntity(unittest.TestCase):
    """Classe que testa a classe Tickets"""

    tickets = Tickets(token=TOKEN)
    properties = tickets.get_properties()

    def test_raise_wrong_property_error(self):
        def _test_raise_wrong_property_error():
            self.tickets.get_by_name("")

        self.assertRaises(
            PyvideskPropertyNotValidError,
            _test_raise_wrong_property_error,
        )

    def test_raise_property_with_wrong_type_error(self):
        def _test_raise_property_with_wrong_type():
            self.tickets.get_by_id("1")

        self.assertRaises(
            PyvideskPropertyWithWrongType,
            _test_raise_property_with_wrong_type,
        )

    def test_raise_wrong_kwarg_error(self):
        def _test_raise_wrong_kwarg_error():
            self.tickets.get_by_id(1, limit=10)

        self.assertRaises(
            PyvideskWrongKwargError,
            _test_raise_wrong_kwarg_error,
        )

    def test_raise_query_options_with_wrong_type_error(self):
        def _test_raise_query_options_with_wrong_type_error():
            self.tickets.get_by_id(1, top="10")

        self.assertRaises(
            PyvideskPropertyWithWrongType,
            _test_raise_query_options_with_wrong_type_error,
        )
