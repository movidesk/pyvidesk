"""
pyvidesk module
"""
from .persons import Persons
from .services import Services
from .tickets import Tickets

__version__ = "0.0.1"


class Pyvidesk:
    """Classe que permite chamar qualquer entity já desenvolvida nesta biblioteca"""

    def __init__(self, token):
        self.token = token

    @property
    def tickets(self):
        """Retorna um objeto de tickets do pyvidesk"""
        return Tickets(token=self.token)

    @property
    def persons(self):
        """Retorna um objeto de persons do pyvidesk"""
        return Persons(token=self.token)

    @property
    def services(self):
        """Retorna um objeto de services do pyvidesk"""
        return Services(token=self.token)

    # TODO: questions and answers
    # @property
    # def survey(self):
    #    """Returns a pyvidesk survey object"""
    #    from pyvidesk.survey import Survey
    #
    #    return Survey(token=self.token)

    # TODO:
    # @property
    # def activities(self):
    #    """Returns a pyvidesk activities object"""
    #    from pyvidesk.activities import Activities
    #
    #    return Activities(token=self.token)

    # TODO:
    # @property
    # def contracts(self):
    #    """Returns a pyvidesk contracts object"""
    #    from pyvidesk.contracts import Contracts
    #
    #    return Contracts(token=self.token)
