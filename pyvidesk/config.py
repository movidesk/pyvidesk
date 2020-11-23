"""
Módulo com algumas constantes de configuração
"""

from .properties import PropertyBase

MAIN_URL = "https://api.movidesk.com/public/v1/"

QUERY_PARAMS = {
    "orderby": (str, tuple, list, PropertyBase),
    "top": int,
    "skip": int,
    "select": (str, tuple, list, PropertyBase),
    "expand": (str, tuple, list, PropertyBase),
}
