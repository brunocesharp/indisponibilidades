# Métricas de Sucesso — Monitoramento de Indisponibilidade

> Gerado em: 26/06/2026
> Versão: 1.0

---

## Objetivo Central

Antes deste sistema, **não existe nenhuma forma de contabilizar ou comprovar que um sistema esteve indisponível**. O projeto entrega duas transformações principais:

- **Usuários (cidadãos)** passam a poder comprovar indisponibilidades para solicitar revisão de prazo processual em petições
- **Administradores** passam a ter rastreabilidade das indisponibilidades ao longo do dia para tomada de decisão e auditoria

---

## North Star Metric

> **Percentual de indisponibilidades registradas que resultaram em relatório gerado corretamente e dentro do prazo**

Esta métrica captura o valor central do sistema: de nada adianta detectar uma indisponibilidade se o relatório não for gerado de forma confiável e no momento certo.

| Aspecto | Detalhe |
|---------|---------|
| **Fórmula** | (Relatórios gerados corretamente / Indisponibilidades que atingiram o limiar) × 100 |
| **Meta inicial** | 100% — toda indisponibilidade que atingir o limiar deve gerar relatório |
| **Baseline** | Inexistente — não há sistema anterior para comparação |
| **Frequência de acompanhamento** | Mensal |
| **Responsável** | Equipe de desenvolvimento do Portal de Serviços |

---

## Métricas de Negócio

| # | Métrica | Descrição | Baseline | Meta (3 meses pós-lançamento) | Responsável |
|---|---------|-----------|----------|-------------------------------|-------------|
| N1 | Cobertura de sistemas monitorados | % dos sistemas cadastrados no Portal que estão sendo monitorados ativamente | 0% (nenhum monitoramento hoje) | 100% dos sistemas cadastrados | Equipe de Infra |
| N2 | Conformidade com a minuta do Tribunal | Sistema aceito formalmente pelo Tribunal como conformante | Não existe | Aprovação formal obtida no lançamento | Equipe de desenvolvimento |
| N3 | Tempo médio de detecção de indisponibilidade | Tempo entre início da indisponibilidade e primeiro registro no sistema | Não medido hoje | ≤ 1 minuto (frequência de verificação padrão) | Equipe de Infra |
| N4 | Relatórios diários gerados para o Administrador | % de dias com relatório diário gerado às 00h sem falha | Não existe | 100% | Equipe de desenvolvimento |

---

## Métricas de Produto e Usuário

### Adoção

| # | Métrica | Descrição | Baseline | Meta | Responsável |
|---|---------|-----------|----------|------|-------------|
| P1 | Sistemas com healthcheck implementado | Nº de sistemas que implementaram o endpoint de healthcheck (.NET ou Java) | 0 | 100% dos sistemas cadastrados | Times de Dev + Equipe de Arquitetura |
| P2 | Usuários que acessaram relatórios | Nº de usuários únicos que consultaram pelo menos 1 relatório no mês | 0 | A definir após 1 mês de operação | Equipe Portal de Serviços |

### Engajamento

| # | Métrica | Descrição | Baseline | Meta | Responsável |
|---|---------|-----------|----------|------|-------------|
| P3 | Relatórios consultados por busca de data | Nº de consultas de relatórios por data realizadas por mês | 0 | A definir após 1 mês de operação | Equipe Portal de Serviços |
| P4 | Petições com relatório de indisponibilidade anexado | Nº de petições que usaram relatório como comprovação de indisponibilidade | 0 | A definir após 1 mês de operação — indica adoção real pelos cidadãos | Tribunal |

### Confiabilidade (Task Success)

| # | Métrica | Descrição | Baseline | Meta | Responsável |
|---|---------|-----------|----------|------|-------------|
| P5 | Taxa de falha na geração de relatórios | % de relatórios que falharam ao ser gerados quando deveriam | Não medido | 0% | Equipe de desenvolvimento |
| P6 | Autenticidade validada por QR Code | % de relatórios cujo QR Code é validado com sucesso | Não medido | 100% | Equipe de desenvolvimento |

---

## Métricas Técnicas

| # | Métrica | Descrição | Critério mínimo | Responsável |
|---|---------|-----------|-----------------|-------------|
| T1 | Tempo de detecção de indisponibilidade | Tempo máximo entre início da indisponibilidade e primeiro registro | ≤ 1 minuto | Equipe de Infra |
| T2 | Disponibilidade do próprio sistema de monitoramento | Uptime do sistema | Toda indisponibilidade > 1 min do sistema de monitoramento é contabilizada como falha crítica | Equipe de Infra |
| T3 | Tempo de geração do relatório diário | Tempo máximo para gerar o relatório diário do Administrador | Gerado até 00h05 (5 min de tolerância) | Equipe de desenvolvimento |

---

## Critérios de Aceitação para Go-live

Estes critérios devem ser atendidos antes do lançamento:

- [ ] 100% dos sistemas cadastrados no Portal estão sendo monitorados
- [ ] Relatório diário do Administrador gerado corretamente em ambiente de homologação por pelo menos 5 dias consecutivos
- [ ] Relatório por limiar (2h) gerado corretamente ao simular indisponibilidade em ambiente de homologação
- [ ] QR Code de validação funcionando em 100% dos relatórios gerados
- [ ] Tempo de detecção de indisponibilidade ≤ 1 minuto confirmado em testes
- [ ] Hierarquia de serviços propagando indisponibilidade corretamente nos testes
- [ ] Conformidade formal com a minuta do Tribunal confirmada

---

## Baseline

| Situação | Antes do sistema |
|----------|-----------------|
| Rastreamento de indisponibilidades | **Inexistente** — não há nenhuma forma de contabilizar ou comprovar indisponibilidades |
| Comprovação para petições | **Inexistente** — cidadãos não têm como comprovar indisponibilidade formalmente |
| Relatórios para Administradores | **Inexistente** — acompanhamento manual ou nenhum |

> O baseline zero reforça o impacto direto do sistema: qualquer relatório gerado corretamente já representa valor que não existia antes.

---

## Responsáveis pelo Acompanhamento

| Área | Métricas sob responsabilidade |
|------|-------------------------------|
| Equipe de desenvolvimento do Portal de Serviços | North Star, N2, N4, P2, P3, P5, P6, T3 |
| Equipe de Infraestrutura | N1, N3, T1, T2 |
| Times de Desenvolvimento (.NET e Java) | P1 |
| Tribunal | P4 (petições com relatório anexado) |

---

## Próximos Passos Sugeridos

- **Gerar o escopo** — consolidar vision, assumptions, stakeholders e métricas em documento formal
- **Ação imediata** — definir instrumentação para captura das métricas P2, P3 e P4 junto ao time do Portal
- **Ação imediata** — validar critérios de aceitação do go-live com o Diretor da DTI e o Tribunal
