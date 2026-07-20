# Dicionário de Dados — Monitoramento de Indisponibilidade

> Gerado em: 20/07/2026 | Versão: 1.1 | Schema: USU_INDISPONIBILIDADE

## Bloco de Auditoria (padrão em todas as tabelas de negócio)

As colunas abaixo repetem-se em SERVICO_MONITORADO, HIERARQUIA_SERVICO, INDISPONIBILIDADE, RELATORIO e RELATORIO_SERVICO. Não são repetidas nas seções seguintes para reduzir ruído. `LOG_SERVICO_MONITORADO` é exceção (append-only).

| Coluna | Tipo Oracle | Nulo | Descrição | Regra |
|--------|-------------|------|-----------|-------|
| `NUM_CPF_USUARIO_CRIACAO` | NUMBER(11) | NÃO | CPF de quem criou | — |
| `NUM_CPF_USUARIO_ATUALIZACAO` | NUMBER(11) | SIM | CPF de quem atualizou | — |
| `NUM_CPF_USUARIO_REMOCAO` | NUMBER(11) | SIM | CPF de quem removeu | Preenchido na remoção lógica |
| `DAT_CRIACAO` | DATE | NÃO | Data de criação | DEFAULT SYSDATE |
| `DAT_ATUALIZACAO` | DATE | SIM | Data da última atualização | — |
| `DAT_REMOCAO` | DATE | SIM | Data de remoção lógica | Soft delete |

---

## SERVICO_MONITORADO

| Campo | Valor |
|-------|-------|
| **Nome do Objeto** | `SERVICO_MONITORADO` |
| **Tipo** | Tabela |
| **Descrição** | Serviço/sistema incluído no monitoramento de healthcheck, com ciclo de vida Ativo/Inativo/Removido |
| **Regras de Negócio** | `COD_SISTEMA` único (UK); `SGL_STATUS` apenas A/I/R (RN-1.5); histórico preservado em inativação/remoção (RN-1.6, RN-1.8) |
| **Relações** | Referenciada por HIERARQUIA_SERVICO (2×), INDISPONIBILIDADE, RELATORIO_SERVICO, LOG_SERVICO_MONITORADO |
| **Responsáveis** | Equipe de AD / Analista responsável |
| **Data de Criação** | 20/07/2026 |
| **Última Alteração** | 20/07/2026 |

### Colunas de SERVICO_MONITORADO

| Coluna | Tipo Oracle | Nulo | Descrição | Regra |
|--------|-------------|------|-----------|-------|
| `ID_SERVICO` | NUMBER(10) | NÃO | Identificador único | Gerado por SQ_SERVICO_MONITORADO |
| `COD_SISTEMA` | VARCHAR2(50) | NÃO | Código do sistema no inventário do Portal | UK — único |
| `SGL_SERVICO` | VARCHAR2(20) | NÃO | Sigla do serviço | — |
| `NOM_SERVICO` | VARCHAR2(150) | NÃO | Nome por extenso | — |
| `DSC_URL_HEALTHCHECK` | VARCHAR2(500) | NÃO | URL do endpoint de healthcheck | Obrigatória e válida (RN-1.2, RN-1.3) |
| `SGL_STATUS` | CHAR(1) | NÃO | Status do serviço | A/I/R — DEFAULT 'A' |
| `DAT_INCLUSAO` | DATE | NÃO | Data de inclusão no monitoramento | DEFAULT SYSDATE |
| *(+ bloco de auditoria)* | — | — | 6 colunas de auditoria (ver topo) | — |

---

## HIERARQUIA_SERVICO

| Campo | Valor |
|-------|-------|
| **Nome do Objeto** | `HIERARQUIA_SERVICO` |
| **Tipo** | Tabela associativa (autorrelacionada) |
| **Descrição** | Vínculo hierárquico pai↔filho entre serviços; resolve o N:M autorrelacionado |
| **Regras de Negócio** | Múltiplos pais/filhos (RN-1.4, RN-3.2); par filho+pai único (UK); filho ≠ pai (CK); `IND_ATIVO='N'` preserva hierarquia de serviço inativado para restauração (RN-1.6, RN-1.7) |
| **Relações** | FK→SERVICO_MONITORADO (filho e pai) |
| **Responsáveis** | Equipe de AD / Analista responsável |
| **Data de Criação** | 20/07/2026 |
| **Última Alteração** | 20/07/2026 |

### Colunas de HIERARQUIA_SERVICO

| Coluna | Tipo Oracle | Nulo | Descrição | Regra |
|--------|-------------|------|-----------|-------|
| `ID_HIERARQUIA` | NUMBER(10) | NÃO | Identificador único | Gerado por SQ_HIERARQUIA_SERVICO |
| `ID_SERVICO_FILHO` | NUMBER(10) | NÃO | Serviço filho | FK→SERVICO_MONITORADO |
| `ID_SERVICO_PAI` | NUMBER(10) | NÃO | Serviço pai | FK→SERVICO_MONITORADO |
| `IND_ATIVO` | CHAR(1) | NÃO | Vínculo vigente/suspenso | S/N — DEFAULT 'S' |
| *(+ bloco de auditoria)* | — | — | 6 colunas de auditoria (ver topo) | — |

---

## INDISPONIBILIDADE

| Campo | Valor |
|-------|-------|
| **Nome do Objeto** | `INDISPONIBILIDADE` |
| **Tipo** | Tabela dependente |
| **Descrição** | Período confirmado de indisponibilidade de um serviço |
| **Regras de Negócio** | Persistido só após 2ª falha consecutiva (RN-2.5); apenas indisponibilidades são gravadas (RN-2.8); `DAT_FIM` nulo = aberto (RN-2.3); fechamento independente por serviço (RN-3.5); `DAT_FIM >= DAT_INICIO` (CK) |
| **Relações** | FK→SERVICO_MONITORADO |
| **Responsáveis** | Equipe de AD / Analista responsável |
| **Data de Criação** | 20/07/2026 |
| **Última Alteração** | 20/07/2026 |

### Colunas de INDISPONIBILIDADE

| Coluna | Tipo Oracle | Nulo | Descrição | Regra |
|--------|-------------|------|-----------|-------|
| `ID_INDISPONIBILIDADE` | NUMBER(12) | NÃO | Identificador único | Gerado por SQ_INDISPONIBILIDADE |
| `ID_SERVICO` | NUMBER(10) | NÃO | Serviço indisponível | FK→SERVICO_MONITORADO |
| `DAT_INICIO` | DATE | NÃO | Início (1ª falha) | — |
| `DAT_FIM` | DATE | SIM | Fim; nulo se em andamento | ≥ DAT_INICIO |
| `NUM_DURACAO_MIN` | NUMBER(10) | SIM | Duração em minutos | Calculada no fechamento |
| *(+ bloco de auditoria)* | — | — | 6 colunas de auditoria (ver topo) | — |

---

## RELATORIO

| Campo | Valor |
|-------|-------|
| **Nome do Objeto** | `RELATORIO` |
| **Tipo** | Tabela |
| **Descrição** | Relatório diário gerado — por limiar (usuário) ou diário do administrador |
| **Regras de Negócio** | Gerado à meia-noite (RN-4.1, RN-5.1); tipo L com código verificador único (RN-4.7); tipo A sem código (RN-5.4); parcial do dia atual (RN-5.6, RN-7.7); `SGL_TIPO` L/A, `SGL_STATUS` C/P/E |
| **Relações** | Referenciada por RELATORIO_SERVICO |
| **Responsáveis** | Equipe de AD / Analista responsável |
| **Data de Criação** | 20/07/2026 |
| **Última Alteração** | 20/07/2026 |

### Colunas de RELATORIO

| Coluna | Tipo Oracle | Nulo | Descrição | Regra |
|--------|-------------|------|-----------|-------|
| `ID_RELATORIO` | NUMBER(10) | NÃO | Identificador único | Gerado por SQ_RELATORIO |
| `DAT_REFERENCIA` | DATE | NÃO | Dia de referência | — |
| `SGL_TIPO` | CHAR(1) | NÃO | Tipo do relatório | L/A |
| `COD_VERIFICADOR` | VARCHAR2(50) | SIM | Código verificador | UK; apenas tipo L (RN-4.7) |
| `NUM_LIMIAR_MIN` | NUMBER(5) | SIM | Limiar aplicado (min) | Snapshot; apenas tipo L (RN-4.2) |
| `IND_PARCIAL` | CHAR(1) | NÃO | Parcial/fechado | S/N — DEFAULT 'N' |
| `SGL_STATUS` | CHAR(1) | NÃO | Situação | C/P/E — DEFAULT 'C' |
| `DAT_GERACAO` | DATE | NÃO | Data/hora da geração | DEFAULT SYSDATE |
| *(+ bloco de auditoria)* | — | — | 6 colunas de auditoria (ver topo) | — |

---

## RELATORIO_SERVICO

| Campo | Valor |
|-------|-------|
| **Nome do Objeto** | `RELATORIO_SERVICO` |
| **Tipo** | Tabela associativa |
| **Descrição** | Sistemas incluídos em um relatório com o total acumulado do dia (snapshot) |
| **Regras de Negócio** | Um serviço por relatório (UK); tipo L inclui só quem atingiu o limiar (RN-4.3); tipo A inclui todos com indisponibilidade (RN-5.2) |
| **Relações** | FK→RELATORIO, FK→SERVICO_MONITORADO |
| **Responsáveis** | Equipe de AD / Analista responsável |
| **Data de Criação** | 20/07/2026 |
| **Última Alteração** | 20/07/2026 |

### Colunas de RELATORIO_SERVICO

| Coluna | Tipo Oracle | Nulo | Descrição | Regra |
|--------|-------------|------|-----------|-------|
| `ID_RELATORIO_SERVICO` | NUMBER(12) | NÃO | Identificador único | Gerado por SQ_RELATORIO_SERVICO |
| `ID_RELATORIO` | NUMBER(10) | NÃO | Relatório de origem | FK→RELATORIO |
| `ID_SERVICO` | NUMBER(10) | NÃO | Serviço incluído | FK→SERVICO_MONITORADO |
| `NUM_TOTAL_MIN` | NUMBER(10) | NÃO | Total acumulado do dia (min) | — |
| *(+ bloco de auditoria)* | — | — | 6 colunas de auditoria (ver topo) | — |

---

## LOG_SERVICO_MONITORADO

| Campo | Valor |
|-------|-------|
| **Nome do Objeto** | `LOG_SERVICO_MONITORADO` |
| **Tipo** | Tabela de log |
| **Descrição** | Auditoria de inclusões, alterações e remoções de serviços |
| **Regras de Negócio** | Alimentada pela trigger `TG_A_IUD_SERVICO_MONITORADO`; `SGL_OPERACAO` I/U/D |
| **Relações** | Referência lógica a SERVICO_MONITORADO (sem FK — preserva histórico após remoção) |
| **Responsáveis** | Equipe de AD / Analista responsável |
| **Data de Criação** | 20/07/2026 |
| **Última Alteração** | 20/07/2026 |

### Colunas de LOG_SERVICO_MONITORADO

| Coluna | Tipo Oracle | Nulo | Descrição | Regra |
|--------|-------------|------|-----------|-------|
| `ID_LOG` | NUMBER(12) | NÃO | Identificador único | Gerado por SQ_LOG_SERVICO_MONITORADO |
| `ID_SERVICO` | NUMBER(10) | NÃO | Serviço afetado | — |
| `SGL_OPERACAO` | CHAR(1) | NÃO | Operação | I/U/D |
| `DAT_OPERACAO` | DATE | NÃO | Data/hora da operação | DEFAULT SYSDATE |

---

## Objetos de Apoio

| Objeto | Tipo | Descrição |
|--------|------|-----------|
| `SQ_SERVICO_MONITORADO` | Sequence | Gera `ID_SERVICO` |
| `SQ_HIERARQUIA_SERVICO` | Sequence | Gera `ID_HIERARQUIA` |
| `SQ_INDISPONIBILIDADE` | Sequence | Gera `ID_INDISPONIBILIDADE` |
| `SQ_RELATORIO` | Sequence | Gera `ID_RELATORIO` |
| `SQ_RELATORIO_SERVICO` | Sequence | Gera `ID_RELATORIO_SERVICO` |
| `SQ_LOG_SERVICO_MONITORADO` | Sequence | Gera `ID_LOG` |
| `TG_A_IUD_SERVICO_MONITORADO` | Trigger | Auditoria de SERVICO_MONITORADO |
