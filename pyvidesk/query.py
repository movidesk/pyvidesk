"""
Módulo que faz consulta de dados ao servidor do Movidesk.
Não deve ser usada diretamente.

Exemplo de uso:

>>> from datetime import date, timedelta
>>> from pyvidesk.tickets import Tickets

>>> yesterday = date.today() - timedelta(days=1)
>>> tickets = Tickets(token="my_token")
>>> ticket_properties = tickets.get_properties()
>>> my_query = (
...    tickets.query()
...    .filter(ticket_properties["lastUpdate"] >= yesterday)
...    .select("id")
...    .top(3)
... )
>>> for ticket in my_query:
...     print(ticket)
... <Model for Ticket(id=2336)>
... <Model for Ticket(id=3139)>
... <Model for Ticket(id=3807)>

>>> print(my_query.all())
... [<Model for Ticket(id=2336)>, <Model for Ticket(id=3139)>, <Model for Ticket(id=3807)>]

>>> print(my_query.first())
... <Model for Ticket(id=2336)>
"""

from .model import Model
from .utils import get_property_name


class Query:
    """
    Classe que organiza e obtem os dados do Movidesk. Não deve ser
    usada diretamente, mas de um objeto das classes Tickets, Persons ou Services.

    É possível obter os resultados de três maneiras:

    1) Iterando sobre o objeto:
    >>> for ticket in my_query:
    ...     print(ticket)

    2) Todos os resultados numa lista:
    >>> my_query.all()

    3) Apenas o primeiro resultado:
    >>> my_query.first()
    """

    def __init__(self, entity, options=None):
        """
        Args:
            entity (pyvidesk.*.*): Objeto que representa uma entidade do Movidesk
                (Tickets, Persons ou Services)
            options (dict): As opções ($top, $skip, $select, $filter, $expand, $orderby)
                da consulta.
        """
        self.entity = entity
        self.options = options or dict()

    def __iter__(self):
        """
        Método que obtem as respostas do servidor.
        Tanto first() quanto all() usam esse método para obter as respostas.

        yields:
            (pyvideks.model.Model): Objeto que representa as respostas do servidor
        """
        result = self.entity.api.get(options=self._get_options())
        if isinstance(result, list):
            for data in result:
                yield self._create_model(data)
        else:
            yield self._create_model(result)

    def __repr__(self):
        return f"<Query for {self.entity}>"

    def _get_options(self):
        """
        Metodo que formata o dicionário de opções atuais para criação da URL de consulta.

        Returns:
            options (dict): As opções da consulta.
        """
        options = dict()

        top = self.options.get("$top")
        if top is not None:
            options["$top"] = top

        skip = self.options.get("$skip")
        if skip is not None:
            options["$skip"] = skip

        select = self.options.get("$select")
        if select:
            options["$select"] = ",".join(select)

        _filter = self.options.get("$filter")
        if _filter:
            options["$filter"] = " and ".join(_filter)

        expand = self.options.get("$expand")
        if expand:
            options["$expand"] = ",".join(expand)

        order_by = self.options.get("$orderby")
        if order_by:
            options["$orderby"] = ",".join(order_by)
        return options

    def _create_model(self, data):
        return Model(self.entity, **data)

    def _get_or_create_option(self, name):
        if name not in self.options:
            self.options[name] = []
        return self.options[name]

    def _new_query(self):
        """
        Método que cria uma cópia desta consulta.
        Todos os construtores de consulta devem usar isso primeiro.

        Returns:
            (pyvidesk.query.Query): Uma instância desta classe.
        """
        options = dict()
        options["$top"] = self.options.get("$top", None)
        options["$skip"] = self.options.get("$skip", None)
        options["$select"] = self.options.get("$select", [])[:]
        options["$filter"] = self.options.get("$filter", [])[:]
        options["$expand"] = self.options.get("$expand", [])[:]
        options["$orderby"] = self.options.get("$orderby", [])[:]
        return Query(entity=self.entity, options=options)

    def as_url(self):
        return self.entity.api._get_url(options=self._get_options())

    def select(self, *values):
        """
        Método que define o parâmetro '$select' da consulta. Pode ser usado múltiplas vezes
        na construção da consulta.

        Args:
            values (pyvidesk.properties.*, ou str): Valores que serão inseridos no
                parâmetro '&select' da consulta.
                Recomenda-se o uso das propriedades de self.entity, no entanto, strings também
                devem funcionar (precisa de mais testes).

        Returs:
            new_query (pyvidesk.query.Query): Uma instância desta classe.
        """
        new_query = self._new_query()
        option = new_query._get_or_create_option("$select")
        option.extend((get_property_name(prop) for prop in values))

        return new_query

    def filter(self, value):
        """
        Método que define o parâmetro '$filter' da consulta. Pode ser usado múltiplas vezes
        na construção da consulta. Os múltiplos filtros são concatenados com o operador 'and'.

        Args:
            value (str): Comparação de uma propriedade de self.entity.
                ``entity_properties["id"] > 1000``, por exemplo.

        Returs:
            new_query (pyvidesk.query.Query): Uma instância desta classe.
        """
        new_query = self._new_query()
        option = new_query._get_or_create_option("$filter")
        option.append(value)
        return new_query

    def expand(self, *values, select=None, inner=None):
        """
        Método que define o parâmetro '$expand' da consulta. Pode ser usado múltiplas vezes
        na construção da consulta.

        Args:
            values (pyvidesk.properties.*, str, tuple or list): Valores que serão inseridos no
                parâmetro '&expand' da consulta.
                Recomenda-se o uso das propriedades de self.entity, no entanto, outros tipos também
                devem funcionar (precisa de mais testes).
            select (pyvidesk.properties.* ou str): Argumento que seta o parâmetro '$select'
                dentro de '$expand'.
            inner (pyvidesk.properties.* ou str; dict): Argumento que seta uma expansão interna.
                Há a possibilidade de setar o parâmetro '$select' dentro deste '$expand' também, mas
                deve-se passar um dicionário com as chaves 'expand' e 'select'.

            Exemplo:
                >>> from pyvidesk.tickets import Tickets
                >>> tickets = Tickets("my_token")
                >>> tickets_properties = tickets.get_properties()
                >>> my_query = tickets.query().expand(
                ...     tickets_properties["clients"], select=tickets_properties["clients"].id
                >>> print(my_query.as_url())
                ... (
                ...     "https://api.movidesk.com/public/v1/tickets?token=my_token"
                ...     "&$expand=clients($select=id)"
                ... )

                >>> my_query = tickets.query().expand(
                ...     tickets_properties["clients"],
                ...     select=tickets_properties["clients"].id,
                ...     inner=tickets_properties["clients"].organization,
                ... )
                >>> print(my_query.as_url())
                ... (
                ...     "https://api.movidesk.com/public/v1/tickets?token=my_token"
                ...     "&$expand=clients($expand=organization;$select=id)"
                ... )

                >>> my_query = tickets.query().expand(
                ...     tickets_properties["clients"],
                ...     select=tickets_properties["clients"].id,
                ...     inner={
                ...         "expand": tickets_properties["clients"].organization,
                ...         "select": tickets_properties["clients"].organization.id,
                ...     },
                ... )
                >>> print(my_query.as_url())
                ... (
                ...     "https://api.movidesk.com/public/v1/tickets?token=my_token"
                ...     "&$expand=clients($expand=organization($select=id);$select=id)"
                ... )

        Returs:
            new_query (pyvidesk.query.Query): Uma instância desta classe.
        """
        expand_complex_type = _get_complex_type_expansion(select=select, inner=inner)
        new_query = self._new_query()
        option = new_query._get_or_create_option("$expand")
        for prop in values:
            option.append(get_property_name(prop) + expand_complex_type)

        return new_query

    def order_by(self, *values):
        """
        Método que define o parâmetro '$orderby' da consulta. Pode ser usado múltiplas vezes
        na construção da consulta.

        Args:
            values (str): Recomenda-se o uso dos métodos asc() e desc() das propriedades, mas
                strings diretas ("id asc", por exemplo) também deve funcionar
                (precisa de mais testes).
        Returs:
            new_query (pyvidesk.query.Query): Uma instância desta classe.
        """
        new_query = self._new_query()
        option = new_query._get_or_create_option("$orderby")
        option.extend(values)
        return new_query

    def top(self, value):
        """
        Método que define o parâmetro '$top' da consulta.

        Args:
            value (int): O número limite de retornos da consulta.

        Returs:
            new_query (pyvidesk.query.Query): Uma instância desta classe.
        """
        new_query = self._new_query()
        new_query.options["$top"] = value
        return new_query

    def skip(self, value):
        """
        Método que define o parâmetro '$skip' da consulta.

        Args:
            value (int): O número de retornos iniciais que a consulta não deve retornar.

        Returs:
            new_query (pyvidesk.query.Query): Uma instância desta classe.
        """
        new_query = self._new_query()
        new_query.options["$skip"] = value
        return new_query

    def all(self):
        """
        Método que retorna uma lista de todas as respostas que corresponderam
        às opções da consulta.

        Returs:
            (list): Lista de modelos (pyvidesk.models.Model) das respostas.
        """
        return list(iter(self))

    def first(self):
        """
        Método que retorna a primeira resposta da consulta.

        Returns:
            (pyvidesk.models.Model): Modelo que representa a resposta, se houver.
                None, do contrário.
        """
        old_value = self.options.get("$top", None)
        self.options["$top"] = 1
        data = list(iter(self))
        self.options["$top"] = old_value
        if data:
            return data[0]

    def raw(self, query_params):
        """
        Executa uma consulta com parâmetros customizados. Permite consultas que essa
        biblioteca ainda não suporta.

        Exemplo:
            >>> from pyvidesk.tickets import Tickets
            >>> tickets = Tickets("my_token")
            >>> tickets.query.raw({"filter": "id eq 123456", "select": "id"})
            ... [{"id": 123456}]

        Args:
            query_params (dict): Um dicionário de parâmetros de consulta contendo "filter",
                "orderby", etc.

        Returs:
            (list): O resultado da consulta.
        """
        return self.entity.api.get(**query_params)


class Q:
    """
    Class que encapsula filtros como objetos de maneira que possam ser combinados logicamente (usando
    `&`, `|` ou `~`).

    Inspirado na classe django.db.models.Q (https://github.com/django/django/blob/master/django/db/models/query_utils.py)
    """

    def __init__(self, query_filter):
        self.filter = query_filter

    def _combine(self, other, condition):
        if not isinstance(other, Q):
            raise TypeError(other)

        return f"({self.filter} {condition} {other.filter})"

    def __or__(self, other):
        return self._combine(other, condition="or")

    def __and__(self, other):
        return self._combine(other, condition="and")

    def __invert__(self):
        return f"not {self.filter}"


def _get_complex_type_expansion(select, inner, is_inner_expansion=False):
    """
    Funcao que obtem uma string que representa o padrão de uma uma expansão complexa
    (interna, concatenada...).
    """
    pattern = ""
    if inner:
        if isinstance(inner, dict):
            pattern += "$expand=" + get_property_name(inner.get("expand"))
            if "inner" in inner:
                inner_pattern = _get_complex_type_expansion(
                    select=inner["inner"].get("select"),
                    inner=inner["inner"].get("expand"),
                    is_inner_expansion=True,
                )
                if inner_pattern:
                    pattern += inner_pattern
                if "select" in inner:
                    pattern = (
                        "".join(pattern.split("))"))
                        + ");$select="
                        + get_property_name(inner.get("select"))
                        + ")"
                    )

            else:
                if "select" in inner:
                    pattern += (
                        "($select=" + get_property_name(inner.get("select")) + ")"
                    )
        else:
            pattern += "$expand=" + get_property_name(inner)
    if select:
        if pattern:
            if is_inner_expansion:
                pattern += "($select=" + get_property_name(select) + ")"
            else:
                pattern += ";$select=" + get_property_name(select)
        else:
            pattern += "$select=" + get_property_name(select)

    if pattern:
        return f"({pattern})"
    return pattern
