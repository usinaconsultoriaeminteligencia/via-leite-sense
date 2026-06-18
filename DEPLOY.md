# Deploy — VIA LEITE SENSE

## Opção 1 — Streamlit Community Cloud (recomendado para demo/maratona)

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
- Main file path: `via_leite_app.py`  ← **IMPORTANTE: não usar dashboard_mvp_avancado.py**

**3. Configurar Secrets**

No painel do app: Settings → Secrets. Cole o conteúdo abaixo (substitua os hashes):

```toml
[auth.credentials.usernames.demo]
name        = "Avaliador Demo"
email       = "demo@vialeite.com.br"
role        = "demo"
password    = "$2b$12$..."   # gerar com: python gerar_senhas.py demo2025

[auth.credentials.usernames.laticinio]
name        = "Laticínio Piloto"
email       = "operacao@vialeite.com.br"
role        = "laticinio"
password    = "$2b$12$..."   # gerar com: python gerar_senhas.py leite2025

[auth.credentials.usernames.admin]
name        = "Admin USINA I.A."
email       = "fagnerpro80@gmail.com"
role        = "admin"
password    = "$2b$12$..."   # gerar com: python gerar_senhas.py usina2025

[auth.cookie]
name        = "via_leite_session"
key         = "GERE_UMA_STRING_ALEATORIA_32_CHARS_AQUI"
expiry_days = 1
```

> Para gerar os hashes bcrypt: `python gerar_senhas.py`

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

# Iniciar com landing + login
streamlit run via_leite_app.py

# Ou iniciar direto no dashboard (sem autenticação obrigatória localmente)
streamlit run dashboard_mvp_avancado.py
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
- [ ] Login com usuário `demo` funcionando
- [ ] Dashboard carregando dados de demonstração
- [ ] Mapa de fazendas visível (página 9 — Painel Executivo)
- [ ] VIA LEITE EDGE com alertas ativos
- [ ] `.streamlit/secrets.toml` **NÃO** está no repositório
