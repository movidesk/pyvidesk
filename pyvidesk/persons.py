"""
Módulo de definições da entidade Persons do Movidesk.
Para uma descrição da entidade:

>>> from pyvidesk.persons import Persons

>>> persons = Persons(token="my_token")
>>> persons.describe()
"""


from dataclasses import dataclass, field
from urllib.parse import urljoin

from .config import MAIN_URL
from .entity import Entity
from .properties import (
    ArrayProperty,
    BooleanProperty,
    ComplexProperty,
    CustomFieldValues,
    DatetimeProperty,
    IntegerProperty,
    StringProperty,
)


@dataclass
class Addresses(ComplexProperty):
    """
    Pessoas » Endereços

    Classe que representa os endereços da pessoa.
    """

    properties: dict = field(
        default_factory=lambda: {
            "addressType": {
                "property": StringProperty,
                "description": (
                    "Tipo do endereço (Comercial, Residencial, etc). "
                    "Se informado um tipo inexistente, o mesmo será criado."
                ),
                "readOnly": False,
            },
            "country": {
                "property": StringProperty,
                "description": "Nome do país.",
                "readOnly": False,
            },
            "postalCode": {
                "property": StringProperty,
                "description": "CEP.",
                "readOnly": False,
            },
            "state": {
                "property": StringProperty,
                "description": "Estado.",
                "readOnly": False,
            },
            "city": {
                "property": StringProperty,
                "description": "Cidade.",
                "readOnly": False,
            },
            "district": {
                "property": StringProperty,
                "description": "Bairro.",
                "readOnly": False,
            },
            "street": {
                "property": StringProperty,
                "description": "Nome da rua ex: Rua Joinville.",
                "readOnly": False,
            },
            "number": {
                "property": StringProperty,
                "description": "Número.",
                "readOnly": False,
            },
            "complement": {
                "property": StringProperty,
                "description": "Complemento ex: Sala 201.",
                "readOnly": False,
            },
            "reference": {
                "property": StringProperty,
                "description": "Ponto de referência ex: Próximo a universidade.",
                "readOnly": False,
            },
            "isDefault": {
                "property": BooleanProperty,
                "description": (
                    "Indicador se esse é o endereço principal da pessoa. "
                    "Somente um endereço poderá ser o endereço principal."
                ),
                "readOnly": False,
            },
        }
    )


@dataclass
class Contacts(ComplexProperty):
    """
    Pessoas » Contatos

    Classe que representa os contatos da pessoa.
    """

    properties: dict = field(
        default_factory=lambda: {
            "contactType": {
                "property": StringProperty,
                "description": (
                    "Tipo do contato ex: (Telefone, Celular, Skype, etc). "
                    "Se informado um tipo inexistente, o mesmo será criado."
                ),
                "readOnly": False,
            },
            "contact": {
                "property": StringProperty,
                "description": "Descrição ex: (11) 9999-9999.",
                "readOnly": False,
            },
            "isDefault": {
                "property": BooleanProperty,
                "description": (
                    "Indicador se esse é o contato principal da pessoa. "
                    "Somente um contato poderá ser o contato principal."
                ),
                "readOnly": False,
            },
        }
    )


@dataclass
class Emails(ComplexProperty):
    """
    Pessoas » Emails

    Classe que representa os emails da pessoa.
    """

    properties: dict = field(
        default_factory=lambda: {
            "emailType": {
                "property": StringProperty,
                "description": (
                    "Tipo do email Ex: (Pessoal, Profissional, etc). "
                    "Se informado um tipo inexistente, o mesmo será criado."
                ),
                "readOnly": False,
            },
            "email": {
                "property": StringProperty,
                "description": "E-mail da pessoa, deve ser válido.",
                "readOnly": False,
            },
            "isDefault": {
                "property": BooleanProperty,
                "description": (
                    "Indicador se esse é o e-mail principal da pessoa. "
                    "Somente um e-mail poderá ser o endereço de e-mail principal."
                ),
                "readOnly": False,
            },
        }
    )


@dataclass
class RelationshipsServices(ComplexProperty):
    """
    Pessoas » Organização » Serviços

    Classe que representa os serviços de um relacionamento da pessoa.
    """

    properties: dict = field(
        default_factory=lambda: {
            "id": {
                "property": IntegerProperty,
                "description": (
                    "Id (Código) do serviço. O mesmo pode ser obtido na consulta "
                    "de serviços no website."
                ),
                "readOnly": False,
            },
            "name": {
                "property": StringProperty,
                "description": "Nome do serviço (Somente leitura).",
                "readOnly": True,
            },
            "copyToChildren": {
                "property": BooleanProperty,
                "description": (
                    "Se este valor for verdadeiro, será incluído esse serviço para todas "
                    "as pessoas ligadas a esta hierarquia. *Se este valor não for informado "
                    "o mesmo será populado por padrão como verdadeiro."
                ),
                "readOnly": False,
            },
        }
    )


@dataclass
class Relationships(ComplexProperty):
    """
    Pessoas » Organizações

    Classe que representa os relacionamentos da pessoa.
    """

    properties: dict = field(
        default_factory=lambda: {
            "id": {
                "property": StringProperty,
                "description": (
                    "Id (Cod. ref.) existente da empresa ou departamento ao qual a "
                    "pessoa pertence. Para informar hierarquia, deve ser seguido o "
                    "padrão IdPai/IdFilho. Para configurar o contrato SLA e os serviços "
                    "permitidos sem relacionar a pessoa a alguma organização, "
                    "não informe esse parâmetro."
                ),
                "readOnly": False,
            },
            "name": {
                "property": StringProperty,
                "description": "Descrição da hierarquia (Somente leitura).",
                "readOnly": True,
            },
            "slaAgreement": {
                "property": StringProperty,
                "description": (
                    "Contrato de SLA utilizado pelo cliente. Deve ser um contrato de SLA "
                    "já cadastrado no Movidesk. Se informado um contrato de SLA inválido, "
                    "o sistema retornará erro."
                ),
                "readOnly": False,
            },
            "forceChildrenToHaveSomeAgreement": {
                "property": BooleanProperty,
                "description": (
                    "Se este valor for informado como verdadeiro, todas as pessoas "
                    "ligadas a esta hierarquia obrigatoriamente terão o mesmo contrato de SLA."
                ),
                "readOnly": False,
            },
            "allowAllServices": {
                "property": BooleanProperty,
                "description": (
                    "Se este valor for verdadeiro, a pessoa terá acesso a todos os itens do "
                    "catálogo de serviços. Caso contrário, deverão ser especificados os serviços "
                    "para os quais a pessoa terá acesso. *Se este valor não for informado o mesmo "
                    "será populado por padrão como verdadeiro."
                ),
                "readOnly": False,
            },
            "includeInParents": {
                "property": BooleanProperty,
                "description": (
                    "Se este valor for verdadeiro, será incluído esse relacionamento nas pessoas "
                    "da organização pai e para desfazer será necessário remover manualmente esse "
                    "relacionamento das pessoas da organização pai."
                ),
                "readOnly": False,
            },
            "loadChildOrganizations": {
                "property": BooleanProperty,
                "description": (
                    "Se este valor for verdadeiro, serão incluídos relacionamentos com as "
                    "organizações filhas da organização pai e para desfazer será necessário "
                    "remover manualmente esses relacionamentos."
                ),
                "readOnly": False,
            },
            "services": {
                "property": RelationshipsServices,
                "description": (
                    "Lista com os serviços que a pessoa terá acesso. "
                    "*Obrigatório informar ao menos um serviço quando o "
                    "campo allowAllServices for falso."
                ),
                "readOnly": False,
            },
        }
    )


@dataclass
class AtAssets(ComplexProperty):
    """
    Pessoas » Ativos

    Classe que representa os ativos da pessoa.
    """

    properties: dict = field(
        default_factory=lambda: {
            "id": {
                "property": StringProperty,
                "description": "Campo Cód. Ref. Identificador único do ativo. (Alfanumérico)",
                "readOnly": False,
            },
            "name": {
                "property": StringProperty,
                "description": "Nome do ativo",
                "readOnly": False,
            },
            "label": {
                "property": StringProperty,
                "description": "Campo etiqueta (Alfanumérico)",
                "readOnly": False,
            },
        }
    )


PARAMS = {
    "id": {
        "property": StringProperty,
        "description": "Campo Cód. Ref. Identificador único da pessoa. (Alfanumérico)",
        "readOnly": False,
    },
    "codeReferenceAdditional": {
        "property": StringProperty,
        "description": (
            "Campo Cód. Ref. Adicional. Identificador não obrigatório, "
            "porém único da pessoa. (Alfanumérico)"
        ),
        "readOnly": False,
    },
    "isActive": {
        "property": BooleanProperty,
        "description": "Campo Pessoa habilitada.",
        "readOnly": False,
    },
    "personType": {
        "property": IntegerProperty,
        "description": "Tipo da pessoa. Pessoa = 1, Empresa = 2, Departamento = 4.",
        "readOnly": False,
    },
    "profileType": {
        "property": IntegerProperty,
        "description": "Tipo do perfil. Agente = 1, Cliente = 2, Agente e Cliente = 3.",
        "readOnly": False,
    },
    "accessProfile": {
        "property": StringProperty,
        "description": (
            "Campo Perfil de acesso. Deve ser um perfil de acesso já cadastrado no Movidesk. "
            "Se informado um perfil de acesso inválido, o sistema retornará erro. "
            "*Campo obrigatório quando a pessoa é do perfil Agente. Se o perfil for Cliente e o "
            "campo não for informado, será setado o perfil de acesso padrão de cliente."
        ),
        "readOnly": False,
    },
    "corporateName": {
        "property": StringProperty,
        "description": (
            "Razão social. *Campo obrigatório quando a pessoa é do tipo "
            "Empresa e o Nome fantasia não foi informado."
        ),
        "readOnly": False,
    },
    "businessName": {
        "property": StringProperty,
        "description": "Nome fantasia para empresas ou Nome para pessoas e departamentos.",
        "readOnly": False,
    },
    "cpfCnpj": {
        "property": StringProperty,
        "description": (
            "CPF (11 dígitos) para pessoas, CNPJ (14 dígitos) para empresas "
            "e inexistente para departamentos."
        ),
        "readOnly": False,
    },
    "userName": {
        "property": StringProperty,
        "description": (
            "Campo usuário. Deve ser único por domínio. Campo obrigatório quando "
            "for informado um domínio para autenticação diferente que o Movidesk."
        ),
        "readOnly": False,
    },
    "role": {
        "property": StringProperty,
        "description": "Cargo da pessoa. Se informado um cargo inexistente o mesmo será criado.",
        "readOnly": False,
    },
    "bossId": {
        "property": StringProperty,
        "description": "Id (Cod. Ref.) existente do superior hierárquico da pessoa.",
        "readOnly": False,
    },
    "bossName": {
        "property": StringProperty,
        "description": "Nome do superior hierárquico (somente leitura).",
        "readOnly": True,
    },
    "classification": {
        "property": StringProperty,
        "description": (
            "Classificação da pessoa. Se informada uma classificação inexistente, "
            "a mesma será criada."
        ),
        "readOnly": False,
    },
    "cultureId": {
        "property": StringProperty,
        "description": (
            "Idioma da pessoa no padrão CultureCode da Microsoft. Exemplo para idioma português do "
            "Brasil: pt-BR. *Caso não seja informado, será utilizado o idioma do "
            "administrador do sistema."
        ),
        "readOnly": False,
    },
    "timeZoneId": {
        "property": StringProperty,
        "description": (
            "Fuso horário da pessoa no padrão IANA. Exemplo para fuso horário de Brasília: "
            "America/Sao_Paulo. *Caso não seja informado, será utilizado o fuso horário do "
            "administrador do sistema."
        ),
        "readOnly": False,
    },
    "authenticateOn": {
        "property": StringProperty,
        "description": (
            "Caso a autenticação em diretório estiver habilitada e a pessoa se autentica em "
            "um domínio diferente do Movidesk, deve ser informado o servidor e domínio já "
            "cadastrados no sistema. Ex: hostdomeuservidorad/dominiodomeuservidorad"
        ),
        "readOnly": False,
    },
    "createdDate": {
        "property": DatetimeProperty,
        "description": (
            "Data da criação da pessoa. Deve ser menor ou igual a data atual. "
            "A data informada deve estar no formato UTC*. Se o campo não for informado, "
            "será populado com a data atual."
        ),
        "readOnly": False,
    },
    "createdBy": {
        "property": StringProperty,
        "description": "Cod. Ref. da pessoa que criou a pessoa consultada. Campo somente leitura.",
        "readOnly": True,
    },
    "changedDate": {
        "property": DatetimeProperty,
        "description": "Data da ultima alteração da pessoa. Campo somente leitura.",
        "readOnly": True,
    },
    "changedBy": {
        "property": StringProperty,
        "description": (
            "Cod. Ref. da pessoa que alterou pela ultima vez a pessoa consultada. "
            "Campo somente leitura."
        ),
        "readOnly": True,
    },
    "observations": {
        "property": StringProperty,
        "description": "Observações.",
        "readOnly": False,
    },
    "addresses": {
        "property": Addresses,
        "description": "Lista com os endereços.",
        "readOnly": False,
    },
    "contacts": {
        "property": Contacts,
        "description": "Lista com os contatos.",
        "readOnly": False,
    },
    "emails": {
        "property": Emails,
        "description": "Lista com os emails.",
        "readOnly": False,
    },
    "teams": {
        "property": ArrayProperty,
        "description": (
            "Array de strings com o nome das equipes. *Quando o tipo de perfil da pessoa for "
            "Agente, é necessário informar ao menos uma equipe."
        ),
        "readOnly": False,
    },
    "relationships": {
        "property": Relationships,
        "description": (
            "Lista com os relacionamentos da pessoa. Deve haver um único relacionamento por "
            "organização. * Pode ser obrigatório (caso esteja parametrizado para ser) quando o "
            "tipo da pessoa for Pessoa e o tipo de perfil for Cliente."
        ),
        "readOnly": False,
    },
    "customFieldValues": {
        "property": CustomFieldValues,
        "description": "Lista com os valores dos campos adicionais da pessoa.",
        "readOnly": False,
    },
    "atAssets": {
        "property": AtAssets,
        "description": "Lista com os valores dos Ativos.",
        "readOnly": False,
    },
}


class Persons(Entity):
    BASE_URL = urljoin(MAIN_URL, "persons")
    VALID_PARAMS = PARAMS
