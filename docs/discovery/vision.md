# Visão do Projeto — Monitoramento de Indisponibilidade

> Gerado em: 26/06/2026
> Versão: 1.0

---

## O Problema

A organização não possui uma forma centralizada e automatizada de monitorar a disponibilidade das suas aplicações. Quando sistemas ficam indisponíveis, a equipe não tem visibilidade consolidada do tempo de indisponibilidade acumulado, nem relatórios estruturados para cumprir exigências externas. Isso compromete a conformidade com a minuta do Tribunal que exige a disponibilização dessas informações aos usuários, com prazo atrelado à entrada do Portal de Serviços.

| Aspecto | Descrição |
|---------|-----------|
| **Quem sente essa dor** | Administradores de sistemas e usuários que precisam acompanhar a saúde das aplicações |
| **Frequência/Impacto** | Diária — indisponibilidades ocorrem sem registro ou notificação adequada |
| **Situação atual** | Sem solução estruturada; monitoramento manual ou inexistente |

---

## Público-Alvo

O sistema possui dois perfis de usuários com responsabilidades distintas.

| Perfil | Descrição | Principal Necessidade | Contexto de Uso |
|--------|-----------|----------------------|-----------------|
| **Administrador de Sistemas** | Opera o sistema, gerencia serviços cadastrados e recebe relatório diário completo | Cadastrar sistemas, configurar hierarquias e acompanhar todas as indisponibilidades | Rotina operacional diária |
| **Usuário** | Acessa relatórios de indisponibilidade e consulta histórico por data | Visualizar relatórios gerados quando um sistema ultrapassa 2h de indisponibilidade | Consulta sob demanda ou notificação |

---

## Proposta de Valor

O sistema centraliza o monitoramento de saúde das aplicações via endpoints de healthcheck padronizados, acumula os períodos de indisponibilidade ao longo do dia, aplica inteligência de hierarquia entre serviços para evitar alarmes falsos, e gera relatórios automáticos para conformidade com exigências do Tribunal.

| Aspecto | Descrição |
|---------|-----------|
| **Transformação esperada** | Substituição do monitoramento manual/inexistente por rastreamento automatizado com relatórios gerados sem intervenção humana |
| **Diferencial** | Hierarquia entre serviços elimina falsos positivos — se o serviço pai cai, os filhos não são contabilizados como indisponíveis independentemente |
| **Frase de elevador** | "Monitora automaticamente a saúde de todos os sistemas, elimina falsos positivos por hierarquia e gera relatórios de indisponibilidade para conformidade com o Tribunal" |

---

## Motivação e Contexto

O projeto está sendo executado agora por exigência regulatória. O Tribunal elaborou uma minuta determinando que informações de indisponibilidade devem ser disponibilizadas aos usuários. O prazo de entrega está diretamente atrelado à entrada do Portal de Serviços.

**Gatilhos identificados:**
- Minuta do Tribunal exigindo rastreabilidade de indisponibilidades
- Prazo vinculado ao lançamento do Portal de Serviços
- Ausência de qualquer solução existente para esse monitoramento

---

## Restrições Conhecidas

| Tipo | Restrição | Impacto |
|------|-----------|---------|
| **Tecnologia** | Os endpoints de healthcheck dos sistemas monitorados devem seguir o padrão `Microsoft.Extensions.Diagnostics.HealthChecks` (ASP.NET Core) | Compatibilidade com ferramentas como Grafana e outros sistemas que consomem esse padrão |
| **Prazo** | Entrega alinhada ao lançamento do Portal de Serviços | Define o deadline máximo do projeto |
| **Integração** | Os sistemas monitorados precisam implementar e expor um endpoint de healthcheck compatível | Dependência de outros times para viabilizar o monitoramento |

---

## Regras de Negócio Centrais

- **Monitoramento contínuo diário:** O sistema verifica os endpoints de healthcheck periodicamente e acumula os períodos de indisponibilidade ao longo do dia.
- **Relatório por limiar:** Se um sistema acumular mais de **2 horas** de indisponibilidade no dia, um relatório é gerado e enviado ao usuário responsável.
- **Relatório diário do administrador:** Ao final de cada dia, um relatório completo com todas as indisponibilidades é gerado automaticamente para o Administrador.
- **Hierarquia de serviços:** Quando um serviço pai está indisponível, os serviços filhos na hierarquia **não** são contabilizados como indisponíveis — apenas o serviço mais alto da cadeia é considerado o ponto de falha.
- **Cadastro de serviços:** Novos sistemas são cadastrados com sigla, nome e endpoint de healthcheck, podendo ser vinculados a uma hierarquia existente.

---

## Declaração de Visão

> "Prover monitoramento automatizado e centralizado da saúde das aplicações, com relatórios de indisponibilidade precisos e livres de falsos positivos, garantindo conformidade com as exigências do Tribunal e transparência para administradores e usuários."

---

## Pontos a Refinar

- [ ] Frequência exata das verificações de healthcheck (ex: a cada 1 minuto, 5 minutos?)
- [ ] Canal de entrega dos relatórios (e-mail, notificação no portal, ambos?)
- [ ] Profundidade máxima da hierarquia de serviços (2 níveis, N níveis?)
- [ ] Critério de "fim do dia" para o relatório do administrador (meia-noite? horário configurável?)
- [ ] Identificação de quem é o "usuário responsável" por cada sistema cadastrado

---

## Próximos Passos Sugeridos

- **Oportunidades** — mapear dores e jobs to be done dos Administradores e Usuários em profundidade
- **Hipóteses** — validar premissas críticas como a adoção do padrão healthcheck pelos outros times
- **Stakeholders** — mapear os times responsáveis pelos sistemas monitorados e o Tribunal como parte interessada
- **Métricas** — definir como medir o sucesso (cobertura de sistemas monitorados, tempo médio até notificação, conformidade com relatórios exigidos)
