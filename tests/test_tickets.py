import unittest

from pyvidesk import properties
from pyvidesk.tickets import Tickets
from tests.config import TOKEN


class TestTickets(unittest.TestCase):
    """Classe que testa a classe Tickets"""

    tickets = Tickets(token=TOKEN)
    properties = tickets.get_properties()

    def test_property_id(self):
        prop = self.properties["id"]
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "id")
        self.assertEqual(
            prop.get_description(),
            "Número do ticket ou número do protocolo (somente leitura).",
        )

    def test_property_type(self):
        prop = self.properties["type"]
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "type")
        self.assertEqual(
            prop.get_description(),
            "Tipo do ticket. 1 = Interno 2 = Público.",
        )

    def test_property_subject(self):
        prop = self.properties["subject"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "subject")
        self.assertEqual(
            prop.get_description(),
            "Assunto do ticket.",
        )

    def test_property_category(self):
        prop = self.properties["category"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "category")
        self.assertEqual(
            prop.get_description(),
            (
                "Nome da categoria do ticket. Deve ser informada uma categoria existente e que "
                "esteja relacionada ao tipo e ao serviço (caso este esteja informado) do ticket."
            ),
        )

    def test_property_urgency(self):
        prop = self.properties["urgency"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "urgency")
        self.assertEqual(
            prop.get_description(),
            (
                "Nome da urgência do ticket. Deve ser informada uma urgência existente e que "
                "esteja relacionada a categoria (caso esta esteja informada no ticket)."
            ),
        )

    def test_property_status(self):
        prop = self.properties["status"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "status")
        self.assertEqual(
            prop.get_description(),
            (
                "Nome do status do ticket. Para alterar esse campo deve ser também informada "
                "a justificativa. O status deve ser um existente e que esteja relacionado ao tipo "
                "do ticket. *Caso não informado, será utilizado o status base Novo padrão."
            ),
        )

    def test_property_baseStatus(self):
        prop = self.properties["baseStatus"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "baseStatus")
        self.assertEqual(
            prop.get_description(),
            (
                "Nome do status base do ticket (Somente leitura)."
                "\n\tNew,"
                "\n\tInAttendance,"
                "\n\tStopped,"
                "\n\tCanceled,"
                "\n\tResolved,"
                "\n\tClosed"
            ),
        )

    def test_property_justification(self):
        prop = self.properties["justification"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "justification")
        self.assertEqual(
            prop.get_description(),
            (
                "Nome da justificativa do ticket. Deve ser informada uma "
                "justificativa existente que esteja relacionada ao status do ticket. "
                "O preenchimento desse campo é obrigatório quando o status do ticket o exigir. "
                "Para alterar esse campo deve ser também informado o status."
            ),
        )

    def test_property_origin(self):
        prop = self.properties["origin"]
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "origin")
        self.assertEqual(
            prop.get_description(),
            (
                "Canal de abertura do ticket (Somente leitura)."
                "\n\t1 Via web pelo cliente"
                "\n\t2 Via web pelo agente"
                "\n\t3 Recebido via email"
                "\n\t4 Gatilho do sistema"
                "\n\t5 Chat (online)"
                "\n\t6 Chat (offline)"
                "\n\t7 Email enviado pelo sistema"
                "\n\t8 Formulário de contato"
                "\n\t9 Via web API"
                "\n\t10 Agendamento automático "
                "\n\t11 JiraIssue"
                "\n\t12 RedmineIssue"
                "\n\t13 ReceivedCall"
                "\n\t14 MadeCall"
                "\n\t15 LostCall"
                "\n\t16 DropoutCall"
                "\n\t17 Acesso remoto"
                "\n\t18 WhatsApp"
                "\n\t19 MovideskIntegration"
                "\n\t20 ZenviaChat"
                "\n\t21 NotAnsweredCall"
                "\n\t23 WhatsApp Business Movidesk"
            ),
        )

    def test_property_createdDate(self):
        prop = self.properties["createdDate"]
        self.assertIsInstance(prop, properties.DatetimeProperty)
        self.assertEqual(prop.full_name, "createdDate")
        self.assertEqual(
            prop.get_description(),
            (
                "Data de abertura do ticket. A data informada deve estar no formato UTC*. "
                "*Caso não for informada, será preenchida com a data atual."
            ),
        )

    def test_property_originEmailAccount(self):
        prop = self.properties["originEmailAccount"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "originEmailAccount")
        self.assertEqual(
            prop.get_description(),
            ("Conta de e-mail na qual o ticket foi recebido (Somente leitura)."),
        )

    def test_property_owner(self):
        prop = self.properties["owner"]
        self.assertIsInstance(prop, properties.ComplexProperty)
        self.assertEqual(prop.full_name, "owner")
        self.assertEqual(
            prop.get_description(),
            (
                "Dados do responsável pelo ticket. Para alterar esse campo deve ser "
                "informada também a equipe do responsável pelo ticket."
            ),
        )

    def test_property_owner_id(self):
        prop = self.properties["owner"].id
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "owner/id")
        self.assertEqual(
            prop.get_description(),
            (
                "Id (Cod. ref.) da organização (Somente leitura, entretanto para "
                "'ticket.clients[n].organization' esse campo é configurável)."
            ),
        )

    def test_property_owner_businessName(self):
        prop = self.properties["owner"].businessName
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "owner/businessName")
        self.assertEqual(
            prop.get_description(),
            ("Nome da organização (Somente leitura)."),
        )

    def test_property_owner_email(self):
        prop = self.properties["owner"].email
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "owner/email")
        self.assertEqual(
            prop.get_description(),
            ("E-mail principal da organização (Somente leitura)."),
        )

    def test_property_owner_phone(self):
        prop = self.properties["owner"].phone
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "owner/phone")
        self.assertEqual(
            prop.get_description(),
            ("Telefone principal da organização (Somente leitura)."),
        )

    def test_property_owner_personType(self):
        prop = self.properties["owner"].personType
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "owner/personType")
        self.assertEqual(
            prop.get_description(),
            (
                "Tipo da pessoa: Pessoa = 1, Empresa = 2, Departamento = 4 (Somente leitura)."
            ),
        )

    def test_property_owner_profileType(self):
        prop = self.properties["owner"].profileType
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "owner/profileType")
        self.assertEqual(
            prop.get_description(),
            (
                "Perfil da pessoa: Agente = 1, Cliente = 2, Agente e Cliente = 3 (Somente leitura)."
            ),
        )

    def test_property_ownerTeam(self):
        prop = self.properties["ownerTeam"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "ownerTeam")
        self.assertEqual(
            prop.get_description(),
            (
                "Equipe do responsável pelo ticket. Para alterar esse campo deve ser "
                "informado também o responsável pelo ticket. Caso o responsável pelo ticket esteja "
                "informado, a equipe do responsável deve estar associada a ele."
            ),
        )

    def test_property_createdBy(self):
        prop = self.properties["createdBy"]
        self.assertIsInstance(prop, properties.ComplexProperty)
        self.assertEqual(prop.full_name, "createdBy")
        self.assertEqual(
            prop.get_description(),
            ("Dados do gerador do ticket."),
        )

    def test_property_createdBy_id(self):
        prop = self.properties["createdBy"].id
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "createdBy/id")
        self.assertEqual(
            prop.get_description(),
            (
                "Id (Cod. ref.) da organização (Somente leitura, entretanto para "
                "'ticket.clients[n].organization' esse campo é configurável)."
            ),
        )

    def test_property_createdBy_businessName(self):
        prop = self.properties["createdBy"].businessName
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "createdBy/businessName")
        self.assertEqual(
            prop.get_description(),
            ("Nome da organização (Somente leitura)."),
        )

    def test_property_createdBy_email(self):
        prop = self.properties["createdBy"].email
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "createdBy/email")
        self.assertEqual(
            prop.get_description(),
            ("E-mail principal da organização (Somente leitura)."),
        )

    def test_property_createdBy_phone(self):
        prop = self.properties["createdBy"].phone
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "createdBy/phone")
        self.assertEqual(
            prop.get_description(),
            ("Telefone principal da organização (Somente leitura)."),
        )

    def test_property_createdBy_personType(self):
        prop = self.properties["createdBy"].personType
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "createdBy/personType")
        self.assertEqual(
            prop.get_description(),
            (
                "Tipo da pessoa: Pessoa = 1, Empresa = 2, Departamento = 4 (Somente leitura)."
            ),
        )

    def test_property_createdBy_profileType(self):
        prop = self.properties["createdBy"].profileType
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "createdBy/profileType")
        self.assertEqual(
            prop.get_description(),
            (
                "Perfil da pessoa: Agente = 1, Cliente = 2, Agente e Cliente = 3 (Somente leitura)."
            ),
        )

    def test_property_serviceFull(self):
        prop = self.properties["serviceFull"]
        self.assertIsInstance(prop, properties.ArrayProperty)
        self.assertEqual(prop.full_name, "serviceFull")
        self.assertEqual(
            prop.get_description(),
            (
                "Lista com os nomes dos níveis do serviço selecionado no ticket (Somente leitura)."
            ),
        )

    def test_property_serviceFirstLevelId(self):
        prop = self.properties["serviceFirstLevelId"]
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "serviceFirstLevelId")
        self.assertEqual(
            prop.get_description(),
            ("Id (Código) do serviço selecionado no ticket."),
        )

    def test_property_serviceFirstLevel(self):
        prop = self.properties["serviceFirstLevel"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "serviceFirstLevel")
        self.assertEqual(
            prop.get_description(),
            (
                "Nome do primeiro nível do serviço selecionado no ticket (Somente leitura)."
            ),
        )

    def serviceSecondLevel(self):
        prop = self.properties["serviceSecondLevel"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "serviceSecondLevel")
        self.assertEqual(
            prop.get_description(),
            (
                "Nome do segundo nível do serviço selecionado no ticket (Somente leitura)."
            ),
        )

    def test_property_serviceThirdLevel(self):
        prop = self.properties["serviceThirdLevel"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "serviceThirdLevel")
        self.assertEqual(
            prop.get_description(),
            (
                "Nome do terceiro nível do serviço selecionado no ticket (Somente leitura)."
            ),
        )

    def test_property_contactForm(self):
        prop = self.properties["contactForm"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "contactForm")
        self.assertEqual(
            prop.get_description(),
            (
                "Nome do formulário de contato através do qual o ticket foi aberto "
                "(Somente leitura)."
            ),
        )

    def test_property_tags(self):
        prop = self.properties["tags"]
        self.assertIsInstance(prop, properties.ArrayProperty)
        self.assertEqual(prop.full_name, "tags")
        self.assertEqual(
            prop.get_description(),
            (
                "Lista de strings com as TAGs as quais o ticket esta relacionado. "
                "Caso sejam informadas TAGs inexistentes, as mesmas serão adicionadas "
                "na base de dados."
            ),
        )

    def test_property_cc(self):
        prop = self.properties["cc"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "cc")
        self.assertEqual(
            prop.get_description(),
            ("Relação dos e-mails informados no campo Cc, separados por vírgula."),
        )

    def test_property_resolvedIn(self):
        prop = self.properties["resolvedIn"]
        self.assertIsInstance(prop, properties.DatetimeProperty)
        self.assertEqual(prop.full_name, "resolvedIn")
        self.assertEqual(
            prop.get_description(),
            (
                "Data na qual o ticket foi indicado pelo agente como resolvido. "
                "A data informada deve estar no formato UTC."
            ),
        )

    def test_property_reopenedIn(self):
        prop = self.properties["reopenedIn"]
        self.assertIsInstance(prop, properties.DatetimeProperty)
        self.assertEqual(prop.full_name, "reopenedIn")
        self.assertEqual(
            prop.get_description(),
            ("Data na qual o ticket teve a ultima reabertura (Somente leitura)."),
        )

    def test_property_closedIn(self):
        prop = self.properties["closedIn"]
        self.assertIsInstance(prop, properties.DatetimeProperty)
        self.assertEqual(prop.full_name, "closedIn")
        self.assertEqual(
            prop.get_description(),
            (
                "Data na qual o ticket foi indicado como fechado. A data informada "
                "deve estar no formato UTC."
            ),
        )

    def test_property_lastActionDate(self):
        prop = self.properties["lastActionDate"]
        self.assertIsInstance(prop, properties.DatetimeProperty)
        self.assertEqual(prop.full_name, "lastActionDate")
        self.assertEqual(
            prop.get_description(),
            ("Data UTC da última ação do ticket (Somente leitura)."),
        )

    def test_property_actionCount(self):
        prop = self.properties["actionCount"]
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "actionCount")
        self.assertEqual(
            prop.get_description(),
            ("Quantidade de ações do ticket (Somente leitura)."),
        )

    def test_property_lastUpdate(self):
        prop = self.properties["lastUpdate"]
        self.assertIsInstance(prop, properties.DatetimeProperty)
        self.assertEqual(prop.full_name, "lastUpdate")
        self.assertEqual(
            prop.get_description(),
            ("Data UTC da última alteração do ticket (Somente leitura)."),
        )

    def test_property_lifetimeWorkingTime(self):
        prop = self.properties["lifeTimeWorkingTime"]
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "lifeTimeWorkingTime")
        self.assertEqual(
            prop.get_description(),
            (
                "Tempo de vida do ticket em minutos em horas úteis desde a "
                "abertura (Somente leitura)."
            ),
        )

    def test_property_stoppedTime(self):
        prop = self.properties["stoppedTime"]
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "stoppedTime")
        self.assertEqual(
            prop.get_description(),
            (
                "Tempo que o ticket ficou no status parado em minutos em "
                "horas corridas (Somente leitura)."
            ),
        )

    def test_property_stoppedTimeWorkingTime(self):
        prop = self.properties["stoppedTimeWorkingTime"]
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "stoppedTimeWorkingTime")
        self.assertEqual(
            prop.get_description(),
            (
                "Tempo que o ticket ficou no status parado em minutos em "
                "horas úteis (Somente leitura)."
            ),
        )

    def test_property_resolvedInFirstCall(self):
        prop = self.properties["resolvedInFirstCall"]
        self.assertIsInstance(prop, properties.BooleanProperty)
        self.assertEqual(prop.full_name, "resolvedInFirstCall")
        self.assertEqual(
            prop.get_description(),
            (
                "Indicador que representa se o ticket foi resolvido já no "
                "momento da abertura ou num momento posterior (Somente leitura)."
            ),
        )

    def test_property_chatWidget(self):
        prop = self.properties["chatWidget"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "chatWidget")
        self.assertEqual(
            prop.get_description(),
            (
                "Aplicativo de chat através do qual o ticket foi aberto (Somente leitura)."
            ),
        )

    def test_property_chatGroup(self):
        prop = self.properties["chatGroup"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "chatGroup")
        self.assertEqual(
            prop.get_description(),
            ("Grupo de chat através do qual o ticket foi aberto (Somente leitura)."),
        )

    def test_property_chatTalkTime(self):
        prop = self.properties["chatTalkTime"]
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "chatTalkTime")
        self.assertEqual(
            prop.get_description(),
            ("Tempo de duração do chat em segundos (Somente leitura)."),
        )

    def test_property_chatWaitingTime(self):
        prop = self.properties["chatWaitingTime"]
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "chatWaitingTime")
        self.assertEqual(
            prop.get_description(),
            (
                "Tempo que o cliente ficou aguardando para ser atendido em segundos "
                "(Somente leitura)."
            ),
        )

    def test_property_sequence(self):
        prop = self.properties["sequence"]
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "sequence")
        self.assertEqual(
            prop.get_description(),
            ("Número inteiro armazenado no campo Sequência."),
        )

    def test_property_slaAgreement(self):
        prop = self.properties["slaAgreement"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "slaAgreement")
        self.assertEqual(
            prop.get_description(),
            ("Contrato SLA utilizado no ticket (Somente leitura)."),
        )

    def test_property_slaAgreementRule(self):
        prop = self.properties["slaAgreementRule"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "slaAgreementRule")
        self.assertEqual(
            prop.get_description(),
            ("Regra do contrato SLA (Somente leitura)."),
        )

    def test_property_slaSolutionTime(self):
        prop = self.properties["slaSolutionTime"]
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "slaSolutionTime")
        self.assertEqual(
            prop.get_description(),
            ("Tempo de solução do contrato SLA (Somente leitura)."),
        )

    def test_property_slaResponseTime(self):
        prop = self.properties["slaResponseTime"]
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "slaResponseTime")
        self.assertEqual(
            prop.get_description(),
            ("Tempo de resposta do contrato SLA (Somente leitura)."),
        )

    def test_property_slaSolutionChangedByUser(self):
        prop = self.properties["slaSolutionChangedByUser"]
        self.assertIsInstance(prop, properties.BooleanProperty)
        self.assertEqual(prop.full_name, "slaSolutionChangedByUser")
        self.assertEqual(
            prop.get_description(),
            (
                "Indica se o contrato SLA foi manualmente alterado pelo usuário (Somente leitura)."
            ),
        )

    def test_property_slaSolutionChangedBy(self):
        prop = self.properties["slaSolutionChangedBy"]
        self.assertIsInstance(prop, properties.ComplexProperty)
        self.assertEqual(prop.full_name, "slaSolutionChangedBy")
        self.assertEqual(
            prop.get_description(),
            ("Dados da pessoa que alterou o contrato SLA (Somente leitura)."),
        )

    def test_property_slaSolutionChangedBy_id(self):
        prop = self.properties["slaSolutionChangedBy"].id
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "slaSolutionChangedBy/id")
        self.assertEqual(
            prop.get_description(),
            (
                "Id (Cod. ref.) da organização (Somente leitura, entretanto para "
                "'ticket.clients[n].organization' esse campo é configurável)."
            ),
        )

    def test_property_slaSolutionChangedBy_businessName(self):
        prop = self.properties["slaSolutionChangedBy"].businessName
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "slaSolutionChangedBy/businessName")
        self.assertEqual(
            prop.get_description(),
            ("Nome da organização (Somente leitura)."),
        )

    def test_property_slaSolutionChangedBy_email(self):
        prop = self.properties["slaSolutionChangedBy"].email
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "slaSolutionChangedBy/email")
        self.assertEqual(
            prop.get_description(),
            ("E-mail principal da organização (Somente leitura)."),
        )

    def test_property_slaSolutionChangedBy_phone(self):
        prop = self.properties["slaSolutionChangedBy"].phone
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "slaSolutionChangedBy/phone")
        self.assertEqual(
            prop.get_description(),
            ("Telefone principal da organização (Somente leitura)."),
        )

    def test_property_slaSolutionChangedBy_personType(self):
        prop = self.properties["slaSolutionChangedBy"].personType
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "slaSolutionChangedBy/personType")
        self.assertEqual(
            prop.get_description(),
            (
                "Tipo da pessoa: Pessoa = 1, Empresa = 2, Departamento = 4 (Somente leitura)."
            ),
        )

    def test_property_slaSolutionChangedBy_profileType(self):
        prop = self.properties["slaSolutionChangedBy"].profileType
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "slaSolutionChangedBy/profileType")
        self.assertEqual(
            prop.get_description(),
            (
                "Perfil da pessoa: Agente = 1, Cliente = 2, Agente e Cliente = 3 (Somente leitura)."
            ),
        )

    def test_property_slaSolutionDate(self):
        prop = self.properties["slaSolutionDate"]
        self.assertIsInstance(prop, properties.DatetimeProperty)
        self.assertEqual(prop.full_name, "slaSolutionDate")
        self.assertEqual(
            prop.get_description(),
            (
                "Data de solução do SLA. Caso informado, será considerado que o SLA foi "
                "manualmente alterado pelo usuário que criou a ação. "
                "A data informada deve estar no formato UTC."
            ),
        )

    def test_property_slaSolutionDateIsPaused(self):
        prop = self.properties["slaSolutionDateIsPaused"]
        self.assertIsInstance(prop, properties.BooleanProperty)
        self.assertEqual(prop.full_name, "slaSolutionDateIsPaused")
        self.assertEqual(
            prop.get_description(),
            ("Indica se a data de solução do SLA está pausada (Somente leitura)."),
        )

    def test_property_slaResponseDate(self):
        prop = self.properties["slaResponseDate"]
        self.assertIsInstance(prop, properties.DatetimeProperty)
        self.assertEqual(prop.full_name, "slaResponseDate")
        self.assertEqual(
            prop.get_description(),
            ("Data UTC de resposta do SLA (Somente leitura)."),
        )

    def test_property_slaRealResponseDate(self):
        prop = self.properties["slaRealResponseDate"]
        self.assertIsInstance(prop, properties.DatetimeProperty)
        self.assertEqual(prop.full_name, "slaRealResponseDate")
        self.assertEqual(
            prop.get_description(),
            ("Data UTC real da resposta do SLA (Somente leitura)."),
        )

    def test_property_jiraIssueKey(self):
        prop = self.properties["jiraIssueKey"]
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "jiraIssueKey")
        self.assertEqual(
            prop.get_description(),
            (
                "Chave da issue do Jira Software que está associada ao ticket por "
                "integração (Somente leitura)."
            ),
        )

    def test_property_redmineIssueId(self):
        prop = self.properties["redmineIssueId"]
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "redmineIssueId")
        self.assertEqual(
            prop.get_description(),
            (
                "ID da issue do Redmine que está associada ao ticket por "
                "integração (Somente leitura)."
            ),
        )

    def test_property_clients(self):
        prop = self.properties["clients"]
        self.assertIsInstance(prop, properties.ComplexProperty)
        self.assertEqual(prop.full_name, "clients")
        self.assertEqual(
            prop.get_description(),
            ("Lista com os clientes do ticket."),
        )

    def test_property_clients_id(self):
        prop = self.properties["clients"].id
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "clients/id")
        self.assertEqual(
            prop.get_description(),
            (
                "Id (Cod. ref.) da organização (Somente leitura, entretanto para "
                "'ticket.clients[n].organization' esse campo é configurável)."
            ),
        )

    def test_property_clients_businessName(self):
        prop = self.properties["clients"].businessName
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "clients/businessName")
        self.assertEqual(
            prop.get_description(),
            ("Nome da organização (Somente leitura)."),
        )

    def test_property_clients_email(self):
        prop = self.properties["clients"].email
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "clients/email")
        self.assertEqual(
            prop.get_description(),
            ("E-mail principal da organização (Somente leitura)."),
        )

    def test_property_clients_phone(self):
        prop = self.properties["clients"].phone
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "clients/phone")
        self.assertEqual(
            prop.get_description(),
            ("Telefone principal da organização (Somente leitura)."),
        )

    def test_property_clients_personType(self):
        prop = self.properties["clients"].personType
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "clients/personType")
        self.assertEqual(
            prop.get_description(),
            (
                "Tipo da pessoa: Pessoa = 1, Empresa = 2, Departamento = 4 (Somente leitura)."
            ),
        )

    def test_property_clients_isDeleted(self):
        prop = self.properties["clients"].isDeleted
        self.assertIsInstance(prop, properties.BooleanProperty)
        self.assertEqual(prop.full_name, "clients/isDeleted")
        self.assertEqual(
            prop.get_description(),
            ("Verdadeiro se o cliente foi deletado (Somente leitura)."),
        )

    def test_property_clients_organization(self):
        prop = self.properties["clients"].organization
        self.assertIsInstance(prop, properties.ComplexProperty)
        self.assertEqual(prop.full_name, "clients/organization")
        self.assertEqual(
            prop.get_description(),
            ("Organização do cliente (Somente leitura)."),
        )

    def test_property_clients_organization_id(self):
        prop = self.properties["clients"].organization.id
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "clients/organization/id")
        self.assertEqual(
            prop.get_description(),
            (
                "Id (Cod. ref.) da organização (Somente leitura, entretanto para "
                "'ticket.clients[n].organization' esse campo é configurável)."
            ),
        )

    def test_property_clients_organization_businessName(self):
        prop = self.properties["clients"].organization.businessName
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "clients/organization/businessName")
        self.assertEqual(
            prop.get_description(),
            ("Nome da organização (Somente leitura)."),
        )

    def test_property_clients_organization_email(self):
        prop = self.properties["clients"].organization.email
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "clients/organization/email")
        self.assertEqual(
            prop.get_description(),
            ("E-mail principal da organização (Somente leitura)."),
        )

    def test_property_clients_organization_phone(self):
        prop = self.properties["clients"].organization.phone
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "clients/organization/phone")
        self.assertEqual(
            prop.get_description(),
            ("Telefone principal da organização (Somente leitura)."),
        )

    def test_property_clients_organization_personType(self):
        prop = self.properties["clients"].organization.personType
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "clients/organization/personType")
        self.assertEqual(
            prop.get_description(),
            (
                "Tipo da pessoa: Pessoa = 1, Empresa = 2, Departamento = 4 (Somente leitura)."
            ),
        )

    def test_property_clients_organization_profileType(self):
        prop = self.properties["clients"].organization.profileType
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "clients/organization/profileType")
        self.assertEqual(
            prop.get_description(),
            (
                "Perfil da pessoa: Agente = 1, Cliente = 2, Agente e Cliente = 3 (Somente leitura)."
            ),
        )

    def test_property_actions(self):
        prop = self.properties["actions"]
        self.assertIsInstance(prop, properties.ComplexProperty)
        self.assertEqual(prop.full_name, "actions")
        self.assertEqual(
            prop.get_description(),
            ("Lista com as ações do ticket."),
        )

    def test_property_actions_id(self):
        prop = self.properties["actions"].id
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "actions/id")
        self.assertEqual(
            prop.get_description(),
            (
                "Id (Número da ação) (Somente leitura). *Deve ser informado "
                "quando necessário alterar a ação já existente."
            ),
        )

    def test_property_actions_type(self):
        prop = self.properties["actions"].type
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "actions/type")
        self.assertEqual(
            prop.get_description(),
            ("Tipo do ticket: 1 = Interno 2 = Público."),
        )

    def test_property_actions_origin(self):
        prop = self.properties["actions"].origin
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "actions/origin")
        self.assertEqual(
            prop.get_description(),
            (
                "Origem da ação (Somente leitura)."
                "\n\t0 First Action"
                "\n\t1 Via web pelo cliente"
                "\n\t2 Via web pelo agente"
                "\n\t3 Recebido via email"
                "\n\t4 Gatilho do sistema"
                "\n\t5 Chat (online)"
                "\n\t6 Chat (offline)"
                "\n\t7 Email enviado pelo sistema"
                "\n\t8 Formulário de contato"
                "\n\t9 Via web API"
                "\n\t10 Abertura automática de tickets"
                "\n\t11 Issue integração Jira"
                "\n\t12 Issue integração Redmine"
                "\n\t13 Chamada recebida integração Telefonia"
                "\n\t14 Chamada realizada integração Telefonia"
                "\n\t15 Chamada perdida integração Telefonia"
                "\n\t16 Chamada que obteve desistência na fila de espera integração Telefonia"
                "\n\t17 Acesso remoto"
                "\n\t18 WhatsApp"
                "\n\t19 Integração Movidesk"
                "\n\t20 Integração Zenvia Chat"
                "\n\t21 Chamada não atendida integração Telefonia"
            ),
        )

    def test_property_actions_description(self):
        prop = self.properties["actions"].description
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "actions/description")
        self.assertEqual(
            prop.get_description(),
            ("Descrição da ação."),
        )

    def test_property_actions_htmlDescription(self):
        prop = self.properties["actions"].htmlDescription
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "actions/htmlDescription")
        self.assertEqual(
            prop.get_description(),
            ("Descrição da ação em formato HTML (Somente leitura)."),
        )

    def test_property_actions_status(self):
        prop = self.properties["actions"].status
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "actions/status")
        self.assertEqual(
            prop.get_description(),
            ("Status da ação (Somente leitura)."),
        )

    def test_property_actions_justification(self):
        prop = self.properties["actions"].justification
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "actions/justification")
        self.assertEqual(
            prop.get_description(),
            ("Justificativa da ação (Somente leitura)."),
        )

    def test_property_actions_createdDate(self):
        prop = self.properties["actions"].createdDate
        self.assertIsInstance(prop, properties.DatetimeProperty)
        self.assertEqual(prop.full_name, "actions/createdDate")
        self.assertEqual(
            prop.get_description(),
            (
                "Data de criação da ação. A data informada deve estar no formato UTC. "
                "*Caso não informada, será preenchida com a data atual."
            ),
        )

    def test_property_actions_createdBy(self):
        prop = self.properties["actions"].createdBy
        self.assertIsInstance(prop, properties.ComplexProperty)
        self.assertEqual(prop.full_name, "actions/createdBy")
        self.assertEqual(
            prop.get_description(),
            ("Dados do gerador da ação."),
        )

    def test_property_actions_createdBy_id(self):
        prop = self.properties["actions"].createdBy.id
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "actions/createdBy/id")
        self.assertEqual(
            prop.get_description(),
            (
                "Id (Cod. ref.) da organização (Somente leitura, entretanto para "
                "'ticket.clients[n].organization' esse campo é configurável)."
            ),
        )

    def test_property_actions_createdBy_businessName(self):
        prop = self.properties["actions"].createdBy.businessName
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "actions/createdBy/businessName")
        self.assertEqual(
            prop.get_description(),
            ("Nome da organização (Somente leitura)."),
        )

    def test_property_actions_createdBy_email(self):
        prop = self.properties["actions"].createdBy.email
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "actions/createdBy/email")
        self.assertEqual(
            prop.get_description(),
            ("E-mail principal da organização (Somente leitura)."),
        )

    def test_property_actions_createdBy_phone(self):
        prop = self.properties["actions"].createdBy.phone
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "actions/createdBy/phone")
        self.assertEqual(
            prop.get_description(),
            ("Telefone principal da organização (Somente leitura)."),
        )

    def test_property_actions_createdBy_personType(self):
        prop = self.properties["actions"].createdBy.personType
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "actions/createdBy/personType")
        self.assertEqual(
            prop.get_description(),
            (
                "Tipo da pessoa: Pessoa = 1, Empresa = 2, Departamento = 4 (Somente leitura)."
            ),
        )

    def test_property_actions_createdBy_profileType(self):
        prop = self.properties["actions"].createdBy.profileType
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "actions/createdBy/profileType")
        self.assertEqual(
            prop.get_description(),
            (
                "Perfil da pessoa: Agente = 1, Cliente = 2, Agente e Cliente = 3 (Somente leitura)."
            ),
        )

    def test_property_actions_isDeleted(self):
        prop = self.properties["actions"].isDeleted
        self.assertIsInstance(prop, properties.BooleanProperty)
        self.assertEqual(prop.full_name, "actions/isDeleted")
        self.assertEqual(
            prop.get_description(),
            ("Verdadeiro se a ação foi deletada (Somente leitura)."),
        )

    def test_property_actions_timeAppointments(self):
        prop = self.properties["actions"].timeAppointments
        self.assertIsInstance(prop, properties.ComplexProperty)
        self.assertEqual(prop.full_name, "actions/timeAppointments")
        self.assertEqual(
            prop.get_description(),
            ("Dados dos apontamentos de hora."),
        )

    def test_property_actions_timeAppointments_id(self):
        prop = self.properties["actions"].timeAppointments.id
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "actions/timeAppointments/id")
        self.assertEqual(
            prop.get_description(),
            (
                "Id (Código) do apontamento (Somente leitura). *Deve ser informado quando "
                "necessário alterar o apontamento já existente."
            ),
        )

    def test_property_actions_timeAppointments_activity(self):
        prop = self.properties["actions"].timeAppointments.activity
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "actions/timeAppointments/activity")
        self.assertEqual(
            prop.get_description(),
            ("Deve ser uma atividade cadastrada previamente no sistema."),
        )

    def test_property_actions_timeAppointments_date(self):
        prop = self.properties["actions"].timeAppointments.date
        self.assertIsInstance(prop, properties.DatetimeProperty)
        self.assertEqual(prop.full_name, "actions/timeAppointments/date")
        self.assertEqual(
            prop.get_description(),
            ("Deve conter a data com as horas zeradas Ex: 2016-08-24T00:00:00."),
        )

    def test_property_actions_timeAppointments_periodStart(self):
        prop = self.properties["actions"].timeAppointments.periodStart
        self.assertIsInstance(prop, properties.TimeProperty)
        self.assertEqual(prop.full_name, "actions/timeAppointments/periodStart")
        self.assertEqual(
            prop.get_description(),
            (
                "Período inicial do apontamento. Ex: 08:00:00. "
                "*Obrigatório quando determinado via parametrização."
            ),
        )

    def test_property_actions_timeAppointments_periodEnd(self):
        prop = self.properties["actions"].timeAppointments.periodEnd
        self.assertIsInstance(prop, properties.TimeProperty)
        self.assertEqual(prop.full_name, "actions/timeAppointments/periodEnd")
        self.assertEqual(
            prop.get_description(),
            (
                "Período final do apontamento. Ex: 12:00:00. "
                "*Obrigatório quando determinado via parametrização."
            ),
        )

    def test_property_actions_timeAppointments_workTime(self):
        prop = self.properties["actions"].timeAppointments.workTime
        self.assertIsInstance(prop, properties.TimeProperty)
        self.assertEqual(prop.full_name, "actions/timeAppointments/workTime")
        self.assertEqual(
            prop.get_description(),
            (
                "Tempo total do apontamento. Ex: 04:00:00. "
                "*Obrigatório quando determinado via parametrização."
            ),
        )

    def test_property_actions_timeAppointments_workTypeName(self):
        prop = self.properties["actions"].timeAppointments.workTypeName
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "actions/timeAppointments/workTypeName")
        self.assertEqual(
            prop.get_description(),
            ("Tipo do horário apontado."),
        )

    def test_property_actions_timeAppointments_createdBy(self):
        prop = self.properties["actions"].timeAppointments.createdBy
        self.assertIsInstance(prop, properties.ComplexProperty)
        self.assertEqual(prop.full_name, "actions/timeAppointments/createdBy")
        self.assertEqual(
            prop.get_description(),
            ("Dados do gerador do apontamento."),
        )

    def test_property_actions_timeAppointments_createdBy_id(self):
        prop = self.properties["actions"].timeAppointments.createdBy.id
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "actions/timeAppointments/createdBy/id")
        self.assertEqual(
            prop.get_description(),
            (
                "Id (Cod. ref.) da organização (Somente leitura, entretanto para "
                "'ticket.clients[n].organization' esse campo é configurável)."
            ),
        )

    def test_property_actions_timeAppointments_createdBy_businessName(self):
        prop = self.properties["actions"].timeAppointments.createdBy.businessName
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(
            prop.full_name, "actions/timeAppointments/createdBy/businessName"
        )
        self.assertEqual(
            prop.get_description(),
            ("Nome da organização (Somente leitura)."),
        )

    def test_property_actions_timeAppointments_createdBy_email(self):
        prop = self.properties["actions"].timeAppointments.createdBy.email
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "actions/timeAppointments/createdBy/email")
        self.assertEqual(
            prop.get_description(),
            ("E-mail principal da organização (Somente leitura)."),
        )

    def test_property_actions_timeAppointments_createdBy_phone(self):
        prop = self.properties["actions"].timeAppointments.createdBy.phone
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "actions/timeAppointments/createdBy/phone")
        self.assertEqual(
            prop.get_description(),
            ("Telefone principal da organização (Somente leitura)."),
        )

    def test_property_actions_timeAppointments_createdBy_personType(self):
        prop = self.properties["actions"].timeAppointments.createdBy.personType
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(
            prop.full_name, "actions/timeAppointments/createdBy/personType"
        )
        self.assertEqual(
            prop.get_description(),
            (
                "Tipo da pessoa: Pessoa = 1, Empresa = 2, Departamento = 4 (Somente leitura)."
            ),
        )

    def test_property_actions_timeAppointments_createdBy_profileType(self):
        prop = self.properties["actions"].timeAppointments.createdBy.profileType
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(
            prop.full_name, "actions/timeAppointments/createdBy/profileType"
        )
        self.assertEqual(
            prop.get_description(),
            (
                "Perfil da pessoa: Agente = 1, Cliente = 2, Agente e Cliente = 3 (Somente leitura)."
            ),
        )

    def test_property_actions_timeAppointments_createdByTeam(self):
        prop = self.properties["actions"].timeAppointments.createdByTeam
        self.assertIsInstance(prop, properties.ComplexProperty)
        self.assertEqual(prop.full_name, "actions/timeAppointments/createdByTeam")
        self.assertEqual(
            prop.get_description(),
            ("Dados do time do gerador do apontamento."),
        )

    def test_property_actions_timeAppointments_createdByTeam_id(self):
        prop = self.properties["actions"].timeAppointments.createdByTeam.id
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "actions/timeAppointments/createdByTeam/id")
        self.assertEqual(
            prop.get_description(),
            ("Id (Cod. ref.) do time (Somente leitura)."),
        )

    def test_property_actions_timeAppointments_createdByTeam_name(self):
        prop = self.properties["actions"].timeAppointments.createdByTeam.name
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "actions/timeAppointments/createdByTeam/name")
        self.assertEqual(
            prop.get_description(),
            ("Nome do time (Somente leitura)."),
        )

    def test_property_actions_expenses(self):
        prop = self.properties["actions"].expenses
        self.assertIsInstance(prop, properties.ComplexProperty)
        self.assertEqual(prop.full_name, "actions/expenses")
        self.assertEqual(
            prop.get_description(),
            ("Dados de despesas."),
        )

    def test_property_actions_expenses_id(self):
        prop = self.properties["actions"].expenses.id
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "actions/expenses/id")
        self.assertEqual(
            prop.get_description(),
            ("Campo Identificador único da Despesa."),
        )

    def test_property_actions_expenses_type(self):
        prop = self.properties["actions"].expenses.type
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "actions/expenses/type")
        self.assertEqual(
            prop.get_description(),
            ("Descrição do Tipo de Despesa relacionado ao apontamento."),
        )

    def test_property_actions_expenses_serviceReport(self):
        prop = self.properties["actions"].expenses.serviceReport
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "actions/expenses/serviceReport")
        self.assertEqual(
            prop.get_description(),
            (
                "Número do Relatório de Serviço emitido contendo a despesa. Somente Leitura."
            ),
        )

    def test_property_actions_expenses_createdBy(self):
        prop = self.properties["actions"].expenses.createdBy
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "actions/expenses/createdBy")
        self.assertEqual(
            prop.get_description(),
            ("Cod. Ref. da pessoa que apontou a despesa."),
        )

    def test_property_actions_expenses_createdByTeam(self):
        prop = self.properties["actions"].expenses.createdByTeam
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "actions/expenses/createdByTeam")
        self.assertEqual(
            prop.get_description(),
            ("Nome da Equipe da pessoa que apontou a despesa."),
        )

    def test_property_actions_expenses_date(self):
        prop = self.properties["actions"].expenses.date
        self.assertIsInstance(prop, properties.DatetimeProperty)
        self.assertEqual(prop.full_name, "actions/expenses/date")
        self.assertEqual(
            prop.get_description(),
            (
                "Data de criação da pessoa. Deve ser menor ou igual a data atual. "
                "A data informada deve estar no formato UTC*."
            ),
        )

    def test_property_actions_expenses_quantity(self):
        prop = self.properties["actions"].expenses.quantity
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "actions/expenses/quantity")
        self.assertEqual(
            prop.get_description(),
            (
                "Quantidade de apontamento. Obrigatório quando não informado o campo value."
            ),
        )

    def test_property_actions_expenses_value(self):
        prop = self.properties["actions"].expenses.value
        self.assertIsInstance(prop, properties.DecimalProperty)
        self.assertEqual(prop.full_name, "actions/expenses/value")
        self.assertEqual(
            prop.get_description(),
            (
                "Valor em moeda apontado. Obrigatório quando não informado o campo quantity."
            ),
        )

    def test_property_actions_attachments(self):
        prop = self.properties["actions"].attachments
        self.assertIsInstance(prop, properties.ComplexProperty)
        self.assertEqual(prop.full_name, "actions/attachments")
        self.assertEqual(
            prop.get_description(),
            ("Dados dos anexos (Somente leitura)."),
        )

    def test_property_actions_attachments_fileName(self):
        prop = self.properties["actions"].attachments.fileName
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "actions/attachments/fileName")
        self.assertEqual(
            prop.get_description(),
            ("Nome do arquivo enviado (Somente leitura)."),
        )

    def test_property_actions_attachments_path(self):
        prop = self.properties["actions"].attachments.path
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "actions/attachments/path")
        self.assertEqual(
            prop.get_description(),
            ("Hash do arquivo enviado (Somente leitura)."),
        )

    def test_property_actions_attachments_createdBy(self):
        prop = self.properties["actions"].attachments.createdBy
        self.assertIsInstance(prop, properties.ComplexProperty)
        self.assertEqual(prop.full_name, "actions/attachments/createdBy")
        self.assertEqual(
            prop.get_description(),
            ("Dados do pessoa que enviou o arquivo (Somente leitura)."),
        )

    def test_property_actions_attachments_createdBy_id(self):
        prop = self.properties["actions"].attachments.createdBy.id
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "actions/attachments/createdBy/id")
        self.assertEqual(
            prop.get_description(),
            (
                "Id (Cod. ref.) da organização (Somente leitura, entretanto para "
                "'ticket.clients[n].organization' esse campo é configurável)."
            ),
        )

    def test_property_actions_attachments_createdBy_businessName(self):
        prop = self.properties["actions"].attachments.createdBy.businessName
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "actions/attachments/createdBy/businessName")
        self.assertEqual(
            prop.get_description(),
            ("Nome da organização (Somente leitura)."),
        )

    def test_property_actions_attachments_createdBy_email(self):
        prop = self.properties["actions"].attachments.createdBy.email
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "actions/attachments/createdBy/email")
        self.assertEqual(
            prop.get_description(),
            ("E-mail principal da organização (Somente leitura)."),
        )

    def test_property_actions_attachments_createdBy_phone(self):
        prop = self.properties["actions"].attachments.createdBy.phone
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "actions/attachments/createdBy/phone")
        self.assertEqual(
            prop.get_description(),
            ("Telefone principal da organização (Somente leitura)."),
        )

    def test_property_actions_attachments_createdBy_personType(self):
        prop = self.properties["actions"].attachments.createdBy.personType
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "actions/attachments/createdBy/personType")
        self.assertEqual(
            prop.get_description(),
            (
                "Tipo da pessoa: Pessoa = 1, Empresa = 2, Departamento = 4 (Somente leitura)."
            ),
        )

    def test_property_actions_attachments_createdBy_profileType(self):
        prop = self.properties["actions"].attachments.createdBy.profileType
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "actions/attachments/createdBy/profileType")
        self.assertEqual(
            prop.get_description(),
            (
                "Perfil da pessoa: Agente = 1, Cliente = 2, Agente e Cliente = 3 (Somente leitura)."
            ),
        )

    def test_property_actions_attachments_createdDate(self):
        prop = self.properties["actions"].attachments.createdDate
        self.assertIsInstance(prop, properties.DatetimeProperty)
        self.assertEqual(prop.full_name, "actions/attachments/createdDate")
        self.assertEqual(
            prop.get_description(),
            ("Data UTC que o arquivo foi enviado (Somente leitura)."),
        )

    def test_property_actions_tags(self):
        prop = self.properties["actions"].tags
        self.assertIsInstance(prop, properties.ArrayProperty)
        self.assertEqual(prop.full_name, "actions/tags")
        self.assertEqual(
            prop.get_description(),
            (
                "Lista de strings com as TAGs as quais a ação esta relacionada. "
                "Caso sejam informadas TAGs inexistentes, as mesmas serão adicionadas "
                "na base de dados."
            ),
        )

    def test_property_parentTickets(self):
        prop = self.properties["parentTickets"]
        self.assertIsInstance(prop, properties.ComplexProperty)
        self.assertEqual(prop.full_name, "parentTickets")
        self.assertEqual(
            prop.get_description(),
            ("Lista com os tickets pais."),
        )

    def test_property_parentTickets_id(self):
        prop = self.properties["parentTickets"].id
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "parentTickets/id")
        self.assertEqual(
            prop.get_description(),
            ("Id (Número) do ticket."),
        )

    def test_property_parentTickets_subject(self):
        prop = self.properties["parentTickets"].subject
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "parentTickets/subject")
        self.assertEqual(
            prop.get_description(),
            ("Assunto do ticket (Somente leitura)."),
        )

    def test_property_parentTickets_isDeleted(self):
        prop = self.properties["parentTickets"].isDeleted
        self.assertIsInstance(prop, properties.BooleanProperty)
        self.assertEqual(prop.full_name, "parentTickets/isDeleted")
        self.assertEqual(
            prop.get_description(),
            ("Verdadeiro se foi deletado (Somente leitura)."),
        )

    def test_property_childrenTickets(self):
        prop = self.properties["childrenTickets"]
        self.assertIsInstance(prop, properties.ComplexProperty)
        self.assertEqual(prop.full_name, "childrenTickets")
        self.assertEqual(
            prop.get_description(),
            ("Lista com os tickets filhos."),
        )

    def test_property_childrenTickets_id(self):
        prop = self.properties["childrenTickets"].id
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "childrenTickets/id")
        self.assertEqual(
            prop.get_description(),
            ("Id (Número) do ticket."),
        )

    def test_property_childrenTickets_subject(self):
        prop = self.properties["childrenTickets"].subject
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "childrenTickets/subject")
        self.assertEqual(
            prop.get_description(),
            ("Assunto do ticket (Somente leitura)."),
        )

    def test_property_childrenTickets_isDeleted(self):
        prop = self.properties["childrenTickets"].isDeleted
        self.assertIsInstance(prop, properties.BooleanProperty)
        self.assertEqual(prop.full_name, "childrenTickets/isDeleted")
        self.assertEqual(
            prop.get_description(),
            ("Verdadeiro se foi deletado (Somente leitura)."),
        )

    def test_property_ownerHistories(self):
        prop = self.properties["ownerHistories"]
        self.assertIsInstance(prop, properties.ComplexProperty)
        self.assertEqual(prop.full_name, "ownerHistories")
        self.assertEqual(
            prop.get_description(),
            (
                "Lista com os históricos de responsabilidades do ticket (Somente leitura)."
            ),
        )

    def test_property_ownerHistories_ownerTeam(self):
        prop = self.properties["ownerHistories"].ownerTeam
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "ownerHistories/ownerTeam")
        self.assertEqual(
            prop.get_description(),
            ("Equipe do responsável pelo ticket (Somente leitura)."),
        )

    def test_property_ownerHistories_owner(self):
        prop = self.properties["ownerHistories"].owner
        self.assertIsInstance(prop, properties.ComplexProperty)
        self.assertEqual(prop.full_name, "ownerHistories/owner")
        self.assertEqual(
            prop.get_description(),
            ("Dados do responsável pelo ticket (Somente leitura)."),
        )

    def test_property_ownerHistories_owner_id(self):
        prop = self.properties["ownerHistories"].owner.id
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "ownerHistories/owner/id")
        self.assertEqual(
            prop.get_description(),
            (
                "Id (Cod. ref.) da organização (Somente leitura, entretanto para "
                "'ticket.clients[n].organization' esse campo é configurável)."
            ),
        )

    def test_property_ownerHistories_owner_businessName(self):
        prop = self.properties["ownerHistories"].owner.businessName
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "ownerHistories/owner/businessName")
        self.assertEqual(
            prop.get_description(),
            ("Nome da organização (Somente leitura)."),
        )

    def test_property_ownerHistories_owner_email(self):
        prop = self.properties["ownerHistories"].owner.email
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "ownerHistories/owner/email")
        self.assertEqual(
            prop.get_description(),
            ("E-mail principal da organização (Somente leitura)."),
        )

    def test_property_ownerHistories_owner_phone(self):
        prop = self.properties["ownerHistories"].owner.phone
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "ownerHistories/owner/phone")
        self.assertEqual(
            prop.get_description(),
            ("Telefone principal da organização (Somente leitura)."),
        )

    def test_property_ownerHistories_owner_personType(self):
        prop = self.properties["ownerHistories"].owner.personType
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "ownerHistories/owner/personType")
        self.assertEqual(
            prop.get_description(),
            (
                "Tipo da pessoa: Pessoa = 1, Empresa = 2, Departamento = 4 (Somente leitura)."
            ),
        )

    def test_property_ownerHistories_owner_profileType(self):
        prop = self.properties["ownerHistories"].owner.profileType
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "ownerHistories/owner/profileType")
        self.assertEqual(
            prop.get_description(),
            (
                "Perfil da pessoa: Agente = 1, Cliente = 2, Agente e Cliente = 3 (Somente leitura)."
            ),
        )

    def test_property_ownerHistories_permanencyTimeFullTime(self):
        prop = self.properties["ownerHistories"].permanencyTimeFullTime
        self.assertIsInstance(prop, properties.FloatProperty)
        self.assertEqual(prop.full_name, "ownerHistories/permanencyTimeFullTime")
        self.assertEqual(
            prop.get_description(),
            (
                "Tempo de permanência do responsável pelo ticket em segundos. (Somente leitura)."
            ),
        )

    def test_property_ownerHistories_permanencyTimeWorkingTime(self):
        prop = self.properties["ownerHistories"].permanencyTimeWorkingTime
        self.assertIsInstance(prop, properties.FloatProperty)
        self.assertEqual(prop.full_name, "ownerHistories/permanencyTimeWorkingTime")
        self.assertEqual(
            prop.get_description(),
            (
                "Tempo útil de permanência do responsável pelo ticket em segundos. "
                "(Somente leitura)."
            ),
        )

    def test_property_ownerHistories_changedBy(self):
        prop = self.properties["ownerHistories"].changedBy
        self.assertIsInstance(prop, properties.ComplexProperty)
        self.assertEqual(prop.full_name, "ownerHistories/changedBy")
        self.assertEqual(
            prop.get_description(),
            (
                "Dados da pessoa que alterou o responsável pelo ticket (Somente leitura)."
            ),
        )

    def test_property_ownerHistories_changedBy_id(self):
        prop = self.properties["ownerHistories"].changedBy.id
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "ownerHistories/changedBy/id")
        self.assertEqual(
            prop.get_description(),
            (
                "Id (Cod. ref.) da organização (Somente leitura, entretanto para "
                "'ticket.clients[n].organization' esse campo é configurável)."
            ),
        )

    def test_property_ownerHistories_changedBy_businessName(self):
        prop = self.properties["ownerHistories"].changedBy.businessName
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "ownerHistories/changedBy/businessName")
        self.assertEqual(
            prop.get_description(),
            ("Nome da organização (Somente leitura)."),
        )

    def test_property_ownerHistories_changedBy_email(self):
        prop = self.properties["ownerHistories"].changedBy.email
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "ownerHistories/changedBy/email")
        self.assertEqual(
            prop.get_description(),
            ("E-mail principal da organização (Somente leitura)."),
        )

    def test_property_ownerHistories_changedBy_phone(self):
        prop = self.properties["ownerHistories"].changedBy.phone
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "ownerHistories/changedBy/phone")
        self.assertEqual(
            prop.get_description(),
            ("Telefone principal da organização (Somente leitura)."),
        )

    def test_property_ownerHistories_changedBy_personType(self):
        prop = self.properties["ownerHistories"].changedBy.personType
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "ownerHistories/changedBy/personType")
        self.assertEqual(
            prop.get_description(),
            (
                "Tipo da pessoa: Pessoa = 1, Empresa = 2, Departamento = 4 (Somente leitura)."
            ),
        )

    def test_property_ownerHistories_changedBy_profileType(self):
        prop = self.properties["ownerHistories"].changedBy.profileType
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "ownerHistories/changedBy/profileType")
        self.assertEqual(
            prop.get_description(),
            (
                "Perfil da pessoa: Agente = 1, Cliente = 2, Agente e Cliente = 3 (Somente leitura)."
            ),
        )

    def test_property_ownerHistories_changedDate(self):
        prop = self.properties["ownerHistories"].changedDate
        self.assertIsInstance(prop, properties.DatetimeProperty)
        self.assertEqual(prop.full_name, "ownerHistories/changedDate")
        self.assertEqual(
            prop.get_description(),
            ("Data UTC que o responsável pelo ticket foi alterado (Somente leitura)."),
        )

    def test_property_statusHistories(self):
        prop = self.properties["statusHistories"]
        self.assertIsInstance(prop, properties.ComplexProperty)
        self.assertEqual(prop.full_name, "statusHistories")
        self.assertEqual(
            prop.get_description(),
            ("Lista com os históricos de status do ticket (Somente leitura)."),
        )

    def test_property_statusHistories_status(self):
        prop = self.properties["statusHistories"].status
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "statusHistories/status")
        self.assertEqual(
            prop.get_description(),
            ("Status do ticket (Somente leitura)."),
        )

    def test_property_statusHistories_justification(self):
        prop = self.properties["statusHistories"].justification
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "statusHistories/justification")
        self.assertEqual(
            prop.get_description(),
            ("Justificativa do ticket (Somente leitura)."),
        )

    def test_property_statusHistories_permanencyTimeFullTime(self):
        prop = self.properties["statusHistories"].permanencyTimeFullTime
        self.assertIsInstance(prop, properties.FloatProperty)
        self.assertEqual(prop.full_name, "statusHistories/permanencyTimeFullTime")
        self.assertEqual(
            prop.get_description(),
            (
                "Tempo de permanência do status do ticket em segundos. (Somente leitura)."
            ),
        )

    def test_property_statusHistories_permanencyTimeWorkingTime(self):
        prop = self.properties["statusHistories"].permanencyTimeWorkingTime
        self.assertIsInstance(prop, properties.FloatProperty)
        self.assertEqual(prop.full_name, "statusHistories/permanencyTimeWorkingTime")
        self.assertEqual(
            prop.get_description(),
            (
                "Tempo útil de permanência do status do ticket em segundos. "
                "(Somente leitura)."
            ),
        )

    def test_property_statusHistories_changedBy(self):
        prop = self.properties["statusHistories"].changedBy
        self.assertIsInstance(prop, properties.ComplexProperty)
        self.assertEqual(prop.full_name, "statusHistories/changedBy")
        self.assertEqual(
            prop.get_description(),
            ("Dados da pessoa que alterou o status do ticket (Somente leitura)."),
        )

    def test_property_statusHistories_changedBy_id(self):
        prop = self.properties["statusHistories"].changedBy.id
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "statusHistories/changedBy/id")
        self.assertEqual(
            prop.get_description(),
            (
                "Id (Cod. ref.) da organização (Somente leitura, entretanto para "
                "'ticket.clients[n].organization' esse campo é configurável)."
            ),
        )

    def test_property_statusHistories_changedBy_businessName(self):
        prop = self.properties["statusHistories"].changedBy.businessName
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "statusHistories/changedBy/businessName")
        self.assertEqual(
            prop.get_description(),
            ("Nome da organização (Somente leitura)."),
        )

    def test_property_statusHistories_changedBy_email(self):
        prop = self.properties["statusHistories"].changedBy.email
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "statusHistories/changedBy/email")
        self.assertEqual(
            prop.get_description(),
            ("E-mail principal da organização (Somente leitura)."),
        )

    def test_property_statusHistories_changedBy_phone(self):
        prop = self.properties["statusHistories"].changedBy.phone
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "statusHistories/changedBy/phone")
        self.assertEqual(
            prop.get_description(),
            ("Telefone principal da organização (Somente leitura)."),
        )

    def test_property_statusHistories_changedBy_personType(self):
        prop = self.properties["statusHistories"].changedBy.personType
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "statusHistories/changedBy/personType")
        self.assertEqual(
            prop.get_description(),
            (
                "Tipo da pessoa: Pessoa = 1, Empresa = 2, Departamento = 4 (Somente leitura)."
            ),
        )

    def test_property_statusHistories_changedBy_profileType(self):
        prop = self.properties["statusHistories"].changedBy.profileType
        self.assertIsInstance(prop, properties.IntegerProperty)
        self.assertEqual(prop.full_name, "statusHistories/changedBy/profileType")
        self.assertEqual(
            prop.get_description(),
            (
                "Perfil da pessoa: Agente = 1, Cliente = 2, Agente e Cliente = 3 (Somente leitura)."
            ),
        )

    def test_property_statusHistories_changedDate(self):
        prop = self.properties["statusHistories"].changedDate
        self.assertIsInstance(prop, properties.DatetimeProperty)
        self.assertEqual(prop.full_name, "statusHistories/changedDate")
        self.assertEqual(
            prop.get_description(),
            ("Data UTC que o status do ticket foi alterado (Somente leitura)."),
        )

    def test_property_customFieldValues(self):
        prop = self.properties["customFieldValues"]
        self.assertIsInstance(prop, properties.ComplexProperty)
        self.assertEqual(prop.full_name, "customFieldValues")
        self.assertEqual(
            prop.get_description(),
            ("Lista com os valores dos campos adicionais do ticket."),
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

    def test_property_assets(self):
        prop = self.properties["assets"]
        self.assertIsInstance(prop, properties.ComplexProperty)
        self.assertEqual(prop.full_name, "assets")
        self.assertEqual(
            prop.get_description(),
            ("Lista com os ativos do ticket."),
        )

    def test_property_assets_id(self):
        prop = self.properties["assets"].id
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "assets/id")
        self.assertEqual(
            prop.get_description(),
            ("Id (Cod. ref.) do ativo (Somente leitura)."),
        )

    def test_property_assets_name(self):
        prop = self.properties["assets"].name
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "assets/name")
        self.assertEqual(
            prop.get_description(),
            ("Nome do ativo (Somente leitura)."),
        )

    def test_property_assets_label(self):
        prop = self.properties["assets"].label
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "assets/label")
        self.assertEqual(
            prop.get_description(),
            ("Etiqueta (única) do ativo (Somente leitura)."),
        )

    def test_property_assets_serialNumber(self):
        prop = self.properties["assets"].serialNumber
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "assets/serialNumber")
        self.assertEqual(
            prop.get_description(),
            ("Número de série do ativo (Somente leitura)."),
        )

    def test_property_assets_categoryFull(self):
        prop = self.properties["assets"].categoryFull
        self.assertIsInstance(prop, properties.ArrayProperty)
        self.assertEqual(prop.full_name, "assets/categoryFull")
        self.assertEqual(
            prop.get_description(),
            (
                "Lista com os nomes dos níveis da categoria selecionada no ativo (Somente leitura)."
            ),
        )

    def test_property_assets_categoryFirstLevel(self):
        prop = self.properties["assets"].categoryFirstLevel
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "assets/categoryFirstLevel")
        self.assertEqual(
            prop.get_description(),
            (
                "Nome do primeiro nível da categoria selecionada no ativo (Somente leitura)."
            ),
        )

    def test_property_assets_categorySecondLevel(self):
        prop = self.properties["assets"].categorySecondLevel
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "assets/categorySecondLevel")
        self.assertEqual(
            prop.get_description(),
            (
                "Nome do segundo nível da categoria selecionada no ativo (Somente leitura)."
            ),
        )

    def test_property_assets_categoryThirdLevel(self):
        prop = self.properties["assets"].categoryThirdLevel
        self.assertIsInstance(prop, properties.StringProperty)
        self.assertEqual(prop.full_name, "assets/categoryThirdLevel")
        self.assertEqual(
            prop.get_description(),
            (
                "Nome do terceiro nível da categoria selecionada no ativo (Somente leitura)."
            ),
        )

    def test_property_assets_isDeleted(self):
        prop = self.properties["assets"].isDeleted
        self.assertIsInstance(prop, properties.BooleanProperty)
        self.assertEqual(prop.full_name, "assets/isDeleted")
        self.assertEqual(
            prop.get_description(),
            ("Verdadeiro se o ativo foi deletado do ticket (Somente leitura)."),
        )
