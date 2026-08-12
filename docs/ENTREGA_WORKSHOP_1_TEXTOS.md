# Entrega — 1º Workshop · Desafio AgroStartup 2026

**Equipe:** VIA LEITE SENSE — USINA I.A. (Goiânia/GO)
**Prazo:** 13/08/2026, 23h59
**Arquivo a anexar:** `docs/Canvas_Plano_Vivo_Testes_VIA_LEITE_SENSE.pdf`

---

## Campo "Descrição da entrega"

> Entregamos o Canvas Plano Vivo de Testes e Validação do Protótipo do VIA LEITE SENSE,
> preenchido nas quatro páginas, com o histórico de versões do documento (v1.0 a v1.2),
> a formulação atual do problema, o público-alvo prioritário com separação entre usuário
> e comprador, a proposta de valor vigente e a descrição da versão atual do protótipo.
>
> O VIA LEITE SENSE é um radar de risco para a cadeia leiteira: cruza clima (INMET/THI),
> indicadores de qualidade (CCS, CBT e temperatura de tanque, ancorados na IN 77/2018) e
> impacto econômico em um Score de 0 a 100, que antecipa em 7, 15 e 30 dias qual produtor
> vai perder produção, qualidade ou bônus. O protótipo está na versão v4.3, no ar e
> demonstrável ao vivo (SPA na Vercel consumindo API FastAPI na Railway).
>
> A seção 6 registra três ciclos de teste executados entre 18/06 e 07/08/2026, cada um com
> hipótese, método, critério de validação definido antes do teste, evidência numérica e
> decisão tomada: (T-01) validação do motor de score sobre a base completa de 54.780
> registros; (T-02) ablação controlada que comprovou que o modelo não depende de
> identificadores pessoais do produtor — a remoção melhorou o MAE de 24,4523 para 24,1726 e
> resolveu a exposição de dados pessoais antes do piloto; (T-03) teste de sensibilidade da
> calibração das sete dimensões de risco, que resultou em uma guarda automatizada
> incorporada à suíte de testes. A seção 7 liga cada alteração do protótipo (v2.0 a v4.3)
> à evidência que a motivou, e o quadro final consolida o estado atual, as limitações
> assumidas e o que permanece sujeito a novos testes.

---

## Campo "URL do arquivo / link"

Subir para o Drive e colar aqui o link de `Canvas_Plano_Vivo_Testes_VIA_LEITE_SENSE.pdf`.

Se o formulário aceitar mais de um link, vale acrescentar:
- Demonstração ao vivo: https://via-leite-sense.vercel.app (usuário `demo` / senha `demo2025`)
- Plano de Negócio v2.0: link do Drive para `docs/PLANO_DE_NEGOCIO.pdf`

---

## Campo "Observações para o avaliador"

> Todas as evidências citadas no canvas são verificáveis. O protótipo pode ser navegado
> agora, sem agendamento, em https://via-leite-sense.vercel.app (usuário `demo`, senha
> `demo2025`), e a API responde em
> https://via-leite-sense-api-production.up.railway.app/health.
>
> As métricas do modelo (R² 0,9944, MAE 24,17 L e MAPE 3,58% sobre 10.920 registros de
> teste), os três rankings de risco e os resultados dos ciclos T-01 a T-03 estão
> versionados no repositório do projeto, junto de uma suíte de 44 testes automatizados e do
> registro datado de cada sessão de desenvolvimento.
>
> Uma nota de transparência: a camada operacional roda hoje sobre dados sintéticos
> calibrados somados a clima real do INMET. Nenhum dado de fazenda real foi utilizado até
> aqui, e o projeto não apresenta dado simulado como real — por isso a calibração
> definitiva dos limiares clínicos está agendada para a Fase 2, com o primeiro laticínio
> parceiro. Os números de mercado, esses sim, são oficiais (IBGE/SIDRA 2024, verificados
> na fonte).
>
> Observação técnica sobre o arquivo: no canvas original, as caixas da segunda linha de
> cada registro da página 3 estavam desenhadas sobre as da primeira linha, o que tornava o
> texto ilegível. A posição foi ajustada no PDF entregue, preservando a identidade visual e
> todos os campos do modelo.
