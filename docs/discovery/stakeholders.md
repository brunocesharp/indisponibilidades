# Stakeholders — Monitoramento de Indisponibilidade

> Gerado em: 26/06/2026
> Versão: 1.0

---

## Mapa de Envolvidos

| # | Stakeholder | Tipo | Influência | Interesse | Quadrante |
|---|-------------|------|------------|-----------|-----------|
| S1 | Diretor da DTI | Interno | Alta | Alto | 🔴 Engajar ativamente |
| S2 | Tribunal (órgão regulador) | Externo | Alta | Alto | 🔴 Engajar ativamente |
| S3 | Time do Portal de Serviços | Interno | Alta | Alto | 🔴 Engajar ativamente |
| S4 | Sistema SSO | Interno | Alta | Baixo | 🟡 Manter satisfeito |
| S5 | Time de Segurança e Infra | Interno | Alta | Baixo | 🟡 Manter satisfeito |
| S6 | Equipe de Arquitetura | Interno | Alta | Médio | 🟡 Manter satisfeito |
| S7 | Times de Desenvolvimento (.NET e Java) | Interno | Média | Alto | 🟢 Manter informado |
| S8 | Administradores de Sistemas | Interno | Média | Alto | 🟢 Manter informado |
| S9 | Usuários (cidadãos) | Externo | Baixa | Alto | 🟢 Manter informado |

---

## Detalhamento por Stakeholder

### S1 — Diretor da DTI
| Aspecto | Descrição |
|---------|-----------|
| **Papel** | Patrocinador interno do projeto |
| **Expectativa** | Entrega dentro do prazo, conformidade com a minuta do Tribunal |
| **Possível preocupação** | Atrasos causados por dependências externas (Portal, times de dev) |
| **Estratégia** | Reportes periódicos de status; envolver em decisões de escopo e prazo |

---

### S2 — Tribunal (órgão regulador)
| Aspecto | Descrição |
|---------|-----------|
| **Papel** | Regulador externo que exige o sistema via minuta |
| **Expectativa** | Sistema em conformidade com a minuta; relatórios autênticos e auditáveis |
| **Possível preocupação** | Formato dos relatórios não atender aos requisitos formais |
| **Estratégia** | Validar formato do relatório (assinatura + QR Code) antes do desenvolvimento — hipóteses U4 e N1 ainda pendentes |

---

### S3 — Time do Portal de Serviços
| Aspecto | Descrição |
|---------|-----------|
| **Papel** | Fornecedor do endpoint de inventário de sistemas e canal de exibição dos relatórios |
| **Expectativa** | Integração simples e bem definida; alinhamento de prazo |
| **Possível preocupação** | Atrasos no Portal impactam diretamente a entrega deste sistema |
| **Dependências** | Endpoint de inventário de sistemas; página de relatórios dentro do Portal |
| **Estratégia** | Manter comunicação frequente; alinhar contrato da API de inventário o quanto antes |

---

### S4 — Sistema SSO (Single Sign-On)
| Aspecto | Descrição |
|---------|-----------|
| **Papel** | Provedor de autenticação e autorização |
| **Expectativa** | Integração respeitando o contrato do token |
| **Fontes de dados** | Usuários internos (AD) via **SIGESP**; usuários externos via **Portal de Serviços** |
| **Contrato conhecido** | Claim `listaGruposSistema = PRT_SRV_ADMINISTRADORES` identifica Administrador de Sistemas |
| **Estratégia** | Solicitar documentação completa das claims disponíveis no token; não há necessidade de engajamento frequente |

---

### S5 — Time de Segurança e Infraestrutura
| Aspecto | Descrição |
|---------|-----------|
| **Papel** | Responsável por disponibilizar acesso aos endpoints de healthcheck dos sistemas internos |
| **Expectativa** | Demandas bem documentadas, sem impacto à segurança da rede |
| **Possível preocupação** | Liberar endpoints internos pode levantar questões de segurança |
| **Estratégia** | Envolver cedo para mapear regras de firewall e rede; documentar quais endpoints precisam ser liberados |

---

### S6 — Equipe de Arquitetura
| Aspecto | Descrição |
|---------|-----------|
| **Papel** | Guardiã dos padrões técnicos aprovados para o tribunal |
| **Expectativa** | Conformidade com os padrões aprovados (`Microsoft.Extensions.Diagnostics.HealthChecks` e `Spring Boot Actuator`) |
| **Decisões já tomadas** | Aprovação do uso de ambas as bibliotecas de healthcheck |
| **Estratégia** | Consultar para decisões arquiteturais relevantes (ex: desacoplamento da camada de observabilidade — hipótese T5) |

---

### S7 — Times de Desenvolvimento (.NET e Java)
| Aspecto | Descrição |
|---------|-----------|
| **Papel** | Responsáveis por implementar os endpoints de healthcheck nas suas aplicações |
| **Expectativa** | Padrão claro e simples de implementar; sem impacto significativo nas suas entregas |
| **Possível preocupação** | Overhead de implementação; conflito com outras prioridades |
| **Estratégia** | Fornecer guias de implementação claros; definir prazo de adoção junto à Equipe de Arquitetura |

---

### S8 — Administradores de Sistemas
| Aspecto | Descrição |
|---------|-----------|
| **Papel** | Usuário operacional do sistema — cadastra hierarquias e recebe relatórios |
| **Expectativa** | Interface simples para gerenciamento; receber alertas de indisponibilidade por e-mail sem atraso |
| **Acesso** | Via Portal de Serviço Administrativo com login pelo AD |
| **Estratégia** | Envolver em testes de usabilidade e validação dos relatórios gerados |

---

### S9 — Usuários (cidadãos)
| Aspecto | Descrição |
|---------|-----------|
| **Papel** | Consumidor final dos relatórios de indisponibilidade |
| **Expectativa** | Relatórios claros, autênticos e acessíveis por data |
| **Acesso** | Via Portal de Serviços com conta gov.br |
| **Estratégia** | Monitorar uso após lançamento; coletar feedback via Portal |

---

## Dependências Críticas entre Stakeholders

```
Tribunal ──────────────────► Define conformidade exigida
                                        │
                                        ▼
Diretor DTI ───────────────► Patrocina e aprova o projeto
                                        │
                         ┌──────────────┼──────────────┐
                         ▼              ▼              ▼
              Time Portal        SSO / SIGESP      Time Segurança/Infra
              (inventário +      (autenticação     (acesso aos
               canal)             e claims)         endpoints)
                         │
                         ▼
              Times Dev .NET e Java
              (implementam healthcheck)
                         │
                         ▼
              Sistema de Monitoramento
                         │
                    ┌────┴────┐
                    ▼         ▼
             Administradores  Usuários
```

---

## Bloqueadores Potenciais

| Stakeholder | Risco | Mitigação |
|-------------|-------|-----------|
| Tribunal | Não aprovar o formato do relatório (assinatura + QR Code) | Validar formato antes do desenvolvimento (hipóteses U4 e N1 pendentes) |
| Time do Portal de Serviços | Atraso no Portal impacta entrega deste sistema | Manter comunicação frequente; monitorar cronograma |
| Time de Segurança e Infra | Demora na liberação de endpoints internos | Envolver cedo; documentar todas as necessidades de acesso |
| Times de Dev (.NET e Java) | Não priorizar a implementação do healthcheck | Definir prazo formal com apoio da Equipe de Arquitetura e Diretor DTI |

---

## Estratégia de Comunicação

| Stakeholder | Canal | Frequência | Responsável |
|-------------|-------|------------|-------------|
| Diretor da DTI | Relatório de status / reunião | Quinzenal | Gerente do projeto |
| Tribunal | Reunião formal / documentação | Pontual (validação do formato) | Gerente do projeto + Jurídico |
| Time do Portal de Serviços | Reunião técnica + chat | Semanal | Tech lead |
| Sistema SSO | Documentação técnica | Pontual (definição do contrato) | Tech lead |
| Time de Segurança e Infra | Reunião técnica | Pontual (mapeamento de acessos) | Tech lead |
| Equipe de Arquitetura | Reunião técnica | Sob demanda (decisões arquiteturais) | Tech lead |
| Times de Dev (.NET e Java) | Guias técnicos + chat | Uma vez (orientação) + suporte | Tech lead |
| Administradores de Sistemas | Treinamento + documentação | Pontual (pré-lançamento) | Analista |
| Usuários (cidadãos) | Portal de Serviços | Pós-lançamento | — |

---

## Próximos Passos Sugeridos

- **Métricas de sucesso** — definir indicadores para conformidade com o Tribunal e adoção do sistema
- **Escopo** — consolidar vision, assumptions e stakeholders em documento formal de escopo
- **Ação imediata** — agendar validação do formato do relatório com o Tribunal (hipóteses U4 e N1)
- **Ação imediata** — solicitar documentação completa da API de inventário do Portal de Serviços
- **Ação imediata** — envolver o Time de Segurança e Infra para mapear liberações de endpoints
