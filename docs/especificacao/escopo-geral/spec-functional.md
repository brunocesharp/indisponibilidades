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

## Feature: Hierarquia e Propagação de Indisponibilidade

**In order to** garantir que o tempo de indisponibilidade de serviços dependentes seja contabilizado corretamente mesmo quando a falha se originou em outro serviço
**As** Sistema de Monitoramento
**I want** acumular o tempo em que ao menos um serviço da cadeia hierárquica estava indisponível, calculando a união dos intervalos de falha sem duplicar períodos sobrepostos

---

### Regras de Negócio

| ID | Regra |
|----|-------|
| RN13 | Todos os serviços continuam sendo verificados normalmente via healthcheck, independentemente do estado dos serviços pai |
| RN14 | O tempo de indisponibilidade de um serviço filho é calculado como a **união** dos intervalos em que ao menos um serviço da cadeia (ele próprio ou qualquer pai) estava indisponível |
| RN15 | Intervalos sobrepostos não são somados — apenas o período em que ao menos um estava indisponível é contabilizado |
| RN16 | Se um serviço possui múltiplos pais, basta **um** pai estar indisponível para o tempo desse pai ser incluído na união do filho |
| RN17 | O limiar para geração do relatório do usuário é de **120 minutos acumulados** no dia, calculado pela união dos intervalos conforme RN14 |
| RN18 | O relatório do **usuário** informa apenas que o serviço ficou indisponível e o tempo total acumulado — sem detalhar origem da falha |
| RN19 | O relatório do **administrador** detalha todos os serviços individualmente, incluindo os que ficaram indisponíveis por herança hierárquica |

---

### Cenário 1 — Filho herda indisponibilidade do pai sem falha própria

```gherkin
Dado que o serviço FILHO está Ativo e saudável
E o serviço PAI está Ativo e é pai do FILHO
Quando o PAI fica indisponível entre 11h00 e 13h30 (150 minutos)
E o FILHO responde com sucesso em todas as verificações nesse período
Então o FILHO acumula 150 minutos de indisponibilidade no dia
E o relatório do usuário é gerado para o FILHO ao atingir 120 minutos acumulados
E o relatório do administrador indica que a indisponibilidade do FILHO foi herdada do PAI
```

---

### Cenário 2 — Filho e pai ficam indisponíveis em períodos sem sobreposição

```gherkin
Dado que o serviço FILHO está Ativo
E o serviço PAI está Ativo e é pai do FILHO
Quando o FILHO fica indisponível entre 11h45 e 12h00 (15 minutos)
E o PAI fica indisponível entre 12h00 e 12h15 (15 minutos)
Então o FILHO acumula 30 minutos de indisponibilidade no dia
E os dois períodos são contabilizados sem sobreposição
```

---

### Cenário 3 — Filho e pai ficam indisponíveis em períodos com sobreposição

```gherkin
Dado que o serviço FILHO está Ativo
E o serviço PAI está Ativo e é pai do FILHO
Quando o FILHO fica indisponível entre 11h45 e 12h00 (15 minutos)
E o PAI fica indisponível entre 11h50 e 12h15 (25 minutos)
Então o FILHO acumula 30 minutos de indisponibilidade no dia
E o período de sobreposição entre 11h50 e 12h00 não é contabilizado duas vezes
```

---

### Cenário 4 — Filho com múltiplos pais, apenas um indisponível

```gherkin
Dado que o serviço FILHO está Ativo e saudável
E o serviço PAI-A está Ativo e é pai do FILHO
E o serviço PAI-B está Ativo e é pai do FILHO
Quando o PAI-A fica indisponível entre 10h00 e 12h30 (150 minutos)
E o PAI-B permanece saudável durante todo o período
E o FILHO responde com sucesso em todas as verificações
Então o FILHO acumula 150 minutos de indisponibilidade no dia
E o relatório do usuário é gerado para o FILHO ao atingir 120 minutos acumulados
```

---

### Cenário 5 — Filho com múltiplos pais, ambos indisponíveis em períodos sobrepostos

```gherkin
Dado que o serviço FILHO está Ativo e saudável
E o serviço PAI-A está Ativo e é pai do FILHO
E o serviço PAI-B está Ativo e é pai do FILHO
Quando o PAI-A fica indisponível entre 10h00 e 11h00 (60 minutos)
E o PAI-B fica indisponível entre 10h30 e 11h30 (60 minutos)
E o FILHO responde com sucesso em todas as verificações
Então o FILHO acumula 90 minutos de indisponibilidade no dia
E o período de sobreposição entre 10h30 e 11h00 não é contabilizado duas vezes
```

---

### Cenário 6 — Filho não atinge o limiar de 120 minutos

```gherkin
Dado que o serviço FILHO está Ativo
E o serviço PAI está Ativo e é pai do FILHO
Quando a união dos intervalos de indisponibilidade do FILHO ao longo do dia totaliza 90 minutos
Então nenhum relatório do usuário é gerado para o FILHO
E o FILHO aparece no relatório diário do administrador com 90 minutos acumulados
```

---

### Cenário 7 — Hierarquia em cadeia (avô → pai → filho)

```gherkin
Dado que o serviço AVÔ está Ativo
E o serviço PAI está Ativo e é filho do AVÔ
E o serviço FILHO está Ativo e é filho do PAI
Quando o AVÔ fica indisponível entre 09h00 e 11h30 (150 minutos)
E o PAI responde com sucesso em todas as verificações
E o FILHO responde com sucesso em todas as verificações
Então o PAI acumula 150 minutos de indisponibilidade no dia
E o FILHO acumula 150 minutos de indisponibilidade no dia
E o relatório do usuário é gerado para o PAI e para o FILHO ao atingirem 120 minutos
E o relatório do administrador indica que a origem da falha foi o AVÔ
```

---

### Cenário 8 — Pai retoma antes, filho continua falhando por conta própria

```gherkin
Dado que o serviço FILHO está Ativo
E o serviço PAI está Ativo e é pai do FILHO
Quando o PAI fica indisponível entre 10h00 e 10h40 (40 minutos) e retorna saudável
E o FILHO continua falhando no healthcheck entre 10h30 e 11h30 (60 minutos)
Então o FILHO acumula 90 minutos de indisponibilidade no dia
E o período de sobreposição entre 10h30 e 10h40 não é contabilizado duas vezes
```

---

### Cenário 9 — Serviço sem hierarquia não herda nenhuma indisponibilidade

```gherkin
Dado que o serviço A está Ativo sem nenhum serviço pai vinculado
E o serviço B está Ativo sem vínculo com o serviço A
Quando o serviço B fica indisponível por qualquer período
Então o serviço A não acumula nenhum tempo de indisponibilidade herdado do serviço B
E o serviço A continua sendo monitorado normalmente
```

---

## Pontos em Aberto

> Nenhum ponto em aberto identificado para esta feature.

---

## Cobertura — Feature: Hierarquia e Propagação

| Cenário | Tipo |
|---------|------|
| 1 — Filho herda do pai sem falha própria | Happy path — herança pura |
| 2 — Pai e filho indisponíveis sem sobreposição | Happy path — união simples |
| 3 — Pai e filho indisponíveis com sobreposição | Regra de negócio — sem duplicação |
| 4 — Múltiplos pais, apenas um indisponível | Happy path — múltiplos pais |
| 5 — Múltiplos pais com sobreposição entre eles | Regra de negócio — múltiplos pais + sem duplicação |
| 6 — Filho não atinge limiar de 120 min | Alternativo — abaixo do limiar |
| 7 — Hierarquia em cadeia (avô → pai → filho) | Happy path — propagação multinível |
| 8 — Pai retoma, filho continua falhando | Alternativo — falhas em sequência mista |
| 9 — Serviço sem hierarquia não herda nada | Isolamento — sem vínculo |

---

## Feature: Monitoramento de Healthcheck

**In order to** detectar e contabilizar com precisão os períodos de indisponibilidade de cada serviço ao longo do dia
**As** Sistema de Monitoramento
**I want** verificar periodicamente o endpoint de healthcheck de cada serviço ativo e registrar o estado retornado, acumulando o tempo de indisponibilidade a partir da primeira verificação do dia

---

### Regras de Negócio

| ID | Regra |
|----|-------|
| RN20 | Apenas serviços com status **Ativo** são verificados; serviços **Inativos** não recebem verificações até serem reativados |
| RN21 | A primeira verificação ocorre após o primeiro intervalo configurado (padrão: 1 minuto), nunca imediatamente ao iniciar |
| RN22 | O serviço é considerado **indisponível** quando o healthcheck retorna: status HTTP fora de 200–204, status `Unhealthy` (0), ou status `Degraded` (1) |
| RN23 | O serviço é considerado **disponível** apenas quando o healthcheck retorna status HTTP 200–204 **e** status `Healthy` (2) |
| RN24 | Timeout de resposta é de **1 minuto**; ausência de resposta nesse prazo conta como indisponibilidade |
| RN25 | Se o sistema de monitoramento ficar fora do ar, o período sem verificação é contabilizado integralmente como indisponibilidade para todos os serviços ativos |
| RN26 | O acúmulo diário reinicia à meia-noite (00h00); o contador do dia anterior é fechado no momento exato da virada |
| RN27 | Serviços cadastrados durante o dia só passam a ser monitorados a partir de 00h00 do dia seguinte |
| RN28 | O intervalo de verificação é configurável por serviço; o padrão é **1 minuto** |

---

### Cenário 1 — Verificação bem-sucedida (Healthy)

```gherkin
Dado que o serviço "API de Pagamentos" está Ativo com intervalo de 1 minuto
E o endpoint de healthcheck está configurado como "https://pagamentos/health"
Quando o intervalo de 1 minuto decorre após o início do monitoramento
E o endpoint retorna HTTP 200 com status Healthy (2)
Então o sistema registra o serviço como disponível naquele instante
E nenhum tempo de indisponibilidade é acumulado
E a próxima verificação é agendada para 1 minuto depois
```

---

### Cenário 2 — Healthcheck retorna Unhealthy

```gherkin
Dado que o serviço "API de Pagamentos" está Ativo com intervalo de 1 minuto
E o serviço estava disponível até 11h59
Quando o intervalo decorre e o endpoint retorna HTTP 200 com status Unhealthy (0)
Então o sistema registra o serviço como indisponível a partir de 12h00
E inicia a contagem do tempo de indisponibilidade
E a próxima verificação é agendada para 1 minuto depois
```

---

### Cenário 3 — Healthcheck retorna Degraded

```gherkin
Dado que o serviço "API de Pagamentos" está Ativo com intervalo de 1 minuto
E o serviço estava disponível até 14h29
Quando o intervalo decorre e o endpoint retorna HTTP 200 com status Degraded (1)
Então o sistema registra o serviço como indisponível a partir de 14h30
E inicia a contagem do tempo de indisponibilidade
```

---

### Cenário 4 — Healthcheck retorna status HTTP fora de 200–204

```gherkin
Dado que o serviço "API de Pagamentos" está Ativo com intervalo de 1 minuto
E o serviço estava disponível até 09h14
Quando o intervalo decorre e o endpoint retorna HTTP 503
Então o sistema registra o serviço como indisponível a partir de 09h15
E inicia a contagem do tempo de indisponibilidade
```

---

### Cenário 5 — Timeout na verificação

```gherkin
Dado que o serviço "API de Pagamentos" está Ativo com intervalo de 1 minuto
E o serviço estava disponível até 10h04
Quando o intervalo decorre e o endpoint não responde dentro de 1 minuto
Então o sistema registra o serviço como indisponível a partir de 10h05
E inicia a contagem do tempo de indisponibilidade
E a próxima verificação é agendada normalmente
```

---

### Cenário 6 — Serviço retorna a ficar disponível após período de falha

```gherkin
Dado que o serviço "API de Pagamentos" está Ativo
E estava indisponível desde 11h00
Quando o intervalo decorre e o endpoint retorna HTTP 200 com status Healthy (2)
Então o sistema encerra o período de indisponibilidade
E registra o intervalo de falha no acúmulo do dia
E a contagem de indisponibilidade para de crescer
```

---

### Cenário 7 — Sistema de monitoramento fica fora do ar

```gherkin
Dado que o serviço "API de Pagamentos" está Ativo e disponível às 08h00
E o sistema de monitoramento fica indisponível entre 08h00 e 08h10 (10 minutos)
Quando o sistema de monitoramento volta às 08h10
Então os 10 minutos sem verificação são contabilizados como indisponibilidade para todos os serviços ativos
E o monitoramento retoma normalmente a partir de 08h10
```

---

### Cenário 8 — Virada de dia fecha o acúmulo anterior

```gherkin
Dado que o serviço "API de Pagamentos" está Ativo
E estava indisponível desde 23h50 do dia 25/06
Quando o relógio atinge 00h00 do dia 26/06
Então o período de 23h50 a 00h00 (10 minutos) é fechado e registrado no acúmulo do dia 25/06
E um novo acúmulo começa para o dia 26/06 a partir de 00h00
E a indisponibilidade em curso continua sendo contabilizada no novo dia
```

---

### Cenário 9 — Serviço cadastrado no meio do dia não é monitorado até o dia seguinte

```gherkin
Dado que um novo serviço "API de Relatórios" é cadastrado às 14h30 do dia 25/06 com status Ativo
Quando o sistema avalia quais serviços devem ser monitorados
Então o serviço "API de Relatórios" não é verificado no restante do dia 25/06
E o monitoramento inicia às 00h01 do dia 26/06 (após o primeiro intervalo a partir da meia-noite)
```

---

### Cenário 10 — Serviço inativo não é verificado

```gherkin
Dado que o serviço "API de Relatórios" está com status Inativo
Quando o intervalo de verificação decorre
Então o sistema não realiza nenhuma chamada ao endpoint do serviço
E nenhum tempo de indisponibilidade é acumulado para o serviço
```

---

### Cenário 11 — Serviço reativado volta a ser monitorado

```gherkin
Dado que o serviço "API de Relatórios" estava Inativo desde 09h00
Quando o administrador altera o status do serviço para Ativo às 11h00
Então o sistema passa a incluir o serviço nas verificações periódicas
E a primeira verificação ocorre após o primeiro intervalo a partir das 11h00
E o acúmulo de indisponibilidade começa a ser contabilizado a partir desse momento
```

---

### Cenário 12 — Intervalo de verificação personalizado

```gherkin
Dado que o serviço "API de Relatórios" está Ativo com intervalo configurado em 5 minutos
Quando o monitoramento está em execução
Então o sistema verifica o healthcheck a cada 5 minutos
E não realiza verificações nos intervalos intermediários
```

---

## Cobertura — Feature: Monitoramento de Healthcheck

| Cenário | Tipo |
|---------|------|
| 1 — Verificação bem-sucedida | Happy path |
| 2 — Retorna Unhealthy | Indisponibilidade por status |
| 3 — Retorna Degraded | Indisponibilidade por status |
| 4 — Retorna HTTP fora de 200–204 | Indisponibilidade por HTTP |
| 5 — Timeout na verificação | Indisponibilidade por ausência de resposta |
| 6 — Serviço retorna a ficar disponível | Encerramento de período de falha |
| 7 — Sistema de monitoramento fora do ar | Exceção — downtime do próprio sistema |
| 8 — Virada de dia | Regra de negócio — fechamento do acúmulo |
| 9 — Serviço cadastrado no meio do dia | Regra de negócio — início de monitoramento |
| 10 — Serviço inativo não é verificado | Regra de negócio — status Inativo |
| 11 — Serviço reativado volta a ser monitorado | Alternativo — reativação |
| 12 — Intervalo personalizado | Regra de negócio — configuração de intervalo |
