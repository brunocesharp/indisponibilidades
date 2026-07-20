# Especificação Funcional — Escopo Geral

> Gerado em: 13/07/2026
> Versão: 2.0
> Status: Rascunho
> Referência: docs/escopo/escopo-geral/escopo.md

---

## Contexto

O Sistema de Monitoramento de Indisponibilidade monitora a saúde das aplicações do TCE-MG via endpoints de healthcheck, registra os períodos de indisponibilidade em banco Oracle 19c e gera relatórios autenticados. Os relatórios permitem que cidadãos comprovem indisponibilidades em petições processuais e que administradores acompanhem a saúde dos sistemas — atendendo à minuta regulatória do Tribunal com prazo atrelado ao Portal de Serviços.

---

## Features Especificadas

- [Feature 1: Gerenciamento de Serviços Monitorados](#feature-1-gerenciamento-de-serviços-monitorados)
- [Feature 2: Monitoramento de Healthcheck](#feature-2-monitoramento-de-healthcheck)
- [Feature 3: Hierarquia de Serviços](#feature-3-hierarquia-de-serviços)
- [Feature 4: Relatório por Limiar](#feature-4-relatório-por-limiar)
- [Feature 5: Relatório Diário do Administrador](#feature-5-relatório-diário-do-administrador)
- [Feature 6: Consulta de Relatórios do Usuário](#feature-6-consulta-de-relatórios-do-usuário)
- [Feature 7: Consulta de Relatórios do Administrador](#feature-7-consulta-de-relatórios-do-administrador)

---

## Feature 1: Gerenciamento de Serviços Monitorados

### Narrativa

```
Feature: Gerenciamento de Serviços Monitorados
  In order to garantir que apenas sistemas válidos e acessíveis sejam monitorados
  As Administrador de Sistemas
  I want incluir, configurar e remover serviços do monitoramento com controle de ciclo de vida
```

### Regras de Negócio

- **RN-1.1** — A lista de sistemas disponíveis para inclusão é obtida via endpoint externo do Portal de Serviços; sistemas já incluídos não aparecem nessa lista.
- **RN-1.2** — A URL do healthcheck é obrigatória e deve ter formato válido.
- **RN-1.3** — A URL do healthcheck deve responder com status code entre 200 e 204 para ser aceita; status `Degraded` com código 200–204 não invalida a URL.
- **RN-1.4** — Um serviço pode ter múltiplos pais na hierarquia.
- **RN-1.5** — Um serviço pode estar nos estados **Ativo**, **Inativo** ou **Removido**; campos editáveis são URL do healthcheck, vínculos hierárquicos e status.
- **RN-1.6** — Inativar um serviço interrompe o monitoramento e remove os vínculos hierárquicos, mantendo o histórico.
- **RN-1.7** — Reativar um serviço exige decisão explícita sobre restaurar ou não a hierarquia anterior.
- **RN-1.8** — Remover um serviço elimina os vínculos hierárquicos permanentemente e mantém o histórico; o serviço não aparece mais na lista de monitorados.

### Cenários

---

#### Cenário 1.1: Incluir serviço sem hierarquia

```gherkin
Dado que sou Administrador autenticado no Portal de Serviço Administrativo
  E existem sistemas no inventário do Portal ainda não incluídos no monitoramento
Quando incluo um sistema informando uma URL de healthcheck que responde com status 200
Então o serviço passa a ser monitorado com status Ativo
  E a URL do healthcheck informada é salva
```

---

#### Cenário 1.2: Incluir serviço com um ou mais pais

```gherkin
Dado que sou Administrador autenticado
  E existem serviços com status Ativo disponíveis como pai
Quando incluo um sistema selecionando dois serviços pai e informando URL de healthcheck válida
Então o serviço passa a ser monitorado com status Ativo
  E os dois vínculos hierárquicos com os pais são registrados
```

---

#### Cenário 1.3: Falha na validação da URL do healthcheck

```gherkin
Esquema do Cenário: Rejeitar URL de healthcheck inválida
  Dado que sou Administrador autenticado
    E selecionei um sistema do inventário para incluir
  Quando tento incluir o serviço informando URL com <situação>
  Então o serviço não é incluído no monitoramento
    E o sistema exibe mensagem indicando que <mensagem>

  Exemplos:
    | situação                              | mensagem                              |
    | campo vazio                           | a URL do healthcheck é obrigatória    |
    | formato inválido (sem https://)       | a URL informada não está funcionando  |
    | URL válida que retorna status 500     | a URL informada não está funcionando  |
```

---

#### Cenário 1.4: Inventário externo indisponível

```gherkin
Dado que sou Administrador autenticado
  E o endpoint de inventário do Portal de Serviços está indisponível
Quando acesso a tela de inclusão de serviços
Então a lista de sistemas disponíveis é exibida vazia
```

---

#### Cenário 1.5: Editar serviço monitorado

```gherkin
Dado que existe um serviço com status Ativo no monitoramento
Quando edito a URL do healthcheck para uma URL válida que responde com status 200
  E removo um serviço pai e adiciono outro
Então a nova URL é salva
  E os vínculos hierárquicos são atualizados conforme informado
```

---

#### Cenário 1.6: Inativar serviço que possui filhos vinculados

```gherkin
Dado que o serviço E-TCE tem status Ativo
  E o serviço Consulta Processual está vinculado a E-TCE como filho
Quando inativo o serviço E-TCE
Então E-TCE passa para status Inativo
  E o monitoramento de E-TCE é interrompido
  E o vínculo hierárquico entre E-TCE e Consulta Processual é removido
  E o histórico de indisponibilidades de E-TCE é mantido
```

---

#### Cenário 1.7: Reativar serviço com opção de restaurar hierarquia

```gherkin
Esquema do Cenário: Reativar serviço com ou sem hierarquia anterior
  Dado que o serviço E-TCE tem status Inativo
    E possuía vínculo hierárquico com Consulta Processual antes de ser inativado
  Quando reativo E-TCE e <decisão> restaurar a hierarquia anterior
  Então E-TCE passa para status Ativo
    E o monitoramento de E-TCE é retomado
    E os vínculos hierárquicos <resultado>

  Exemplos:
    | decisão  | resultado                                       |
    | opto por | são restaurados com Consulta Processual como pai |
    | opto por não | permanecem removidos                        |
```

---

#### Cenário 1.8: Remover serviço do monitoramento

```gherkin
Dado que o serviço Portal de Serviços tem status Inativo
  E possuía vínculos hierárquicos registrados
Quando removo o serviço Portal de Serviços
Então o serviço passa para status Removido
  E não aparece mais na lista de serviços monitorados
  E todos os vínculos hierárquicos são eliminados permanentemente
  E o histórico de indisponibilidades é mantido
```

### Pontos em Aberto

> Nenhum ponto em aberto identificado para esta feature.

---

## Feature 2: Monitoramento de Healthcheck

### Narrativa

```
Feature: Monitoramento de Healthcheck
  In order to registrar com precisão os períodos reais de indisponibilidade, evitando falsos positivos por falhas transitórias de rede
  As Sistema de Monitoramento
  I want verificar periodicamente os endpoints, confirmar indisponibilidade com duas falhas consecutivas via buffer e persistir apenas períodos confirmados no banco
```

### Regras de Negócio

- **RN-2.1** — O sistema verifica os endpoints de todos os serviços com status **Ativo** na frequência configurada (padrão: 1 minuto).
- **RN-2.2** — Serviços com status **Inativo** ou **Removido** não são verificados.
- **RN-2.3** — Resposta com status code fora de 200–204 e erro de conexão (timeout, DNS, host inacessível) são tratados como indisponibilidade.
- **RN-2.4** — A primeira falha cria registro no buffer em memória; o período **não** é persistido no banco ainda.
- **RN-2.5** — A segunda falha consecutiva confirma a indisponibilidade: persiste o início do período no Oracle 19c com o horário da primeira falha e atualiza o buffer.
- **RN-2.6** — Quando o endpoint retorna sucesso, o período é fechado no banco com o horário de fim, o buffer é limpo e o ciclo normal retoma.
- **RN-2.7** — O buffer é mantido exclusivamente em memória; restart do sistema zera o buffer sem recuperação de estado.
- **RN-2.8** — Apenas os períodos de indisponibilidade são persistidos; verificações de sucesso não são armazenadas.
- **RN-2.9** — Falha ao persistir no Oracle 19c gera exceção enviada ao sistema de log do tribunal.

### Cenários

---

#### Cenário 2.1: Primeira falha cria registro no buffer sem persistir no banco

```gherkin
Dado que o serviço E-TCE tem status Ativo
  E não possui registro no buffer
Quando o endpoint de E-TCE retorna status 503
Então um registro é criado no buffer para E-TCE com o horário da falha
  E nenhum período de indisponibilidade é persistido no banco
```

---

#### Cenário 2.2: Segunda falha consecutiva confirma e persiste o período

```gherkin
Dado que o serviço E-TCE tem status Ativo
  E possui registro no buffer da primeira falha ocorrida às 11:35
Quando o endpoint de E-TCE retorna status 503 novamente
Então o período de indisponibilidade de E-TCE é persistido no banco com início às 11:35
  E o buffer é atualizado indicando que o período já está sendo gravado
```

---

#### Cenário 2.3: Recuperação fecha o período e limpa o buffer

```gherkin
Dado que o serviço E-TCE tem um período de indisponibilidade aberto no banco desde as 11:35
  E o buffer indica que o período está sendo gravado
Quando o endpoint de E-TCE retorna status 200 às 13:35
Então o período de indisponibilidade é fechado com fim às 13:35
  E o registro de E-TCE é removido do buffer
  E o ciclo de verificação retoma normalmente
```

---

#### Cenário 2.4: Recuperação após primeira falha não persiste nada no banco

```gherkin
Dado que o serviço E-TCE tem status Ativo
  E possui registro no buffer apenas da primeira falha (período não persistido no banco)
Quando o endpoint de E-TCE retorna status 200
Então o registro de E-TCE é removido do buffer
  E nenhum período de indisponibilidade é persistido no banco
```

---

#### Cenário 2.5: Erro de conexão tratado como indisponibilidade

```gherkin
Dado que o serviço E-TCE tem status Ativo
  E não possui registro no buffer
Quando ocorre timeout ao tentar verificar o endpoint de E-TCE
Então um registro é criado no buffer para E-TCE com o horário da falha
  E nenhum período de indisponibilidade é persistido no banco
```

---

#### Cenário 2.6: Serviços fora do ciclo de verificação

```gherkin
Esquema do Cenário: Serviço não verificado pelo monitoramento
  Dado que o serviço Portal de Serviços tem status <status>
  Quando o ciclo de verificação de healthcheck é executado
  Então o endpoint do serviço Portal de Serviços não é verificado

  Exemplos:
    | status   |
    | Inativo  |
    | Removido |
```

---

#### Cenário 2.7: Restart do sistema zera o buffer

```gherkin
Dado que o buffer contém registros de primeira falha para os serviços E-TCE e SIGESP
Quando o sistema de monitoramento é reiniciado
Então o buffer é zerado
  E o ciclo de verificação reinicia do zero para todos os serviços
  E nenhuma recuperação do estado anterior do buffer é realizada
```

---

#### Cenário 2.8: Falha ao persistir no banco gera exceção

```gherkin
Dado que o serviço E-TCE possui registro de primeira falha no buffer
Quando o endpoint de E-TCE falha novamente
  E o Oracle 19c está indisponível no momento da persistência
Então uma exceção é gerada e enviada ao sistema de log do tribunal
  E o período de indisponibilidade não é persistido no banco
```

### Pontos em Aberto

> Nenhum ponto em aberto identificado para esta feature.

---

## Feature 3: Hierarquia de Serviços

### Narrativa

```
Feature: Hierarquia de Serviços
  In order to enriquecer os relatórios com contexto sobre a causa raiz das falhas e as relações entre sistemas
  As Administrador de Sistemas
  I want que a hierarquia seja registrada e exibida nos relatórios, mantendo o monitoramento independente por serviço
```

### Regras de Negócio

- **RN-3.1** — Cada serviço segue o fluxo de monitoramento de forma independente; a hierarquia não interfere na detecção de indisponibilidade.
- **RN-3.2** — Um serviço pode ter múltiplos pais e múltiplos filhos.
- **RN-3.3** — O relatório do Usuário exibe apenas o sistema acessado, sem informações hierárquicas.
- **RN-3.4** — O relatório do Administrador exibe todos os sistemas com indisponibilidade no dia com a relação hierárquica indicada, mesmo que pai e filho tenham ficado indisponíveis em horários distintos.
- **RN-3.5** — Quando um serviço é recuperado, seu período é fechado independentemente do status dos demais da hierarquia.

### Cenários

---

#### Cenário 3.1: Pai e filho registram períodos independentes no banco

```gherkin
Dado que E-TCE e Consulta Processual têm status Ativo
  E Consulta Processual é filho de E-TCE
  E ambos possuem registro de primeira falha no buffer
Quando ambos os endpoints retornam status 503 novamente
Então o período de E-TCE é persistido no banco com seu próprio horário de início
  E o período de Consulta Processual é persistido no banco com seu próprio horário de início
  E cada serviço possui seu próprio registro de indisponibilidade
```

---

#### Cenário 3.2: Recuperação independente dentro da hierarquia

```gherkin
Esquema do Cenário: Recuperação de serviço independente do outro na hierarquia
  Dado que E-TCE e Consulta Processual têm períodos de indisponibilidade abertos no banco
  Quando o endpoint de <serviço> retorna status 200
  Então o período de indisponibilidade de <serviço> é fechado no banco
    E o período de <outro> permanece aberto

  Exemplos:
    | serviço              | outro                |
    | E-TCE                | Consulta Processual  |
    | Consulta Processual  | E-TCE                |
```

---

#### Cenário 3.3: Relatório do Usuário exibe apenas o sistema acessado

```gherkin
Dado que E-TCE e Consulta Processual tiveram indisponibilidade no mesmo dia
  E o usuário acessa apenas o sistema Consulta Processual
Quando o usuário consulta o relatório do dia
Então o relatório exibe apenas os períodos de indisponibilidade de Consulta Processual
  E nenhuma informação sobre E-TCE ou sobre a relação hierárquica é exibida
```

---

#### Cenário 3.4: Relatório do Administrador exibe hierarquia independente dos horários

```gherkin
Dado que E-TCE ficou indisponível das 08h às 09h
  E Consulta Processual ficou indisponível das 14h às 15h no mesmo dia
  E Consulta Processual é filho de E-TCE
Quando o Administrador consulta o relatório do dia
Então o relatório exibe o período de E-TCE com seus horários
  E o relatório exibe o período de Consulta Processual com seus horários
  E a relação hierárquica entre E-TCE (pai) e Consulta Processual (filho) é indicada no relatório
```

### Pontos em Aberto

> Nenhum ponto em aberto identificado para esta feature.

---

## Feature 4: Relatório por Limiar

### Narrativa

```
Feature: Relatório por Limiar
  In order to permitir que cidadãos comprovem indisponibilidade de sistemas em petições processuais
  As Sistema de Monitoramento
  I want gerar automaticamente ao final de cada dia um relatório autenticável com os sistemas que atingiram o limiar de indisponibilidade
```

### Regras de Negócio

- **RN-4.1** — O relatório é gerado automaticamente à meia-noite (configurável), ao final do dia.
- **RN-4.2** — O limiar de indisponibilidade é configurável (padrão: 120 minutos); um sistema entra no relatório se a **soma total** do dia for **maior ou igual** ao limiar, independente dos períodos serem contínuos ou não.
- **RN-4.3** — O relatório exibe apenas sistemas que atingiram o limiar; sistemas abaixo não aparecem.
- **RN-4.4** — Para cada sistema, o relatório exibe todos os períodos do dia (hora de início, hora de término, tempo do período) e o total acumulado.
- **RN-4.5** — O relatório não é enviado por e-mail; fica disponível apenas na página de consulta do Portal de Serviços.
- **RN-4.6** — O relatório contém: cabeçalho com logo e nome do tribunal, data de referência, tabela de períodos por sistema, total do dia e QR Code com URL de autenticação, código verificador e código do usuário.
- **RN-4.7** — O código verificador é único por relatório diário; o código do usuário é único por usuário e incluído conforme quem acessa o relatório.
- **RN-4.8** — Se nenhum sistema atingir o limiar, nenhum relatório é gerado para o dia.
- **RN-4.9** — Falha na geração gera exceção enviada ao sistema de log do tribunal.

### Cenários

---

#### Cenário 4.1: Sistemas que entram e que ficam fora do relatório por limiar

```gherkin
Esquema do Cenário: Inclusão ou exclusão de sistema pelo limiar
  Dado que o limiar configurado é 120 minutos
    E o sistema <nome> acumulou <total> minutos de indisponibilidade no dia
  Quando o relatório por limiar é gerado à meia-noite
  Então o sistema <nome> <resultado> no relatório

  Exemplos:
    | nome                | total | resultado           |
    | E-TCE               | 120   | é incluído          |
    | Consulta Processual | 135   | é incluído          |
    | Portal de Serviços  | 90    | não é incluído      |
```

---

#### Cenário 4.2: Sistema com múltiplos períodos não contínuos atinge o limiar pela soma

```gherkin
Dado que o limiar configurado é 120 minutos
  E Consulta Processual ficou indisponível das 14h às 15h (60 min) e das 17h às 18h15 (75 min)
Quando o relatório por limiar é gerado
Então Consulta Processual é incluído com os dois períodos exibidos individualmente
  E o total acumulado do dia exibe 135 minutos
```

---

#### Cenário 4.3: Nenhum sistema atinge o limiar no dia

```gherkin
Dado que nenhum sistema acumulou indisponibilidade igual ou superior a 120 minutos no dia
Quando o processamento do fechamento do dia é executado
Então nenhum relatório por limiar é gerado
  E a consulta da data exibe mensagem informando que não houve indisponibilidades
```

---

#### Cenário 4.4: Código do usuário incluído conforme quem acessa o relatório

```gherkin
Dado que o relatório por limiar do dia está disponível para consulta
  E o usuário Maria possui o código de usuário "000000123"
Quando Maria acessa o relatório
Então o QR Code do relatório exibido contém o código verificador do relatório
  E o código "000000123" de Maria
```

---

#### Cenário 4.5: Falha na geração do relatório por limiar

```gherkin
Dado que um ou mais sistemas atingiram o limiar no dia
Quando ocorre uma falha durante a geração do relatório
Então uma exceção é gerada e enviada ao sistema de log do tribunal
  E o relatório não é disponibilizado para consulta
```

### Pontos em Aberto

> Nenhum ponto em aberto identificado para esta feature.

---

## Feature 5: Relatório Diário do Administrador

### Narrativa

```
Feature: Relatório Diário do Administrador
  In order to acompanhar todas as indisponibilidades do dia com contexto hierárquico completo
  As Administrador de Sistemas
  I want receber automaticamente ao final do dia um relatório consolidado com todos os sistemas que tiveram indisponibilidade, sem filtro de limiar
```

### Regras de Negócio

- **RN-5.1** — O relatório é gerado automaticamente à meia-noite (configurável), junto com o relatório por limiar.
- **RN-5.2** — Inclui **todos** os sistemas com indisponibilidade no dia, sem filtro de limiar.
- **RN-5.3** — Exibe a relação hierárquica entre os sistemas.
- **RN-5.4** — Segue o mesmo formato do relatório por limiar, porém **sem** código verificador e **sem** código do usuário.
- **RN-5.5** — Se nenhum sistema teve indisponibilidade no dia, o relatório não é gerado.
- **RN-5.6** — O Administrador pode gerar um relatório parcial do dia atual sob demanda; o relatório parcial indica que está em andamento.
- **RN-5.7** — Falha na geração gera exceção enviada ao sistema de log do tribunal.

### Cenários

---

#### Cenário 5.1: Relatório diário inclui todos os sistemas, inclusive abaixo do limiar

```gherkin
Dado que no dia ocorreram indisponibilidades em E-TCE (120 min) e Portal de Serviços (45 min)
  E o limiar configurado é 120 minutos
Quando o relatório diário do Administrador é gerado à meia-noite
Então o relatório inclui E-TCE com seus períodos e total de 120 minutos
  E o relatório inclui Portal de Serviços com seus períodos e total de 45 minutos
  E a relação hierárquica entre os sistemas é indicada
  E o relatório não contém código verificador nem código do usuário
```

---

#### Cenário 5.2: Relatório diário não é gerado quando não há indisponibilidades

```gherkin
Dado que nenhum sistema teve indisponibilidade registrada no dia
Quando o processamento do fechamento do dia é executado
Então o relatório diário do Administrador não é gerado
  E a consulta da data pelo Administrador exibe mensagem informando ausência de indisponibilidades
```

---

#### Cenário 5.3: Administrador gera relatório parcial do dia atual

```gherkin
Dado que o Administrador está autenticado no Portal de Serviço Administrativo
  E E-TCE tem um período de indisponibilidade em andamento desde as 13h45
Quando o Administrador aciona o botão "Gerar Parcial"
Então o sistema gera um relatório com as indisponibilidades até o momento
  E o relatório exibe indicação de que é um relatório parcial em andamento
  E o período aberto de E-TCE aparece com horário de início mas sem horário de fim
```

---

#### Cenário 5.4: Falha na geração do relatório diário

```gherkin
Dado que um ou mais sistemas tiveram indisponibilidade no dia
Quando ocorre uma falha durante a geração do relatório diário do Administrador
Então uma exceção é gerada e enviada ao sistema de log do tribunal
  E o relatório não é disponibilizado para consulta
```

### Pontos em Aberto

> Nenhum ponto em aberto identificado para esta feature.

---

## Feature 6: Consulta de Relatórios do Usuário

### Narrativa

```
Feature: Consulta de Relatórios do Usuário
  In order to acessar de forma rápida e sempre disponível os relatórios que preciso para comprovar indisponibilidades
  As Usuário autenticado no Portal de Serviços
  I want consultar o relatório por limiar por data em uma tela dedicada, publicada de forma independente
```

### Regras de Negócio

- **RN-6.1** — A tela de consulta do Usuário é um projeto separado, publicado e implantado de forma independente das demais telas, para garantir o acesso mais direto possível e reduzir o risco de indisponibilidade.
- **RN-6.2** — A tela exibe apenas o relatório por limiar: os sistemas que atingiram o limiar de indisponibilidade no dia, sem informações hierárquicas.
- **RN-6.3** — Relatórios ficam disponíveis a partir do dia seguinte (d-1); qualquer data histórica pode ser consultada.
- **RN-6.4** — Quando nenhum sistema atingiu o limiar na data consultada, a tela exibe mensagem informando ausência de indisponibilidades.
- **RN-6.5** — Consulta de data futura ou do dia atual exibe mensagem informando que não há relatório disponível para a data selecionada.
- **RN-6.6** — Usuário não autenticado é redirecionado para o login do Portal de Serviços.
- **RN-6.7** — O botão "Baixar PDF" fica disponível no relatório d-1 concluído.

### Cenários

---

#### Cenário 6.1: Usuário consulta o relatório por limiar de uma data d-1

```gherkin
Dado que estou autenticado no Portal de Serviços
  E existem sistemas que atingiram o limiar na data consultada
Quando acesso a tela de consulta do Usuário e consulto uma data d-1
Então a tela exibe apenas os sistemas que atingiram o limiar, sem informações hierárquicas
```

---

#### Cenário 6.2: Consulta de data sem indisponibilidades

```gherkin
Dado que estou autenticado no Portal de Serviços
  E nenhum sistema atingiu o limiar na data consultada
Quando consulto o relatório de uma data específica
Então a tela exibe mensagem informando que não houve indisponibilidades naquele dia
```

---

#### Cenário 6.3: Tentativa de consulta de data futura ou do dia atual

```gherkin
Dado que estou autenticado como Usuário no Portal de Serviços
Quando consulto o relatório de uma data futura ou da data atual
Então a tela exibe mensagem informando que não há relatório disponível para a data selecionada
```

---

#### Cenário 6.4: Usuário não autenticado tenta acessar a tela

```gherkin
Dado que não estou autenticado no Portal de Serviços
Quando tento acessar a tela de consulta de relatórios do Usuário
Então sou redirecionado para a página de login do Portal de Serviços
```

---

#### Cenário 6.5: Download de PDF disponível para relatório d-1 concluído

```gherkin
Dado que estou autenticado e existe relatório concluído para a data consultada
Quando consulto o relatório de uma data d-1
Então o botão "Baixar PDF" está disponível na tela
```

### Pontos em Aberto

> Nenhum ponto em aberto identificado para esta feature.

---

## Feature 7: Consulta de Relatórios do Administrador

### Narrativa

```
Feature: Consulta de Relatórios do Administrador
  In order to acompanhar todas as indisponibilidades do dia com contexto hierárquico
  As Administrador de Sistemas autenticado no Portal de Serviço Administrativo
  I want consultar os relatórios de indisponibilidade por data em uma tela dedicada ao meu perfil
```

### Regras de Negócio

- **RN-7.1** — O acesso à tela do Administrador requer o perfil identificado via claim `listaGruposSistema` do token SSO, com valor `PRT_SRV_ADMINISTRADORES`.
- **RN-7.2** — A tela exibe todos os sistemas com indisponibilidade no dia, com a relação hierárquica indicada.
- **RN-7.3** — Relatórios ficam disponíveis a partir do dia seguinte (d-1); qualquer data histórica pode ser consultada.
- **RN-7.4** — Quando não há indisponibilidades na data consultada, a tela exibe mensagem informando ausência.
- **RN-7.5** — Usuário não autenticado é redirecionado para o login do Portal de Serviços.
- **RN-7.6** — O botão "Baixar PDF" fica disponível no relatório d-1 concluído; o botão "Baixar Parcial" fica disponível no relatório do dia atual.
- **RN-7.7** — O Administrador pode gerar o relatório parcial do dia atual, exibido com indicação de que está em andamento.

### Cenários

---

#### Cenário 7.1: Administrador consulta os relatórios de uma data d-1

```gherkin
Dado que estou autenticado como Administrador (claim PRT_SRV_ADMINISTRADORES)
  E existem sistemas com indisponibilidade na data consultada
Quando acesso a tela de consulta do Administrador e consulto uma data d-1
Então a tela exibe todos os sistemas com indisponibilidade, com relação hierárquica
```

---

#### Cenário 7.2: Consulta de data sem indisponibilidades

```gherkin
Dado que estou autenticado como Administrador
  E não há indisponibilidades registradas na data consultada
Quando consulto o relatório de uma data específica
Então a tela exibe mensagem informando que não houve indisponibilidades naquele dia
```

---

#### Cenário 7.3: Usuário não autenticado tenta acessar a tela

```gherkin
Dado que não estou autenticado no Portal de Serviços
Quando tento acessar a tela de consulta de relatórios do Administrador
Então sou redirecionado para a página de login do Portal de Serviços
```

---

#### Cenário 7.4: Download de PDF disponível para relatório d-1 concluído

```gherkin
Dado que estou autenticado como Administrador e existe relatório concluído para a data consultada
Quando consulto o relatório de uma data d-1
Então o botão "Baixar PDF" está disponível na tela
```

---

#### Cenário 7.5: Administrador baixa relatório parcial do dia atual

```gherkin
Dado que estou autenticado como Administrador
  E existem indisponibilidades registradas no dia atual
Quando aciono o botão "Gerar Parcial"
Então o relatório parcial é exibido com indicação de que está em andamento
  E o botão "Baixar Parcial" está disponível
```

### Pontos em Aberto

> Nenhum ponto em aberto identificado para esta feature.

---

## Próximos Passos Sugeridos

- **Modelagem de dados** — definir entidades, atributos e relacionamentos no Oracle 19c com base nas regras levantadas
- **spec-nonfunctional** — levantar requisitos de disponibilidade, performance e segurança
- **refinement-api** — detalhar contratos dos endpoints de healthcheck, inventário do Portal e SSO
- **dotnet-execution-plan** — dividir em entregas incrementais por camada (.NET + Angular)

---

## Histórico

| Data       | Versão | Alteração                                                        | Autor   |
|------------|--------|------------------------------------------------------------------|---------|
| 26/06/2026 | 1.0    | Versão inicial                                                   | —       |
| 13/07/2026 | 2.0    | Reescrita completa seguindo template BDD v1.1 — cenários limpos, Esquema do Cenário onde aplicável, narrativas Feature Injection revisadas | Claude  |
| 16/07/2026 | 2.1    | Remoção da Feature 7 (Autenticação de Relatório) e da assinatura digital dos relatórios; QR Code e códigos mantidos | Claude  |
| 16/07/2026 | 2.2    | Separação da Consulta de Relatórios em duas telas/features: Usuário (relatório por limiar, projeto publicado de forma independente) e Administrador (inalterada) | Claude  |
