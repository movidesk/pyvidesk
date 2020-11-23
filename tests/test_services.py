import unittest

from pyvidesk import properties
from pyvidesk.services import Services
from tests.config import TOKEN


class TestServices(unittest.TestCase):
    """Classe que testa a classe Persons"""

    services = Services(token=TOKEN)
    properties = services.get_properties()

    def test_property_id(self):
        prop = self.properties["id"]
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "id")
        self.assertEqual(
            prop.get_description(),
            "Campo Identificador único do serviço (somente leitura).",
        )

    def test_property_name(self):
        prop = self.properties["name"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "name")
        self.assertEqual(
            prop.get_description(),
            ("Campo Nome do serviço."),
        )

    def test_property_description(self):
        prop = self.properties["description"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "description")
        self.assertEqual(
            prop.get_description(),
            ("Campo descrição."),
        )

    def test_property_parentServiceId(self):
        prop = self.properties["parentServiceId"]
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "parentServiceId")
        self.assertEqual(
            prop.get_description(),
            ("Campo id que representa o serviço pai."),
        )

    def test_property_serviceForTicketType(self):
        prop = self.properties["serviceForTicketType"]
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "serviceForTicketType")
        self.assertEqual(
            prop.get_description(),
            (
                "Disponível para tickets do tipo. Público= 0, Interno = 1, Públicos e internos = 2."
            ),
        )

    def test_property_isVisible(self):
        prop = self.properties["isVisible"]
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "isVisible")
        self.assertEqual(
            prop.get_description(),
            ("Visível para: Agente = 1, Cliente = 2, Agente e Cliente = 3."),
        )

    def test_property_allowSelection(self):
        prop = self.properties["allowSelection"]
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "allowSelection")
        self.assertEqual(
            prop.get_description(),
            ("Permitir a seleção para: Agente = 1, Cliente = 2, Agente e Cliente = 3."),
        )

    def test_property_allowFinishTicket(self):
        prop = self.properties["allowFinishTicket"]
        self.assertIsInstance(prop, properties.BooleanProperty)
        self.assertEqual(prop.full_name, "allowFinishTicket")
        self.assertEqual(
            prop.get_description(),
            (
                "Ao desmarcar esse parâmetro o ticket não poderá ser concluído "
                "se estiver com este item selecionado. O agente precisa escolher "
                "um novo item antes de efetuar a conclusão do ticket."
            ),
        )

    def test_property_isActive(self):
        prop = self.properties["isActive"]
        self.assertIsInstance(prop, properties.BooleanProperty)
        self.assertEqual(prop.full_name, "isActive")
        self.assertEqual(
            prop.get_description(),
            (
                "Serviços desabilitados não estarão visíveis para a seleção dentro dos tickets. "
                "Desmarque essa opção caso queira que o serviço não esteja mais disponível "
                "no sistema."
            ),
        )

    def test_property_automationMacro(self):
        prop = self.properties["automationMacro"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "automationMacro")
        self.assertEqual(
            prop.get_description(),
            (
                "Nome da macro que deverá ser executada automaticamente ao selecionar o serviço."
            ),
        )

    def test_property_defaultCategory(self):
        prop = self.properties["defaultCategory"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "defaultCategory")
        self.assertEqual(
            prop.get_description(),
            (
                "Nome da categoria que deverá aparecer como padrão ao "
                "selecionar o serviço no ticket."
            ),
        )

    def test_property_defaultUrgency(self):
        prop = self.properties["defaultUrgency"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "defaultUrgency")
        self.assertEqual(
            prop.get_description(),
            (
                "Nome da urgência que deverá aparecer como padrão ao "
                "selecionar o serviço no ticket."
            ),
        )

    def test_property_allowAllCategories(self):
        prop = self.properties["allowAllCategories"]
        self.assertIsInstance(prop, properties.BooleanProperty)
        self.assertEqual(prop.full_name, "allowAllCategories")
        self.assertEqual(
            prop.get_description(),
            ("Permite selecionar todas as categorias."),
        )

    def test_property_categories(self):
        prop = self.properties["categories"]
        self.assertIsInstance(prop, properties.ArrayProperty)
        self.assertEqual(prop.full_name, "categories")
        self.assertEqual(
            prop.get_description(),
            (
                "Lista com os nome das categorias do serviço. "
                "Deve ser informado quando o campo allowAllCategories for falso."
            ),
        )
