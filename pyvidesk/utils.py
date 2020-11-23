"""
Módulo com funcoes que são usados em múltiplos módulos desta biblioteca.
"""


def get_property_name(prop):
    try:
        name = prop.name_
    except AttributeError:
        name = prop

    return name
