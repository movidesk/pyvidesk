"""
Módulo com todas as exceções desta biblioteca.
"""


from .config import QUERY_PARAMS


class PyvideskError(Exception):
    pass


class PyvideskRequestsError(PyvideskError):
    """
    Erro quando a requisição acusa um erro antes de retornar uma resposta.
    """

    pass


class PyvideskBadResponseError(PyvideskError):
    """
    Erro quando a resposta acusa um HTTPError por meio do método raise_for_status
    da biblioteca requests.
    """

    pass


class PyvideskSaveWithoutIdError(PyvideskError):
    """
    Erro quando um uma requisição patch é solicitada em um modelo sem o ID definido.

    >>> person = persons.get_by_id("1", select="businessName")
    >>> person.businessName = "Murilo Scarpa Sitonio"
    >>> print(person.id)  # Como setamos a opção select, a query retorna apenas a propriedade
    ...  # 'businessName'. Logo, não sabemos qual o id de 'person' e não conseguimos mandar
    ...  # a reuisição PATCH para o servidor.
    ... None
    >>> person.save()
    ...
    ...
    pyvidesk.exceptions.PyvideskSaveWithoutIdError: ...
    """

    pass


class PyvideskCannotSetReadOnlyProperty(PyvideskError):
    """
    Erro quando tenta-se setar um valor de uma propriedade "somente leitura".

    Exemplo:

    >>> person = persons.get_by_id("1")
    >>> person.id = "2"  # 'id' é uma propriedade que permite apenas leitura
    ...
    ...
    pyvidesk.exceptions.PyvideskCannotSetReadOnlyProperty: ...
    """

    pass


class PyvideskPropertyNotValidError(PyvideskError):
    """
    Erro quando o usuario usa um parametro invalido para uma classe.

    Exemplo:

    >>> from pyvidesk.persons import Persons
    >>> persons = Persons('token')
    >>> persons.get_by_name('my_name')  # A API /persons nao tem uma propriedade 'name'
    >>> # cadastrada no Movidesk
    >>> Traceback (most recent call last):
    ...
    ...
    pyvidesk.exceptions.PyvideskParamNotValidError: ...
    """

    def __init__(self, param, class_):
        message = (
            f"'{param}' não é um parâmetro válido para a classe '{class_.__class__.__name__}'.\n"
            f"Parâmetros aceitos para a classe '{class_.__class__.__name__}': "
            f"{', '.join(class_.get_properties())}."
        )
        super().__init__(message)

    # TODO: suggest a similar param based on name ('userName' in the example above)


class PyvideskPropertyWithWrongType(PyvideskError):
    """
    Erro quando o usuario usa um parametro com um tipo invalido.

    Exemplo:

    >>> from pyvidesk.persons import Persons
    >>> persons = Persons('token')
    >>> persons.get_by_personType('4')
    >>> Traceback (most recent call last):
    ...
    ...
    pyvidesk.exceptions.PyvideskParamWithWrongType: O parâmetro 'personType' não deve ter um
    valor de tipo 'str'. O tipo correto é: 'int'.

    OU

    >>> persons.get_by_personType(4, top='10')
    >>> Traceback (most recent call last):
    ...
    ...
    pyvidesk.exceptions.PyvideskParamWithWrongType: O parâmetro 'top' não deve ter um
    valor de tipo 'str'. O tipo correto é: 'int'.
    """

    def __init__(self, param, value, correct_type):
        if isinstance(correct_type, tuple):
            correct_type = ", ".join([f"'{_type.__name__}'" for _type in correct_type])
        else:
            correct_type = f"'{correct_type.__name__}'"
        message = (
            f"O parâmetro '{param}' não deve ter um valor de tipo '{value.__class__.__name__}'."
            f" O tipo correto é: {correct_type}."
        )
        super().__init__(message)

    # TODO: validade the value itself (personType, for example, must be 1, 2, or 4)


class PyvideskWrongKwargError(PyvideskError):
    """
    Erro quando o usuario usa um 'kwarg' invalido para o metodo.

    Exemplo:

    >>> from pyvidesk.persons import Persons
    >>> persons = Persons('token')
    >>> persons.get_by_personType(4, limit=10)
    >>> Traceback (most recent call last):
    ...
    ...
    pyvidesk.exceptions.PyvideskWrongKwargError: 'limit' não é um 'kwarg' valido para esse mtodo.
    'kwargs' validos: personType, filter, orderby, top, skip, select, expand
    """

    def __init__(self, param, kwarg):
        message = (
            f"'{kwarg}' não é um 'kwarg' valido para esse metodo. 'kwargs' validos: "
            f"{param}, {', '.join(QUERY_PARAMS.keys())}"
        )
        super().__init__(message)


def get_wrong_type_message(param, value, correct_type):
    if isinstance(correct_type, tuple):
        correct_type = ", ".join([f"'{_type.__name__}'" for _type in correct_type])
    else:
        correct_type = f"'{correct_type.__name__}'"
    return (
        f"O parâmetro '{param}' não deve ter um valor de tipo '{value.__class__.__name__}'."
        f" O tipo correto é: {correct_type}."
    )
