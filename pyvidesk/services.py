"""
Módulo de definições da entidade Services do Movidesk.
Para uma descrição da entidade:

>>> from pyvidesk.services import Services

>>> services = Services(token="my_token")
>>> services.describe()
"""

from urllib.parse import urljoin

from .config import MAIN_URL
from .entity import Entity
from .properties import ArrayProperty, BooleanProperty, IntegerProperty, StringProperty

PARAMS = {
    "id": {
        "property": IntegerProperty,
        "description": "Campo Identificador único do serviço (somente leitura).",
        "readOnly": True,
    },
    "name": {
        "property": StringProperty,
        "description": "Campo Nome do serviço.",
        "readOnly": False,
    },
    "description": {
        "property": StringProperty,
        "description": "Campo descrição.",
        "readOnly": False,
    },
    "parentServiceId": {
        "property": IntegerProperty,
        "description": "Campo id que representa o serviço pai.",
        "readOnly": False,
    },
    "serviceForTicketType": {
        "property": IntegerProperty,
        "description": (
            "Disponível para tickets do tipo. Público= 0, Interno = 1, Públicos e internos = 2."
        ),
        "readOnly": False,
    },
    "isVisible": {
        "property": IntegerProperty,
        "description": "Visível para: Agente = 1, Cliente = 2, Agente e Cliente = 3.",
        "readOnly": False,
    },
    "allowSelection": {
        "property": IntegerProperty,
        "description": (
            "Permitir a seleção para: Agente = 1, Cliente = 2, Agente e Cliente = 3."
        ),
        "readOnly": False,
    },
    "allowFinishTicket": {
        "property": BooleanProperty,
        "description": (
            "Ao desmarcar esse parâmetro o ticket não poderá ser concluído se estiver com "
            "este item selecionado. O agente precisa escolher um novo item antes de efetuar "
            "a conclusão do ticket."
        ),
        "readOnly": False,
    },
    "isActive": {
        "property": BooleanProperty,
        "description": (
            "Serviços desabilitados não estarão visíveis para a seleção dentro dos tickets. "
            "Desmarque essa opção caso queira que o serviço não esteja mais disponível no sistema."
        ),
        "readOnly": False,
    },
    "automationMacro": {
        "property": StringProperty,
        "description": (
            "Nome da macro que deverá ser executada automaticamente ao selecionar o serviço."
        ),
        "readOnly": False,
    },
    "defaultCategory": {
        "property": StringProperty,
        "description": (
            "Nome da categoria que deverá aparecer como padrão ao selecionar o serviço no ticket."
        ),
        "readOnly": False,
    },
    "defaultUrgency": {
        "property": StringProperty,
        "description": (
            "Nome da urgência que deverá aparecer como padrão ao selecionar o serviço no ticket."
        ),
        "readOnly": False,
    },
    "allowAllCategories": {
        "property": BooleanProperty,
        "description": "Permite selecionar todas as categorias.",
        "readOnly": False,
    },
    "categories": {
        "property": ArrayProperty,
        "description": (
            "Lista com os nome das categorias do serviço. Deve ser informado quando "
            "o campo allowAllCategories for falso."
        ),
        "readOnly": False,
    },
}


class Services(Entity):
    BASE_URL = urljoin(MAIN_URL, "services")
    VALID_PARAMS = PARAMS
