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
| U1 | Todos os usuários (Administrador e Usuário) já têm acesso ao Portal de Serviços | Alto — o canal de entrega dos relatórios depende do Portal | Média — Portal ainda não foi lançado | ⚠️ VALIDAR PRIMEIRO | Confirmar com o time do Portal quem terá acesso no lançamento |
| U2 | Os Administradores cadastrados aceitarão receber notificações por e-mail quando ocorrer indisponibilidade | Médio — se não aceitarem, o canal de alerta perde efetividade | Baixa — não foi confirmado com os administradores | ⚠️ VALIDAR PRIMEIRO | Entrevistar os Administradores potenciais |
| U3 | Os Usuários vão consultar os relatórios proativamente por data, sem necessidade de notificação ativa | Médio — se precisarem de notificação, o modelo atual é insuficiente | Média — inferido da descrição do sistema | 👀 Monitorar | Observar uso após lançamento |
| U4 | Os relatórios com assinatura digital e QR Code de validação são suficientes para atender a exigência do Tribunal | Alto — se o Tribunal exigir outro formato, os relatórios precisarão ser reformulados | Baixa — não confirmado formalmente com o Tribunal | ⚠️ VALIDAR PRIMEIRO | Validar o formato do relatório com o Tribunal antes do desenvolvimento |

---

## Hipóteses sobre o Negócio

| # | Hipótese | Impacto se errada | Certeza atual | Prioridade | Como validar |
|---|----------|-------------------|---------------|------------|--------------|
| N1 | O sistema estará em conformidade com a minuta do Tribunal assim que entrar no ar | Alto — se não estiver em conformidade, o projeto não cumpre seu objetivo principal | Média — a minuta foi lida, mas conformidade formal não foi confirmada | ⚠️ VALIDAR PRIMEIRO | Revisão formal da minuta com jurídico ou representante do Tribunal |
| N2 | O prazo de entrega está alinhado com o lançamento do Portal de Serviços | Alto — um atraso no Portal impacta diretamente o prazo deste sistema | Baixa — depende de outro time | ⚠️ VALIDAR PRIMEIRO | Confirmar cronograma com o time do Portal de Serviços |
| N3 | Os e-mails de alerta enviados aos Administradores são suficientes como canal de comunicação de indisponibilidade | Médio — pode ser necessário um canal adicional (ex: SMS, push) | Baixa — não validado com os Administradores | 👀 Monitorar | Validar com os Administradores após lançamento |

---

## Hipóteses Técnicas

| # | Hipótese | Impacto se errada | Certeza atual | Prioridade | Como validar |
|---|----------|-------------------|---------------|------------|--------------|
| T1 | Os times responsáveis pelas aplicações .NET irão implementar o padrão `Microsoft.Extensions.Diagnostics.HealthChecks` nos seus sistemas | Alto — sem o endpoint padronizado, o monitoramento não funciona | Baixa — depende de adesão de outros times | ⚠️ VALIDAR PRIMEIRO | Alinhar com os times e definir prazo de adoção |
| T2 | Os times responsáveis pelas aplicações Java irão implementar o **Spring Boot Actuator** (`/actuator/health`) nos seus sistemas | Alto — sem o endpoint, aplicações Java não são monitoradas | Baixa — depende de adesão de outros times | ⚠️ VALIDAR PRIMEIRO | Alinhar com os times Java e verificar versões do Spring Boot em uso |
| T3 | O endpoint externo que fornece a lista de sistemas estará disponível e com contrato de API definido antes do início do desenvolvimento | Alto — sem esse contrato, não é possível construir a integração de inventário | Baixa — não confirmado | ⚠️ VALIDAR PRIMEIRO | Identificar o time responsável e solicitar documentação da API |
| T4 | O formato de resposta do Spring Boot Actuator (`/actuator/health`) é compatível com o que o sistema espera dos endpoints de healthcheck | Alto — se os formatos forem incompatíveis, será necessário um adaptador | Média — ambos seguem padrões abertos, mas podem ter diferenças | ⚠️ VALIDAR PRIMEIRO | Fazer spike técnico comparando os formatos de resposta de ambas as bibliotecas |
| T5 | A camada de integração com ferramentas de observabilidade (ex: Prometheus) pode ser desacoplada do core do sistema, permitindo trocar a tecnologia sem impacto | Alto — se houver acoplamento forte, qualquer troca de ferramenta exige refatoração ampla | Média — depende das decisões arquiteturais do time | ✅ Confirmar e seguir | Definir a arquitetura com interface/adapter para a camada de métricas no início do projeto |
| T6 | O token de autenticação do Portal de Serviços carrega as informações de tipo de usuário necessárias (Administrador ou Usuário) de forma legível pelo sistema | Alto — se o token não carregar essa informação, não é possível diferenciar o tipo de relatório | Baixa — depende do contrato de autenticação do Portal | ⚠️ VALIDAR PRIMEIRO | Solicitar ao time do Portal a especificação do token (claims, formato) |

---

## Resumo de Prioridades

### ⚠️ Validar Primeiro (Alto impacto + Baixa/Média certeza)

| # | Hipótese | Responsável sugerido |
|---|----------|----------------------|
| U1 | Acesso de todos os usuários ao Portal de Serviços | Time do Portal de Serviços |
| U2 | Aceitação de e-mails de alerta pelos Administradores | Entrevista com Administradores |
| U4 | Formato do relatório (assinatura + QR Code) aceito pelo Tribunal | Jurídico / Representante do Tribunal |
| N1 | Conformidade com a minuta do Tribunal | Jurídico / Representante do Tribunal |
| N2 | Prazo alinhado com o Portal de Serviços | Time do Portal de Serviços |
| T1 | Adoção do padrão .NET HealthChecks pelos times | Times de desenvolvimento .NET |
| T2 | Adoção do Spring Boot Actuator pelos times Java | Times de desenvolvimento Java |
| T3 | Disponibilidade do endpoint externo de inventário de sistemas | Time responsável pelo endpoint |
| T4 | Compatibilidade entre formatos ASP.NET e Spring Boot Actuator | Spike técnico |
| T6 | Claims do token de autenticação do Portal | Time do Portal de Serviços |

### ✅ Confirmar e Seguir

| # | Hipótese |
|---|----------|
| T5 | Desacoplamento da camada de observabilidade via adapter |

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
