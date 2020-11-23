"""
Módulo que representa um entidade no Movidesk (Tickets, Persons ou Services).

Exemplo de uso.

>>> from pyvidesk.tickets import Tickets

>>> tickets = Tickets(token="my_token")
>>> ticket = ticket.get_by_id(3)
>>> print(ticket)
... <Model for Ticket(id=3)>
>>> print(ticket.id)
... 3
>>> print(ticket.subject)
... 'Assunto'
"""


from .api import Api
from .config import QUERY_PARAMS
from .exceptions import (
    PyvideskPropertyNotValidError,
    PyvideskPropertyWithWrongType,
    PyvideskWrongKwargError,
)
from .model import EmptyModel
from .properties import ComplexProperty
from .query import Query
from .utils import get_property_name


class Entity:
    """Classe que representa uma entidade do Movidesk (Tickets, Persons...)"""

    def __init__(self, token):
        """
        Args:
            token (str): O token que permitirá o acesso aos dados do Movidesk.
        """
        base_url = self.BASE_URL + f"?token={token}"
        self.api = Api(base_url=base_url)

    @property
    def query(self):
        return Query(entity=self)

    def get_properties(self, **kwargs):  # pylint: disable=unused-argument
        """
        Metodo que obtem as propriedades da entidade.

        Args:
            kwargs (): Utilizado apenas para adequacao do metodo de mesmo nome
                da classe ComplexProperty.

        Returns:
            properties (dict): Dicionário com as propriedades da entidade.
        """
        properties = dict()
        for property_name, property_infos in self.VALID_PARAMS.items():
            property_class = property_infos["property"]
            properties[property_name] = property_class(
                name_=property_name,
                description_=property_infos["description"],
                read_only=property_infos["readOnly"],
            )
        return properties

    def describe(self):
        """Metodo que descreve a entidade e suas principais propriedades"""

        def _describe(properties, escape_code=""):
            """
            Funcao que introduz uma recursão na hora de buscarmos todas as propriedades da entity.

            Args:
                properties (dict): Dicionário com nome e objeto das propriedades.
                escape_code (str): Utilizado quando queremos tabular uma propriedade
                    e facilitar a visualização de propriedades complexas.
            """
            for property_name, property_obj in properties.items():
                print(escape_code + f"Propriedade: {property_name}")
                print(escape_code + f"Tipo: {property_obj.alias}")
                print(
                    escape_code + f"Descrição: {property_obj.get_description()}",
                )
                if isinstance(property_obj, ComplexProperty):
                    _describe(
                        properties=property_obj.get_properties(),
                        escape_code=escape_code + "\t",
                    )
                print("\n")

        print(
            "\n\n\t\t------------------------------------"
            f"Descrição da entidade {self.__class__.__name__}"
            "------------------------------------------------------\n\n"
        )
        _describe(properties=self.get_properties())
        print(
            "\n\n----------------------------------------------------------------------"
            "--------------------------------------------------------------------------\n\n"
        )

    def get_empty_model(self):
        return EmptyModel(entity=self)

    def __getattr__(self, attr):
        """
        Utilizado para requisições mais simples. Não deve ser usado para consulta de
        propriedades complexas.

        Exemplo:

        >>> from pyvidesk.persons import Persons

        >>> persons = Persons(token="my_token")
        >>> person = persons.get_by_id("1", select="businessName")
        >>> print(person)
        ... <Model for Person(businessName=Murilo Scarpa Sitonio)>

        Returns:
            (pyvidesk.model.Model): Se o parametro de filtro for o id, como no exemplo acima.
            OU
            (pyvidesk.query.Query): Caso o filtro possa retornar múltiplos valores.

        Raises:
            PyvideskPropertyNotValidError: Se a propriedade nao pertencer a entidade.
        """
        try:
            param = attr.split("get_by_")[1]
        except IndexError as attr_error:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{attr}'"
            ) from attr_error

        if param not in self.VALID_PARAMS:
            raise PyvideskPropertyNotValidError(param=param, class_=self)

        def wrapper(*args, **kwargs):
            self._pre_validate_request(param, *args, **kwargs)
            properties = self.get_properties()
            param_value = kwargs.pop(param, None) or args[0]
            query = Query(
                entity=self,
                options=_organize_options(options=kwargs),
            ).filter(properties[param] == param_value)

            if param in ("id", "codeReferenceAdditional"):
                return query.first()
            return query

        return wrapper

    def _pre_validate_request(self, property_name, *args, **kwargs):
        """
        Pre validacao da requisicao analisando o tipo dos valores.

        Args:
            property_name (str): O nome da propriedade.

        Raises:
            PyvideskPropertyWithWrongType: A propriedade tem um tipo de valor diferente
                do definido na documentacao do Movidesk;
            PyvideskWrongKwargError: O kwarg usado nao é uma das opcoes da query
                (select, top, skip...);
        """
        properties = self.get_properties()
        for arg in args:
            if not isinstance(arg, properties[property_name].alias):
                raise PyvideskPropertyWithWrongType(
                    param=property_name,
                    value=arg,
                    correct_type=properties[property_name].alias,
                )

        for key, value in kwargs.items():
            try:
                valid_params = {**properties, **QUERY_PARAMS}
                try:
                    data_type = valid_params[key].alias
                except AttributeError:
                    data_type = valid_params[key]
            except KeyError as wrong_wkarg_error:
                raise PyvideskWrongKwargError(
                    param=property_name, kwarg=key
                ) from wrong_wkarg_error

            if not isinstance(value, data_type):
                raise PyvideskPropertyWithWrongType(
                    param=key, value=value, correct_type=data_type
                )


def _organize_options(options):
    """Funcao que organiza as opcoes da query de __getattr__"""

    def organize_option_that_can_have_multiple_values(option):
        if isinstance(option, (tuple, list)):
            return [get_property_name(prop) for prop in option]
        return [get_property_name(option)]

    _options = dict()
    for option, option_value in options.items():
        if option in ("top", "skip"):
            _options["$" + option] = option_value
        else:
            _options["$" + option] = organize_option_that_can_have_multiple_values(
                option_value
            )

    return _options
