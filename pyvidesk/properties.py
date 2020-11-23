"""
Módulo com todos os tipos de propriedades do Movidesk.

Exemplo de uso:

>>> from datetime import datetime
>>> from pyvidesk.tickets import Tickets

>>> my_date = datetime(2020, 1, 1, 20, 0, 0)
>>> tickets = Tickets(token="my_token")
>>> tickets_properties = tickets.get_properties()
>>> print(tickets_properties["createdDate"] >= my_date)
... createdDate ge 2020-01-01T20:00:00Z
>>> print(tickets_properties["createdDate"].get_description())
... Data de abertura do ticket. A data informada deve estar no formato UTC*.
... *Caso não for informada, será preenchida com a data atual.
"""

from dataclasses import dataclass, field
import datetime
from decimal import Decimal

from dateutil.parser import parse as dateutil_parse


class PropertyBase:
    """
    Classe base para todas as propriedades (exceto as complexas).
    """

    def __init__(self, name_, description_, read_only, fathers=None):
        """
        Args:
            name_ (str): O nome da propriedade.
            fathers (str): O nome da(s) propriedade(s) "pai(s)", separados por '/',
                se houver mais de um.
            description_ (str): A descrição da propriedade, conforme documentação do
                Movidesk.
            read_only (bool): True, se a propriedade for somente leitura. False, do contrário.

            ('_' em 'name_' e 'description_' para padronizar com a classe ComplexProperty)
        """
        self.name_ = name_
        self._fathers = fathers
        self.description_ = description_
        self._read_only = read_only

    @property
    def is_read_only(self):
        return self._read_only

    @property
    def full_name(self):
        if self._fathers:
            return "/".join((self._fathers, self.name_))
        return self.name_

    def get_description(self):
        return self.description_

    def __repr__(self):
        return "<Property({0})>".format(self.full_name)

    def serialize(self, value):
        """
        Usado para serializar o valor para JSON.

        A ideia desse método é ser usado na hora da criação de objeto que representará
        uma entidade do Movidesk.
        Esse objeto poderá ser manipulado para alteração de dados.

        Args:
            value (): O valor na linguagem Python.

        Returns:
            (): O valor que será usado no JSON.
        """
        raise NotImplementedError()

    def deserialize(self, value):
        """
        Usado para serializar o valor para linguagem python.

        A ideia desse método é ser usado na hora da criação de objeto que representará
        uma entidade do Movidesk.
        Esse objeto poderá ser manipulado para alteração de dados.

        Args:
            value (): O valor no JSON.

        Returns:
            (): O valor na linguagem Python.
        """
        raise NotImplementedError()

    def escape_value(self, value):
        """
        Usado para ajustar o valor na hora de usar a propriedade na classe Query.

        Args:
            value (): Valor da propriedade.

        Returns:
            value (): Valor que pode ser usado na classe Query.
        """
        if value is None:
            return "null"
        return value

    def asc(self):
        return f"{self.full_name} asc"

    def desc(self):
        return f"{self.full_name} desc"

    def __eq__(self, other):
        value = self.escape_value(other)
        return f"{self.full_name} eq {value}"

    def __ne__(self, other):
        value = self.escape_value(other)
        return f"{self.full_name} ne {value}"

    def __ge__(self, other):
        value = self.escape_value(other)
        return f"{self.full_name} ge {value}"

    def __gt__(self, other):
        value = self.escape_value(other)
        return f"{self.full_name} gt {value}"

    def __le__(self, other):
        value = self.escape_value(other)
        return f"{self.full_name} le {value}"

    def __lt__(self, other):
        value = self.escape_value(other)
        return f"{self.full_name} lt {value}"


class IntegerProperty(PropertyBase):
    """
    Propriedade que armazena um inteiro.
    """

    alias = int

    def serialize(self, value):
        return value

    def deserialize(self, value):
        return value


class FloatProperty(IntegerProperty):
    """
    Propriedade que armazena um float.
    """

    alias = float


class StringProperty(PropertyBase):
    """
    Propriedade que armazena uma string.
    """

    alias = str

    def serialize(self, value):
        return value

    def deserialize(self, value):
        return value

    def escape_value(self, value):
        if value is None:
            return "null"
        return f"'{value}'"


class ArrayProperty(StringProperty):
    """
    Propriedade que armazena um array de strings.
    """

    alias = list

    def has(self, value):
        """
        Metodo que checa tem o objetivo de preparar uma query para verificar
        se um array de strings contém um string.

        Args:
            value (str): A string que será procurada no array.

        Returns:
            (str): Uma string que representa essa query.
        """

        if "/" in self.full_name:
            p1, p2 = self.full_name.split("/")
            return f"{p1}/any(x: x/{p2}/any(y: y eq {self.escape_value(value)}))"
        return f"{self.full_name}/any(x: x eq {self.escape_value(value)})"

    # __contains__ precisa retornar um valor booleano, logo, não podemos aplicar a lógica acima
    # para alterar o operador 'in'


class BooleanProperty(PropertyBase):
    """
    Propriedade que armazena um valor booleano.
    """

    alias = bool

    def escape_value(self, value):
        if value:
            return "true"
        return "false"

    def serialize(self, value):
        return bool(value)

    def deserialize(self, value):
        return bool(value)


class DatetimeProperty(PropertyBase):
    """
    Propriedade que armazena um objeto datetime.
    JSON não suporta objetos datetime nativamente, então as datas são
    formatadas como strings seguindo a ISO-8601.

    A classe também aceita objetos datetime.date.
    """

    alias = (datetime.datetime, datetime.date)

    def escape_value(self, value):
        if value is None:
            return "null"

        if isinstance(value, str):
            value = dateutil_parse(value)

        return value.isoformat() + "Z"
        # O Z no final vem da prórpria ISO-8601 e do padrão de datas pelo UTC do Movidesk:
        # "If the time is in UTC, add a 'Z' directly after the time without a space."
        # Sem o "Z", recebemos o seguinte erro:
        # Message: The query specified in the URI is not valid. The DateTimeOffset
        # text should be in format 'yyyy-mm-ddThh:mm:ss('.'s+)?(zzzzzz)?'
        # and each field value is within valid range.

    def serialize(self, value):
        if isinstance(value, datetime.date):
            value = datetime.datetime.combine(value, datetime.datetime.min.time())
        if isinstance(value, datetime.datetime):
            return value.isoformat()

    def deserialize(self, value):
        if value:
            return dateutil_parse(value)


class TimeProperty(PropertyBase):
    """
    Propriedade que armazena um objeto datetime.time.
    """

    alias = datetime.time

    def escape_value(self, value):
        if value is None:
            return "null"

        if isinstance(value, str):
            value = dateutil_parse(value).time()

        return value.isoformat()

    def serialize(self, value):
        if isinstance(value, datetime.time):
            return value.isoformat()

    def deserialize(self, value):
        if value:
            return dateutil_parse(value).time()


class DecimalProperty(PropertyBase):
    """
    Propriedade que armazena um valor decimal. JSON não suporta isso nativamente,
    então o valor será formatado como um float.
    """

    alias = Decimal

    def escape_value(self, value):
        if value is None:
            return "null"
        return str(value)

    def serialize(self, value):
        if value is not None:
            return float(value)

    def deserialize(self, value):
        if value is not None:
            return Decimal(str(value))


@dataclass
class ComplexProperty:
    """Classe que representa uma propriedade complexa do Movidesk"""

    name_: str  # a propriedade complexa pode ter uma propriedade 'name'
    description_: str  # a propriedade complexa pode ter uma propriedade 'description'
    properties: dict
    read_only: bool = False
    fathers: str = None
    alias: type = dict

    def __post_init__(self):
        for property_name, property_infos in self.properties.items():
            property_class = property_infos["property"]
            setattr(
                self,
                property_name,
                property_class(
                    name_=property_name,
                    fathers=self.full_name,
                    description_=property_infos["description"],
                    read_only=property_infos["readOnly"],
                ),
            )

    @property
    def full_name(self):
        if self.fathers:
            return "/".join((self.fathers, self.name_))
        return self.name_

    @property
    def is_read_only(self):
        return self.read_only

    def get_description(self):
        return self.description_

    def get_properties(self, as_model=False):
        """
        Metodo que obtem as propriedades "filhas" dessa proprieda.

        Returns:
            properties (dict): Dicionário com as propriedades da entidade.
            as_model (bool): True, se as propriedades forem usadas para criar um modelo.
                False, do contrário.

            TODO: pensar em outro nome/outra maneira para 'as_model'
        """
        properties = {}
        for property_name, property_infos in self.properties.items():
            property_class = property_infos["property"]
            property_obj = property_class(
                name_=property_name,
                fathers=self.full_name,
                description_=property_infos["description"],
                read_only=property_infos.get("readOnly"),
            )
            if as_model:  # para criar um Model de ComplexProperty
                properties[property_obj.name_] = property_obj
            else:
                properties[property_obj.full_name] = property_obj
        return properties

    def serialize(self, value):
        if isinstance(value, list):
            data = []
            for v in value:
                data.append(self._serialize(v))
            return data
        return self._serialize(value)

    def _serialize(self, values):
        if values is None:
            return "null"
        data = dict()
        for prop, value in values.items():
            data[prop] = getattr(self, prop).serialize(value)
        return data

    def deserialize(self, value):
        if isinstance(value, list):
            data = []
            for i in value:
                data.append(self._deserialize(i))
            return data
        return self._deserialize(value)

    def _deserialize(self, values):
        data = dict()
        for prop, value in values.items():
            try:
                data[prop] = getattr(self, prop).deserialize(value)
            except AttributeError:  # algumas propriedas não estão documentadas
                data[prop] = value
        return data


@dataclass
class CustomFieldValuesItems(ComplexProperty):
    """
    Entity » Campos adicionais » Itens

    Classe que representa os itens do campo customFieldValues.
    """

    properties: dict = field(
        default_factory=lambda: {
            "personId": {
                "property": IntegerProperty,
                "description": (
                    "Id (Cod. ref.) da empresa, departamento ou pessoa. "
                    "*Obrigatório quando o tipo do campo for lista de pessoas."
                ),
                "readOnly": False,
            },
            "clientId": {
                "property": IntegerProperty,
                "description": (
                    "Id (Cod. ref.) da empresa, departamento ou pessoa. "
                    "*Obrigatório quando o tipo do campo for lista de clientes."
                ),
                "readOnly": False,
            },
            "team": {
                "property": StringProperty,
                "description": (
                    "Nome da equipe. *Obrigatório quando o tipo do campo lista de agentes "
                    "(o personId pode ser informado para especificar o agente da equipe)."
                ),
                "readOnly": False,
            },
            "customFieldItem": {
                "property": StringProperty,
                "description": (
                    "Nome do item do campo adicional. *Obrigatório quando o tipo do campo for: "
                    "lista de valores, seleção múltipla ou seleção única."
                ),
                "readOnly": False,
            },
        }
    )


@dataclass
class CustomFieldValues(ComplexProperty):
    """
    Entity » Campos adicionais

    Classe que representa o campo customFieldValues.
    """

    properties: dict = field(
        default_factory=lambda: {
            "customFieldId": {
                "property": IntegerProperty,
                "description": (
                    "Id do campo adicional "
                    "(pode ser obtido na listagem de campos adicionais no website)."
                ),
                "readOnly": False,
            },
            "customFieldRuleId": {
                "property": IntegerProperty,
                "description": (
                    "Id da regra de exibição dos campos adicionais "
                    "(pode ser obtido na listagem de regras para exibição no website)."
                ),
                "readOnly": False,
            },
            "line": {
                "property": IntegerProperty,
                "description": (
                    "Número da linha da regra de exibição na tela do ticket. "
                    "Quando a regra não permitir a adição de novas linhas deve ser informado "
                    "o valor 1 e não devem ser repetidos valores de campos adicionais para o id "
                    "da regra em conjunto com o id do campo. Para alterar o valor de um campo "
                    "deve ser informada a linha em que ele se encontra. Os campos que estiverem "
                    "na base de dados e não forem enviados no corpo da requisição serão excluídos."
                ),
                "readOnly": False,
            },
            "value": {
                "property": StringProperty,
                "description": (
                    "Valor texto do campo adicional. *Obrigatório quando o tipo do campo for: "
                    "texto de uma linha, texto com várias linhas, texto HTML, expressão regular, "
                    "numérico, data, hora, data e hora, e-mail, telefone ou URL. "
                    "Os campos de data devem estar em horário *UTC e no formato "
                    "YYYY-MM-DDThh:MM:ss.000Z e o campo hora deve ser informado juntamente com a "
                    "data fixa '1991-01-01'. O campo numérico deve estar no formato brasileiro, "
                    "por exemplo '1.530,75'."
                ),
                "readOnly": False,
            },
            "items": {
                "property": CustomFieldValuesItems,
                "description": (
                    "Lista de itens. *Obrigatório quando o tipo do campo for: "
                    "lista de valores, lista de pessoas, lista de clientes, lista de agentes, "
                    "seleção múltipla ou seleção única. Deve ser informado apenas um item se o "
                    "campo adicional não permitir seleção múltipla."
                ),
                "readOnly": False,
            },
        }
    )
