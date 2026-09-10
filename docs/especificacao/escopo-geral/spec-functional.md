# Especificação Funcional — Monitoramento de Indisponibilidade

> Gerado em: 10/09/2026
> Versão: 1.0
> Status: Rascunho
> Referência: docs/escopo/escopo-geral/escopo.md

---

## Contexto

Este documento especifica, em BDD, a **Feature 8 — Validação de Autenticidade do
Relatório (`/autenticar`)** (escopo §9): consulta pública, sem autenticação,
disponível a Usuários (cidadãos) e Administradores, que confirma a veracidade
de um relatório por limiar a partir do código verificador impresso nele
(digitado manualmente ou lido via QR Code).

> **Nota:** as Funcionalidades 1 a 7 do escopo já possuem especificação própria
> em `docs/especificacao/escopo-geral/Funcionalidade N - *.docx`, produzida
> antes da existência deste arquivo — por isso não são repetidas aqui. Este
> `spec-functional.md` nasce cobrindo apenas a Feature 8; se essas
> especificações anteriores precisarem ser consolidadas neste mesmo arquivo no
> futuro, isso deve ser um passo explícito, não assumido por esta versão.

---

## Features Especificadas

- [Feature 8: Validação de Autenticidade do Relatório (/autenticar)](#feature-8-validação-de-autenticidade-do-relatório-autenticar)

---

## Feature 8: Validação de Autenticidade do Relatório (/autenticar)

### Narrativa

```
Feature: Validação de Autenticidade do Relatório
  In order to confirmar, sem depender do emissor, que um relatório apresentado
    (impresso ou em PDF) é genuíno e não foi adulterado ou forjado — evitando
    que relatórios falsos sejam aceitos como prova de indisponibilidade em
    petições ou auditorias
  As Usuário (cidadão) ou Administrador
  I want consultar a autenticidade de um relatório na rota pública /autenticar,
    informando o código verificador impresso nele (manualmente ou via QR Code)
```

### Regras de Negócio

- **RN-8.1** — A consulta em `/autenticar` usa exclusivamente o `COD_VERIFICADOR` informado (digitado manualmente ou recebido via querystring do QR Code, parâmetro `verificador`). O parâmetro `usuario` da querystring do QR Code não é validado nem exibido na tela.
- **RN-8.2** — Apenas relatórios do tipo Por Limiar (`SGL_TIPO='L'`) podem ser autenticados por esta rota — é o único tipo que possui `COD_VERIFICADOR` (RN-5.4). Um código que corresponda a um relatório diário do Administrador (tipo A) é tratado como não encontrado.
- **RN-8.3** — Em caso de código verificador válido, a tela exibe: mensagem de autenticidade confirmada, data de referência do relatório, e os sistemas incluídos (com períodos e indisponibilidade total do dia) — dados equivalentes aos do relatório original.
- **RN-8.4** — Em caso de código inexistente, inválido ou pertencente a um relatório não autenticável (tipo A), a tela exibe uma mensagem genérica de "código verificador não encontrado", sem detalhar o motivo — evita fornecer pistas para tentativa de adivinhação.
- **RN-8.5** — O campo de código verificador é obrigatório no formulário de consulta manual; um envio vazio é bloqueado no front-end, sem chamar o backend.
- **RN-8.6** — A rota `/autenticar` é acessível sem autenticação, igualmente a Usuários e a Administradores, como parte da Aplicação Pública (DMZ).
- **RN-8.7** — Após 10 tentativas de consulta malsucedidas em 1 minuto a partir do mesmo endereço IP, novas tentativas são bloqueadas por 5 minutos, com mensagem informando o bloqueio temporário.

### Cenários

---

#### Cenário 8.1: Confirmar autenticidade de um relatório com código verificador válido

Dado que existe um relatório por limiar (tipo L) de 23/01/2026 com código verificador "0000001"
  E que esse relatório inclui E-TCE (120 minutos) e Consulta Processual (135 minutos)
Quando um Usuário acessa `/autenticar` e informa o código verificador "0000001"
Então o sistema exibe a mensagem "Documento autêntico"
  E exibe a data de referência 23/01/2026
  E exibe os sistemas do relatório, com seus períodos e a indisponibilidade total do dia

---

#### Cenário 8.2: Confirmar autenticidade via QR Code

Dado que existe um relatório por limiar de 23/01/2026 com código verificador "0000001"
Quando um Administrador escaneia o QR Code do relatório, que abre `/autenticar?verificador=0000001&usuario=000000123`
Então o sistema exibe automaticamente o mesmo resultado do Cenário 8.1, sem exigir digitação manual do código
  E o parâmetro "usuario" da querystring não é exibido nem usado na validação (RN-8.1)

---

#### Cenário 8.3: Código verificador não encontrado

Esquema do Cenário: Código informado não corresponde a um relatório autenticável
  Dado {situação}
  Quando alguém acessa `/autenticar` informando o código "{código informado}"
  Então o sistema exibe a mensagem "Código verificador não encontrado. Verifique o código informado."

  Exemplos:
    | situação | código informado |
    | nenhum relatório foi gerado com esse código | "9999999" |
    | código corresponde ao identificador interno de um relatório diário do Administrador (tipo A), que não possui código verificador (RN-8.2) | "45" |

---

#### Cenário 8.4: Consulta sem informar o código verificador

Dado que um Usuário está na tela `/autenticar`
Quando tenta consultar sem informar nenhum código verificador
Então o sistema exibe a mensagem "Informe o código verificador"
  E não realiza a consulta ao backend

---

#### Cenário 8.5: Bloqueio temporário por excesso de tentativas

Dado que o mesmo endereço IP realizou 10 consultas malsucedidas em `/autenticar` no último minuto
Quando uma 11ª tentativa é realizada dentro dessa mesma janela de 1 minuto
Então o sistema bloqueia a consulta e exibe a mensagem "Muitas tentativas. Aguarde alguns minutos e tente novamente."
  E o bloqueio é removido automaticamente após 5 minutos

### Pontos em Aberto

- [ ] **Formato/algoritmo definitivo do `COD_VERIFICADOR`** — ainda não definido (o protótipo de PDF usa um exemplo sequencial simples, `"0000001"`); afeta diretamente o espaço de busca e a eficácia real do rate limiting da RN-8.7 (hipótese U5 do escopo). Responsável: Tribunal / Equipe de Arquitetura.
- [ ] **Relatório Diário do Administrador (tipo A) também deve ser autenticável?** — o escopo §4 menciona QR Code de autenticidade para esse tipo, mas RN-5.4 define que só o tipo L possui código verificador; hoje a RN-8.2 trata um código de relatório tipo A como não encontrado (hipótese U6 do escopo). Responsável: Tribunal.

---

## Próximos Passos Sugeridos

- **spec-nonfunctional** — detalhar o requisito de rate limiting (RN-8.7) como requisito não funcional formal (throttling, escopo por IP vs. sessão, observabilidade dos bloqueios)
- **refinement-screens** — detalhar a tela `/autenticar` (layout do formulário manual, estado de carregamento, mensagens de sucesso/erro)
- **refinement-api** — detalhar o contrato do endpoint anônimo `GET /relatorios/autenticar` (já referenciado na tarefa 4.12 do plano de execução)

---

## Histórico

| Data | Versão | Alteração | Autor |
|------|--------|-----------|-------|
| 10/09/2026 | 1.0 | Versão inicial — Feature 8 (Validação de Autenticidade do Relatório) | Bruno / Claude |
