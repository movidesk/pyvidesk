import unittest

from pyvidesk import properties
from pyvidesk.persons import Persons
from tests.config import TOKEN


class TestPersons(unittest.TestCase):
    """Classe que testa a classe Persons"""

    persons = Persons(token=TOKEN)
    properties = persons.get_properties()

    def test_property_id(self):
        prop = self.properties["id"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "id")
        self.assertEqual(
            prop.get_description(),
            "Campo Cód. Ref. Identificador único da pessoa. (Alfanumérico)",
        )

    def test_property_codeReferenceAdditional(self):
        prop = self.properties["codeReferenceAdditional"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "codeReferenceAdditional")
        self.assertEqual(
            prop.get_description(),
            (
                "Campo Cód. Ref. Adicional. Identificador não obrigatório, porém único da pessoa. "
                "(Alfanumérico)"
            ),
        )

    def test_property_isActive(self):
        prop = self.properties["isActive"]
        self.assertIsInstance(prop, properties.BooleanProperty)
        self.assertEqual(prop.full_name, "isActive")
        self.assertEqual(
            prop.get_description(),
            ("Campo Pessoa habilitada."),
        )

    def test_property_personType(self):
        prop = self.properties["personType"]
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "personType")
        self.assertEqual(
            prop.get_description(),
            ("Tipo da pessoa. Pessoa = 1, Empresa = 2, Departamento = 4."),
        )

    def test_property_profileType(self):
        prop = self.properties["profileType"]
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "profileType")
        self.assertEqual(
            prop.get_description(),
            ("Tipo do perfil. Agente = 1, Cliente = 2, Agente e Cliente = 3."),
        )

    def test_property_accessProfile(self):
        prop = self.properties["accessProfile"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "accessProfile")
        self.assertEqual(
            prop.get_description(),
            (
                "Campo Perfil de acesso. Deve ser um perfil de acesso já cadastrado no Movidesk. "
                "Se informado um perfil de acesso inválido, o sistema retornará erro. "
                "*Campo obrigatório quando a pessoa é do perfil Agente. Se o perfil for Cliente e "
                "o campo não for informado, será setado o perfil de acesso padrão de cliente."
            ),
        )

    def test_property_corporateName(self):
        prop = self.properties["corporateName"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "corporateName")
        self.assertEqual(
            prop.get_description(),
            (
                "Razão social. *Campo obrigatório quando a "
                "pessoa é do tipo Empresa e o Nome fantasia não foi informado."
            ),
        )

    def test_property_businessName(self):
        prop = self.properties["businessName"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "businessName")
        self.assertEqual(
            prop.get_description(),
            ("Nome fantasia para empresas ou Nome para pessoas e departamentos."),
        )

    def test_property_cpfCnpj(self):
        prop = self.properties["cpfCnpj"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "cpfCnpj")
        self.assertEqual(
            prop.get_description(),
            (
                "CPF (11 dígitos) para pessoas, CNPJ (14 dígitos) para empresas "
                "e inexistente para departamentos."
            ),
        )

    def test_property_userName(self):
        prop = self.properties["userName"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "userName")
        self.assertEqual(
            prop.get_description(),
            (
                "Campo usuário. Deve ser único por domínio. Campo obrigatório quando for "
                "informado um domínio para autenticação diferente que o Movidesk."
            ),
        )

    def test_property_role(self):
        prop = self.properties["role"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "role")
        self.assertEqual(
            prop.get_description(),
            ("Cargo da pessoa. Se informado um cargo inexistente o mesmo será criado."),
        )

    def test_property_bossId(self):
        prop = self.properties["bossId"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "bossId")
        self.assertEqual(
            prop.get_description(),
            ("Id (Cod. Ref.) existente do superior hierárquico da pessoa."),
        )

    def test_property_bossName(self):
        prop = self.properties["bossName"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "bossName")
        self.assertEqual(
            prop.get_description(),
            ("Nome do superior hierárquico (somente leitura)."),
        )

    def test_property_classification(self):
        prop = self.properties["classification"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "classification")
        self.assertEqual(
            prop.get_description(),
            (
                "Classificação da pessoa. Se informada uma classificação inexistente, "
                "a mesma será criada."
            ),
        )

    def test_property_cultureId(self):
        prop = self.properties["cultureId"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "cultureId")
        self.assertEqual(
            prop.get_description(),
            (
                "Idioma da pessoa no padrão CultureCode da Microsoft. "
                "Exemplo para idioma português do Brasil: pt-BR. "
                "*Caso não seja informado, será utilizado o idioma do administrador do sistema."
            ),
        )

    def test_property_timeZoneId(self):
        prop = self.properties["timeZoneId"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "timeZoneId")
        self.assertEqual(
            prop.get_description(),
            (
                "Fuso horário da pessoa no padrão IANA. Exemplo para fuso horário de "
                "Brasília: America/Sao_Paulo. *Caso não seja informado, será utilizado "
                "o fuso horário do administrador do sistema."
            ),
        )

    def test_property_authenticateOn(self):
        prop = self.properties["authenticateOn"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "authenticateOn")
        self.assertEqual(
            prop.get_description(),
            (
                "Caso a autenticação em diretório estiver habilitada e a pessoa se "
                "autentica em um domínio diferente do Movidesk, deve ser informado o "
                "servidor e domínio já cadastrados no sistema. "
                "Ex: hostdomeuservidorad/dominiodomeuservidorad"
            ),
        )

    def test_property_createdDate(self):
        prop = self.properties["createdDate"]
        self.assertIsInstance(prop, properties.DatetimeProperty)
        self.assertEqual(prop.full_name, "createdDate")
        self.assertEqual(
            prop.get_description(),
            (
                "Data da criação da pessoa. Deve ser menor ou igual a data atual. "
                "A data informada deve estar no formato UTC*. "
                "Se o campo não for informado, será populado com a data atual."
            ),
        )

    def test_property_createdBy(self):
        prop = self.properties["createdBy"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "createdBy")
        self.assertEqual(
            prop.get_description(),
            (
                "Cod. Ref. da pessoa que criou a pessoa consultada. Campo somente leitura."
            ),
        )

    def test_property_changedDate(self):
        prop = self.properties["changedDate"]
        self.assertIsInstance(prop, properties.DatetimeProperty)
        self.assertEqual(prop.full_name, "changedDate")
        self.assertEqual(
            prop.get_description(),
            ("Data da ultima alteração da pessoa. Campo somente leitura."),
        )

    def test_property_changedBy(self):
        prop = self.properties["changedBy"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "changedBy")
        self.assertEqual(
            prop.get_description(),
            (
                "Cod. Ref. da pessoa que alterou pela ultima vez a pessoa consultada. "
                "Campo somente leitura."
            ),
        )

    def test_property_observations(self):
        prop = self.properties["observations"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "observations")
        self.assertEqual(
            prop.get_description(),
            ("Observações."),
        )

    def test_property_addresses(self):
        prop = self.properties["addresses"]
        self.assertIsInstance(prop, properties.ComplexProperty)
        self.assertEqual(prop.full_name, "addresses")
        self.assertEqual(
            prop.get_description(),
            ("Lista com os endereços."),
        )

    def test_property_addresses_addressType(self):
        prop = self.properties["addresses"].addressType
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "addresses/addressType")
        self.assertEqual(
            prop.get_description(),
            (
                "Tipo do endereço (Comercial, Residencial, etc). "
                "Se informado um tipo inexistente, o mesmo será criado."
            ),
        )

    def test_property_addresses_country(self):
        prop = self.properties["addresses"].country
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "addresses/country")
        self.assertEqual(
            prop.get_description(),
            ("Nome do país."),
        )

    def test_property_addresses_postalCode(self):
        prop = self.properties["addresses"].postalCode
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "addresses/postalCode")
        self.assertEqual(
            prop.get_description(),
            ("CEP."),
        )

    def test_property_addresses_state(self):
        prop = self.properties["addresses"].state
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "addresses/state")
        self.assertEqual(
            prop.get_description(),
            ("Estado."),
        )

    def test_property_addresses_city(self):
        prop = self.properties["addresses"].city
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "addresses/city")
        self.assertEqual(
            prop.get_description(),
            ("Cidade."),
        )

    def test_property_addresses_district(self):
        prop = self.properties["addresses"].district
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "addresses/district")
        self.assertEqual(
            prop.get_description(),
            ("Bairro."),
        )

    def test_property_addresses_street(self):
        prop = self.properties["addresses"].street
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "addresses/street")
        self.assertEqual(
            prop.get_description(),
            ("Nome da rua ex: Rua Joinville."),
        )

    def test_property_addresses_number(self):
        prop = self.properties["addresses"].number
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "addresses/number")
        self.assertEqual(
            prop.get_description(),
            ("Número."),
        )

    def test_property_addresses_complement(self):
        prop = self.properties["addresses"].complement
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "addresses/complement")
        self.assertEqual(
            prop.get_description(),
            ("Complemento ex: Sala 201."),
        )

    def test_property_addresses_reference(self):
        prop = self.properties["addresses"].reference
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "addresses/reference")
        self.assertEqual(
            prop.get_description(),
            ("Ponto de referência ex: Próximo a universidade."),
        )

    def test_property_addresses_isDefault(self):
        prop = self.properties["addresses"].isDefault
        self.assertIsInstance(prop, properties.BooleanProperty)
        self.assertEqual(prop.full_name, "addresses/isDefault")
        self.assertEqual(
            prop.get_description(),
            (
                "Indicador se esse é o endereço principal da pessoa. "
                "Somente um endereço poderá ser o endereço principal."
            ),
        )

    def test_property_contacts(self):
        prop = self.properties["contacts"]
        self.assertIsInstance(prop, properties.ComplexProperty)
        self.assertEqual(prop.full_name, "contacts")
        self.assertEqual(
            prop.get_description(),
            ("Lista com os contatos."),
        )

    def test_property_contacts_contactType(self):
        prop = self.properties["contacts"].contactType
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "contacts/contactType")
        self.assertEqual(
            prop.get_description(),
            (
                "Tipo do contato ex: (Telefone, Celular, Skype, etc). "
                "Se informado um tipo inexistente, o mesmo será criado."
            ),
        )

    def test_property_contacts_contact(self):
        prop = self.properties["contacts"].contact
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "contacts/contact")
        self.assertEqual(
            prop.get_description(),
            ("Descrição ex: (11) 9999-9999."),
        )

    def test_property_contacts_isDefault(self):
        prop = self.properties["contacts"].isDefault
        self.assertIsInstance(prop, properties.BooleanProperty)
        self.assertEqual(prop.full_name, "contacts/isDefault")
        self.assertEqual(
            prop.get_description(),
            (
                "Indicador se esse é o contato principal da pessoa. "
                "Somente um contato poderá ser o contato principal."
            ),
        )

    def test_property_emails(self):
        prop = self.properties["emails"]
        self.assertIsInstance(prop, properties.ComplexProperty)
        self.assertEqual(prop.full_name, "emails")
        self.assertEqual(
            prop.get_description(),
            ("Lista com os emails."),
        )

    def test_property_emails_emailType(self):
        prop = self.properties["emails"].emailType
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "emails/emailType")
        self.assertEqual(
            prop.get_description(),
            (
                "Tipo do email Ex: (Pessoal, Profissional, etc). "
                "Se informado um tipo inexistente, o mesmo será criado."
            ),
        )

    def test_property_emails_email(self):
        prop = self.properties["emails"].email
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "emails/email")
        self.assertEqual(
            prop.get_description(),
            ("E-mail da pessoa, deve ser válido."),
        )

    def test_property_emails_isDefault(self):
        prop = self.properties["emails"].isDefault
        self.assertIsInstance(prop, properties.BooleanProperty)
        self.assertEqual(prop.full_name, "emails/isDefault")
        self.assertEqual(
            prop.get_description(),
            (
                "Indicador se esse é o e-mail principal da pessoa. "
                "Somente um e-mail poderá ser o endereço de e-mail principal."
            ),
        )

    def test_property_teams(self):
        prop = self.properties["teams"]
        self.assertIsInstance(prop, properties.ArrayProperty)
        self.assertEqual(prop.full_name, "teams")
        self.assertEqual(
            prop.get_description(),
            (
                "Array de strings com o nome das equipes. *Quando o tipo de perfil da pessoa "
                "for Agente, é necessário informar ao menos uma equipe."
            ),
        )

    def test_property_relationships(self):
        prop = self.properties["relationships"]
        self.assertIsInstance(prop, properties.ComplexProperty)
        self.assertEqual(prop.full_name, "relationships")
        self.assertEqual(
            prop.get_description(),
            (
                "Lista com os relacionamentos da pessoa. "
                "Deve haver um único relacionamento por organização. "
                "* Pode ser obrigatório (caso esteja parametrizado para ser) "
                "quando o tipo da pessoa for Pessoa e o tipo de perfil for Cliente."
            ),
        )

    def test_property_relationships_id(self):
        prop = self.properties["relationships"].id
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "relationships/id")
        self.assertEqual(
            prop.get_description(),
            (
                "Id (Cod. ref.) existente da empresa ou departamento ao qual a pessoa pertence. "
                "Para informar hierarquia, deve ser seguido o padrão IdPai/IdFilho. "
                "Para configurar o contrato SLA e os serviços permitidos sem relacionar a "
                "pessoa a alguma organização, não informe esse parâmetro."
            ),
        )

    def test_property_relationships_name(self):
        prop = self.properties["relationships"].name
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "relationships/name")
        self.assertEqual(
            prop.get_description(),
            ("Descrição da hierarquia (Somente leitura)."),
        )

    def test_property_relationships_slaAgreement(self):
        prop = self.properties["relationships"].slaAgreement
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "relationships/slaAgreement")
        self.assertEqual(
            prop.get_description(),
            (
                "Contrato de SLA utilizado pelo cliente. "
                "Deve ser um contrato de SLA já cadastrado no Movidesk. "
                "Se informado um contrato de SLA inválido, o sistema retornará erro."
            ),
        )

    def test_property_relationships_forceChildrenToHaveSomeAgreement(self):
        prop = self.properties["relationships"].forceChildrenToHaveSomeAgreement
        self.assertIsInstance(prop, properties.BooleanProperty)
        self.assertEqual(
            prop.full_name, "relationships/forceChildrenToHaveSomeAgreement"
        )
        self.assertEqual(
            prop.get_description(),
            (
                "Se este valor for informado como verdadeiro, todas as pessoas "
                "ligadas a esta hierarquia obrigatoriamente terão o "
                "mesmo contrato de SLA."
            ),
        )

    def test_property_relationships_allowAllServices(self):
        prop = self.properties["relationships"].allowAllServices
        self.assertIsInstance(prop, properties.BooleanProperty)
        self.assertEqual(prop.full_name, "relationships/allowAllServices")
        self.assertEqual(
            prop.get_description(),
            (
                "Se este valor for verdadeiro, a pessoa terá acesso a todos os "
                "itens do catálogo de serviços. Caso contrário, deverão ser especificados os "
                "serviços para os quais a pessoa terá acesso. *Se este valor não for "
                "informado o mesmo será populado por padrão como verdadeiro."
            ),
        )

    def test_property_relationships_includeInParents(self):
        prop = self.properties["relationships"].includeInParents
        self.assertIsInstance(prop, properties.BooleanProperty)
        self.assertEqual(prop.full_name, "relationships/includeInParents")
        self.assertEqual(
            prop.get_description(),
            (
                "Se este valor for verdadeiro, será incluído esse relacionamento "
                "nas pessoas da organização pai e para desfazer será necessário "
                "remover manualmente esse relacionamento das pessoas da organização pai."
            ),
        )

    def test_property_relationships_loadChildOrganizations(self):
        prop = self.properties["relationships"].loadChildOrganizations
        self.assertIsInstance(prop, properties.BooleanProperty)
        self.assertEqual(prop.full_name, "relationships/loadChildOrganizations")
        self.assertEqual(
            prop.get_description(),
            (
                "Se este valor for verdadeiro, serão incluídos relacionamentos com as "
                "organizações filhas da organização pai e para desfazer será "
                "necessário remover manualmente esses relacionamentos."
            ),
        )

    def test_property_relationships_services(self):
        prop = self.properties["relationships"].services
        self.assertIsInstance(prop, properties.ComplexProperty)
        self.assertEqual(prop.full_name, "relationships/services")
        self.assertEqual(
            prop.get_description(),
            (
                "Lista com os serviços que a pessoa terá acesso. "
                "*Obrigatório informar ao menos um serviço quando o "
                "campo allowAllServices for falso."
            ),
        )

    def test_property_relationships_services_id(self):
        prop = self.properties["relationships"].services.id
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "relationships/services/id")
        self.assertEqual(
            prop.get_description(),
            (
                "Id (Código) do serviço. "
                "O mesmo pode ser obtido na consulta de serviços no website."
            ),
        )

    def test_property_relationships_services_name(self):
        prop = self.properties["relationships"].services.name
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "relationships/services/name")
        self.assertEqual(
            prop.get_description(),
            ("Nome do serviço (Somente leitura)."),
        )

    def test_property_relationships_services_copyToChildren(self):
        prop = self.properties["relationships"].services.copyToChildren
        self.assertIsInstance(prop, properties.BooleanProperty)
        self.assertEqual(prop.full_name, "relationships/services/copyToChildren")
        self.assertEqual(
            prop.get_description(),
            (
                "Se este valor for verdadeiro, será incluído esse serviço para todas "
                "as pessoas ligadas a esta hierarquia. *Se este valor não for "
                "informado o mesmo será populado por padrão como verdadeiro."
            ),
        )

    def test_property_customFieldValues(self):
        prop = self.properties["customFieldValues"]
        self.assertIsInstance(prop, properties.ComplexProperty)
        self.assertEqual(prop.full_name, "customFieldValues")
        self.assertEqual(
            prop.get_description(),
            ("Lista com os valores dos campos adicionais da pessoa."),
        )

    def test_property_customFieldValues_customFieldId(self):
        prop = self.properties["customFieldValues"].customFieldId
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "customFieldValues/customFieldId")
        self.assertEqual(
            prop.get_description(),
            (
                "Id do campo adicional "
                "(pode ser obtido na listagem de campos adicionais no website)."
            ),
        )

    def test_property_customFieldValues_customFieldRuleId(self):
        prop = self.properties["customFieldValues"].customFieldRuleId
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "customFieldValues/customFieldRuleId")
        self.assertEqual(
            prop.get_description(),
            (
                "Id da regra de exibição dos campos adicionais "
                "(pode ser obtido na listagem de regras para exibição no website)."
            ),
        )

    def test_property_customFieldValues_line(self):
        prop = self.properties["customFieldValues"].line
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "customFieldValues/line")
        self.assertEqual(
            prop.get_description(),
            (
                "Número da linha da regra de exibição na tela do ticket. "
                "Quando a regra não permitir a adição de novas linhas deve ser informado "
                "o valor 1 e não devem ser repetidos valores de campos adicionais para o id "
                "da regra em conjunto com o id do campo. Para alterar o valor de um campo "
                "deve ser informada a linha em que ele se encontra. Os campos que estiverem "
                "na base de dados e não forem enviados no corpo da requisição serão excluídos."
            ),
        )

    def test_property_customFieldValues_value(self):
        prop = self.properties["customFieldValues"].value
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "customFieldValues/value")
        self.assertEqual(
            prop.get_description(),
            (
                "Valor texto do campo adicional. *Obrigatório quando o tipo do campo for: "
                "texto de uma linha, texto com várias linhas, texto HTML, expressão regular, "
                "numérico, data, hora, data e hora, e-mail, telefone ou URL. "
                "Os campos de data devem estar em horário *UTC e no formato "
                "YYYY-MM-DDThh:MM:ss.000Z e o campo hora deve ser informado juntamente com "
                "a data fixa '1991-01-01'. O campo numérico deve estar no formato brasileiro, "
                "por exemplo '1.530,75'."
            ),
        )

    def test_property_customFieldValues_items(self):
        prop = self.properties["customFieldValues"].items
        self.assertIsInstance(prop, properties.ComplexProperty)
        self.assertEqual(prop.full_name, "customFieldValues/items")
        self.assertEqual(
            prop.get_description(),
            (
                "Lista de itens. *Obrigatório quando o tipo do campo for: "
                "lista de valores, lista de pessoas, lista de clientes, lista de agentes, "
                "seleção múltipla ou seleção única. Deve ser informado apenas um item "
                "se o campo adicional não permitir seleção múltipla."
            ),
        )

    def test_property_customFieldValues_items_personId(self):
        prop = self.properties["customFieldValues"].items.personId
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "customFieldValues/items/personId")
        self.assertEqual(
            prop.get_description(),
            (
                "Id (Cod. ref.) da empresa, departamento ou pessoa. "
                "*Obrigatório quando o tipo do campo for lista de pessoas."
            ),
        )

    def test_property_customFieldValues_items_clientId(self):
        prop = self.properties["customFieldValues"].items.clientId
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "customFieldValues/items/clientId")
        self.assertEqual(
            prop.get_description(),
            (
                "Id (Cod. ref.) da empresa, departamento ou pessoa. "
                "*Obrigatório quando o tipo do campo for lista de clientes."
            ),
        )

    def test_property_customFieldValues_items_team(self):
        prop = self.properties["customFieldValues"].items.team
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "customFieldValues/items/team")
        self.assertEqual(
            prop.get_description(),
            (
                "Nome da equipe. "
                "*Obrigatório quando o tipo do campo lista de agentes "
                "(o personId pode ser informado para especificar o agente da equipe)."
            ),
        )

    def test_property_customFieldValues_items_customFieldItem(self):
        prop = self.properties["customFieldValues"].items.customFieldItem
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "customFieldValues/items/customFieldItem")
        self.assertEqual(
            prop.get_description(),
            (
                "Nome do item do campo adicional. "
                "*Obrigatório quando o tipo do campo for: "
                "lista de valores, seleção múltipla ou seleção única."
            ),
        )

    def test_property_atAssets(self):
        prop = self.properties["atAssets"]
        self.assertIsInstance(prop, properties.ComplexProperty)
        self.assertEqual(prop.full_name, "atAssets")
        self.assertEqual(
            prop.get_description(),
            ("Lista com os valores dos Ativos."),
        )

    def test_property_atAssets_id(self):
        prop = self.properties["atAssets"].id
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "atAssets/id")
        self.assertEqual(
            prop.get_description(),
            ("Campo Cód. Ref. Identificador único do ativo. (Alfanumérico)"),
        )

    def test_property_atAssets_name(self):
        prop = self.properties["atAssets"].name
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "atAssets/name")
        self.assertEqual(
            prop.get_description(),
            ("Nome do ativo"),
        )

    def test_property_atAssets_label(self):
        prop = self.properties["atAssets"].label
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "atAssets/label")
        self.assertEqual(
            prop.get_description(),
            ("Campo etiqueta (Alfanumérico)"),
        )
