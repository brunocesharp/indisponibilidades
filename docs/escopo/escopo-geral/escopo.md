# Escopo Geral — Monitoramento de Indisponibilidade

> Gerado em: 26/06/2026
> Versão: 1.0
> Situação: **Rascunho**
> Repositório: https://github.com/brunocesharp/indisponibilidades

---

## Declaração de Visão

> "Prover monitoramento automatizado e centralizado da saúde das aplicações, com relatórios de indisponibilidade precisos e livres de falsos positivos, garantindo conformidade com as exigências do Tribunal e transparência para administradores e usuários."

---

## Problema

A organização não possui nenhuma forma de contabilizar ou comprovar que um sistema esteve indisponível. Indisponibilidades ocorrem sem registro, sem notificação estruturada e sem rastreabilidade. Isso impede que cidadãos comprovem indisponibilidade para petições processuais e que administradores acompanhem a saúde das aplicações — e coloca o tribunal em desconformidade com a minuta regulatória que exige essa informação disponível aos usuários.

---

## Público-Alvo

| Perfil | Descrição | Acesso |
|--------|-----------|--------|
| **Administrador de Sistemas** | Opera o sistema, gerencia hierarquias e recebe relatório diário | Portal de Serviço Administrativo — login via AD |
| **Usuário (cidadão)** | Consulta relatórios de indisponibilidade por data para uso em petições | Portal de Serviços — login via gov.br |

---

## Motivação e Prazo

- **Regulatória:** minuta do Tribunal exige disponibilização de informações de indisponibilidade aos usuários
- **Prazo:** alinhado ao lançamento do Portal de Serviços *(prazos confirmados com o time do Portal)*

---

## Funcionalidades do Escopo

### 1. Monitoramento de Healthcheck

| Aspecto | Detalhe |
|---------|---------|
| **O que faz** | Verifica periodicamente os endpoints de healthcheck dos sistemas cadastrados e acumula o tempo de indisponibilidade ao longo do dia |
| **Frequência padrão** | 1 minuto (configurável via arquivo de configuração) |
| **Padrões suportados** | `Microsoft.Extensions.Diagnostics.HealthChecks` (ASP.NET Core) e `Spring Boot Actuator` `/actuator/health` (Java) |
| **Inventário de sistemas** | Obtido via endpoint externo do Portal de Serviços — este sistema não gerencia cadastro de aplicações |
| **Detecção** | Indisponibilidade > 1 minuto já começa a ser contabilizada |

---

### 2. Hierarquia de Serviços

| Aspecto | Detalhe |
|---------|---------|
| **O que faz** | Permite cadastrar relações hierárquicas entre serviços |
| **Comportamento** | Quando um serviço pai está indisponível, todos os filhos na hierarquia **também** são contabilizados como indisponíveis — o serviço mais alto da cadeia é o início da falha |
| **Profundidade** | Sem limite de níveis |
| **Cadastro** | Administrador cadastra sigla, nome, endpoint de healthcheck e vínculo hierárquico (opcional) |

---

### 3. Relatório por Limiar (Usuário)

| Aspecto | Detalhe |
|---------|---------|
| **O que faz** | Gera relatório quando um sistema acumula mais de **2 horas** de indisponibilidade no dia |
| **Destinatário** | Usuários que acessam o Portal de Serviços |
| **Canal** | Página de relatórios dentro do Portal de Serviços |
| **Autenticidade** | Relatório assinado digitalmente com QR Code para validação de autenticidade |

---

### 4. Relatório Diário do Administrador

| Aspecto | Detalhe |
|---------|---------|
| **O que faz** | Gera relatório completo de todas as indisponibilidades do dia |
| **Horário padrão** | Meia-noite (configurável via arquivo de configuração) |
| **Destinatário** | Administradores de Sistemas |
| **Canal** | E-mail (conta AD) + página de relatórios no Portal de Serviço Administrativo |
| **Autenticidade** | Relatório assinado digitalmente com QR Code para validação de autenticidade |

---

### 5. Consulta de Relatórios

| Aspecto | Detalhe |
|---------|---------|
| **O que faz** | Permite buscar relatórios de indisponibilidade por data |
| **Acesso** | Requer autenticação; tipo de relatório exibido determinado pelo perfil do usuário via claim `listaGruposSistema` do token SSO |
| **Administrador** | Acessa todos os relatórios (`listaGruposSistema = PRT_SRV_ADMINISTRADORES`) |
| **Usuário** | Acessa relatórios por limiar (sistemas com > 2h de indisponibilidade) |

---

### 6. Gerenciamento de Serviços (Administrador)

| Aspecto | Detalhe |
|---------|---------|
| **O que faz** | Interface para o Administrador cadastrar e gerenciar serviços monitorados |
| **Dados cadastrais** | Sigla, nome do sistema, endpoint de healthcheck |
| **Hierarquia** | Vínculo opcional a um serviço pai existente |
| **Fonte de sistemas** | Lista base obtida via endpoint do Portal de Serviços |

---

## Fora do Escopo

| Item | Justificativa |
|------|---------------|
| Cadastro e gerenciamento de usuários | Responsabilidade do SSO (SIGESP para internos, Portal de Serviços para externos) |
| Cadastro de sistemas no inventário geral | Responsabilidade do Portal de Serviços — este sistema consome o endpoint |
| Autenticação e controle de acesso | Responsabilidade do SSO — este sistema consome o token |
| Dashboard em tempo real estilo Grafana | Fora do escopo; compatibilidade com Prometheus mantida via desacoplamento da camada de observabilidade |

---

## Restrições Técnicas

| Tipo | Restrição |
|------|-----------|
| **Healthcheck .NET** | `Microsoft.Extensions.Diagnostics.HealthChecks` (ASP.NET Core) |
| **Healthcheck Java** | `Spring Boot Actuator` — endpoint `/actuator/health` |
| **Autenticação** | Token SSO — claim `listaGruposSistema = PRT_SRV_ADMINISTRADORES` identifica Administrador |
| **Observabilidade** | Camada desacoplada via adapter — sem acoplamento a Prometheus ou outra ferramenta específica |
| **Configuração** | Frequência de verificação e horário do relatório diário configuráveis via arquivo de configuração, sem necessidade de redeploy |

---

## Integrações Necessárias

| Sistema | Tipo | O que fornece |
|---------|------|---------------|
| Portal de Serviços | Consumo de API (GET) | Lista de sistemas cadastrados para monitoramento |
| SSO | Consumo de token JWT | Autenticação e identificação do perfil do usuário |
| SIGESP | Indireto (via SSO) | Dados de usuários internos (Administradores via AD) |
| Servidores de e-mail do tribunal | SMTP/relay interno | Envio de alertas e relatórios diários para Administradores |

---

## Hipóteses Críticas Pendentes

> ⚠️ As hipóteses abaixo ainda não foram validadas e podem impactar o escopo.

| # | Hipótese | Ação necessária |
|---|----------|-----------------|
| U4 | Formato do relatório (assinatura + QR Code) é aceito pelo Tribunal | Validar com representante do Tribunal antes do desenvolvimento |
| N1 | O sistema estará em conformidade com a minuta do Tribunal ao entrar no ar | Revisão formal da minuta com jurídico ou Tribunal |
| T4 | Formatos de resposta de ASP.NET HealthChecks e Spring Boot Actuator são compatíveis | Spike técnico antes do início do desenvolvimento |

---

## Stakeholders Principais

| Stakeholder | Papel | Engajamento |
|-------------|-------|-------------|
| Diretor da DTI | Patrocinador interno | Reportes quinzenais |
| Tribunal | Regulador — define conformidade | Validação formal do formato de relatório |
| Time do Portal de Serviços | Fornece inventário e canal de relatórios | Semanal — dependência crítica de prazo |
| Time de Segurança e Infra | Libera acesso aos endpoints internos | Envolver cedo |
| Equipe de Arquitetura | Guardiã dos padrões técnicos | Sob demanda |
| Times Dev (.NET e Java) | Implementam os endpoints de healthcheck | Guia técnico + prazo definido |

---

## Métricas de Sucesso

| Métrica | Meta |
|---------|------|
| ⭐ **North Star:** % de indisponibilidades que geraram relatório correto e no prazo | 100% |
| Cobertura de sistemas monitorados | 100% dos sistemas cadastrados |
| Tempo de detecção de indisponibilidade | ≤ 1 minuto |
| Relatório diário sem falha | 100% dos dias |
| Taxa de falha na geração de relatórios | 0% |

---

## Critérios de Aceitação para Go-live

- [ ] 100% dos sistemas cadastrados no Portal sendo monitorados
- [ ] Relatório diário do Administrador gerado corretamente por 5 dias consecutivos em homologação
- [ ] Relatório por limiar (2h) gerado corretamente ao simular indisponibilidade em homologação
- [ ] QR Code de validação funcionando em 100% dos relatórios gerados
- [ ] Assinatura digital nos relatórios validada
- [ ] Tempo de detecção ≤ 1 minuto confirmado em testes
- [ ] Hierarquia de serviços propagando indisponibilidade corretamente nos testes
- [ ] Conformidade formal com a minuta do Tribunal confirmada

---

## Documentos de Discovery

| Documento | Localização |
|-----------|-------------|
| Visão do projeto | `discovery/vision.md` |
| Hipóteses e premissas | `discovery/assumptions.md` |
| Stakeholders | `discovery/stakeholders.md` |
| Métricas de sucesso | `discovery/success-metrics.md` |

---

## Próximos Passos

1. **Validar hipóteses pendentes** (U4, N1) com o Tribunal antes de iniciar o desenvolvimento
2. **Spike técnico** (T4) — comparar formatos ASP.NET HealthChecks e Spring Boot Actuator
3. **Envolver Time de Segurança e Infra** para mapear liberações de endpoints
4. **Especificação funcional** — detalhar regras de negócio em BDD (Given/When/Then)
5. **Plano de execução** — dividir em entregas incrementais por camada
