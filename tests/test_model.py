from datetime import datetime, date
import unittest

from pyvidesk.exceptions import (
    PyvideskBadResponseError,
    PyvideskCannotSetReadOnlyProperty,
    PyvideskPropertyNotValidError,
    PyvideskRequestsError,
    PyvideskSaveWithoutIdError,
)
from pyvidesk import Pyvidesk
from tests.config import TOKEN


class TestModel(unittest.TestCase):
    """Classe que testa a classe Model"""

    pyvidesk = Pyvidesk(token=TOKEN)

    def test_raise_save_without_id_error(self):
        def _test_raise_save_without_id_error():
            now = datetime.now()
            ticket = self.pyvidesk.tickets.get_by_id(3, select="subject")
            ticket.createdDate = now
            ticket.save()

        self.assertRaises(
            PyvideskSaveWithoutIdError,
            _test_raise_save_without_id_error,
        )

    def test_raise_change_readonly_property_error(self):
        def _test_raise_change_readonly_property_error():
            ticket = self.pyvidesk.tickets.get_by_id(3)
            ticket.id = 4

        self.assertRaises(
            PyvideskCannotSetReadOnlyProperty,
            _test_raise_change_readonly_property_error,
        )

    def test_return_None_for_property_not_select_in_query(self):
        ticket = self.pyvidesk.tickets.get_by_id(3, select="subject")
        self.assertIsNone(ticket.id)

    def test_raise_get_property_that_does_not_belong_to_entity(self):
        def _test_raise_get_property_that_does_not_belong_to_entity():
            ticket = self.pyvidesk.tickets.get_by_id(3)
            return ticket.businessName

        self.assertRaises(
            PyvideskPropertyNotValidError,
            _test_raise_get_property_that_does_not_belong_to_entity,
        )

    def test_serialize_change_property(self):
        ticket = self.pyvidesk.tickets.get_by_id(3)
        ticket_properties = ticket.get_properties()
        now = datetime.now()
        ticket.createdDate = now
        result = ticket._serialize_all_changes()
        expected = {"createdDate": ticket_properties["createdDate"].serialize(now)}
        self.assertDictEqual(result, expected)

    def test_change_property(self):
        ticket_id = 1  # TODO: Mudar o ID
        ticket = self.pyvidesk.tickets.get_by_id(ticket_id)
        now = datetime.now()
        ticket.createdDate = now
        ticket.save()
        _ticket = self.pyvidesk.tickets.get_by_id(ticket_id)
        self.assertEqual(_ticket.createdDate, now)

    def test_serialize_change_complex_property(self):
        """
        Teste de serialização de mudança numa propriedade complexa.
        """
        ticket = self.pyvidesk.tickets.get_by_id(3)
        for action in ticket.actions:
            action.description = "Teste"

        result = {
            action["description"]
            for action in ticket._serialize_all_changes()["actions"]
        }
        expected = {"Teste"}
        self.assertSetEqual(result, expected)

    def test_change_complex_property(self):
        """
        Teste de mudança numa propriedade complexa.
        """
        ticket_id = 1  # TODO: Mudar o ID
        ticket = self.pyvidesk.tickets.get_by_id(ticket_id)
        for action in ticket.actions:
            action.description = "Teste"
        ticket.save()

        _ticket = self.pyvidesk.tickets.get_by_id(ticket_id)
        result = {action.description for action in _ticket.actions}
        expected = {"Teste"}
        self.assertEqual(result, expected)

    def test_serialize_change_nested_complex_property(self):
        """
        Teste de serialização de mudança numa propriedade complexa que
        tem como "pai" outra propriedade complexa.
        """
        ticket = self.pyvidesk.tickets.get_by_id(3)
        ticket_properties = ticket.get_properties()
        today = date.today()
        for action in ticket.actions:
            for appointment in action.timeAppointments:
                appointment.date = today

        result = {
            appointment["date"]
            for action in ticket._serialize_all_changes()["actions"]
            for appointment in action["timeAppointments"]
        }
        expected = {ticket_properties["createdDate"].serialize(today)}
        self.assertSetEqual(result, expected)

    def test_change_nested_complex_property(self):
        """
        Teste de mudança numa propriedade complexa que
        tem como "pai" outra propriedade complexa.
        """
        ticket_id = 1  # TODO: Mudar o ID
        ticket = self.pyvidesk.tickets.get_by_id(ticket_id)
        today = date.today()
        for action in ticket.actions:
            for appointment in action.timeAppointments:
                appointment.date = today
        ticket.save()

        _ticket = self.pyvidesk.tickets.get_by_id(ticket_id)
        result = {
            appointment.date
            for action in _ticket.actions
            for appointment in action.timeAppointments
        }
        expected = {today}
        self.assertSetEqual(result, expected)

    def test_serialize_read_only_property_in_empty_model(self):
        ticket = self.pyvidesk.tickets.get_empty_model()
        ticket_properties = ticket.get_properties()
        ticket.createdBy.id = "1"
        result = ticket._serialize_all_changes()
        expected = {
            "createdBy": {"id": ticket_properties["createdBy"].id.serialize("1")}
        }
        self.assertDictEqual(result, expected)

    def test_serialize_multiple_properties_in_empty_model(self):
        """
        Teste quando setamos múltiplas propriedades num modelo vazio.
        """
        ticket = self.pyvidesk.tickets.get_empty_model()
        ticket_properties = ticket.get_properties()
        ticket.subject = "Assunto"
        ticket.type = 1
        ticket.serviceFirstLevelId = 190853
        ticket.createdBy.id = "2263751"
        ticket.clients = [{"id": "917910092"}]
        ticket.actions = [{"description": "Descrição", "type": 1}]
        ticket.ownerTeam = "Administradores"
        ticket.owner.id = "2222"

        result = ticket._serialize_all_changes()
        expected = {
            "subject": ticket_properties["subject"].serialize("Assunto"),
            "type": ticket_properties["type"].serialize(1),
            "serviceFirstLevelId": ticket_properties["serviceFirstLevelId"].serialize(
                190853
            ),
            "createdBy": {"id": ticket_properties["createdBy"].id.serialize("2263751")},
            "clients": [{"id": ticket_properties["clients"].id.serialize("917910092")}],
            "actions": [
                {
                    "description": ticket_properties["actions"].description.serialize(
                        "Descrição"
                    ),
                    "type": ticket_properties["actions"].type.serialize(1),
                }
            ],
            "ownerTeam": ticket_properties["ownerTeam"].serialize("Administradores"),
            "owner": {"id": ticket_properties["owner"].id.serialize("2222")},
        }

        self.assertDictEqual(result, expected)

    def test_raise_when_try_to_create_whitout_all_properties_seted(self):
        def _test_raise_when_try_to_create_whitout_all_properties_seted():
            empty_ticket = self.pyvidesk.tickets.get_empty_model()
            empty_ticket.subject = "Assunto"
            empty_ticket.create()

        self.assertRaises(
            PyvideskBadResponseError,
            _test_raise_when_try_to_create_whitout_all_properties_seted,
        )

    def test_create_ticket(self):
        """
        Teste de criação de um ticket.
        """
        ticket = self.pyvidesk.tickets.get_empty_model()
        ticket.subject = "Assunto"
        ticket.type = 1
        ticket.serviceFirstLevelId = 190853
        ticket.createdBy.id = "2263751"
        ticket.clients = [{"id": "917910092"}]
        ticket.actions = [{"description": "Descrição", "type": 1}]
        ticket.ownerTeam = "Administradores"
        ticket.owner.id = "2222"
        ticket.create()

        self.assertEqual(ticket.subject, "Assunto")
        self.assertEqual(ticket.type, 1)
        self.assertEqual(ticket.serviceFirstLevelId, 190853)
        self.assertEqual(ticket.createdBy.id, "2263751")
        self.assertListEqual(ticket.clients, [{"id": "917910092"}])
        self.assertListEqual(ticket.actions, [{"description": "Descrição", "type": 1}])
        self.assertEqual(ticket.ownerTeam, "Administradores")
        self.assertEqual(ticket.owner.id, "2222")
        self.assertIsNotNone(ticket.id)

    def test_raise_delete_ticket(self):
        def _test_raise_delete_ticket():
            ticket = self.pyvidesk.tickets.get_by_id(3)
            ticket.delete()

        self.assertRaises(PyvideskRequestsError, _test_raise_delete_ticket)

    def test_create_person(self):
        """
        Teste de criação de uma pessoa.
        """
        person = self.pyvidesk.persons.get_empty_model()
        person.personType = 2
        person.profileType = 2
        person.businessName = "Meu nome"
        created_person = person.create()

        self.assertEqual(created_person.personType, 2)
        self.assertEqual(created_person.profileType, 2)
        self.assertEqual(created_person.businessName, "Meu nome")
        self.assertIsNotNone(created_person.id)

    def test_delete_person(self):
        def _test_delete_person(person_id):
            self.pyvidesk.persons.get_by_id(person_id)

        person_id = "1"  # TODO: Mudar o ID
        person = self.pyvidesk.persons.get_by_id(person_id)
        person.delete()
        self.assertRaises(PyvideskBadResponseError, _test_delete_person, person_id)

    def test_create_service(self):
        service = self.pyvidesk.services.get_empty_model()
        service.name = "Meu nome"
        service.create()

        self.assertEqual(service.name, "Meu nome")
        self.assertIsNotNone(service.id)

    def test_delete_service(self):
        def _test_delete_service(service_id):
            self.pyvidesk.services.get_by_id(service_id)

        service_id = 1  # TODO: Mudar o ID
        service = self.pyvidesk.services.get_by_id(service_id)
        service.delete()
        self.assertRaises(PyvideskBadResponseError, _test_delete_service, service_id)
