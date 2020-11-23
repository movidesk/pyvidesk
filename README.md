# pyvidesk

Biblioteca Python para uso da API do Movidesk.

## Informações Gerais

Atualmente, esta biblioteca suporta requisições GET, POST, PATCH e DELETE as entidades [Tickets](https://atendimento.movidesk.com/kb/pt-br/article/256/movidesk-ticket-api), [Persons](https://atendimento.movidesk.com/kb/pt-br/article/189/movidesk-person-api) e [Services](https://atendimento.movidesk.com/kb/pt-br/article/7440/api-servicos) por meio da API do Movidesk.

## Uso

```python
from pyvidesk import Pyvidesk

persons = Pyvidesk(token="Meu_token_secreto").persons
person = persons.get_by_id("2222")
print(person)
print(person.id)
print(person.isActive)
print(person.businessName)
# <Model for Person(id=2222)>
# 2222
# True
# Murilo Scarpa Sitonio
```

Você pode usar a lógica acima para consultar qualquer propriedade da entidade e ainda setar as opções da query:

```python
from pyvidesk import Pyvidesk

persons = Pyvidesk(token="Meu_token_secreto").persons
my_query = persons.get_by_isActive(True, select=("id", "businessName"), top=10)
# my_query contém uma lista de Models, apenas com as informações "id" e "businessName", 
# das 10 primeiras pessoas ativas.
```

Para consultas mais complexas recomenda-se o uso da classe `Query`, obtida por meio da propriedade `query`, e das propriedades específicas da entidade, obtidas por meio de `get_properties()`:

```python
from datetime import date, timedelta

from pyvidesk import Pyvidesk

tickets = Pyvidesk(token="Meu_token_secreto").tickets
tickets_properties = tickets.get_properties()
my_query = (
    tickets.query.filter(
        tickets_properties["owner"].businessName == "Murilo Scarpa Sitonio"
    )
    .filter(tickets_properties["createdDate"] >= date.today() - timedelta(days=1))
    .expand(tickets_properties["clients"])
    .select(tickets_properties["id"])
)
print(my_query.url())
# https://api.movidesk.com/public/v1/tickets?token=Meu_token_secreto&$select=id&$filter=owner/businessName 
# eq 'Murilo Scarpa Sitonio' and createdDate ge 2020-10-01&$expand=clients
```

Para acessar os resultados da consulta deve-se seguir uma das três abordagens:

- Iterar sobre o objeto:
```python
for data in my_query:
    print(data)
```

- Agrupar todos os resultados numa lista:
```python
data = my_query.all()
```

- Obter apenas o primeiro resultado:
```python
data = my_query.first()
```

### Exemplos de consulta mais complexa

```python
from pyvidesk import Pyvidesk
from pyvidesk.lambdas import AnyAny

# AnyAny implementa dois operadores lambdas concatenados.

tickets = Pyvidesk(token="Meu_token_secreto").tickets
tickets_properties = tickets.get_properties()

my_query = (
    tickets.query.filter(
        AnyAny(
            tickets_properties["customFieldValues"].items.customFieldItem
            == "Equipamento XYZ"
        )
    )
    .expand(
        tickets_properties["customFieldValues"],
        inner={
            "expand": tickets_properties["customFieldValues"].items,
            "select": tickets_properties["customFieldValues"].items.customFieldItem,
        },
        select=tickets_properties["customFieldValues"].items,
    )
    .select(tickets_properties["id"])
    .order_by(tickets_properties["id"].desc())
    .top(5)
    .skip(200)
)

print(my_query.as_url())
# https://api.movidesk.com/public/v1/tickets?token=Meu_token_secreto&$top=5&$skip=200&$select=id
# &$filter=customFieldValues/any(x: x/items/any(y: y/customFieldItem eq 'Equipamento XYZ'))
# &$expand=customFieldValues($expand=items($select=customFieldItem);$select=items)&$orderby=id desc

for ticket in my_query:
    print(ticket)

# <Model for Ticket(id=1003)>
# <Model for Ticket(id=1002)>
# <Model for Ticket(id=1001)>
# <Model for Ticket(id=987)>
# <Model for Ticket(id=984)>
```

### Exemplos de consulta mais complexa - múltiplas expansões

```python
my_query = (
    tickets.query.filter(tickets_properties["id"] >= 1000)
    .expand(
        tickets_properties["actions"],
        inner={
            "expand": tickets_properties["actions"].timeAppointments,
            "inner": {
                "expand": tickets_properties["actions"].timeAppointments.createdBy,
                "select": tickets_properties["actions"].timeAppointments.createdBy.id,
            },
            "select": tickets_properties["actions"].timeAppointments.activity,
        },
        select=tickets_properties["actions"].id,
    )
    .select(tickets_properties["id"])
    .order_by(tickets_properties["id"].desc())
    .top(5)
    .skip(200)
)

print(my_query.as_url())
# https://api.movidesk.com/public/v1/tickets?token=Meu_token_secreto&$top=5&$skip=200&$select=id
# &$filter=id ge 1000
# &$expand=actions($expand=timeAppointments($expand=createdBy($select=id);$select=activity);$select=id)
# &$orderby=id desc

for ticket in my_query:
    print(ticket)

# <Model for Ticket(id=4067)>
# <Model for Ticket(id=4066)>
# <Model for Ticket(id=4065)>
# <Model for Ticket(id=4064)>
# <Model for Ticket(id=4063)>
```

Para manipulação com operadores lógicos, deve-se usar a class `Q`, inspirada em [django.db.models.Q](https://github.com/django/django/blob/master/django/db/models/query_utils.py).

### Exemplos de consulta mais complexa - operador lógico OR

Para operações `or`, utilize `|`.

```python
from pyvidesk.query import Q

my_query = tickets.query.filter(
    Q(tickets_properties["clients"].id == 55)
    | Q(tickets_properties["clients"].organization.id == 66)
)

print(my_query.as_url())
# https://api.movidesk.com/public/v1/tickets?token=Meu_token_secreto
# &$filter=(clients/id eq '55' or clients/organization/id eq '66')
```

### Exemplos de consulta mais complexa - operador lógico NOT e método `has`

Para operações `not`, utilize `~`. E para checar se uma string está contida num array, utilize o método `has`.

```python
my_query = tickets.query.filter(~Q(tickets_properties["tags"].has("My tag")))

print(my_query.as_url())
# https://api.movidesk.com/public/v1/tickets?token=Meu_token_secreto&$filter=not tags/any(x: x eq 'My tag')
```

## Classe Model

Todas as consultas ao servidor retornam um objeto da classe `Model`. Este objeto pode ser manipulado e as alterações podem ser enviadas ao servidor com o método `save()`:

```python
from pyvidesk import Pyvidesk

tickets = Pyvidesk(token="Meu_token_secreto").tickets
ticket = tickets.get_by_id(1)
today = date.today()
for action in ticket.actions:
    for appointment in action.timeAppointments:
        appointment.date = today

ticket.save()  # Assim, uma requisição PATCH é enviada ao servidor.
```

É possível excluir um modelo do servidor com o método `delete()`:

```python
from pyvidesk import Pyvidesk

persons = Pyvidesk(token="Meu_token_secreto").persons
person = persons.get_by_id("1")
person.delete()  # Assim, uma requisição DELETE é enviada ao servidor.
```

Para criação de modelos, deve-se usar a classe `EmptyModel` e o método `create()`:

```python
from pyvidesk import Pyvidesk

ticket = Pyvidesk(token="Meu_token_secreto").tickets.get_empty_model()
print(ticket)
# <EmptyModel for Ticket()>

ticket.subject = "Assunto"
ticket.type = 1
ticket.serviceFirstLevelId = 190853
ticket.createdBy.id = "2263751"
ticket.clients = [{"id": "917910092"}]
ticket.actions = [{"description": "Descrição", "type": 1}]
ticket.ownerTeam = "Administradores"
ticket.owner.id = "2222"

ticket.create()  # Assim, uma requisição POST é enviada ao servidor.
```

Também há a opção de se trabalhar diretamente com o `JSON` enviado pelo servidor, chamando o método `raw()`:

```python
from pyvidesk import Pyvidesk

persons = Pyvidesk(token="Meu_token_secreto").persons
person = persons.get_by_id("2222", select="businessName")
print(person.raw())
# {'businessName': 'Murilo Scarpa Sitonio'}
```