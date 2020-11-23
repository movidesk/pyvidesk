"""
Módulo que implementa operadores lambda do Odata.
http://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part2-url-conventions.html#_Toc31361024
"""


def _lambda_operator_base(string, lambda_operator):
    """
    Funcao base que constroi uma consulta usando um operador lambda do Odata.

    Args:
        string (str): String "cru" que serve de base para construir o operador.
            Ex.: client/id eq '1'
        lambda_operator (str): O operador lambda.

    Returns:
        (str): A consulta.
    """
    properties, operator, *value = string.split()
    value = " ".join(value)
    properties = properties.split("/")
    prop = properties.pop(0)

    return f"{prop}/{lambda_operator}(x: x/{'/'.join(properties)} {operator} {value})"


def Any(string):
    return _lambda_operator_base(string=string, lambda_operator="any")


def All(string):
    return _lambda_operator_base(string=string, lambda_operator="all")


def _nested_lambda_operator_base(string, lambda_operator1, lambda_operator2):
    """
    Funcao base que constroi uma consulta usando dois operadores lambda do Odata.

    Args:
        string (str): String "cru" que serve de base para construir o operador.
            Ex.: customFieldValues/items/customFieldItem eq 'MGSSUSTR6-06R'
        lambda_operator1 (str): O primeiro operador lambda.
        lambda_operator1 (str): O segundo operador lambda.

    Returns:
        (str): A consulta.
    """
    properties, operator, *value = string.split()
    value = " ".join(value)
    p1, p2, p3 = properties.split("/")
    return f"{p1}/{lambda_operator1}(x: x/{p2}/{lambda_operator2}(y: y/{p3} {operator} {value}))"


def AnyAny(string):
    return _nested_lambda_operator_base(
        string=string, lambda_operator1="any", lambda_operator2="any"
    )


def AnyAll(string):
    return _nested_lambda_operator_base(
        string=string, lambda_operator1="any", lambda_operator2="all"
    )


def AllAny(string):
    return _nested_lambda_operator_base(
        string=string, lambda_operator1="all", lambda_operator2="any"
    )


def AllAll(string):
    return _nested_lambda_operator_base(
        string=string, lambda_operator1="all", lambda_operator2="all"
    )
