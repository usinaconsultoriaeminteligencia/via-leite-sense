"""
auth.py — Autenticação nativa do VIA LEITE SENSE.

Implementação própria com bcrypt + st.session_state.
Sem dependência de streamlit-authenticator — funciona em qualquer ambiente.

Ordem de precedência para credenciais:
  1. st.secrets["auth"]   — Streamlit Cloud
  2. config_auth.yaml     — desenvolvimento local
  3. _DEFAULT_USERS       — fallback embutido para demonstração

Papéis:
  admin      → acesso total
  laticinio  → analítico + fornecedores
  demo       → somente leitura
"""
from __future__ import annotations

import hashlib
import hmac
import time
from pathlib import Path
from typing import Optional

import bcrypt
import streamlit as st
import yaml
from yaml.loader import SafeLoader

# ---------------------------------------------------------------------------
# Credenciais padrão (SOMENTE para demonstração)
# Senhas em texto puro — são hasheadas em runtime na primeira execução
# NUNCA usar senhas de produção aqui
# ---------------------------------------------------------------------------
_DEFAULT_USERS: dict[str, dict] = {
    "demo": {
        "name": "Avaliador Demo",
        "email": "demo@vialeite.com.br",
        "role": "demo",
        "password_plain": "demo2025",
    },
    "laticinio": {
        "name": "Laticínio Piloto",
        "email": "operacao@vialeite.com.br",
        "role": "laticinio",
        "password_plain": "leite2025",
    },
    "admin": {
        "name": "Fagner Vieira",
        "email": "fagnerpro80@gmail.com",
        "role": "admin",
        "password_plain": "usina2025",
    },
}

# Cache em sessão para hashes gerados
_HASH_CACHE_KEY = "_vls_hash_cache"


# ---------------------------------------------------------------------------
# Carregamento de credenciais
# ---------------------------------------------------------------------------
def _carregar_usuarios() -> dict[str, dict]:
    """
    Retorna dicionário {username: {name, email, role, password_hash}}.
    """
    # 1 — Streamlit secrets
    try:
        auth_secrets = st.secrets.get("auth", {})
        usuarios_raw = auth_secrets.get("credentials", {}).get("usernames", {})
        if usuarios_raw:
            return {k: dict(v) for k, v in usuarios_raw.items()}
    except Exception:
        pass

    # 2 — config_auth.yaml local
    yaml_path = Path("config_auth.yaml")
    if yaml_path.exists():
        try:
            with yaml_path.open(encoding="utf-8") as f:
                cfg = yaml.load(f, Loader=SafeLoader) or {}
            usuarios_raw = cfg.get("credentials", {}).get("usernames", {})
            if usuarios_raw:
                return {k: dict(v) for k, v in usuarios_raw.items()}
        except Exception:
            pass

    # 3 — defaults embutidos (gera hashes em runtime)
    if _HASH_CACHE_KEY not in st.session_state:
        st.session_state[_HASH_CACHE_KEY] = {}

    cache = st.session_state[_HASH_CACHE_KEY]
    resultado: dict[str, dict] = {}
    for uname, dados in _DEFAULT_USERS.items():
        if uname not in cache:
            plain = dados["password_plain"].encode()
            cache[uname] = bcrypt.hashpw(plain, bcrypt.gensalt(rounds=12)).decode()
        resultado[uname] = {
            "name": dados["name"],
            "email": dados["email"],
            "role": dados["role"],
            "password": cache[uname],
        }
    return resultado


# ---------------------------------------------------------------------------
# Verificação de senha
# ---------------------------------------------------------------------------
def _verificar_senha(senha_plain: str, hash_armazenado: str) -> bool:
    try:
        return bcrypt.checkpw(senha_plain.encode(), hash_armazenado.encode())
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Controle de tentativas (anti-brute-force)
# ---------------------------------------------------------------------------
_TENTATIVAS_KEY = "_vls_tentativas"
_BLOQUEIO_KEY = "_vls_bloqueio_ate"
_MAX_TENTATIVAS = 5
_BLOQUEIO_SEGUNDOS = 60


def _verificar_bloqueio() -> Optional[int]:
    """Retorna segundos restantes de bloqueio, ou None se não bloqueado."""
    bloqueio_ate = st.session_state.get(_BLOQUEIO_KEY, 0)
    restante = int(bloqueio_ate - time.time())
    return restante if restante > 0 else None


def _registrar_tentativa_falha() -> None:
    tentativas = st.session_state.get(_TENTATIVAS_KEY, 0) + 1
    st.session_state[_TENTATIVAS_KEY] = tentativas
    if tentativas >= _MAX_TENTATIVAS:
        st.session_state[_BLOQUEIO_KEY] = time.time() + _BLOQUEIO_SEGUNDOS
        st.session_state[_TENTATIVAS_KEY] = 0


def _resetar_tentativas() -> None:
    st.session_state[_TENTATIVAS_KEY] = 0
    st.session_state.pop(_BLOQUEIO_KEY, None)


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------
def autenticar(username: str, password: str) -> bool:
    """
    Valida credenciais. Em caso de sucesso, popula session_state.
    Retorna True se autenticado.
    """
    bloqueio = _verificar_bloqueio()
    if bloqueio:
        st.error(f"Muitas tentativas. Aguarde {bloqueio}s para tentar novamente.")
        return False

    usuarios = _carregar_usuarios()
    usuario = usuarios.get(username.strip().lower())

    if not usuario:
        _registrar_tentativa_falha()
        return False

    hash_armazenado = usuario.get("password", "")
    if not _verificar_senha(password, hash_armazenado):
        _registrar_tentativa_falha()
        return False

    # Sucesso
    _resetar_tentativas()
    st.session_state["authentication_status"] = True
    st.session_state["username"] = username.strip().lower()
    st.session_state["name"] = usuario.get("name", username)
    st.session_state["role"] = usuario.get("role", "demo")
    return True


def logout() -> None:
    for key in ["authentication_status", "username", "name", "role"]:
        st.session_state.pop(key, None)


def esta_autenticado() -> bool:
    return st.session_state.get("authentication_status") is True


def get_papel_usuario() -> Optional[str]:
    return st.session_state.get("role")


def get_nome_usuario() -> str:
    return st.session_state.get("name", "")


# ---------------------------------------------------------------------------
# Componentes de UI
# ---------------------------------------------------------------------------
def renderizar_formulario_login(titulo: str = "Acesso à plataforma") -> None:
    """
    Renderiza o formulário de login.
    Atualiza session_state automaticamente.
    """
    st.markdown(f"#### {titulo}")
    st.caption("Entre com suas credenciais para acessar o painel.")

    with st.form("login_form", clear_on_submit=False):
        usuario = st.text_input("Usuário", placeholder="ex: demo")
        senha = st.text_input("Senha", type="password", placeholder="••••••••")
        btn = st.form_submit_button("Entrar →", use_container_width=True, type="primary")

        if btn:
            if not usuario or not senha:
                st.warning("Preencha usuário e senha.")
            elif not autenticar(usuario, senha):
                st.error("Usuário ou senha incorretos.")
            else:
                st.rerun()


def renderizar_sidebar_usuario() -> None:
    """Exibe nome, papel e botão de logout na sidebar."""
    if not esta_autenticado():
        return

    papel_label = {
        "admin": "🔑 Admin",
        "laticinio": "🏭 Laticínio",
        "demo": "👁️ Demo",
    }.get(get_papel_usuario() or "", "—")

    with st.sidebar:
        st.markdown("---")
        st.markdown(f"👤 **{get_nome_usuario()}**")
        st.caption(papel_label)
        if st.button("Sair", use_container_width=True):
            logout()
            st.rerun()


def requer_autenticacao() -> bool:
    """
    Guard de acesso. Renderiza bloqueio se não autenticado.
    Use no topo de cada página protegida.
    Retorna True se autenticado, False caso contrário (e st.stop() é chamado).
    """
    if esta_autenticado():
        return True
    st.warning("🔒 Acesso restrito. Faça login na página principal.")
    st.page_link("via_leite_app.py", label="→ Ir para o Login", icon="🏠")
    st.stop()
    return False  # nunca alcançado
