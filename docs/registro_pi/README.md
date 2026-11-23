# Registro de PI — painel (prioridade P0 de 09/11 a ~30/11/2026)

Plano completo: [`../ROTEIRO_REGISTRO_PI.md`](../ROTEIRO_REGISTRO_PI.md) · Riscos: [`../PESQUISA_ANTERIORIDADE_PI_2026-11-09.md`](../PESQUISA_ANTERIORIDADE_PI_2026-11-09.md)

**Regra:** tudo que não custa dinheiro anda agora. O que custa fica pronto para pagar **a partir de 20/11/2026**,
quando entram as férias da Saneago.

## Fase A — sem custo (09/11 → 19/11)

| # | Tarefa | Quem | Status |
|---|---|---|---|
| A1 | Pesquisa de anterioridade (INPI marcas, software e patentes; web) | Claude | ✅ 09/11 |
| A2 | Logotipo da marca em JPG 945×945 → [`marca_via_leite_sense_inpi.jpg`](marca_via_leite_sense_inpi.jpg) | Claude | ✅ 09/11 |
| A3 | Especificação das classes 42 e 9 com itens da NCL 13 → [`ESPECIFICACAO_MARCA.md`](ESPECIFICACAO_MARCA.md) | Claude | ✅ 09/11 |
| A4 | Minuta do termo de cessão e confidencialidade da equipe → [`TERMO_CESSAO_DIREITOS_EQUIPE.md`](TERMO_CESSAO_DIREITOS_EQUIPE.md) | Claude | ✅ 09/11 |
| A5 | Ficha do e-Software e script de pacote/hash testado → [`FICHA_E_SOFTWARE.md`](FICHA_E_SOFTWARE.md), [`gerar_pacote_inpi.ps1`](gerar_pacote_inpi.ps1) | Claude | ✅ 09/11 |
| A6 | **Titular:** **USINA I.A. TECNOLOGIA E INOVACAO I.S. INOVA SIMPLES (I.S.)**, CNPJ **63.230.034/0001-92**. Aberta em 16/10/2025, ativa, porte ME, natureza 234-8 (Empresa Simples de Inovação). Titular único: Fagner. CNAEs 6209-1/00, 6201-5/01 e 6319-4/00, compatíveis com as classes 42 e 9. Usar **exatamente** essa grafia em todos os pedidos. | Claude (cartão CNPJ) | ✅ 10/11 |
| A6b | Comprovante de inscrição: há um em `Desktop\CNPJ USINA.pdf`, emitido em 25/04/2026. Ele vale "na data da emissão", então **emitir um novo no dia do depósito** (consultacnpj.redesim.gov.br, gratuito) para anexar à petição 3019. Não colocar esse PDF no repositório: tem endereço e contatos. | Fagner | ◐ |
| A7 | Decidir a **contrapartida** do termo (gratuita ou quotas/vesting) e **colher as 5 assinaturas** (gov.br serve) | Fagner + equipe | ☐ |
| A8 | Definir **quem entra como autor** do software (só quem escreveu código ou modelos) | Fagner + Diego | ☐ |
| A9 | Ler as cláusulas de PI do **regulamento INOVA SENAI / Projeto Integrador (FATESG)** e do termo **FAPEG/SENAR** da Fase D. A minuta de dados de 03/09 coloca o SENAI/FATESG como interveniente. | Fagner | ☐ |
| A10 | Subir a conta **gov.br para prata ou ouro** (validação facial no app gov.br ou pelo banco) | Fagner | ☐ |
| A11 | Cadastro no **e-INPI** com o titular (gratuito) | Fagner | ☐ |
| A12 | Reutilizar a minuta já existente `Downloads\via leite\Minuta_Termo_Confidencialidade_Via-Leite-Sense.docx` (03/09) para pilotos. Ela já tem a cláusula 6.2 que afirma a titularidade da USINA I.A. sobre plataforma, código e marca. | Fagner | ☐ |

## Fase B — com custo (a partir de 20/11)

| # | Tarefa | Custo estimado | Depende de |
|---|---|---|---|
| B1 | Domínios `vialeitesense.com.br` + `vialeite.com.br` no registro.br (com o CNPJ) | cerca de R$ 80 por ano | A6 |
| B2 | Certificado digital **e-CNPJ A1** | cerca de R$ 150–250 | A6 |
| B3 | **Marca**: 2 × GRU 389 (classes 42 e 9) e depósito no e-Marcas | cerca de R$ 880 | A6, A10, A11 |
| B4 | **Software**: tag `v1.0-inpi`, script, GRU 730, Declaração de Veracidade assinada, protocolo no e-Software | cerca de R$ 210 | A7, A8, B2 |
| B5 | Apontar o domínio para a Vercel e criar o e-mail `contato@` | R$ 0 | B1 |
| | **Total** | **cerca de R$ 1.320–1.420** | |

| B3b | **Logo após o depósito da marca:** petição **3019, "Trâmite prioritário de marcas com direito à gratuidade"**, uma por processo, com o comprovante Inova Simples anexado | **R$ 0** | B3, A6b |

### O que o Inova Simples muda
- **Desconto de 50%** nas taxas de marca: confirmado pela Nota nº 9/2020 da Procuradoria do INPI. As Empresas
  Simples de Inovação entram na redução da Resolução 251/2019, como as ME/EPP. As estimativas acima já contam com ele.
- **Exame prioritário da marca, de graça** (art. 65-A, § 8º; Portaria INPI/PR 27/2025 e Portarias 66 e 67/2026).
  Não é automático: depois do protocolo é preciso peticionar o **código 3019** com o comprovante. A fila cai de
  cerca de 10 meses para poucos meses. A prioridade não afasta a chance de oposição ou de indeferimento.
- **Software (GRU 730):** as fontes de 10/2026 dizem que não há desconto para programa de computador. Conferir na
  emissão se a tela oferece desconto para "empresa simples de inovação".
- **Limite do regime:** a comercialização experimental vai até o teto anual do MEI (§ 10). Quando a USINA I.A. virar
  ME ou LTDA:
  - se o **CNPJ for mantido** na transformação, marca, software e domínio continuam no mesmo titular;
  - se mudar, peticionar a **transferência de titularidade** no INPI e trocar o titular no registro.br.
- **Responsabilidade:** o DREI tem tratado a empresa Inova Simples como sociedade em comum, com responsabilidade
  ilimitada dos titulares. Isso não afeta a PI, mas é mais um motivo para transformar a empresa em LTDA quando houver
  contrato pago.

**Ordem no dia 20/11:** B1 → B3 (a marca garante a prioridade de data) → B2 → B4.
Se o dinheiro sair em partes, priorizar **B3**: a marca é a única das três frentes em que esperar pode fazer perder o direito.

## Fase C — acompanhamento (após o depósito)
- Revista da Propriedade Industrial (RPI) às terças: conferir a publicação e o prazo de oposição de 60 dias.
- Responder exigência ou oposição em até 60 dias (cerca de R$ 90 cada).
- Certificado do software: conferir a publicação na RPI.
