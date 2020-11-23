"""
Módulo que representa um ticket, uma pessoa ou um serviço.

Não deve ser usado diretamente, mas obtido no retorno de algum método
da classe Entity ou Query.

Exemplo de uso:

>>> from pyvidesk.tickets import Tickets

>>> tickets = Tickets(token="my_token")
>>> ticket = ticket.get_by_id(3)
>>> print(ticket)
... <Model for Ticket(id=3)>

--------------------------------------------------------------------------

>>> from datetime import date, timedelta
>>> from pyvidesk.tickets import Tickets

>>> yesterday = date.today() - timedelta(days=1)
>>> tickets = Tickets(token="my_token")
>>> ticket_properties = tickets.get_properties()
>>> my_query = (
...    tickets.query()
...    .filter(ticket_properties["lastUpdate"] >= yesterday)
...    .select("id")
...    .top(5)
... )
>>> for ticket in my_query:
...     print(ticket)
... <Model for Ticket(id=2336)>
... <Model for Ticket(id=3139)>
... <Model for Ticket(id=3807)>
... <Model for Ticket(id=3822)>
... <Model for Ticket(id=3843)>

--------------------------------------------------------------------------

>>> from pyvidesk.tickets import Ticket

>>> tickets = Tickets(token="my_token")
>>> ticket = tickets.get_empty_model()
>>> print(ticket)
... <Model for Ticket()>
"""


from .exceptions import (
    PyvideskCannotSetReadOnlyProperty,
    PyvideskPropertyNotValidError,
    PyvideskPropertyWithWrongType,
    PyvideskSaveWithoutIdError,
)
from .properties import ComplexProperty


class Model:
    """
    Classe que modela um objeto da entity.

    Exemplo de uso:

    >>> from datetime import date
    >>> from pyvidesk.tickets import Tickets

    >>> tickets = Tickets("my_token")
    >>> today = date.today()
    >>> ticket = tickets.get_by_id(3)
    >>> for action in ticket.actions:
    ...     for appointment in action.timeAppointments:
    ...         appointment.date = today
    >>> ticket.save()

    -------------------------------------------------------------------------

    >>> from pyvidesk.persons import Persons

    >>> persons = Persons("my_token")
    >>> person = persons.get_by_id(1)
    >>> person.delete()
    """

    __is_complex__ = False

    def __init__(self, entity, name_=None, **properties):
        """
        Args:
            entity (): Objeto que representa a entidade do modelo. Aqui, entidade pode ser
                tanto Tickets, Persons e Services, como as propriedades complexas dessas
                entidades. Assim, conseguimos acessar os valores das propriedades complexas
                na forma de atributos;
            name_ (str): O nome da entidade. Importante para propriedades complexas.
            properties (kwargs): As propriedades e valores obtidos pela query.


            _state (dict): Representa o estado da query no servidor do Movidesk.
        """
        self._entity = entity
        self._entity_properties = self._entity.get_properties(
            as_model=self.__is_complex__
        )
        self._properties = properties
        self._name = name_
        self._state = dict()

        for prop, prop_value in self._properties.items():
            try:
                property_obj = self._entity_properties[prop]
            except KeyError:
                self._state[
                    prop
                ] = "Propriedade ainda não suportada por esta biblioteca."
                continue

            if isinstance(property_obj, ComplexProperty):
                if isinstance(prop_value, dict):
                    self._state[prop] = _ComplexPropertyModel(
                        entity=property_obj,
                        name_=prop,
                        **prop_value,
                    )
                if isinstance(prop_value, list):
                    self._state[prop] = []
                    for values in prop_value:
                        self._state[prop].append(
                            _ComplexPropertyModel(
                                entity=property_obj,
                                name_=prop[:-1],
                                **values,
                            )
                        )
                continue
            self._state[prop] = property_obj.deserialize(value=prop_value)

    def __repr__(self):
        if "id" in self._properties:
            properties_text = f"id={self._properties['id']}"
        else:
            properties_text = ", ".join(
                [
                    f"{prop}={prop_value}"
                    for prop, prop_value in self._properties.items()
                ]
            )
        name = self._name or self._entity.__class__.__name__[:-1]
        return f"<{self.__class__.__name__} for {name}({properties_text})>"

    def __setattr__(self, attr, value):
        if attr in (
            "_entity",
            "_entity_properties",
            "_properties",
            "_name",
            "_state",
        ):
            super().__setattr__(attr, value)
            return

        if attr not in self._entity_properties:
            raise PyvideskPropertyNotValidError(param=attr, class_=self._entity)

        if not isinstance(value, self._entity_properties[attr].alias):
            raise PyvideskPropertyWithWrongType(
                param=self._entity_properties[attr].full_name,
                value=value,
                correct_type=self._entity_properties[attr].alias,
            )

        if self._entity_properties[attr].is_read_only:
            raise PyvideskCannotSetReadOnlyProperty(
                f"{self._entity_properties[attr].full_name} é uma propriedade "
                "que permite apenas leitura!"
            )

        super().__setattr__(attr, value)

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return getattr(self, attr)
        try:
            return self._state[attr]
        except KeyError as wrong_property:
            if attr in self._entity_properties:
                entity = self._entity_properties[attr]
                if isinstance(entity, ComplexProperty):
                    self._state[attr] = _EmptyComplexPropertyModel(
                        entity=entity,
                        name_=attr,
                    )
                    return self._state[attr]
                return
            raise PyvideskPropertyNotValidError(
                param=attr, class_=self._entity
            ) from wrong_property

    @property
    def _state_raw(self):
        """
        Metodo que retorna o estado do modelo no formato JSON. Útil para o método save().
        """
        state_raw = dict()
        for prop, prop_value in self._state.items():
            if isinstance(prop_value, Model):
                state_raw[prop] = prop_value._state
            elif _is_list_of_complex_propeties(prop_value, class_=self.__class__):
                state_raw[prop] = []
                for p in prop_value:
                    state_raw[prop].append(p._state_raw)
            else:
                state_raw[prop] = prop_value
        return state_raw

    def _get_changes(self):
        """
        Metodo que obtem as mudancas de 'primeiro nivel'.
        Ou seja, esse metodo nao obtem as mudancas em propriedades complexas.
        """
        changes = dict()
        for prop, prop_value in self.__dict__.items():
            if prop in self._entity_properties:
                if prop in self._state:
                    if prop_value != self._state.get(prop, prop_value):
                        changes[prop] = self.__dict__[prop]
                else:
                    changes[prop] = self.__dict__[prop]
        return changes

    def _get_all_changes(self):
        """
        Metodo que obtem todas as mudancas do modelo, incluindo as propriedades complexas.
        """
        changes = self._get_changes()
        for prop, prop_value in self._state.items():
            if prop in self._entity_properties:
                if isinstance(prop_value, Model):
                    _changes = prop_value._get_changes()
                    if _changes:
                        changes[prop] = _changes
                        continue

                if _is_list_of_complex_propeties(prop_value, class_=self.__class__):
                    _changes = _get_changes_on_children_properties(prop_value)
                    if _changes:
                        changes[prop] = _changes
                        continue

                if prop in self._state:
                    if prop_value != self._state.get(prop, prop_value):
                        changes[prop] = self.__dict__[prop]
                else:
                    changes[prop] = self.__dict__[prop]
        return changes

    def _do_change(self, prop_name, prop_changes):
        """
        Metodo que prepara as mudancas para a requisicao PATCH e realiza
        tais mudancas no modelo.

        Essas mudancas afetam apenas o atributo _state, logo, se chamarmos o metodo
        raw() ainda obteremos os valores do modelo sem as mudancas.

        Apos a conclusao do metodo save(), raw() retorna os valores com as mudancas
        implementadas.

        Args:
            prop_name (str): O nome da propriedade;
            prop_changes (str, list, int, datetime, _ComplexProperty): As mudancas da propriedade.
        """
        if _is_list_of_complex_propeties(prop_changes):
            prop_models = {
                prop_model.id: prop_model for prop_model in self._state[prop_name]
            }
            for prop_change in prop_changes:
                prop_obj = prop_models[prop_change.pop("id")]
                for subprop_name, subprop_change in prop_change.items():
                    prop_obj._do_change(subprop_name, subprop_change)
        else:
            self._state[prop_name] = prop_changes

    def _serialize_all_changes(self):
        """
        Metodo que obtem e prepara (por meio da serializacao dos valores)
        as mudancas para a requisicao PATCH.

        Returns:
            changes (dict): Dicionario com as propriedades que serao alteradas
        """
        changes = dict()

        for prop, prop_changes in self._get_all_changes().items():
            self._do_change(prop, prop_changes)
            prop_value = getattr(self, prop)

            if isinstance(prop_value, Model):
                prop_value = prop_value._state_raw

            if _is_list_of_complex_propeties(prop_value, class_=self.__class__):
                prop_value = [p._state_raw for p in prop_value]
            property_obj = self._entity_properties[prop]
            changes[prop] = property_obj.serialize(value=prop_value)

        return changes

    def get_properties(self):
        return self._entity.get_properties()

    def save(self):
        """Metodo que salva as alteracoes feitas no modelo"""

        if not self.id:
            raise PyvideskSaveWithoutIdError(
                f"Não é possível atualizar {self.__repr__()}, pois o ID não está definido!"
            )

        changes = self._serialize_all_changes()
        if changes:
            self._entity.api.patch(changes=changes, model_id=self.id)
            model = self._entity.get_by_id(self.id)
            self._properties = model._properties
            self._state = model._state

    def delete(self):
        if not self.id:
            raise PyvideskSaveWithoutIdError(
                f"Não é possível deletar {self.__repr__()}, pois o ID não está definido!"
            )

        self._entity.api.delete(model_id=self.id)
        self._properties = self._state = dict()
        return self._entity.get_empty_model()

    def raw(self):
        """Metodo que retorna o JSON "cru" do modelo"""
        return self._properties


class _ComplexPropertyModel(Model):
    __is_complex__ = True

    def save(self):
        pass

    def delete(self):
        pass


class EmptyModel(Model):
    """
    Classe que retorna um modelo vazio da entidade.
    Deve ser usado na criacao de Tickets, Persons ou Services.

    A principal diferença para a classe Model é que nao checamos se um atributo é
    'readonly' e só checamos se um atributo pertence a entidade quando chamamos o metodo
    create().

    Exemplo:
    >>> from pyvidesk.tickets import Tickets
    >>> tickets = Tickets("meu_token_secreto")
    >>> ticket = tickets.get_empty_model()
    >>> ticket.subject = "Assunto"
    >>> ticket.type = 1
    >>> ticket.serviceFirstLevelId = 190853
    >>> ticket.createdBy.id = "2263751"
    >>> ticket.clients = [{"id": "917910092"}]
    >>> ticket.actions = [{"description": "Descrição", "type": 1}]
    >>> ticket.ownerTeam = "Administradores"
    >>> ticket.owner.id = "2222"
    >>> ticket.create()
    """

    def __setattr__(self, attr, value):
        if attr in (
            "_entity",
            "_entity_properties",
            "_properties",
            "_name",
            "_state",
        ):
            super().__setattr__(attr, value)
            return

        if attr not in self._entity_properties:
            raise PyvideskPropertyNotValidError(param=attr, class_=self._entity)

        if not isinstance(value, self._entity_properties[attr].alias):
            raise PyvideskPropertyWithWrongType(
                param=self._entity_properties[attr].full_name,
                value=value,
                correct_type=self._entity_properties[attr].alias,
            )

        self.__dict__[attr] = value

    def _do_change(self, prop_name, prop_changes):
        """
        Sobscrevendo este método da classe Model.
        """
        self._state[prop_name] = prop_changes

    def create(self):
        """
        Funcao que cria o modelo.

        Returns:
            (pyvidesk.model.Model): Objeto da classe Model que representa o
                modelo criado no servidor.
        """
        changes = self._serialize_all_changes()
        if changes:
            model_id = self._entity.api.post(infos=changes)

        return self._entity.get_by_id(model_id)

    def save(self):
        pass

    def delete(self):
        pass


class _EmptyComplexPropertyModel(EmptyModel):
    __is_complex__ = True

    def create(self):
        pass


def _get_changes_on_children_properties(values):
    """Funcao que obtem as mudancas das propriedades complexas"""
    changes = []
    for property_obj in values:
        _changes = property_obj._get_all_changes()
        changes += [{**_changes, "id": property_obj.id}] if _changes else []
        # O 'id' da propriedade é importante para sabermos em qual modelo aplicar a mudança
    return changes


def _is_list_of_complex_propeties(property_obj, class_=dict):
    return isinstance(property_obj, list) and all(
        isinstance(p, class_) for p in property_obj
    )
