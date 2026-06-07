"""
gerar_senhas.py — Utilitário para gerar hashes bcrypt para secrets.toml.

Uso:
    python gerar_senhas.py
    python gerar_senhas.py minha_senha_aqui
"""
from __future__ import annotations

import sys
import bcrypt


def gerar_hash(senha: str) -> str:
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt(rounds=12)).decode()


def main() -> None:
    senhas = sys.argv[1:] if len(sys.argv) > 1 else ["demo2025", "leite2025", "usina2025"]

    print("\n=== VIA LEITE SENSE — Gerador de Hashes Bcrypt ===\n")
    for senha in senhas:
        h = gerar_hash(senha)
        print(f"Senha: {senha!r}")
        print(f"Hash:  {h}")
        print()


if __name__ == "__main__":
    main()
