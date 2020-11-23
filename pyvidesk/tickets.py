# pylint: disable=too-many-lines
"""
Módulo de definições da entidade Tickets do Movidesk.
Para uma descrição da entidade:

>>> from pyvidesk.tickets import Tickets

>>> tickets = Tickets(token="my_token")
>>> tickets.describe()
"""


from dataclasses import dataclass, field
from urllib.parse import urljoin

from .config import MAIN_URL
from .entity import Entity
from .properties import (
    ArrayProperty,
    BooleanProperty,
    ComplexProperty,
    CustomFieldValues,
    DatetimeProperty,
    DecimalProperty,
    FloatProperty,
    IntegerProperty,
    StringProperty,
    TimeProperty,
)


@dataclass
class TicketPerson(ComplexProperty):
    """Classe que representa uma pessoa, vista nos dados do ticket"""

    properties: dict = field(
        default_factory=lambda: {
            "id": {
                "property": StringProperty,
                "description": (
                    "Id (Cod. ref.) da organização (Somente leitura, entretanto para "
                    "'ticket.clients[n].organization' esse campo é configurável)."
                ),
                "readOnly": True,
            },
            "businessName": {
                "property": StringProperty,
                "description": ("Nome da organização (Somente leitura)."),
                "readOnly": True,
            },
            "email": {
                "property": StringProperty,
                "description": ("E-mail principal da organização (Somente leitura)."),
                "readOnly": True,
            },
            "phone": {
                "property": StringProperty,
                "description": ("Telefone principal da organização (Somente leitura)."),
                "readOnly": True,
            },
            "personType": {
                "property": IntegerProperty,
                "description": (
                    "Tipo da pessoa: Pessoa = 1, Empresa = 2, Departamento = 4 (Somente leitura)."
                ),
                "readOnly": True,
            },
            "profileType": {
                "property": IntegerProperty,
                "description": (
                    "Perfil da pessoa: Agente = 1, Cliente = 2, Agente e Cliente = 3 "
                    "(Somente leitura)."
                ),
                "readOnly": True,
            },
        }
    )


@dataclass
class CreatedByTeam(ComplexProperty):
    """
    Tickets » Ações » Apontamentos de horas >> Time

    Classe que representa o time de quem gerou o apontamento de horas de uma ação.
    """

    properties: dict = field(
        default_factory=lambda: {
            "id": {
                "property": IntegerProperty,
                "description": ("Id (Cod. ref.) do time (Somente leitura)."),
                "readOnly": True,
            },
            "name": {
                "property": StringProperty,
                "description": ("Nome do time (Somente leitura)."),
                "readOnly": True,
            },
        }
    )


@dataclass
class TimeAppointments(ComplexProperty):
    """
    Tickets » Ações » Apontamentos de horas

    Classe que representa os apontamentos de horas de uma ação.
    """

    alias: type = list
    properties: dict = field(
        default_factory=lambda: {
            "id": {
                "property": IntegerProperty,
                "description": (
                    "Id (Código) do apontamento (Somente leitura). "
                    "*Deve ser informado quando necessário alterar o apontamento já existente."
                ),
                "readOnly": True,
            },
            "activity": {
                "property": StringProperty,
                "description": (
                    "Deve ser uma atividade cadastrada previamente no sistema."
                ),
                "readOnly": False,
            },
            "date": {
                "property": DatetimeProperty,
                "description": (
                    "Deve conter a data com as horas zeradas Ex: 2016-08-24T00:00:00."
                ),
                "readOnly": False,
            },
            "periodStart": {
                "property": TimeProperty,
                "description": (
                    "Período inicial do apontamento. Ex: 08:00:00. "
                    "*Obrigatório quando determinado via parametrização."
                ),
                "readOnly": False,
            },
            "periodEnd": {
                "property": TimeProperty,
                "description": (
                    "Período final do apontamento. Ex: 12:00:00. "
                    "*Obrigatório quando determinado via parametrização."
                ),
                "readOnly": False,
            },
            "workTime": {
                "property": TimeProperty,
                "description": (
                    "Tempo total do apontamento. Ex: 04:00:00. "
                    "*Obrigatório quando determinado via parametrização."
                ),
                "readOnly": False,
            },
            "workTypeName": {
                "property": StringProperty,
                "description": ("Tipo do horário apontado."),
                "readOnly": False,
            },
            "createdBy": {
                "property": TicketPerson,
                "description": ("Dados do gerador do apontamento."),
                "readOnly": True,
            },
            "createdByTeam": {
                "property": CreatedByTeam,
                "description": ("Dados do time do gerador do apontamento."),
                "readOnly": True,
            },
        }
    )


@dataclass
class Expenses(ComplexProperty):
    """
    Tickets » Ações » Despesas

    Classe que representa as despesas de horas de uma ação.
    """

    alias: type = list
    properties: dict = field(
        default_factory=lambda: {
            "id": {
                "property": IntegerProperty,
                "description": ("Campo Identificador único da Despesa."),
                "readOnly": True,
            },
            "type": {
                "property": StringProperty,
                "description": (
                    "Descrição do Tipo de Despesa relacionado ao apontamento."
                ),
                "readOnly": False,
            },
            "serviceReport": {
                "property": StringProperty,
                "description": (
                    "Número do Relatório de Serviço emitido contendo a despesa. Somente Leitura."
                ),
                "readOnly": True,
            },
            "createdBy": {
                "property": StringProperty,
                "description": ("Cod. Ref. da pessoa que apontou a despesa."),
                "readOnly": False,
            },
            "createdByTeam": {
                "property": StringProperty,
                "description": ("Nome da Equipe da pessoa que apontou a despesa."),
                "readOnly": False,
            },
            "date": {
                "property": DatetimeProperty,
                "description": (
                    "Data de criação da pessoa. Deve ser menor ou igual a data atual. "
                    "A data informada deve estar no formato UTC*."
                ),
                "readOnly": False,
            },
            "quantity": {
                "property": IntegerProperty,
                "description": (
                    "Quantidade de apontamento. Obrigatório quando não informado o campo value."
                ),
                "readOnly": False,
            },
            "value": {
                "property": DecimalProperty,
                "description": (
                    "Valor em moeda apontado. Obrigatório quando não informado o campo quantity."
                ),
                "readOnly": False,
            },
        }
    )


@dataclass
class Attachments(ComplexProperty):
    """
    Tickets » Ações » Despesas

    Classe que representa as despesas de horas de uma ação.
    """

    alias: type = list
    properties: dict = field(
        default_factory=lambda: {
            "fileName": {
                "property": StringProperty,
                "description": ("Nome do arquivo enviado (Somente leitura)."),
                "readOnly": True,
            },
            "path": {
                "property": StringProperty,
                "description": ("Hash do arquivo enviado (Somente leitura)."),
                "readOnly": True,
            },
            "createdBy": {
                "property": TicketPerson,
                "description": (
                    "Dados do pessoa que enviou o arquivo (Somente leitura)."
                ),
                "readOnly": True,
            },
            "createdDate": {
                "property": DatetimeProperty,
                "description": (
                    "Data UTC que o arquivo foi enviado (Somente leitura)."
                ),
                "readOnly": True,
            },
        }
    )


@dataclass
class Actions(ComplexProperty):
    """
    Tickets » Ações

    Classe que representa os clientes do ticket.
    """

    alias: type = list
    properties: dict = field(
        default_factory=lambda: {
            "id": {
                "property": IntegerProperty,
                "description": (
                    "Id (Número da ação) (Somente leitura). "
                    "*Deve ser informado quando necessário alterar a ação já existente."
                ),
                "readOnly": True,
            },
            "type": {
                "property": IntegerProperty,
                "description": ("Tipo do ticket: 1 = Interno 2 = Público."),
                "readOnly": False,
            },
            "origin": {
                "property": IntegerProperty,
                "description": (
                    "Origem da ação (Somente leitura)."
                    "\n\t0 First Action"
                    "\n\t1 Via web pelo cliente"
                    "\n\t2 Via web pelo agente"
                    "\n\t3 Recebido via email"
                    "\n\t4 Gatilho do sistema"
                    "\n\t5 Chat (online)"
                    "\n\t6 Chat (offline)"
                    "\n\t7 Email enviado pelo sistema"
                    "\n\t8 Formulário de contato"
                    "\n\t9 Via web API"
                    "\n\t10 Abertura automática de tickets"
                    "\n\t11 Issue integração Jira"
                    "\n\t12 Issue integração Redmine"
                    "\n\t13 Chamada recebida integração Telefonia"
                    "\n\t14 Chamada realizada integração Telefonia"
                    "\n\t15 Chamada perdida integração Telefonia"
                    "\n\t16 Chamada que obteve desistência na fila de espera integração Telefonia"
                    "\n\t17 Acesso remoto"
                    "\n\t18 WhatsApp"
                    "\n\t19 Integração Movidesk"
                    "\n\t20 Integração Zenvia Chat"
                    "\n\t21 Chamada não atendida integração Telefonia"
                ),
                "readOnly": True,
            },
            "description": {
                "property": StringProperty,
                "description": ("Descrição da ação."),
                "readOnly": False,
            },
            "htmlDescription": {
                "property": StringProperty,
                "description": ("Descrição da ação em formato HTML (Somente leitura)."),
                "readOnly": True,
            },
            "status": {
                "property": StringProperty,
                "description": ("Status da ação (Somente leitura)."),
                "readOnly": True,
            },
            "justification": {
                "property": StringProperty,
                "description": ("Justificativa da ação (Somente leitura)."),
                "readOnly": True,
            },
            "createdDate": {
                "property": DatetimeProperty,
                "description": (
                    "Data de criação da ação. A data informada deve estar no formato UTC. "
                    "*Caso não informada, será preenchida com a data atual."
                ),
                "readOnly": False,
            },
            "createdBy": {
                "property": TicketPerson,
                "description": "Dados do gerador da ação.",
                "readOnly": False,
            },
            "isDeleted": {
                "property": BooleanProperty,
                "description": ("Verdadeiro se a ação foi deletada (Somente leitura)."),
                "readOnly": True,
            },
            "tags": {
                "property": ArrayProperty,
                "description": (
                    "Lista de strings com as TAGs as quais a ação esta relacionada. "
                    "Caso sejam informadas TAGs inexistentes, as mesmas serão adicionadas "
                    "na base de dados."
                ),
                "readOnly": False,
            },
            "timeAppointments": {
                "property": TimeAppointments,
                "description": ("Dados dos apontamentos de hora."),
                "readOnly": False,
            },
            "expenses": {
                "property": Expenses,
                "description": ("Dados de despesas."),
                "readOnly": False,
            },
            "attachments": {
                "property": Attachments,
                "description": ("Dados dos anexos (Somente leitura)."),
                "readOnly": True,
            },
        }
    )


@dataclass
class Clients(TicketPerson):
    """
    Tickets » Clientes

    Classe que representa os clientes do ticket.
    """

    alias: type = list

    def __post_init__(self):
        self.properties["organization"] = {
            "property": TicketPerson,
            "description": ("Organização do cliente (Somente leitura)."),
            "readOnly": True,
        }
        self.properties["isDeleted"] = {
            "property": BooleanProperty,
            "description": ("Verdadeiro se o cliente foi deletado (Somente leitura)."),
            "readOnly": True,
        }
        super().__post_init__()


@dataclass
class SubTickets(ComplexProperty):
    """
    Tickets » Tickets Pais/Filhos

    Classe que representa os campos parentTickets e childrenTickets.
    """

    alias: type = list
    properties: dict = field(
        default_factory=lambda: {
            "id": {
                "property": IntegerProperty,
                "description": ("Id (Número) do ticket."),
                "readOnly": True,
            },
            "subject": {
                "property": StringProperty,
                "description": ("Assunto do ticket (Somente leitura)."),
                "readOnly": True,
            },
            "isDeleted": {
                "property": BooleanProperty,
                "description": ("Verdadeiro se foi deletado (Somente leitura)."),
                "readOnly": True,
            },
        }
    )


@dataclass
class TicketHistory(ComplexProperty):
    """Classe que representa os historicos do ticket"""

    alias: type = list
    properties: dict = field(
        default_factory=lambda: {
            "permanencyTimeFullTime": {
                "property": FloatProperty,
                "description": (
                    "Tempo de permanência do responsável pelo ticket em segundos. "
                    "(Somente leitura)."
                ),
                "readOnly": True,
            },
            "permanencyTimeWorkingTime": {
                "property": FloatProperty,
                "description": (
                    "Tempo útil de permanência do responsável pelo ticket em segundos. "
                    "(Somente leitura)."
                ),
                "readOnly": True,
            },
            "changedBy": {
                "property": TicketPerson,
                "description": (
                    "Dados da pessoa que alterou o responsável pelo ticket (Somente leitura)."
                ),
                "readOnly": True,
            },
            "changedDate": {
                "property": DatetimeProperty,
                "description": (
                    "Data UTC que o responsável pelo ticket foi alterado (Somente leitura)."
                ),
                "readOnly": True,
            },
        }
    )


@dataclass
class OwnerHistories(TicketHistory):
    """
    Tickets » Históricos de responsabilidades

    Classe que representa o campo ownerHistories.
    """

    alias: type = list

    def __post_init__(self):
        self.properties["ownerTeam"] = {
            "property": StringProperty,
            "description": ("Equipe do responsável pelo ticket (Somente leitura)."),
            "readOnly": True,
        }
        self.properties["owner"] = {
            "property": TicketPerson,
            "description": ("Dados do responsável pelo ticket (Somente leitura)."),
            "readOnly": True,
        }
        super().__post_init__()


@dataclass
class StatusHistories(TicketHistory):
    """
    Tickets » Históricos de status

    Classe que representa o campo statusHistories.
    """

    alias: type = list

    def __post_init__(self):
        self.properties["status"] = {
            "property": StringProperty,
            "description": ("Status do ticket (Somente leitura)."),
            "readOnly": True,
        }
        self.properties["justification"] = {
            "property": StringProperty,
            "description": ("Justificativa do ticket (Somente leitura)."),
            "readOnly": True,
        }
        self.properties["permanencyTimeFullTime"][
            "description"
        ] = "Tempo de permanência do status do ticket em segundos. (Somente leitura)."
        self.properties["permanencyTimeWorkingTime"][
            "description"
        ] = "Tempo útil de permanência do status do ticket em segundos. (Somente leitura)."
        self.properties["changedBy"][
            "description"
        ] = "Dados da pessoa que alterou o status do ticket (Somente leitura)."
        self.properties["changedDate"][
            "description"
        ] = "Data UTC que o status do ticket foi alterado (Somente leitura)."
        super().__post_init__()


@dataclass
class Assets(ComplexProperty):
    """
    Tickets » Ativos

    Classe que representa o campo assets.
    """

    alias: type = list
    properties: dict = field(
        default_factory=lambda: {
            "id": {
                "property": StringProperty,
                "description": ("Id (Cod. ref.) do ativo (Somente leitura)."),
                "readOnly": True,
            },
            "name": {
                "property": StringProperty,
                "description": ("Nome do ativo (Somente leitura)."),
                "readOnly": True,
            },
            "label": {
                "property": StringProperty,
                "description": ("Etiqueta (única) do ativo (Somente leitura)."),
                "readOnly": True,
            },
            "serialNumber": {
                "property": StringProperty,
                "description": ("Número de série do ativo (Somente leitura)."),
                "readOnly": True,
            },
            "categoryFull": {
                "property": ArrayProperty,
                "description": (
                    "Lista com os nomes dos níveis da categoria selecionada no ativo "
                    "(Somente leitura)."
                ),
                "readOnly": True,
            },
            "categoryFirstLevel": {
                "property": StringProperty,
                "description": (
                    "Nome do primeiro nível da categoria selecionada no ativo (Somente leitura)."
                ),
                "readOnly": True,
            },
            "categorySecondLevel": {
                "property": StringProperty,
                "description": (
                    "Nome do segundo nível da categoria selecionada no ativo (Somente leitura)."
                ),
                "readOnly": True,
            },
            "categoryThirdLevel": {
                "property": StringProperty,
                "description": (
                    "Nome do terceiro nível da categoria selecionada no ativo (Somente leitura)."
                ),
                "readOnly": True,
            },
            "isDeleted": {
                "property": BooleanProperty,
                "description": (
                    "Verdadeiro se o ativo foi deletado do ticket (Somente leitura)."
                ),
                "readOnly": True,
            },
        }
    )


PARAMS = {
    "id": {
        "property": IntegerProperty,
        "description": "Número do ticket ou número do protocolo (somente leitura).",
        "readOnly": True,
    },
    # TODO: StringProperty ou IntegerProperty?
    # A documentação diz que que é string, mas quando tentamos a query
    # /tickets?token=$select=id,subject,createdDate&$filter=id eq '3'
    # obtemos a seguinte resposta:
    # The query specified in the URI is not valid.
    # A binary operator with incompatible types was detected.
    # Found operand types 'Edm.Int32' and 'Edm.String' for operator kind 'Equal'.
    # Se usarmos int, o retorno é algo do tipo {'id': '3'}
    # ou seja, a propriedade id é uma string.
    "type": {
        "property": IntegerProperty,
        "description": "Tipo do ticket. 1 = Interno 2 = Público.",
        "readOnly": False,
    },
    "subject": {
        "property": StringProperty,
        "description": "Assunto do ticket.",
        "readOnly": False,
    },
    "category": {
        "property": StringProperty,
        "description": (
            "Nome da categoria do ticket. Deve ser informada uma categoria existente "
            "e que esteja relacionada ao tipo e ao serviço (caso este esteja informado) do ticket."
        ),
        "readOnly": False,
    },
    "urgency": {
        "property": StringProperty,
        "description": (
            "Nome da urgência do ticket. Deve ser informada uma urgência "
            "existente e que esteja relacionada a categoria (caso esta esteja informada no ticket)."
        ),
        "readOnly": False,
    },
    "isDeleted": {
        "property": BooleanProperty,
        "description": (""),
        "readOnly": True,
    },
    "canceledIn": {
        "property": BooleanProperty,
        "description": (""),
        "readOnly": True,
    },
    "movideskTicketNumber": {
        "property": IntegerProperty,
        "description": (""),
        "readOnly": True,
    },
    "linkedToIntegratedTicketNumber": {
        "property": BooleanProperty,
        "description": (""),
        "readOnly": True,
    },
    "status": {
        "property": StringProperty,
        "description": (
            "Nome do status do ticket. Para alterar esse campo deve ser também informada "
            "a justificativa. O status deve ser um existente e que esteja relacionado ao "
            "tipo do ticket. *Caso não informado, será utilizado o status base Novo padrão."
        ),
        "readOnly": False,
    },
    "baseStatus": {
        "property": StringProperty,
        "description": (
            "Nome do status base do ticket (Somente leitura)."
            "\n\tNew,"
            "\n\tInAttendance,"
            "\n\tStopped,"
            "\n\tCanceled,"
            "\n\tResolved,"
            "\n\tClosed"
        ),
        "readOnly": True,
    },
    "justification": {
        "property": StringProperty,
        "description": (
            "Nome da justificativa do ticket. Deve ser informada uma justificativa "
            "existente que esteja relacionada ao status do ticket. O preenchimento desse campo é "
            "obrigatório quando o status do ticket o exigir. Para alterar esse campo deve ser "
            "também informado o status."
        ),
        "readOnly": False,
    },
    "origin": {
        "property": IntegerProperty,
        "description": (
            "Canal de abertura do ticket (Somente leitura)."
            "\n\t1 Via web pelo cliente"
            "\n\t2 Via web pelo agente"
            "\n\t3 Recebido via email"
            "\n\t4 Gatilho do sistema"
            "\n\t5 Chat (online)"
            "\n\t6 Chat (offline)"
            "\n\t7 Email enviado pelo sistema"
            "\n\t8 Formulário de contato"
            "\n\t9 Via web API"
            "\n\t10 Agendamento automático "
            "\n\t11 JiraIssue"
            "\n\t12 RedmineIssue"
            "\n\t13 ReceivedCall"
            "\n\t14 MadeCall"
            "\n\t15 LostCall"
            "\n\t16 DropoutCall"
            "\n\t17 Acesso remoto"
            "\n\t18 WhatsApp"
            "\n\t19 MovideskIntegration"
            "\n\t20 ZenviaChat"
            "\n\t21 NotAnsweredCall"
            "\n\t23 WhatsApp Business Movidesk"
        ),
        "readOnly": True,
    },
    "createdDate": {
        "property": DatetimeProperty,
        "description": (
            "Data de abertura do ticket. A data informada deve estar no formato UTC*. "
            "*Caso não for informada, será preenchida com a data atual."
        ),
        "readOnly": False,
    },
    "originEmailAccount": {
        "property": StringProperty,
        "description": "Conta de e-mail na qual o ticket foi recebido (Somente leitura).",
        "readOnly": True,
    },
    "owner": {
        "property": TicketPerson,
        "description": (
            "Dados do responsável pelo ticket. Para alterar esse campo deve ser "
            "informada também a equipe do responsável pelo ticket."
        ),
        "readOnly": False,
    },
    "ownerTeam": {
        "property": StringProperty,
        "description": (
            "Equipe do responsável pelo ticket. Para alterar esse campo deve ser informado "
            "também o responsável pelo ticket. Caso o responsável pelo ticket esteja informado, "
            "a equipe do responsável deve estar associada a ele."
        ),
        "readOnly": False,
    },
    "createdBy": {
        "property": TicketPerson,
        "description": "Dados do gerador do ticket.",
        "readOnly": False,
    },
    "serviceFull": {
        "property": ArrayProperty,
        "description": (
            "Lista com os nomes dos níveis do serviço selecionado no ticket "
            "(Somente leitura)."
        ),
        "readOnly": True,
    },
    "serviceFirstLevelId": {
        "property": IntegerProperty,
        "description": "Id (Código) do serviço selecionado no ticket.",
        "readOnly": False,
    },
    "serviceFirstLevel": {
        "property": StringProperty,
        "description": "Nome do primeiro nível do serviço selecionado no ticket (Somente leitura).",
        "readOnly": True,
    },
    "serviceSecondLevel": {
        "property": StringProperty,
        "description": "Nome do segundo nível do serviço selecionado no ticket (Somente leitura).",
        "readOnly": True,
    },
    "serviceThirdLevel": {
        "property": StringProperty,
        "description": "Nome do terceiro nível do serviço selecionado no ticket (Somente leitura).",
        "readOnly": True,
    },
    "contactForm": {
        "property": StringProperty,
        "description": (
            "Nome do formulário de contato através do qual o ticket foi aberto "
            "(Somente leitura)."
        ),
        "readOnly": True,
    },
    "tags": {
        "property": ArrayProperty,
        "description": (
            "Lista de strings com as TAGs as quais o ticket esta relacionado. "
            "Caso sejam informadas TAGs inexistentes, as mesmas serão adicionadas na base de dados."
        ),
        "readOnly": False,
    },
    "cc": {
        "property": StringProperty,
        "description": "Relação dos e-mails informados no campo Cc, separados por vírgula.",
        "readOnly": False,
    },
    "resolvedIn": {
        "property": DatetimeProperty,
        "description": (
            "Data na qual o ticket foi indicado pelo agente como resolvido. "
            "A data informada deve estar no formato UTC."
        ),
        "readOnly": False,
    },
    "reopenedIn": {
        "property": DatetimeProperty,
        "description": "Data na qual o ticket teve a ultima reabertura (Somente leitura).",
        "readOnly": True,
    },
    "closedIn": {
        "property": DatetimeProperty,
        "description": (
            "Data na qual o ticket foi indicado como fechado. "
            "A data informada deve estar no formato UTC."
        ),
        "readOnly": False,
    },
    "lastActionDate": {
        "property": DatetimeProperty,
        "description": "Data UTC da última ação do ticket (Somente leitura).",
        "readOnly": True,
    },
    "actionCount": {
        "property": IntegerProperty,
        "description": "Quantidade de ações do ticket (Somente leitura).",
        "readOnly": True,
    },
    "lastUpdate": {
        "property": DatetimeProperty,
        "description": "Data UTC da última alteração do ticket (Somente leitura).",
        "readOnly": True,
    },
    "lifeTimeWorkingTime": {
        "property": IntegerProperty,
        "description": (
            "Tempo de vida do ticket em minutos em horas úteis desde a abertura "
            "(Somente leitura)."
        ),
        "readOnly": True,
    },
    "stoppedTime": {
        "property": IntegerProperty,
        "description": (
            "Tempo que o ticket ficou no status parado em minutos em horas corridas "
            "(Somente leitura)."
        ),
        "readOnly": True,
    },
    "stoppedTimeWorkingTime": {
        "property": IntegerProperty,
        "description": (
            "Tempo que o ticket ficou no status parado em minutos em horas úteis "
            "(Somente leitura)."
        ),
        "readOnly": True,
    },
    "resolvedInFirstCall": {
        "property": BooleanProperty,
        "description": (
            "Indicador que representa se o ticket foi resolvido já no momento da "
            "abertura ou num momento posterior (Somente leitura)."
        ),
        "readOnly": True,
    },
    "chatWidget": {
        "property": StringProperty,
        "description": "Aplicativo de chat através do qual o ticket foi aberto (Somente leitura).",
        "readOnly": True,
    },
    "chatGroup": {
        "property": StringProperty,
        "description": "Grupo de chat através do qual o ticket foi aberto (Somente leitura).",
        "readOnly": True,
    },
    "chatTalkTime": {
        "property": IntegerProperty,
        "description": "Tempo de duração do chat em segundos (Somente leitura).",
        "readOnly": True,
    },
    "chatWaitingTime": {
        "property": IntegerProperty,
        "description": (
            "Tempo que o cliente ficou aguardando para ser atendido em segundos "
            "(Somente leitura)."
        ),
        "readOnly": True,
    },
    "sequence": {
        "property": IntegerProperty,
        "description": "Número inteiro armazenado no campo Sequência.",
        "readOnly": False,
    },
    "slaAgreement": {
        "property": StringProperty,
        "description": "Contrato SLA utilizado no ticket (Somente leitura).",
        "readOnly": True,
    },
    "slaAgreementRule": {
        "property": StringProperty,
        "description": "Regra do contrato SLA (Somente leitura).",
        "readOnly": True,
    },
    "slaSolutionTime": {
        "property": IntegerProperty,
        "description": "Tempo de solução do contrato SLA (Somente leitura).",
        "readOnly": True,
    },
    "slaResponseTime": {
        "property": IntegerProperty,
        "description": "Tempo de resposta do contrato SLA (Somente leitura).",
        "readOnly": True,
    },
    "slaSolutionChangedByUser": {
        "property": BooleanProperty,
        "description": (
            "Indica se o contrato SLA foi manualmente alterado pelo usuário "
            "(Somente leitura)."
        ),
        "readOnly": True,
    },
    "slaSolutionChangedBy": {
        "property": TicketPerson,
        "description": "Dados da pessoa que alterou o contrato SLA (Somente leitura).",
        "readOnly": True,
    },
    "slaSolutionDate": {
        "property": DatetimeProperty,
        "description": (
            "Data de solução do SLA. Caso informado, será considerado que o SLA foi "
            "manualmente alterado pelo usuário que criou a ação. A data informada deve "
            "estar no formato UTC."
        ),
        "readOnly": True,
    },
    "slaSolutionDateIsPaused": {
        "property": BooleanProperty,
        "description": "Indica se a data de solução do SLA está pausada (Somente leitura).",
        "readOnly": True,
    },
    "slaResponseDate": {
        "property": DatetimeProperty,
        "description": "Data UTC de resposta do SLA (Somente leitura).",
        "readOnly": True,
    },
    "slaRealResponseDate": {
        "property": DatetimeProperty,
        "description": "Data UTC real da resposta do SLA (Somente leitura).",
        "readOnly": True,
    },
    "jiraIssueKey": {
        "property": StringProperty,
        "description": (
            "Chave da issue do Jira Software que está associada ao ticket por "
            "integração (Somente leitura)."
        ),
        "readOnly": True,
    },
    "redmineIssueId": {
        "property": IntegerProperty,
        "description": (
            "ID da issue do Redmine que está associada ao ticket por "
            "integração (Somente leitura)."
        ),
        "readOnly": True,
    },
    "clients": {
        "property": Clients,
        "description": "Lista com os clientes do ticket.",
        "readOnly": False,
    },
    "actions": {
        "property": Actions,
        "description": "Lista com as ações do ticket.",
        "readOnly": False,
    },
    "parentTickets": {
        "property": SubTickets,
        "description": "Lista com os tickets pais.",
        "readOnly": False,
    },
    "childrenTickets": {
        "property": SubTickets,
        "description": "Lista com os tickets filhos.",
        "readOnly": False,
    },
    "ownerHistories": {
        "property": OwnerHistories,
        "description": "Lista com os históricos de responsabilidades do ticket (Somente leitura).",
        "readOnly": True,
    },
    "statusHistories": {
        "property": StatusHistories,
        "description": "Lista com os históricos de status do ticket (Somente leitura).",
        "readOnly": True,
    },
    "customFieldValues": {
        "property": CustomFieldValues,
        "description": "Lista com os valores dos campos adicionais do ticket.",
        "readOnly": False,
    },
    "assets": {
        "property": Assets,
        "description": "Lista com os ativos do ticket.",
        "readOnly": False,
    },
}


class Tickets(Entity):
    BASE_URL = urljoin(MAIN_URL, "tickets")
    VALID_PARAMS = PARAMS
