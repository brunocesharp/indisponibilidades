# Hipóteses e Premissas — Monitoramento de Indisponibilidade

> Gerado em: 26/06/2026
> Versão: 1.0

---

## Conceito

Toda decisão de produto carrega suposições embutidas. O objetivo deste documento é tornar essas suposições explícitas para validá-las antes de construir a coisa errada.

Classificação por dois eixos:
- **Impacto se errada**: o quanto o projeto é afetado caso a hipótese seja falsa
- **Certeza atual**: o quanto temos evidência de que ela é verdadeira

| Quadrante | Ação |
|-----------|------|
| Alto impacto + Baixa certeza | ⚠️ **VALIDAR PRIMEIRO** |
| Alto impacto + Alta certeza | ✅ Confirmar e seguir |
| Baixo impacto + Baixa certeza | 👀 Monitorar |
| Baixo impacto + Alta certeza | ✔️ Ignorar |

---

## Hipóteses sobre Usuários

| # | Hipótese | Impacto se errada | Certeza atual | Prioridade | Como validar |
|---|----------|-------------------|---------------|------------|--------------|
| U1 | Todos os usuários têm acesso ao Portal de Serviços | Alto — o canal de entrega dos relatórios depende do Portal | ✅ **Validada** | ✅ VALIDADA | **Cidadãos:** qualquer pessoa com conta gov.br. **Administradores:** acesso via Portal de Serviço Administrativo com login pelo AD (Active Directory) do tribunal |
| U2 | Os Administradores aceitarão receber notificações por e-mail quando ocorrer indisponibilidade | Médio — se não aceitarem, o canal de alerta perde efetividade | ✅ **Validada** | ✅ VALIDADA | Todos os Administradores possuem conta AD da rede interna do tribunal e estão habilitados a receber e-mails dos sistemas do tribunal |
| U3 | Os Usuários vão consultar os relatórios proativamente por data, sem necessidade de notificação ativa | Médio — se precisarem de notificação, o modelo atual é insuficiente | Média — inferido da descrição do sistema | 👀 Monitorar | Observar uso após lançamento |
| U4 | Os relatórios com assinatura digital e QR Code de validação são suficientes para atender a exigência do Tribunal | Alto — se o Tribunal exigir outro formato, os relatórios precisarão ser reformulados | Baixa — não confirmado formalmente com o Tribunal | ⚠️ VALIDAR PRIMEIRO | Validar o formato do relatório com o Tribunal antes do desenvolvimento |

---

## Hipóteses sobre o Negócio

| # | Hipótese | Impacto se errada | Certeza atual | Prioridade | Como validar |
|---|----------|-------------------|---------------|------------|--------------|
| N1 | O sistema estará em conformidade com a minuta do Tribunal assim que entrar no ar | Alto — se não estiver em conformidade, o projeto não cumpre seu objetivo principal | Média — a minuta foi lida, mas conformidade formal não foi confirmada | ⚠️ VALIDAR PRIMEIRO | Revisão formal da minuta com jurídico ou representante do Tribunal |
| N2 | O prazo de entrega está alinhado com o lançamento do Portal de Serviços | Alto — um atraso no Portal impacta diretamente o prazo deste sistema | ✅ **Validada** | ✅ VALIDADA | Prazos já alinhados com o time do Portal de Serviços |
| N3 | Os e-mails de alerta enviados aos Administradores são suficientes como canal de comunicação de indisponibilidade | Médio — pode ser necessário um canal adicional (ex: SMS, push) | Baixa — não validado com os Administradores | 👀 Monitorar | Validar com os Administradores após lançamento |

---

## Hipóteses Técnicas

| # | Hipótese | Impacto se errada | Certeza atual | Prioridade | Como validar |
|---|----------|-------------------|---------------|------------|--------------|
| T1 | Os times responsáveis pelas aplicações .NET irão implementar o padrão `Microsoft.Extensions.Diagnostics.HealthChecks` nos seus sistemas | Alto — sem o endpoint padronizado, o monitoramento não funciona | ✅ **Validada** | ✅ VALIDADA | Aprovado pela equipe de arquitetura do tribunal |
| T2 | Os times responsáveis pelas aplicações Java irão implementar o **Spring Boot Actuator** (`/actuator/health`) nos seus sistemas | Alto — sem o endpoint, aplicações Java não são monitoradas | ✅ **Validada** | ✅ VALIDADA | Aprovado pela equipe de arquitetura do tribunal |
| T3 | O endpoint externo que fornece a lista de sistemas estará disponível e com contrato de API definido antes do início do desenvolvimento | Alto — sem esse contrato, não é possível construir a integração de inventário | ✅ **Validada** | ✅ VALIDADA | Endpoint já existe dentro do Portal de Serviços e está documentado |
| T4 | O formato de resposta do Spring Boot Actuator (`/actuator/health`) é compatível com o que o sistema espera dos endpoints de healthcheck | Alto — se os formatos forem incompatíveis, será necessário um adaptador | Média — ambos seguem padrões abertos, mas podem ter diferenças | ⚠️ VALIDAR PRIMEIRO | Fazer spike técnico comparando os formatos de resposta de ambas as bibliotecas |
| T5 | A camada de integração com ferramentas de observabilidade (ex: Prometheus) pode ser desacoplada do core do sistema, permitindo trocar a tecnologia sem impacto | Alto — se houver acoplamento forte, qualquer troca de ferramenta exige refatoração ampla | Média — depende das decisões arquiteturais do time | ✅ Confirmar e seguir | Definir a arquitetura com interface/adapter para a camada de métricas no início do projeto |
| T6 | O token de autenticação do Portal de Serviços carrega as informações de tipo de usuário necessárias (Administrador ou Usuário) de forma legível pelo sistema | Alto — se o token não carregar essa informação, não é possível diferenciar o tipo de relatório | ✅ **Validada** | ✅ VALIDADA | A claim `listaGruposSistema` com valor `PRT_SRV_ADMINISTRADORES` identifica o Administrador de Sistemas |

---

## Resumo de Prioridades

### ⚠️ Validar Primeiro (Alto impacto + Baixa/Média certeza)

| # | Hipótese | Responsável sugerido |
|---|----------|----------------------|
| U4 | Formato do relatório (assinatura + QR Code) aceito pelo Tribunal | Jurídico / Representante do Tribunal |
| N1 | Conformidade com a minuta do Tribunal | Jurídico / Representante do Tribunal |
| T4 | Compatibilidade entre formatos ASP.NET HealthChecks e Spring Boot Actuator | Spike técnico |

### ✅ Validadas

| # | Hipótese | Evidência |
|---|----------|-----------|
| U1 | Acesso ao Portal de Serviços | Cidadãos via gov.br; Administradores via AD no Portal Administrativo |
| U2 | Administradores habilitados para e-mail | Todos possuem conta AD e estão habilitados nos sistemas do tribunal |
| N2 | Prazo alinhado com o Portal de Serviços | Confirmado com o time do Portal |
| T1 | Adoção do padrão .NET HealthChecks | Aprovado pela equipe de arquitetura |
| T2 | Adoção do Spring Boot Actuator (Java) | Aprovado pela equipe de arquitetura |
| T3 | Endpoint externo de inventário disponível | Endpoint existente no Portal de Serviços |
| T5 | Desacoplamento da camada de observabilidade via adapter | Decisão arquitetural a confirmar no início |
| T6 | Claim `listaGruposSistema = PRT_SRV_ADMINISTRADORES` identifica Administrador | Confirmado pelo time do Portal |

### 👀 Monitorar

| # | Hipótese |
|---|----------|
| U3 | Consulta proativa de relatórios pelos Usuários |
| N3 | E-mail como canal suficiente para os Administradores |

---

## Próximos Passos Sugeridos

- **Stakeholders** — identificar os times e pessoas que podem validar as hipóteses críticas (Portal de Serviços, times .NET e Java, representante do Tribunal)
- **Métricas** — definir indicadores de conformidade com o Tribunal
- **Spike técnico** — comparar formatos de resposta de `Microsoft.Extensions.Diagnostics.HealthChecks` e `Spring Boot Actuator` (hipótese T4)
