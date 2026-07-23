# Escopo Geral — Monitoramento de Indisponibilidade

> Gerado em: 26/06/2026
> Atualizado em: 23/07/2026
> Versão: 1.2
> Situação: **Rascunho**
> Repositório: https://github.com/brunocesharp/indisponibilidades
>
> **Alterações v1.2:** definição da arquitetura de implantação em duas aplicações independentes — Aplicação Pública (tempo real + relatório do usuário) com deploy próprio em rede isolada (DMZ) para exposição a usuários externos ao tribunal, e Aplicação Administrativa na rede interna.
> **Alterações v1.1:** revisão do Monitoramento de Indisponibilidade — página de acompanhamento em tempo real (dados do banco, atualização automática a cada minuto, refresh manual, sistema único com publicação separada, botão de acesso à tela de relatório do usuário), tela de relatório do usuário sem autenticação e relatório por limiar de 2h gerado na madrugada do dia posterior. Entrega do relatório por limiar mantida como página pública sem autenticação (sem envio ativo).

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
| **Horário de geração** | Relatório gerado na madrugada do dia posterior ao evento |
| **Destinatário** | Usuários finais |
| **Canal** | Página de relatórios no sistema de monitoramento de indisponibilidade, acessível sem autenticação |
| **Autenticidade** | Relatório com QR Code para validação de autenticidade |

---

### 4. Relatório Diário do Administrador

| Aspecto | Detalhe |
|---------|---------|
| **O que faz** | Gera relatório completo de todas as indisponibilidades do dia |
| **Horário padrão** | Meia-noite (configurável via arquivo de configuração) |
| **Destinatário** | Administradores de Sistemas |
| **Canal** | E-mail (conta AD) + página de relatórios no Portal de Serviço Administrativo |
| **Autenticidade** | Relatório com QR Code para validação de autenticidade |

---

### 5. Página de Acompanhamento em Tempo Real

| Aspecto | Detalhe |
|---------|---------|
| **O que faz** | Exibe o estado atual das aplicações cadastradas no monitoramento de indisponibilidade, com dados extraídos do banco de dados do sistema |
| **Atualização automática** | Atualiza automaticamente a cada minuto |
| **Refresh manual** | Possui botão de atualizar acionado manualmente pelo usuário |
| **Navegação** | Inclui botão de acesso à tela de relatório do usuário |
| **Publicação** | Faz parte da **Aplicação Pública** — aplicação separada, com deploy próprio, publicada em rede isolada (DMZ) para permitir exposição a usuários externos ao tribunal, sem acesso à rede interna. Independente da aplicação administrativa |
| **Acesso** | Não requer autenticação |

---

### 6. Consulta de Relatórios do Usuário

| Aspecto | Detalhe |
|---------|---------|
| **O que faz** | Permite ao Usuário buscar o relatório por limiar por data |
| **Tela** | Parte da **Aplicação Pública**, junto ao monitoramento em tempo real — aplicação separada, com deploy próprio, publicada em rede isolada (DMZ) para exposição a usuários externos ao tribunal, sem acesso à rede interna. Independente da aplicação administrativa |
| **Acesso** | Não requer autenticação |
| **Conteúdo** | Sistemas que atingiram o limiar no dia (sem hierarquia) |

---

### 7. Consulta de Relatórios do Administrador

| Aspecto | Detalhe |
|---------|---------|
| **O que faz** | Permite ao Administrador buscar relatórios de indisponibilidade por data |
| **Tela** | Página de relatórios no Portal de Serviço Administrativo |
| **Acesso** | Requer perfil de Administrador via claim `listaGruposSistema = PRT_SRV_ADMINISTRADORES` do token SSO |
| **Conteúdo** | Todos os sistemas com indisponibilidade no dia, com relação hierárquica; permite relatório parcial do dia atual |

---

### 8. Gerenciamento de Serviços (Administrador)

| Aspecto | Detalhe |
|---------|---------|
| **O que faz** | Interface para o Administrador cadastrar e gerenciar serviços monitorados |
| **Dados cadastrais** | Sigla, nome do sistema, endpoint de healthcheck |
| **Hierarquia** | Vínculo opcional a um serviço pai existente |
| **Fonte de sistemas** | Lista base obtida via endpoint do Portal de Serviços |

---

## Arquitetura de Implantação

O sistema é dividido em **duas aplicações independentes**, com deploys próprios, para atender à segregação de rede:

| Aplicação | Conteúdo | Rede / Publicação | Acesso |
|-----------|----------|-------------------|--------|
| **Aplicação Pública** | Página de acompanhamento em tempo real (Seção 5) e consulta de relatórios do usuário (Seção 6) | Rede isolada (DMZ), com deploy próprio, exposta a usuários externos ao tribunal sem acesso à rede interna | Sem autenticação |
| **Aplicação Administrativa** | Gerenciamento de serviços, relatório diário e consulta de relatórios do Administrador (Seções 7 e 8) | Rede interna do tribunal | Requer perfil de Administrador via token SSO |

O serviço de monitoramento (healthcheck) e o banco de dados são compartilhados; a Aplicação Pública consome apenas os dados necessários para exibição, sem acesso às funções administrativas.

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
| **Segregação de rede** | Aplicação Pública (tempo real + relatório do usuário) empacotada e publicada de forma independente, com deploy próprio, para implantação em rede isolada (DMZ) acessível a usuários externos ao tribunal. Aplicação Administrativa permanece na rede interna |

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
| U4 | Formato do relatório (QR Code) é aceito pelo Tribunal | Validar com representante do Tribunal antes do desenvolvimento |
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
