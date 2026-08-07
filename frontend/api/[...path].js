/**
 * VIA LEITE SENSE — Proxy da API (Vercel Serverless Function)
 *
 * Porquê existir
 * --------------
 * O frontend é um SPA estático: qualquer chave que ele carregue fica visível
 * no "ver código-fonte" do browser. Esta função corre no servidor da Vercel,
 * guarda a chave e é o único ponto que fala com a Railway.
 *
 *   Browser  →  /api/...  (esta função, mesma origem)  →  Railway  ─X-API-Key─┐
 *                                                                            │
 *   O browser nunca vê a chave. ───────────────────────────────────────────────┘
 *
 * Como a mesma origem serve o SPA e o /api, deixa de haver pedido cross-origin
 * e o CORS do backend passa a poder ficar vazio em produção.
 *
 * Variáveis de ambiente (definir no painel da Vercel, nunca no repositório):
 *   VIA_LEITE_API_URL   base da API na Railway, ex.: https://xxx.up.railway.app
 *   VIA_LEITE_API_KEY   uma das chaves listadas em VIA_LEITE_API_KEYS no backend
 *
 * Autor: USINA I.A. / Fagner Vieira
 */

// Cabeçalhos que não devem ser reenviados para a Railway: dizem respeito à
// ligação browser→Vercel e não à ligação Vercel→Railway. Reenviar `host`
// quebra o roteamento; reenviar `cookie` vazaria sessão para outro domínio.
const HEADERS_A_REMOVER = new Set([
  "host",
  "connection",
  "content-length",
  "accept-encoding",
  "cookie",
  "x-api-key", // nunca aceitar chave vinda do browser: ela é decidida aqui
]);

function corpoDoPedido(req) {
  if (req.body === undefined || req.body === null) return undefined;
  if (typeof req.body === "string") return req.body;
  if (Buffer.isBuffer(req.body)) return req.body;
  return JSON.stringify(req.body);
}

export default async function handler(req, res) {
  const base = process.env.VIA_LEITE_API_URL;
  const chave = process.env.VIA_LEITE_API_KEY;

  // Falha fechada e explícita: sem configuração o proxy não tenta adivinhar.
  if (!base || !chave) {
    res.status(503).json({
      detail:
        "Proxy por configurar: defina VIA_LEITE_API_URL e VIA_LEITE_API_KEY no ambiente da Vercel.",
    });
    return;
  }

  // `/api/suppliers/19?x=1` → `/suppliers/19?x=1`
  //
  // O caminho sai do `req.url` e não de `req.query.path`: o parâmetro do
  // catch-all chegou vazio em produção e todo o pedido foi parar à raiz da
  // Railway, que respondeu 404 a tudo. O `req.url` é o que o runtime entrega
  // sempre, sem depender da convenção de nomes do ficheiro.
  const url = req.url || "";
  const posicaoConsulta = url.indexOf("?");
  const semConsulta = posicaoConsulta === -1 ? url : url.slice(0, posicaoConsulta);
  const consulta = posicaoConsulta === -1 ? "" : url.slice(posicaoConsulta);
  const caminho = semConsulta.replace(/^\/api\/?/, "").replace(/^\/+/, "");
  const destino = `${base.replace(/\/+$/, "")}/${caminho}${consulta}`;

  const cabecalhos = {};
  for (const [nome, valor] of Object.entries(req.headers)) {
    if (!HEADERS_A_REMOVER.has(nome.toLowerCase())) {
      cabecalhos[nome] = valor;
    }
  }
  cabecalhos["X-API-Key"] = chave;

  try {
    const resposta = await fetch(destino, {
      method: req.method,
      headers: cabecalhos,
      body: ["GET", "HEAD"].includes(req.method) ? undefined : corpoDoPedido(req),
    });

    res.status(resposta.status);
    const tipo = resposta.headers.get("content-type");
    if (tipo) res.setHeader("Content-Type", tipo);

    // 204 tem de sair sem corpo — os DELETE da API devolvem-no.
    if (resposta.status === 204) {
      res.end();
      return;
    }
    res.send(Buffer.from(await resposta.arrayBuffer()));
  } catch (erro) {
    // A mensagem do erro pode conter o URL interno; não vai para o browser.
    console.error("Falha ao contactar a API:", erro);
    res.status(502).json({ detail: "Falha ao contactar a API." });
  }
}
