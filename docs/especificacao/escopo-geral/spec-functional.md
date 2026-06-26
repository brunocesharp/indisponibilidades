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

## Pontos em Aberto

> Nenhum ponto em aberto identificado para esta feature.

---

## Cobertura

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
