import unittest

from pyvidesk import Pyvidesk
from pyvidesk.persons import Persons
from pyvidesk.services import Services
from pyvidesk.tickets import Tickets
from tests.config import TOKEN


class TestEntityGetAttr(unittest.TestCase):
    """Classe que testa o método __getattr__ de entity"""

    pyvidesk = Pyvidesk(token=TOKEN)

    def test_pyvidesk_persons_instance_is_Persons_class(self):
        self.assertIsInstance(self.pyvidesk.persons, Persons)

    def test_pyvidesk_tickets_instance_is_Tickets_class(self):
        self.assertIsInstance(self.pyvidesk.tickets, Tickets)

    def test_pyvidesk_services_instance_is_Services_class(self):
        self.assertIsInstance(self.pyvidesk.services, Services)

    def test_get_by_id_Persons_class(self):
        person_id = "346669244"
        person = self.pyvidesk.persons.get_by_id(person_id)
        self.assertEqual(person.id, person_id)

    def test_get_by_id_Persons_class_with_kwarg(self):
        person_id = "346669244"
        person = self.pyvidesk.persons.get_by_id(id=person_id)
        self.assertEqual(person.id, person_id)

    def test_get_by_id_Persons_class_with_select(self):
        person_id = "346669244"
        select_values = ("id", "businessName", "userName")
        person = self.pyvidesk.persons.get_by_id(person_id, select=select_values)
        self.assertEqual(person.id, person_id)
        self.assertTrue(all(key in select_values for key in person._properties))

    def test_get_by_id_Persons_class_with_kwarg_with_select(self):
        person_id = "346669244"
        select_values = ("id", "businessName", "userName")
        person = self.pyvidesk.persons.get_by_id(id=person_id, select=select_values)
        self.assertEqual(person.id, person_id)
        self.assertTrue(all(key in select_values for key in person._properties))

    def test_get_by_getattr_Persons_class(self):
        result = self.pyvidesk.persons.get_by_isActive(True).as_url()
        expected = self.pyvidesk.persons.api.base_url + "&$filter=isActive eq true"
        self.assertEqual(result, expected)

    def test_get_by_getattr_Persons_class_with_kwarg(self):
        result = self.pyvidesk.persons.get_by_isActive(isActive=True).as_url()
        expected = self.pyvidesk.persons.api.base_url + "&$filter=isActive eq true"
        self.assertEqual(result, expected)

    def test_get_by_getattr_Persons_class_with_select_as_str(self):
        select_values = "businessName"
        result = self.pyvidesk.persons.get_by_isActive(
            True, select=select_values
        ).as_url()
        expected = (
            self.pyvidesk.persons.api.base_url
            + "&$select=businessName&$filter=isActive eq true"
        )
        self.assertEqual(result, expected)

    def test_get_by_getattr_Persons_class_with_select_as_property(self):
        select_values = self.pyvidesk.persons.get_properties()["businessName"]
        result = self.pyvidesk.persons.get_by_isActive(
            True, select=select_values
        ).as_url()
        expected = (
            self.pyvidesk.persons.api.base_url
            + "&$select=businessName&$filter=isActive eq true"
        )
        self.assertEqual(result, expected)

    def test_get_by_getattr_Persons_class_with_select_as_iterable_of_str(self):
        select_values = ("id", "businessName", "userName", "isActive")
        result = self.pyvidesk.persons.get_by_isActive(
            True, select=select_values
        ).as_url()
        expected = (
            self.pyvidesk.persons.api.base_url
            + "&$select=id,businessName,userName,isActive&$filter=isActive eq true"
        )
        self.assertEqual(result, expected)

    def test_get_by_getattr_Persons_class_with_select_as_iterable_of_properties(self):
        """Teste com select como uma tupla de propriedades"""
        properties = self.pyvidesk.persons.get_properties()
        select_values = (
            properties["id"],
            properties["businessName"],
            properties["userName"],
            properties["isActive"],
        )
        result = self.pyvidesk.persons.get_by_isActive(
            True, select=select_values
        ).as_url()
        expected = (
            self.pyvidesk.persons.api.base_url
            + "&$select=id,businessName,userName,isActive&$filter=isActive eq true"
        )
        self.assertEqual(result, expected)

    def test_getattr_Persons_class_with_kwarg_with_select_as_iterable_of_strings(self):
        select_values = ("id", "businessName", "userName", "isActive")
        result = self.pyvidesk.persons.get_by_isActive(
            isActive=True, select=select_values
        ).as_url()
        expected = (
            self.pyvidesk.persons.api.base_url
            + "&$select=id,businessName,userName,isActive&$filter=isActive eq true"
        )
        self.assertEqual(result, expected)

    def test_getattr_Persons_class_with_top(self):
        result = self.pyvidesk.persons.get_by_isActive(True, top=100).as_url()
        expected = (
            self.pyvidesk.persons.api.base_url + "&$top=100&$filter=isActive eq true"
        )
        self.assertEqual(result, expected)

    def test_getattr_Persons_class_with_skip(self):
        result = self.pyvidesk.persons.get_by_isActive(True, skip=100).as_url()
        expected = (
            self.pyvidesk.persons.api.base_url + "&$skip=100&$filter=isActive eq true"
        )
        self.assertEqual(result, expected)

    def test_getattr_Persons_class_with_top_with_select(self):
        select_values = ("id", "businessName", "userName", "isActive")
        result = self.pyvidesk.persons.get_by_isActive(
            True, top=100, select=select_values
        ).as_url()
        expected = (
            self.pyvidesk.persons.api.base_url
            + "&$top=100&$select=id,businessName,userName,isActive&$filter=isActive eq true"
        )
        self.assertEqual(result, expected)

    def test_getattr_Persons_class_with_top_with_select_with_skip(
        self,
    ):
        """Teste com select, top e skip"""
        select_values = ("id", "businessName", "userName", "isActive")
        result = self.pyvidesk.persons.get_by_isActive(
            True, top=100, skip=40, select=select_values
        ).as_url()
        expected = self.pyvidesk.persons.api.base_url + (
            "&$top=100&$skip=40"
            "&$select=id,businessName,userName,isActive"
            "&$filter=isActive eq true"
        )
        self.assertEqual(result, expected)

    def test_get_by_id_Tickets_class(self):
        ticket_id = 3
        ticket = self.pyvidesk.tickets.get_by_id(ticket_id)
        # TODO: olhar o arquivo tickets.py
        self.assertEqual(int(ticket.id), ticket_id)

    def test_get_by_id_Tickets_class_with_kwarg(self):
        ticket_id = 3
        ticket = self.pyvidesk.tickets.get_by_id(id=ticket_id)
        # TODO: olhar o arquivo tickets.py
        self.assertEqual(int(ticket.id), ticket_id)

    def test_get_by_id_Tickets_class_with_select(self):
        ticket_id = 3
        select_values = ("id", "subject", "createdDate")
        ticket = self.pyvidesk.tickets.get_by_id(ticket_id, select=select_values)
        self.assertEqual(ticket.id, ticket_id)
        self.assertTrue(all(key in select_values for key in ticket._properties))

    def test_get_by_id_Tickets_class_with_kwarg_with_select(self):
        ticket_id = 3
        select_values = ("id", "subject", "createdDate")
        ticket = self.pyvidesk.tickets.get_by_id(id=ticket_id, select=select_values)
        self.assertEqual(ticket.id, ticket_id)
        self.assertTrue(all(key in select_values for key in ticket._properties))

    def test_get_by_getattr_Tickets_class(self):
        result = self.pyvidesk.tickets.get_by_slaSolutionDateIsPaused(True).as_url()
        expected = (
            self.pyvidesk.tickets.api.base_url
            + "&$filter=slaSolutionDateIsPaused eq true"
        )
        self.assertEqual(result, expected)

    def test_get_by_getattr_Tickets_class_with_kwarg(self):
        result = self.pyvidesk.tickets.get_by_slaSolutionDateIsPaused(
            slaSolutionDateIsPaused=True
        ).as_url()
        expected = (
            self.pyvidesk.tickets.api.base_url
            + "&$filter=slaSolutionDateIsPaused eq true"
        )
        self.assertEqual(result, expected)

    def test_get_by_getattr_Tickets_class_with_select_as_str(self):
        select_values = "subject"
        result = self.pyvidesk.tickets.get_by_slaSolutionDateIsPaused(
            True, select=select_values
        ).as_url()
        expected = (
            self.pyvidesk.tickets.api.base_url
            + "&$select=subject&$filter=slaSolutionDateIsPaused eq true"
        )
        self.assertEqual(result, expected)

    def test_get_by_getattr_Tickets_class_with_select_as_property(self):
        select_values = self.pyvidesk.tickets.get_properties()["subject"]
        result = self.pyvidesk.tickets.get_by_slaSolutionDateIsPaused(
            True, select=select_values
        ).as_url()
        expected = (
            self.pyvidesk.tickets.api.base_url
            + "&$select=subject&$filter=slaSolutionDateIsPaused eq true"
        )
        self.assertEqual(result, expected)

    def test_get_by_getattr_Tickets_class_with_select_as_iterable_of_str(self):
        """
        Teste quando select é uma tupla de strings.
        """
        select_values = ("id", "subject", "createdDate", "slaSolutionDateIsPaused")
        result = self.pyvidesk.tickets.get_by_slaSolutionDateIsPaused(
            True, select=select_values
        ).as_url()
        expected = (
            self.pyvidesk.tickets.api.base_url
            + "&$select=id,subject,createdDate,slaSolutionDateIsPaused"
            + "&$filter=slaSolutionDateIsPaused eq true"
        )
        self.assertEqual(result, expected)

    def test_get_by_getattr_Tickets_class_with_select_as_iterable_of_properties(self):
        """Teste com select como uma tupla de propriedades"""
        properties = self.pyvidesk.tickets.get_properties()
        select_values = (
            properties["id"],
            properties["subject"],
            properties["createdDate"],
            properties["slaSolutionDateIsPaused"],
        )
        result = self.pyvidesk.tickets.get_by_slaSolutionDateIsPaused(
            True, select=select_values
        ).as_url()
        expected = (
            self.pyvidesk.tickets.api.base_url
            + "&$select=id,subject,createdDate,slaSolutionDateIsPaused"
            + "&$filter=slaSolutionDateIsPaused eq true"
        )
        self.assertEqual(result, expected)

    def test_getattr_Tickets_class_with_kwarg_with_select_as_iterable_of_strings(self):
        """
        Teste quando select é uma tupla de strings e há um kwarg para o parametro principal.
        """
        select_values = ("id", "subject", "createdDate", "slaSolutionDateIsPaused")
        result = self.pyvidesk.tickets.get_by_slaSolutionDateIsPaused(
            slaSolutionDateIsPaused=True, select=select_values
        ).as_url()
        expected = (
            self.pyvidesk.tickets.api.base_url
            + "&$select=id,subject,createdDate,slaSolutionDateIsPaused"
            + "&$filter=slaSolutionDateIsPaused eq true"
        )
        self.assertEqual(result, expected)

    def test_getattr_Tickets_class_with_top(self):
        result = self.pyvidesk.tickets.get_by_slaSolutionDateIsPaused(
            True, top=100
        ).as_url()
        expected = (
            self.pyvidesk.tickets.api.base_url
            + "&$top=100&$filter=slaSolutionDateIsPaused eq true"
        )
        self.assertEqual(result, expected)

    def test_getattr_Tickets_class_with_skip(self):
        result = self.pyvidesk.tickets.get_by_slaSolutionDateIsPaused(
            True, skip=100
        ).as_url()
        expected = (
            self.pyvidesk.tickets.api.base_url
            + "&$skip=100&$filter=slaSolutionDateIsPaused eq true"
        )
        self.assertEqual(result, expected)

    def test_getattr_Tickets_class_with_top_with_select(self):
        """
        Teste quando select é e top são utilizados.
        """
        select_values = ("id", "subject", "createdDate", "slaSolutionDateIsPaused")
        result = self.pyvidesk.tickets.get_by_slaSolutionDateIsPaused(
            True, top=100, select=select_values
        ).as_url()
        expected = (
            self.pyvidesk.tickets.api.base_url
            + "&$top=100&$select=id,subject,createdDate,slaSolutionDateIsPaused"
            + "&$filter=slaSolutionDateIsPaused eq true"
        )
        self.assertEqual(result, expected)

    def test_getattr_Tickets_class_with_top_with_select_with_skip(
        self,
    ):
        """Teste com select, top e skip"""
        select_values = ("id", "subject", "createdDate", "slaSolutionDateIsPaused")
        result = self.pyvidesk.tickets.get_by_slaSolutionDateIsPaused(
            True, top=100, skip=40, select=select_values
        ).as_url()
        expected = self.pyvidesk.tickets.api.base_url + (
            "&$top=100&$skip=40"
            "&$select=id,subject,createdDate,slaSolutionDateIsPaused"
            "&$filter=slaSolutionDateIsPaused eq true"
        )
        self.assertEqual(result, expected)
