# Especificação Funcional — Escopo Geral
# Monitoramento de Indisponibilidade

> Gerado em: 26/06/2026
> Versão: 1.0
> Situação: **Rascunho**

---

## Feature: Gerenciamento de Serviços Monitorados

**In order to** controlar quais sistemas são monitorados e garantir que indisponibilidades sejam rastreadas corretamente
**As** Administrador de Sistemas
**I want** incluir, configurar, editar e remover serviços do monitoramento, informando o endpoint de healthcheck e os vínculos hierárquicos

---

### Regras de Negócio

| ID | Regra |
|----|-------|
| RN01 | A lista de sistemas disponíveis para monitoramento é obtida via endpoint externo do Portal de Serviços |
| RN02 | Apenas sistemas ainda não incluídos no monitoramento aparecem na lista de inclusão |
| RN03 | A URL do healthcheck é obrigatória para incluir um serviço |
| RN04 | A URL do healthcheck deve ter formato válido |
| RN05 | A URL do healthcheck deve responder com status code entre 200 e 204 para ser aceita |
| RN06 | Status `Degraded` do padrão HealthChecks não invalida a URL — apenas status code fora do intervalo 200–204 |
| RN07 | Um serviço pode ter múltiplos pais na hierarquia |
| RN08 | Um serviço pode estar nos estados: **Ativo**, **Inativo** ou **Removido** |
| RN09 | Serviço **Inativo** para de ser monitorado, mantém histórico e perde vínculos hierárquicos enquanto inativo |
| RN10 | Ao reativar um serviço, o sistema pergunta se deseja restaurar a hierarquia anterior |
| RN11 | Serviço **Removido** sai da lista de monitoramento, mantém histórico e perde vínculos hierárquicos permanentemente |
| RN12 | Campos editáveis de um serviço monitorado: URL do healthcheck, vínculos hierárquicos e status (Ativo/Inativo) |

---

### Cenário 1 — Incluir serviço no monitoramento sem hierarquia

```gherkin
Dado que o Administrador está autenticado no Portal de Serviço Administrativo
E existem sistemas disponíveis no inventário do Portal de Serviços ainda não incluídos no monitoramento
Quando o Administrador seleciona um sistema da lista
E informa uma URL de healthcheck válida que responde com status code entre 200 e 204
E confirma a inclusão
Então o sistema é incluído no monitoramento com status Ativo
E a URL do healthcheck informada é salva
```

---

### Cenário 2 — Incluir serviço no monitoramento com um ou mais pais

```gherkin
Dado que o Administrador está autenticado no Portal de Serviço Administrativo
E existem sistemas disponíveis no inventário ainda não incluídos no monitoramento
E existem serviços com status Ativo que podem ser selecionados como pai
Quando o Administrador seleciona um sistema da lista
E informa uma URL de healthcheck válida que responde com status code entre 200 e 204
E seleciona um ou mais serviços pai
E confirma a inclusão
Então o sistema é incluído no monitoramento com status Ativo
E a URL do healthcheck informada é salva
E os vínculos hierárquicos com os serviços pai são registrados
```

---

### Cenário 3 — Tentativa de inclusão sem informar URL do healthcheck

```gherkin
Dado que o Administrador está autenticado no Portal de Serviço Administrativo
E selecionou um sistema da lista para incluir no monitoramento
Quando o Administrador confirma a inclusão sem informar a URL do healthcheck
Então o sistema exibe uma mensagem indicando que o campo URL do healthcheck é obrigatório
E o serviço não é incluído no monitoramento
```

---

### Cenário 4 — Tentativa de inclusão com URL em formato inválido

```gherkin
Dado que o Administrador está autenticado no Portal de Serviço Administrativo
E selecionou um sistema da lista para incluir no monitoramento
Quando o Administrador informa uma URL com formato inválido
E confirma a inclusão
Então o sistema exibe uma mensagem indicando que a URL informada não está funcionando
E o serviço não é incluído no monitoramento
```

---

### Cenário 5 — Tentativa de inclusão com URL que não responde com sucesso

```gherkin
Dado que o Administrador está autenticado no Portal de Serviço Administrativo
E selecionou um sistema da lista para incluir no monitoramento
Quando o Administrador informa uma URL com formato válido
E o endpoint retorna um status code fora do intervalo 200–204
E confirma a inclusão
Então o sistema exibe uma mensagem indicando que a URL informada não está funcionando
E o serviço não é incluído no monitoramento
```

---

### Cenário 6 — URL com resposta de status Degraded não invalida o cadastro

```gherkin
Dado que o Administrador está autenticado no Portal de Serviço Administrativo
E selecionou um sistema da lista para incluir no monitoramento
Quando o Administrador informa uma URL com formato válido
E o endpoint retorna status Degraded com status code entre 200 e 204
E confirma a inclusão
Então o sistema é incluído no monitoramento com status Ativo
E a URL do healthcheck informada é salva
```

---

### Cenário 7 — Inventário externo indisponível ao tentar incluir serviço

```gherkin
Dado que o Administrador está autenticado no Portal de Serviço Administrativo
E o endpoint de inventário do Portal de Serviços está indisponível
Quando o Administrador acessa a tela de inclusão de serviços
Então a lista de sistemas disponíveis é exibida vazia
```

---

### Cenário 8 — Editar URL do healthcheck de um serviço monitorado

```gherkin
Dado que o Administrador está autenticado no Portal de Serviço Administrativo
E existe um serviço com status Ativo no monitoramento
Quando o Administrador altera a URL do healthcheck do serviço
E a nova URL tem formato válido e responde com status code entre 200 e 204
E confirma a edição
Então a nova URL do healthcheck é salva para o serviço
```

---

### Cenário 9 — Editar vínculos hierárquicos de um serviço monitorado

```gherkin
Dado que o Administrador está autenticado no Portal de Serviço Administrativo
E existe um serviço com status Ativo no monitoramento
Quando o Administrador adiciona ou remove um ou mais serviços pai do vínculo hierárquico
E confirma a edição
Então os vínculos hierárquicos do serviço são atualizados conforme informado
```

---

### Cenário 10 — Inativar serviço monitorado

```gherkin
Dado que o Administrador está autenticado no Portal de Serviço Administrativo
E existe um serviço com status Ativo no monitoramento
Quando o Administrador inativa o serviço
Então o serviço passa para status Inativo
E o monitoramento do serviço é interrompido
E os vínculos hierárquicos do serviço são removidos
E o histórico de indisponibilidades é mantido
```

---

### Cenário 11 — Reativar serviço sem restaurar hierarquia

```gherkin
Dado que o Administrador está autenticado no Portal de Serviço Administrativo
E existe um serviço com status Inativo que possuía vínculos hierárquicos antes de ser inativado
Quando o Administrador ativa o serviço
E opta por não restaurar a hierarquia anterior
Então o serviço passa para status Ativo
E o monitoramento do serviço é retomado
E os vínculos hierárquicos permanecem removidos
```

---

### Cenário 12 — Reativar serviço restaurando hierarquia anterior

```gherkin
Dado que o Administrador está autenticado no Portal de Serviço Administrativo
E existe um serviço com status Inativo que possuía vínculos hierárquicos antes de ser inativado
Quando o Administrador ativa o serviço
E opta por restaurar a hierarquia anterior
Então o serviço passa para status Ativo
E o monitoramento do serviço é retomado
E os vínculos hierárquicos anteriores são restaurados
```

---

### Cenário 13 — Remover serviço do monitoramento

```gherkin
Dado que o Administrador está autenticado no Portal de Serviço Administrativo
E existe um serviço no monitoramento
Quando o Administrador remove o serviço
Então o serviço passa para status Removido
E o serviço não aparece mais na lista de serviços monitorados
E todos os vínculos hierárquicos do serviço são removidos permanentemente
E o histórico de indisponibilidades é mantido
```

---

## Pontos em Aberto — Gerenciamento de Serviços

> Nenhum ponto em aberto identificado para esta feature.

---

## Cobertura — Gerenciamento de Serviços

| Cenário | Tipo |
|---------|------|
| 1 — Incluir sem hierarquia | Happy path |
| 2 — Incluir com um ou mais pais | Happy path com variação |
| 3 — Inclusão sem URL | Exceção — validação obrigatória |
| 4 — Inclusão com URL formato inválido | Exceção — validação de formato |
| 5 — Inclusão com URL sem resposta de sucesso | Exceção — validação de chamada |
| 6 — URL com Degraded não invalida | Regra de negócio específica |
| 7 — Inventário externo indisponível | Exceção — dependência externa |
| 8 — Editar URL | Happy path — edição |
| 9 — Editar hierarquia | Happy path — edição |
| 10 — Inativar serviço | Happy path — ciclo de vida |
| 11 — Reativar sem restaurar hierarquia | Alternativo — ciclo de vida |
| 12 — Reativar restaurando hierarquia | Alternativo — ciclo de vida |
| 13 — Remover serviço | Happy path — ciclo de vida |

---

## Feature: Monitoramento de Healthcheck

**In order to** registrar com precisão os períodos de indisponibilidade dos sistemas
**As** Sistema de Monitoramento
**I want** verificar periodicamente os endpoints de healthcheck, detectar indisponibilidades com confirmação em duas etapas via buffer e persistir os períodos de indisponibilidade no banco de dados Oracle 19c

---

### Regras de Negócio

| ID | Regra |
|----|-------|
| RN13 | O sistema verifica os endpoints de healthcheck de todos os serviços com status **Ativo** na frequência configurada (padrão: 1 minuto) |
| RN14 | Serviços com status **Inativo** ou **Removido** não são verificados |
| RN15 | Uma resposta com status code fora do intervalo 200–204 é tratada como indisponibilidade |
| RN16 | Erros de conexão (timeout, DNS não resolve, host inacessível) são tratados como indisponibilidade |
| RN17 | A primeira falha detectada cria um registro no buffer em memória para o endpoint; o período de indisponibilidade ainda **não** é persistido no banco |
| RN18 | A segunda falha consecutiva confirma a indisponibilidade: o sistema persiste o início do período no banco Oracle 19c com o horário da primeira falha registrada no buffer e atualiza o buffer indicando que o registro já está sendo gravado |
| RN19 | Falhas consecutivas após a segunda mantêm o período de indisponibilidade aberto no banco; nenhuma ação adicional é necessária |
| RN20 | Quando o endpoint retorna sucesso (200–204), o sistema fecha o período de indisponibilidade no banco gravando o horário de fim, limpa o buffer e retoma o ciclo normal de verificação |
| RN21 | O buffer é mantido exclusivamente em memória; em caso de restart do sistema, o buffer é zerado e o fluxo reinicia do zero sem recuperação de estado anterior |
| RN22 | Apenas os períodos de indisponibilidade (início e fim) são persistidos; verificações individuais de sucesso não são armazenadas |
| RN23 | Falha ao persistir no banco Oracle 19c gera uma exceção que é enviada ao sistema de log do tribunal |

---

### Cenário 14 — Verificação com sucesso em serviço sem histórico de falha

```gherkin
Dado que existe um serviço com status Ativo no monitoramento
E o serviço não possui registro no buffer
Quando o sistema verifica o endpoint de healthcheck
E o endpoint retorna status code entre 200 e 204
Então nenhuma ação é executada
E o ciclo de verificação continua normalmente
```

---

### Cenário 15 — Primeira falha detectada (criação no buffer)

```gherkin
Dado que existe um serviço com status Ativo no monitoramento
E o serviço não possui registro no buffer
Quando o sistema verifica o endpoint de healthcheck
E o endpoint retorna status code fora do intervalo 200–204
Então um registro é criado no buffer para o endpoint com o horário da falha
E nenhum período de indisponibilidade é persistido no banco
```

---

### Cenário 16 — Primeira falha por erro de conexão (criação no buffer)

```gherkin
Dado que existe um serviço com status Ativo no monitoramento
E o serviço não possui registro no buffer
Quando o sistema tenta verificar o endpoint de healthcheck
E ocorre erro de conexão (timeout, DNS não resolve ou host inacessível)
Então um registro é criado no buffer para o endpoint com o horário da falha
E nenhum período de indisponibilidade é persistido no banco
```

---

### Cenário 17 — Segunda falha consecutiva (confirmação e persistência no banco)

```gherkin
Dado que existe um serviço com status Ativo no monitoramento
E o serviço possui registro no buffer indicando a primeira falha
Quando o sistema verifica o endpoint de healthcheck novamente
E o endpoint retorna status code fora do intervalo 200–204
Então o início do período de indisponibilidade é persistido no banco Oracle 19c com o horário da primeira falha registrada no buffer
E o buffer é atualizado indicando que o período já está sendo gravado no banco
```

---

### Cenário 18 — Falhas subsequentes após confirmação

```gherkin
Dado que existe um serviço com status Ativo no monitoramento
E o serviço possui registro no buffer indicando que o período já está sendo gravado no banco
Quando o sistema verifica o endpoint de healthcheck
E o endpoint retorna status code fora do intervalo 200–204
Então nenhuma ação adicional é executada
E o período de indisponibilidade permanece aberto no banco
```

---

### Cenário 19 — Recuperação do serviço após indisponibilidade confirmada

```gherkin
Dado que existe um serviço com status Ativo no monitoramento
E o serviço possui um período de indisponibilidade aberto no banco
E o serviço possui registro no buffer indicando que o período está sendo gravado
Quando o sistema verifica o endpoint de healthcheck
E o endpoint retorna status code entre 200 e 204
Então o período de indisponibilidade é fechado no banco com o horário de fim
E o registro do serviço é removido do buffer
E o ciclo de verificação retoma normalmente
```

---

### Cenário 20 — Recuperação após primeira falha (sem persistência no banco)

```gherkin
Dado que existe um serviço com status Ativo no monitoramento
E o serviço possui registro no buffer apenas com a primeira falha (período ainda não persistido no banco)
Quando o sistema verifica o endpoint de healthcheck
E o endpoint retorna status code entre 200 e 204
Então o registro do serviço é removido do buffer
E nenhum período de indisponibilidade é persistido no banco
E o ciclo de verificação retoma normalmente
```

---

### Cenário 21 — Serviço com status Inativo não é verificado

```gherkin
Dado que existe um serviço com status Inativo no monitoramento
Quando o ciclo de verificação de healthcheck é executado
Então o endpoint do serviço não é verificado
```

---

### Cenário 22 — Serviço com status Removido não é verificado

```gherkin
Dado que existe um serviço com status Removido no monitoramento
Quando o ciclo de verificação de healthcheck é executado
Então o endpoint do serviço não é verificado
```

---

### Cenário 23 — Restart do sistema zera o buffer

```gherkin
Dado que o sistema de monitoramento possui registros no buffer para um ou mais endpoints
Quando o sistema de monitoramento é reiniciado
Então o buffer é zerado
E o fluxo de verificação reinicia do zero para todos os serviços
E nenhuma tentativa de recuperação do estado anterior do buffer é realizada
```

---

### Cenário 24 — Falha ao persistir indisponibilidade no banco

```gherkin
Dado que existe um serviço com status Ativo no monitoramento
E o serviço possui registro no buffer com a primeira falha
Quando o sistema verifica o endpoint e detecta a segunda falha consecutiva
E o banco de dados Oracle 19c está indisponível no momento da persistência
Então uma exceção é gerada
E a exceção é enviada ao sistema de log do tribunal
E o período de indisponibilidade não é persistido no banco
```

---

### Pontos em Aberto — Monitoramento de Healthcheck

> Nenhum ponto em aberto identificado para esta feature.

---

### Cobertura — Monitoramento de Healthcheck

| Cenário | Tipo |
|---------|------|
| 14 — Verificação com sucesso sem histórico de falha | Happy path |
| 15 — Primeira falha por resposta inválida | Buffer — primeira etapa |
| 16 — Primeira falha por erro de conexão | Buffer — primeira etapa (variação) |
| 17 — Segunda falha consecutiva — persistência no banco | Buffer — confirmação |
| 18 — Falhas subsequentes após confirmação | Regra de negócio — estado contínuo |
| 19 — Recuperação após indisponibilidade confirmada | Happy path — recuperação |
| 20 — Recuperação após primeira falha (sem banco) | Alternativo — recuperação parcial |
| 21 — Serviço Inativo não verificado | Regra de negócio — ciclo de vida |
| 22 — Serviço Removido não verificado | Regra de negócio — ciclo de vida |
| 23 — Restart zera buffer | Exceção — resiliência |
| 24 — Falha ao persistir no banco | Exceção — dependência externa |
