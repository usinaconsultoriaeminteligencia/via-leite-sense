# Deploy — VIA LEITE SENSE

> ⚠️ **Produção atual: Vercel (frontend) + Railway (backend).** O deploy Streamlit
> abaixo é **legado** — o app `via-leite-sense.streamlit.app` foi descomissionado e
> hoje redireciona para a Vercel (ver `via_leite_app.py`).
>
> **Publicar produção (via CLI, enquanto o auto-deploy GitHub não estiver conectado):**
> - **Frontend (Vercel):** `vercel --cwd frontend --prod --yes`
> - **Backend (Railway):** `railway up --ci` (a partir da raiz do repo; projeto já linkado)
>
> URLs: frontend `https://via-leite-sense.vercel.app` ·
> API `https://via-leite-sense-api-production.up.railway.app`
> Detalhes do backend em `backend/README.md`; do frontend em `frontend/README.md`.

---

## 🔒 Autenticação da API (obrigatória desde 06/08/2026)

Até 06/08/2026 os 30 endpoints da API estavam abertos ao público, incluindo os
11 de escrita. Hoje **toda a rota exige a chave `X-API-Key`**, exceto `/health`.

O caminho do pedido em produção é:

```
Browser ──/api/…──► Vercel (frontend/api/[...path].js) ──X-API-Key──► Railway
                    guarda a chave
```

O SPA é estático e **não pode** guardar a chave: qualquer valor que ele carregue
fica visível no código-fonte da página. É por isso que o proxy existe e por isso
que `frontend/index.html` aponta para `/api` e não para a URL da Railway.

### Variáveis a definir

| Onde | Variável | Valor |
|------|----------|-------|
| Railway | `VIA_LEITE_API_KEYS` | chaves válidas, separadas por vírgula |
| Railway | `VIA_LEITE_ENV` | `production` (retira localhost do CORS) |
| Vercel | `VIA_LEITE_API_URL` | `https://via-leite-sense-api-production.up.railway.app` |
| Vercel | `VIA_LEITE_API_KEY` | **uma** das chaves acima |

Opcional: `VIA_LEITE_PUBLIC_DOCS=1` reabre `/docs` e `/openapi.json`, fechados
por omissão porque o esquema descreve os endpoints de escrita e os campos de
dados pessoais.

### Gerar uma chave

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Rodar a chave sem downtime

`VIA_LEITE_API_KEYS` aceita várias porque a rotação precisa de uma janela em que
as duas valem:

1. Railway: `VIA_LEITE_API_KEYS = <antiga>,<nova>` — as duas passam a valer.
2. Vercel: `VIA_LEITE_API_KEY = <nova>` — redeploy do frontend.
3. Confirmar que o site funciona.
4. Railway: `VIA_LEITE_API_KEYS = <nova>` — a antiga morre.

### Se faltar configuração

O sistema **falha fechado**, nunca aberto:

- Backend sem `VIA_LEITE_API_KEYS` → `503` em toda a rota não pública.
- Proxy sem `VIA_LEITE_API_URL`/`VIA_LEITE_API_KEY` → `503` com a mensagem do
  que falta.

Nunca há chave por omissão embutida no código — um valor "só para
desenvolvimento" é exactamente o que acaba em produção.

### Desenvolvimento local

```bash
# terminal 1 — API
VIA_LEITE_API_KEYS=chave-local uvicorn backend.app:app --reload

# terminal 2 — frontend
# em frontend/index.html, trocar a meta para http://127.0.0.1:8000
python -m http.server 8600 --directory frontend
```

Sem o proxy, o browser precisa de enviar a chave. Para desenvolvimento, o mais
simples é correr o `vercel dev` a partir de `frontend/`, que levanta o proxy
localmente com as mesmas variáveis.

---

## Opção 1 — Streamlit Community Cloud (LEGADO — não é mais a produção)

### Pré-requisitos
- Conta GitHub com o repositório `via-leite-sense` criado
- Conta em [share.streamlit.io](https://share.streamlit.io) (login com GitHub)

### Passo a passo

**1. Commitar e subir o projeto**
```bash
git init
git add .
git commit -m "feat: via leite sense sprint1 - login + landing + deploy"
git remote add origin https://github.com/SEU_USUARIO/via-leite-sense.git
git push -u origin master
```

**2. Criar o app no Streamlit Cloud**
- Acesse share.streamlit.io → "New app"
- Repositório: `SEU_USUARIO/via-leite-sense`
- Branch: `master`
- Main file path: `via_leite_app.py` (página de redirect — é a única que resta)

**3. Secrets — não há**

O app Streamlit foi reduzido a um redirect em 25/08/2026: sem login, sem dados,
sem `secrets.toml`. A autenticação vive na API (`X-API-Key`, `backend/security.py`).

**4. Aguardar o build**
- O Streamlit Cloud instala as dependências de `requirements.txt` automaticamente
- Tempo típico: 2–5 minutos no primeiro deploy

**5. URL gerada**
```
https://SEU_USUARIO-via-leite-sense-via-leite-app-HASH.streamlit.app
```
Você pode configurar um nome customizado nas configurações do app.

---

## Opção 2 — Execução local (desenvolvimento)

```powershell
# Instalar dependências
pip install -r requirements.txt

# Gerar dados sintéticos (se ainda não existirem)
python gerador_leite_sintetico.py --output-dir dados_teste

# Treinar modelo
python treino_mvp_avancado.py

# Subir a API localmente (é a aplicação de facto)
uvicorn backend.app:app --reload

# Servir o frontend SPA contra a API local
cd frontend && python -m http.server 3000
```

---

## Variáveis de ambiente (multi-tenant)

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `MVP_DATA_DIR` | `dados_teste` | Pasta com os CSVs do cliente |
| `MVP_ARTEFATOS_DIR` | `artefatos_teste` | Pasta com modelo e métricas |
| `IOT_SIMULATION_MODE` | `true` | Modo IoT simulado |
| `IOT_PROVIDER` | `simulated` | Provider IoT ativo |

---

## Checklist pré-apresentação

- [ ] Deploy funcionando em URL pública
- [ ] Redirect do Streamlit Cloud levando à Vercel (QR codes do pitch)
- [ ] VIA LEITE EDGE com alertas ativos
- [ ] Nenhuma rota da API responde sem `X-API-Key` (exceto `/health`)
- [ ] Relatório em PDF: `GET /suppliers/{id}/report.pdf` devolvendo `%PDF-`
