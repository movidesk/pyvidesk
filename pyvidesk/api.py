"""
Módulo que realiza as requisições ao servidor.

A classe API não deve ser utilizada diretamente, e sim apenas por meio das classes
Query (requisição GET), Model (requisição PATCH) e EmptyModel (requisição POST).
"""

from functools import wraps
from re import findall

import requests
from requests.exceptions import RequestException

from .exceptions import PyvideskRequestsError, PyvideskBadResponseError


def catch_requests_errors(func):
    """
    Decorator que checa se há algum problema com a requisição
    antes do envio dos parâmetros ao servidor.

    Raises:
        PyvideskRequestsError
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RequestException as error:
            raise PyvideskRequestsError(str(error)) from error

    return wrapper


def handle_response_error(func):
    """
    Decorator que checa se o Movidesk retornou uma resposta bem sucedida ou não.
    Em caso negativo, uma exceção é mostrada ao usuário.

    Returns:
        response (requests.Response): Objeto que representa a resposta do servidor, se bem sucedida.

    Raises:
        PyvideskBadResponseError
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        try:
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as HTTPError:
            status_code = f"HTTP {response.status_code}"
            message = "None"
            if "application/json" in response.headers.get("content-type", ""):
                error_infos = response.json()
                if isinstance(error_infos, dict):
                    message = error_infos.get("message", message)
                else:
                    message = error_infos

            msg = " | ".join(
                [
                    f"Code: {status_code}",
                    f"Reason: {response.reason}",
                    f"Message: {message}",
                ]
            )
            raise PyvideskBadResponseError(msg) from HTTPError

    return wrapper


class Api:
    """Classe que faz as requisições ao servidor"""

    def __init__(self, base_url):
        """
        Args:
            base_url (str): A URL base que usaremos em todas as consultas
        """
        self.base_url = base_url

    def get(self, options):
        """
        Método que obtem a resposta de uma requisição GET ao servidor, se esta for bem sucedida.

        Args:
            options (dict): Dicionário com informações que serão passadas ao servidor na requisição
                GET.

        Returns:
            (dict): Dicionário com informações da resposta.
        """
        response = self._get(options=options)
        if response.status_code == requests.codes.no_content:
            return
        return response.json()

    @handle_response_error
    @catch_requests_errors
    def _get(self, options):
        """
        Método que realiza a requisição GET de fato.
        """
        return requests.get(url=self._get_url(options=options))

    def patch(self, changes, model_id):
        """
        Método que obtem a resposta de uma requisição PATCH ao servidor, se esta for bem sucedida.

        Args:
            changes (dict): Dicionário com as mudanças que serão aplicadas modelo da entidade.
            model_id (int ou str): O ID do modelo que alteraremos.

        Returns:
            (dict): Dicionário com informações da resposta.
        """
        response = self._patch(changes=changes, model_id=model_id)
        return response.json()

    @handle_response_error
    @catch_requests_errors
    def _patch(self, changes, model_id):
        """
        Método que realiza a requisição PATCH de fato.
        """
        return requests.patch(self._get_url(options={"id": model_id}), json=changes)

    def post(self, infos):
        """
        Método que obtem a resposta de uma requisição POST ao servidor, se esta for bem sucedida.

        Args:
            infos (dict): Dicionário com informações que serão passadas ao servidor na requisição
                POST.

        Returns:
            (int ou str): O ID do modelo criado no servidor.
        """
        response = self._post(infos=infos)
        return response.json()["id"]

    @handle_response_error
    @catch_requests_errors
    def _post(self, infos):
        """
        Método que realiza a requisição POST de fato.
        """
        return requests.post(self.base_url, json=infos)

    def delete(self, model_id):
        """
        Método que obtem a resposta de uma requisição DELETE ao servidor, se esta for bem sucedida.

        Args:
            model_id (int ou str): O ID do modelo que deletaremos.
        """
        if "tickets" in self.base_url:
            raise PyvideskRequestsError("A API 'tickets' não tem um método DELETE!")
        return self._delete(model_id=model_id)

    @handle_response_error
    @catch_requests_errors
    def _delete(self, model_id):
        """
        Método que realiza a requisição DELETE de fato.
        """
        return requests.delete(self._get_url(options={"id": model_id}))

    def _get_url(self, options):
        """
        Método que obtem a URL completa que será utilizad nas requisições.

        Args:
            options (dict): Dicionário com informações que estarão presentes na URL.

        Returns:
            (str): A URL.
        """
        if _is_filtering_only_by_id(options=options):
            return (
                self.base_url
                + "&id="
                + unescape_value(value=options["$filter"].split()[-1])
            )

        return self.base_url + _format_options(options)


def _format_options(options):
    """
    Funcao que obtem as opcoes formatadas da URL.

    Args:
        options (dict): Dicionário com informações que estarão presentes na URL.

    Returns:
        (str): As opções formatadas.
    """
    _options = "&".join(
        [
            "=".join((key, str(value)))
            for key, value in options.items()
            if value is not None
        ]
    )
    if _options:
        return "&" + _options
    return ""


def _is_filtering_only_by_id(options):
    """
    Funcao que checa se a query tem como unico filtro o ID de uma entidade.

    Args:
        options (str): As opções da query.

    Returns:
        (bool): Verdadeiro, se o unico filtro é na propriedade ID. False, do contrário.
    """
    if "$select" in options:
        return False

    filter_ = options.get("$filter")
    try:
        prop, operator, _ = filter_.split()
        if prop == "id" and operator == "eq":
            return True
        return False
    except (AttributeError, ValueError):
        return False


def unescape_value(value):
    _value = findall(r"\'(.+?)\'", value)
    if _value:
        return _value[0]
    return value
