# Ficha do registro de programa de computador (e-Software / INPI)

**Preparado em:** 09/11/2026. Os campos com **[CONFIRMAR]** dependem de decisão ou de dado pessoal.
**Não colocar CPF neste arquivo**: o repositório é público. Preencher os CPFs direto no formulário do INPI.

| Campo do e-Software | Preenchimento | Origem |
|---|---|---|
| Título do programa | **VIA LEITE SENSE — Radar de Risco Produtivo, Qualidade e Rentabilidade para a Cadeia Leiteira** | README |
| Data de criação | **07/06/2026** | primeiro commit `76439e2` |
| Data de publicação | **07/06/2026** [CONFIRMAR] | criação do repositório público no GitHub (`createdAt` 2026-06-07). Se ele nasceu privado, usar a data em que ficou público ou a do primeiro deploy na Vercel (`18edd1c`, 01/07/2026). |
| Linguagens | Python · JavaScript · HTML · CSS · SQL | 53 arquivos `.py`; frontend SPA; DuckDB |
| Campo de aplicação | **[ESCOLHER na tabela do INPI]**: agropecuária / pecuária leiteira; informação e gestão | tabela "Campo de Aplicação" do e-Software |
| Tipo de programa | **[ESCOLHER na tabela do INPI]**: aplicativo; inteligência artificial / análise de dados; aplicação web | tabela "Tipo de Programa" |
| Algoritmo hash | **SHA-512** | [`gerar_pacote_inpi.ps1`](gerar_pacote_inpi.ps1) |
| Resumo hash | gerado **no dia do protocolo** pelo script (não usar o hash do teste de 09/11) | — |
| Titular | **USINA I.A. TECNOLOGIA E INOVACAO I.S. INOVA SIMPLES (I.S.) — CNPJ 63.230.034/0001-92** (natureza 234-8, Empresa Simples de Inovação, porte ME) | cartão CNPJ |
| Autores | **[CONFIRMAR]**: só quem escreveu código ou modelos. Os commits estão todos como "USINA I.A.", então a lista precisa vir da equipe. Provável: Fagner Pinho Pereira Vieira dos Santos; Diego Santana (arquitetura/backend), se tiver contribuído com código. | Etapa 0.2 |
| Vínculo autor → titular | **cessão de direitos** (termo assinado). Não é vínculo empregatício. | [`TERMO_CESSAO_DIREITOS_EQUIPE.md`](TERMO_CESSAO_DIREITOS_EQUIPE.md) |
| Programa derivado? | Não (primeiro registro) | — |
| Declaração de Veracidade | baixar no módulo da GRU ou no e-Software e assinar com certificado **ICP-Brasil (e-CNPJ)** | Etapa 0.4 |
| GRU | **730**, cerca de R$ 210, sem desconto. Confirmar na emissão. | — |

## Sobre código feito com ajuda de IA
O direito autoral no Brasil protege obra de **autor humano**. O registro continua possível: autores são as pessoas
que conceberam, dirigiram, revisaram e integraram o código. Não declarar a IA como autora. Guardar o histórico de
commits e decisões (`DECISIONS.md`, `SESSION_LOG.md`) como prova da direção humana do desenvolvimento.

## No dia do protocolo
```powershell
git tag -a v1.0-inpi -m "Versao registrada no INPI"
```
```powershell
powershell -ExecutionPolicy Bypass -File docs\registro_pi\gerar_pacote_inpi.ps1 -Ref v1.0-inpi
```
```powershell
git push origin v1.0-inpi
```
O script grava o `.zip` e o `MANIFESTO.txt` em `Documents\INPI_ViaLeiteSense`. Copie os dois para o Drive **e**
para um pendrive.

Teste de 09/11/2026 (commit `0ef03f7`): o script rodou sem erro. Os únicos CPFs encontrados são fictícios (demo do
frontend e teste unitário) e ficam na lista de exceções.
