const seedSuppliers = [
  {
    id: "19",
    nome: "Fazenda Santa Helena",
    documento: "12.345.678/0001-90",
    municipio: "Serranópolis",
    polo: "Jataí",
    laticinio: "Laticínio 4",
    sistema: "Pasto",
    capacidadeLitros: 420,
    historicoMeses: 38,
    qualidade: "CCS acima da meta em ciclos recentes",
    operacionais: "Ordenha mecânica, tanque individual e coleta diária",
    logisticos: "Acesso rural sensível à chuva",
    financeiros: "Contrato com bonificação por volume",
    litrosDia: 372.35,
    risco: 76.2,
    classeRisco: "Alto",
    scoreVolume: 100,
    scoreQualidade: 49.4,
    scoreLogistica: 88.8,
    scoreContinuidade: 57.7,
    tendenciaPct: -8.62,
    descartePct: 2.0,
    ccs: 615.8,
    cbt: 137.41,
    recomendacao: "Priorizar visita técnica, proteger volume contratado e abrir plano de qualidade."
  },
  {
    id: "5",
    nome: "Sítio Boa Vista",
    documento: "987.654.321-00",
    municipio: "Jataí",
    polo: "Jataí",
    laticinio: "Laticínio 2",
    sistema: "Pasto",
    capacidadeLitros: 980,
    historicoMeses: 64,
    qualidade: "CBT em elevação e descarte recorrente",
    operacionais: "Ordenha canalizada, resfriamento próprio",
    logisticos: "Rota consolidada, sem restrição grave",
    financeiros: "Preço base com bônus trimestral",
    litrosDia: 953.68,
    risco: 74.3,
    classeRisco: "Médio",
    scoreVolume: 100,
    scoreQualidade: 71.2,
    scoreLogistica: 56.1,
    scoreContinuidade: 45,
    tendenciaPct: -15.78,
    descartePct: 1.88,
    ccs: 647.79,
    cbt: 231.46,
    recomendacao: "Proteger volume com contato comercial e revisar manejo de ordenha."
  },
  {
    id: "14",
    nome: "Fazenda Limoeiro",
    documento: "23.456.789/0001-10",
    municipio: "Serranópolis",
    polo: "Jataí",
    laticinio: "Laticínio 1",
    sistema: "Pasto",
    capacidadeLitros: 360,
    historicoMeses: 22,
    qualidade: "Qualidade estável, baixa escala produtiva",
    operacionais: "Ordenha balde ao pé, coleta alternada",
    logisticos: "Estrada não pavimentada em trecho crítico",
    financeiros: "Pagamento mensal padrão",
    litrosDia: 319.23,
    risco: 70.5,
    classeRisco: "Médio",
    scoreVolume: 52.3,
    scoreQualidade: 86.4,
    scoreLogistica: 84.5,
    scoreContinuidade: 62.4,
    tendenciaPct: -0.1,
    descartePct: 1.98,
    ccs: 446.9,
    cbt: 222.12,
    recomendacao: "Abrir plano logístico e avaliar janela de coleta em dias de chuva."
  },
  {
    id: "7",
    nome: "Fazenda Rio Claro",
    documento: "34.567.890/0001-20",
    municipio: "Santo Antônio da Barra",
    polo: "Rio Verde",
    laticinio: "Laticínio 1",
    sistema: "Pasto",
    capacidadeLitros: 560,
    historicoMeses: 51,
    qualidade: "CCS dentro do esperado",
    operacionais: "Ordenha mecânica e tanque compartilhado",
    logisticos: "Rota longa com custo alto por litro",
    financeiros: "Margem sob acompanhamento",
    litrosDia: 507.98,
    risco: 59.4,
    classeRisco: "Médio",
    scoreVolume: 51.5,
    scoreQualidade: 56.9,
    scoreLogistica: 91.6,
    scoreContinuidade: 40.2,
    tendenciaPct: 2.82,
    descartePct: 2.32,
    ccs: 524.48,
    cbt: 142.18,
    recomendacao: "Revisar custo logístico e consolidar coleta com fornecedores próximos."
  },
  {
    id: "13",
    nome: "Agropecuária Santa Rita",
    documento: "45.678.901/0001-30",
    municipio: "Jataí",
    polo: "Jataí",
    laticinio: "Laticínio 4",
    sistema: "Pasto",
    capacidadeLitros: 1850,
    historicoMeses: 80,
    qualidade: "Volume alto, qualidade oscilante",
    operacionais: "Ordenha mecânica, equipe própria",
    logisticos: "Acesso bom, rota prioritária",
    financeiros: "Contrato estratégico",
    litrosDia: 1780.26,
    risco: 56.7,
    classeRisco: "Médio",
    scoreVolume: 65.1,
    scoreQualidade: 47.1,
    scoreLogistica: 38.9,
    scoreContinuidade: 79.8,
    tendenciaPct: 0.01,
    descartePct: 2,
    ccs: 490.82,
    cbt: 114.64,
    recomendacao: "Manter relacionamento executivo e plano preventivo de qualidade."
  },
  {
    id: "21",
    nome: "Sítio Três Nascentes",
    documento: "56.789.012/0001-40",
    municipio: "Santo Antônio da Barra",
    polo: "Rio Verde",
    laticinio: "Laticínio 1",
    sistema: "Pasto",
    capacidadeLitros: 760,
    historicoMeses: 44,
    qualidade: "Indicadores controlados",
    operacionais: "Rotina operacional estável",
    logisticos: "Rota com baixo atraso",
    financeiros: "Sem pendências",
    litrosDia: 733.92,
    risco: 49.2,
    classeRisco: "Baixo",
    scoreVolume: 21.1,
    scoreQualidade: 58.9,
    scoreLogistica: 92.4,
    scoreContinuidade: 37.6,
    tendenciaPct: 14.29,
    descartePct: 2.29,
    ccs: 423.22,
    cbt: 159.89,
    recomendacao: "Manter acompanhamento regular e avaliar expansão de volume."
  }
];

const storageKeys = {
  suppliers: "via_leite_suppliers",
  events: "via_leite_events",
  plans: "via_leite_action_plans"
};

const API_BASE = window.VIA_LEITE_API_BASE || "http://127.0.0.1:8000";

const state = {
  route: window.location.hash.replace("#", "") || "comando",
  selectedSupplier: "19",
  managementTab: "fornecedores",
  editingSupplierId: null,
  editingPlanId: null,
  onboardingResult: null,
  apiOnline: false,
  apiData: {
    portfolio: null,
    riskDistribution: null,
    qualitySummary: null,
    actionPlans: null,
    actionPlanEffectiveness: null,
    impact: null,
    trainingSummary: null
  },
  scenario: {
    qualidade: 18,
    logistica: 12,
    clima: -8
  }
};

const money = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL", minimumFractionDigits: 2, maximumFractionDigits: 2 });
const number = new Intl.NumberFormat("pt-BR", { minimumFractionDigits: 0, maximumFractionDigits: 0 });
const decimal = new Intl.NumberFormat("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const percent = new Intl.NumberFormat("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => Array.from(document.querySelectorAll(selector));

let suppliers = loadSuppliers();
let events = loadEvents();
let actionPlans = loadActionPlans();

async function init() {
  hydrateFilterOptions();
  bindEvents();
  updateApiStatus(false, "Conectando à API...");
  setRoute(state.route);
  render();
  await hydrateFromApi();
}

async function hydrateFromApi() {
  try {
    const apiSuppliers = await apiFetch("/suppliers");
    const apiEvents = await apiFetch("/management-events");
    const apiActionPlans = await apiFetch("/action-plans");
    const apiActionPlanEffectiveness = await apiFetch("/action-plans/effectiveness");
    const portfolio = await apiFetch("/portfolio");
    const riskDistribution = await apiFetch("/risk-distribution");
    const qualitySummary = await apiFetch("/quality-summary");
    const impact = await apiFetch("/impact");
    const trainingSummary = await apiFetch("/training-base/summary");
    await syncLocalDataToApi(apiSuppliers, apiEvents, apiActionPlans);
    if (Array.isArray(apiSuppliers) && apiSuppliers.length) {
      suppliers = apiSuppliers;
    }
    if (Array.isArray(apiEvents)) {
      events = apiEvents;
    }
    if (Array.isArray(apiActionPlans)) {
      actionPlans = apiActionPlans;
    }
    state.apiData = {
      portfolio,
      riskDistribution,
      qualitySummary,
      actionPlans: apiActionPlans,
      actionPlanEffectiveness: apiActionPlanEffectiveness,
      impact,
      trainingSummary
    };
    state.apiOnline = true;
    updateApiStatus(true);
    localStorage.removeItem(storageKeys.suppliers);
    localStorage.removeItem(storageKeys.events);
    localStorage.removeItem(storageKeys.plans);
    hydrateFilterOptions();
    render();
  } catch (error) {
    state.apiOnline = false;
    updateApiStatus(false, `Modo offline (${error.message})`);
    console.info("API indisponível; mantendo dados locais da demo.", error);
  }
}

async function refreshApiData() {
  if (!state.apiOnline) return;
  try {
    const portfolio = await apiFetch("/portfolio");
    const riskDistribution = await apiFetch("/risk-distribution");
    const qualitySummary = await apiFetch("/quality-summary");
    const apiActionPlans = await apiFetch("/action-plans");
    const apiActionPlanEffectiveness = await apiFetch("/action-plans/effectiveness");
    const impact = await apiFetch("/impact");
    const apiEvents = await apiFetch("/management-events");
    state.apiData = {
      ...state.apiData,
      portfolio,
      riskDistribution,
      qualitySummary,
      actionPlans: apiActionPlans,
      actionPlanEffectiveness: apiActionPlanEffectiveness,
      impact
    };
    events = Array.isArray(apiEvents) ? apiEvents : events;
    actionPlans = Array.isArray(apiActionPlans) ? apiActionPlans : actionPlans;
  } catch (error) {
    state.apiOnline = false;
    updateApiStatus(false);
    console.info("API indisponível durante atualização de dados.", error);
  }
}

async function syncLocalDataToApi(apiSuppliers, apiEvents, apiActionPlans) {
  const localSuppliers = readLocalArray(storageKeys.suppliers);
  const localEvents = readLocalArray(storageKeys.events);
  const localPlans = readLocalArray(storageKeys.plans);
  const apiSupplierIds = new Set((apiSuppliers || []).map((item) => String(item.id)));
  const apiEventIds = new Set((apiEvents || []).map((item) => String(item.id)));
  const apiPlanIds = new Set((apiActionPlans || []).map((item) => String(item.id)));

  const suppliersToSync = localSuppliers.filter((item) => item?.id && !apiSupplierIds.has(String(item.id)) && !isSeedSupplier(item));
  const eventsToSync = localEvents.filter((item) => item?.id && !apiEventIds.has(String(item.id)));
  const plansToSync = localPlans.filter((item) => item?.id && !apiPlanIds.has(String(item.id)));

  for (const supplier of suppliersToSync) {
    await apiFetch("/suppliers", { method: "POST", body: JSON.stringify(supplier) });
  }
  for (const event of eventsToSync) {
    await apiFetch("/management-events", { method: "POST", body: JSON.stringify(event) });
  }
  for (const plan of plansToSync) {
    await apiFetch("/action-plans", { method: "POST", body: JSON.stringify(plan) });
  }
}

function readLocalArray(key) {
  try {
    const parsed = JSON.parse(localStorage.getItem(key) || "[]");
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function isSeedSupplier(candidate) {
  return seedSuppliers.some((item) => String(item.id) === String(candidate.id) && item.nome === candidate.nome);
}

function updateApiStatus(online, label) {
  const status = $("#apiStatus");
  if (!status) return;
  status.classList.toggle("offline", !online);
  status.querySelector(".status-dot").classList.toggle("offline", !online);
  status.querySelector(".status-copy").firstChild.textContent = label || (online ? "Conectado à API" : "Modo offline");
}

async function apiFetch(path, options = {}) {
  const headers = {
    ...(options.body ? { "Content-Type": "application/json" } : {}),
    ...(options.headers || {})
  };
  const response = await fetch(`${API_BASE}${path}`, {
    headers,
    ...options
  });
  if (!response.ok) {
    throw new Error(`Falha na API: ${response.status}`);
  }
  if (response.status === 204) {
    return null;
  }
  return response.json();
}

function loadSuppliers() {
  const raw = localStorage.getItem(storageKeys.suppliers);
  if (!raw) return [...seedSuppliers];
  try {
    return JSON.parse(raw);
  } catch {
    return [...seedSuppliers];
  }
}

function loadEvents() {
  const raw = localStorage.getItem(storageKeys.events);
  if (!raw) return [];
  try {
    return JSON.parse(raw);
  } catch {
    return [];
  }
}

function loadActionPlans() {
  const raw = localStorage.getItem(storageKeys.plans);
  if (!raw) return buildActionPlans(suppliers);
  try {
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : buildActionPlans(suppliers);
  } catch {
    return buildActionPlans(suppliers);
  }
}

function persist() {
  localStorage.setItem(storageKeys.suppliers, JSON.stringify(suppliers));
  localStorage.setItem(storageKeys.events, JSON.stringify(events));
  localStorage.setItem(storageKeys.plans, JSON.stringify(actionPlans));
}

function hydrateFilterOptions() {
  const dairy = $("#dairyFilter");
  const region = $("#regionFilter");
  dairy.querySelectorAll("option:not(:first-child)").forEach((option) => option.remove());
  region.querySelectorAll("option:not(:first-child)").forEach((option) => option.remove());

  unique(suppliers.map((item) => item.laticinio)).forEach((item) => {
    dairy.insertAdjacentHTML("beforeend", `<option value="${item}">${item}</option>`);
  });
  unique(suppliers.map((item) => item.polo)).forEach((item) => {
    region.insertAdjacentHTML("beforeend", `<option value="${item}">${item}</option>`);
  });
}

function bindEvents() {
  $$(".nav-link").forEach((link) => {
    link.addEventListener("click", (event) => {
      event.preventDefault();
      window.location.hash = link.dataset.route;
      setRoute(link.dataset.route);
    });
  });

  ["riskFilter", "dairyFilter", "regionFilter", "searchFilter"].forEach((id) => {
    $(`#${id}`).addEventListener("input", render);
  });

  $("#resetFilters").addEventListener("click", () => {
    $("#riskFilter").value = "Todos";
    $("#dairyFilter").value = "Todos";
    $("#regionFilter").value = "Todos";
    $("#searchFilter").value = "";
    render();
  });

  $("#openManagement").addEventListener("click", () => {
    state.managementTab = "fornecedores";
    window.location.hash = "gestao";
    setRoute("gestao");
  });

  window.addEventListener("hashchange", () => {
    setRoute(window.location.hash.replace("#", "") || "comando");
  });
}

function setRoute(route) {
  state.route = route;
  $$(".route").forEach((section) => section.classList.toggle("active", section.dataset.view === route));
  $$(".nav-link").forEach((link) => link.classList.toggle("active", link.dataset.route === route));
  render();
}

function getFilteredSuppliers() {
  const risk = $("#riskFilter").value;
  const dairy = $("#dairyFilter").value;
  const region = $("#regionFilter").value;
  const search = $("#searchFilter").value.trim().toLowerCase();

  return suppliers.filter((item) => {
    const matchRisk = risk === "Todos" || item.classeRisco === risk;
    const matchDairy = dairy === "Todos" || item.laticinio === dairy;
    const matchRegion = region === "Todos" || item.polo === region;
    const blob = `${item.id} ${item.nome} ${item.municipio} ${item.polo} ${item.sistema}`.toLowerCase();
    const matchSearch = !search || blob.includes(search);
    return matchRisk && matchDairy && matchRegion && matchSearch;
  });
}

function shouldUseApiAggregates() {
  return state.apiOnline
    && $("#riskFilter")?.value === "Todos"
    && $("#dairyFilter")?.value === "Todos"
    && $("#regionFilter")?.value === "Todos"
    && !$("#searchFilter")?.value.trim();
}

function render() {
  const data = getFilteredSuppliers();
  renderCommand(data);
  renderPortfolio(data);
  renderSupplier360(data);
  renderManagement(data);
  renderPlans(data);
  renderImpact(data);
}

function renderCommand(data) {
  const portfolio = shouldUseApiAggregates() ? state.apiData.portfolio : null;
  const quality = shouldUseApiAggregates() ? state.apiData.qualitySummary : null;
  const training = shouldUseApiAggregates() ? state.apiData.trainingSummary : null;
  const riskVolume = portfolio?.litrosRisco ?? sum(data.filter((item) => ["Alto", "Médio"].includes(item.classeRisco)), "litrosDia");
  const avgRisk = portfolio?.scoreMedio ?? avg(data, "risco");
  const critical = portfolio?.criticos ?? data.filter((item) => item.classeRisco === "Alto").length;
  const attention = portfolio?.atencao ?? data.filter((item) => item.classeRisco === "Médio").length;
  const eventImpact = portfolio?.impactoGerencialLitros ?? sum(events, "impactoLitros");
  const topRisk = data.slice().sort((a, b) => b.risco - a.risco)[0];

  $("#comando").innerHTML = `
    <div class="kpi-grid">
      ${kpi("Litros por dia em risco", `${number.format(riskVolume)} L`, "Fornecedores em risco alto ou médio")}
      ${kpi("Fornecedores críticos", critical, `${attention} em atenção`)}
      ${kpi("Score médio de risco", decimal.format(avgRisk), "Carteira filtrada")}
      ${kpi("Impacto gerencial", `${number.format(eventImpact)} L`, "Eventos registrados pelo gestor")}
    </div>

    <div class="grid-2">
      <section class="panel">
        <h2>Prioridade da semana</h2>
        ${supplierTable(data.slice().sort((a, b) => b.risco - a.risco).slice(0, 6), false)}
      </section>
      <section class="panel intelligence-panel">
        <div>
          <p class="eyebrow">Leitura operacional</p>
          <h2>Decisão recomendada para hoje</h2>
          <p class="decision-copy">
            Priorizar ${topRisk?.nome || "fornecedores críticos"} e proteger ${number.format(riskVolume)} L/dia com ações de campo, qualidade e logística.
          </p>
        </div>
        <div class="insight-grid">
          ${insightItem("Carteira monitorada", `${number.format(portfolio?.fornecedores ?? suppliers.length)} fornecedores`)}
          ${insightItem("Base analítica", `${number.format(training?.linhas ?? 0)} registros`)}
          ${insightItem("Qualidade crítica", `${number.format(quality?.fornecedoresQualidadeCritica ?? data.filter((item) => item.scoreQualidade >= 70).length)} fornecedores`)}
          ${insightItem("Eventos rastreados", `${number.format(events.length)} lançamentos`)}
        </div>
        <div class="signal-list">
          <span>Volume em risco</span>
          <span>CCS e CBT</span>
          <span>Rota e acesso</span>
          <span>Impacto financeiro</span>
        </div>
      </section>
    </div>

    <div class="grid-3" style="margin-top: 18px;">
      <section class="panel">
        <h2>Distribuição de risco</h2>
        ${riskBars(data)}
      </section>
      <section class="panel">
        <h2>Qualidade</h2>
        ${barRow("CCS média", quality?.ccsMedia ?? avg(data, "ccs"), 800)}
        ${barRow("CBT média", quality?.cbtMedia ?? avg(data, "cbt"), 300)}
        ${barRow("Descarte", quality?.descartePct ?? avg(data, "descartePct"), 5)}
      </section>
      <section class="panel">
        <h2>Rastreabilidade</h2>
        <p class="muted">Fornecedores cadastrados, variáveis gerenciais e eventos ficam disponíveis para decisão e futura integração com DuckDB/API.</p>
        <p><strong>${number.format(suppliers.length)}</strong> fornecedores na carteira</p>
        <p><strong>${number.format(events.length)}</strong> lançamentos gerenciais</p>
      </section>
    </div>
  `;
}

function renderPortfolio(data) {
  $("#carteira").innerHTML = `
    <section class="panel">
      <h2>Carteira de fornecedores</h2>
      <p class="muted">Ranking por risco composto de volume, qualidade, logística, continuidade e eventos gerenciais.</p>
      ${supplierTable(data.slice().sort((a, b) => b.risco - a.risco), true)}
    </section>
  `;
}

function renderSupplier360(data) {
  const list = data.length ? data : suppliers;
  if (!list.some((item) => item.id === state.selectedSupplier)) {
    state.selectedSupplier = list[0]?.id || "";
  }
  const supplier = list.find((item) => item.id === state.selectedSupplier) || suppliers[0];
  const supplierEvents = events.filter((item) => item.idFornecedor === supplier.id);

  $("#fornecedor-360").innerHTML = `
    <div class="supplier-layout">
      <section class="panel">
        <h2>Selecionar fornecedor</h2>
        <div class="supplier-list">
          ${list.map((item) => `
            <button class="supplier-button ${item.id === supplier.id ? "active" : ""}" data-supplier="${item.id}">
              <strong>${item.nome}</strong>
              <small>${item.municipio} - ${item.polo} - ${item.laticinio}</small>
              <span class="risk-pill risk-${item.classeRisco}">${item.classeRisco}</span>
            </button>
          `).join("")}
        </div>
      </section>

      <section class="panel">
        <h2>${supplier.nome}</h2>
        <p class="muted">${supplier.municipio} - ${supplier.sistema} - ${supplier.laticinio}</p>
        <div class="score-grid">
          ${scoreCard("Risco", supplier.risco)}
          ${scoreCard("Volume", supplier.scoreVolume)}
          ${scoreCard("Qualidade", supplier.scoreQualidade)}
          ${scoreCard("Logística", supplier.scoreLogistica)}
        </div>
        <div class="detail-grid">
          ${detail("Capacidade produtiva", `${number.format(supplier.capacidadeLitros)} L`)}
          ${detail("Histórico", `${number.format(supplier.historicoMeses)} meses`)}
          ${detail("Tendência", `${percent.format(supplier.tendenciaPct)}%`)}
          ${detail("CCS média", number.format(supplier.ccs))}
          ${detail("CBT média", number.format(supplier.cbt))}
          ${detail("Eventos", number.format(supplierEvents.length))}
        </div>
        <h3 style="margin-top: 18px;">Recomendação</h3>
        <p>${supplier.recomendacao}</p>
        <h3>Variáveis gerenciais</h3>
        <div class="detail-grid">
          ${detail("Qualidade", supplier.qualidade)}
          ${detail("Operacionais", supplier.operacionais)}
          ${detail("Logísticas", supplier.logisticos)}
          ${detail("Financeiras", supplier.financeiros)}
        </div>
      </section>
    </div>
  `;

  $$("#fornecedor-360 [data-supplier]").forEach((button) => {
    button.addEventListener("click", () => {
      state.selectedSupplier = button.dataset.supplier;
      renderSupplier360(getFilteredSuppliers());
    });
  });
}

function renderManagement() {
  $("#gestao").innerHTML = `
    <div class="tabs">
      <button class="tab-button ${state.managementTab === "fornecedores" ? "active" : ""}" data-management-tab="fornecedores">Cadastro de fornecedores</button>
      <button class="tab-button ${state.managementTab === "eventos" ? "active" : ""}" data-management-tab="eventos">Lançamentos gerenciais</button>
      <button class="tab-button ${state.managementTab === "onboarding" ? "active" : ""}" data-management-tab="onboarding">Onboarding</button>
    </div>
    ${state.managementTab === "fornecedores" ? supplierForm() : state.managementTab === "eventos" ? eventForm() : onboardingForm()}
  `;

  $$("[data-management-tab]").forEach((button) => {
    button.addEventListener("click", () => {
      state.managementTab = button.dataset.managementTab;
      renderManagement();
    });
  });

  if (state.managementTab === "fornecedores") bindSupplierForm();
  if (state.managementTab === "eventos") bindEventForm();
  if (state.managementTab === "onboarding") bindOnboardingForm();
  bindTableActions();
}

function supplierForm() {
  const editing = suppliers.find((item) => item.id === state.editingSupplierId) || null;
  return `
    <div class="management-layout">
      <section class="panel">
        <h2>${editing ? "Editar fornecedor" : "Dados cadastrais"}</h2>
        <form id="supplierForm" class="form-grid">
          ${input("id", "Identificação", "", "Ex.: 1024", editing?.id || "")}
          ${input("nome", "Nome ou razão social", "", "Ex.: Fazenda Limoeiro", editing?.nome || "")}
          ${input("documento", "CPF ou CNPJ", "", "Ex.: 12.345.678/0001-90", editing?.documento || "")}
          ${input("municipio", "Município", "", "Ex.: Rio Verde", editing?.municipio || "")}
          ${input("polo", "Polo", "", "Ex.: Rio Verde", editing?.polo || "")}
          ${input("laticinio", "Laticínio", "", "Ex.: Laticínio 1", editing?.laticinio || "")}
          ${input("sistema", "Sistema produtivo", "", "Ex.: Pasto", editing?.sistema || "")}
          ${input("capacidadeLitros", "Capacidade produtiva (L)", "number", "0", editing?.capacidadeLitros || "")}
          ${input("historicoMeses", "Histórico de fornecimento (meses)", "number", "0", editing?.historicoMeses || "")}
          ${input("risco", "Score de risco", "number", "0", editing?.risco || "")}
          ${textarea("qualidade", "Indicadores de qualidade", editing?.qualidade || "")}
          ${textarea("operacionais", "Variáveis operacionais", editing?.operacionais || "")}
          ${textarea("logisticos", "Variáveis logísticas", editing?.logisticos || "")}
          ${textarea("financeiros", "Variáveis financeiras", editing?.financeiros || "")}
          <div class="wide form-actions">
            <button class="primary-button" type="submit">${editing ? "Atualizar fornecedor" : "Salvar fornecedor"}</button>
            <button class="ghost-button" type="button" id="resetSupplierForm">Limpar formulário</button>
          </div>
        </form>
      </section>
      <section class="panel">
        <h2>Fornecedores cadastrados</h2>
        ${supplierTable(suppliers.slice().sort((a, b) => Number(a.id) - Number(b.id)), false, true)}
      </section>
    </div>
  `;
}

function eventForm() {
  return `
    <div class="management-layout">
      <section class="panel">
        <h2>Lançamento gerencial</h2>
        <form id="eventForm" class="form-grid">
          <label>
            Fornecedor
            <select name="idFornecedor" required>
              ${suppliers.map((item) => `<option value="${item.id}">${item.nome} - ${item.laticinio}</option>`).join("")}
            </select>
          </label>
          ${input("data", "Data de referência", "date", "")}
          <label>
            Categoria
            <select name="categoria" required>
              <option>Custo extra</option>
              <option>Interrupção operacional</option>
              <option>Penalidade de qualidade</option>
              <option>Bonificação</option>
              <option>Restrição logística</option>
              <option>Ajuste financeiro</option>
            </select>
          </label>
          ${input("impactoLitros", "Impacto em litros", "number", "0")}
          ${input("valorFinanceiro", "Valor financeiro (R$)", "number", "0")}
          ${input("responsavel", "Responsável", "", "Gestor")}
          ${textarea("descricao", "Descrição detalhada")}
          <div class="wide form-actions">
            <button class="primary-button" type="submit">Salvar lançamento</button>
            <button class="danger-button" type="button" id="clearEvents">Limpar lançamentos</button>
          </div>
        </form>
      </section>
      <section class="panel">
        <h2>Histórico gerencial</h2>
        ${eventsTable()}
      </section>
    </div>
  `;
}

function onboardingForm() {
  return `
    <div class="management-layout">
      <section class="panel">
        <h2>Onboarding de cliente</h2>
        <p class="muted">Valida o pacote, importa a base, avalia a prontidão de treino e prepara o ambiente de piloto.</p>
        <form id="onboardingForm" class="form-grid">
          ${input("cliente", "Nome do cliente", "", "Ex.: Laticínio Exemplo", "")}
          ${input("inputDir", "Pasta do pacote", "", "Ex.: docs\\templates_dados_reais", "docs\\templates_dados_reais")}
          ${input("outputRoot", "Raiz de saída", "", "Ex.: onboarding_clientes", "onboarding_clientes")}
          ${input("climatePath", "Arquivo de clima (opcional)", "", "Ex.: dados_inmet_processado\\fact_clima_diario_inmet.csv", "")}
          <label>
            Treino
            <select name="skipTrain">
              <option value="false">Executar quando houver massa suficiente</option>
              <option value="true">Pular treino nesta rodada</option>
            </select>
          </label>
          <div class="wide form-actions">
            <button class="primary-button" type="submit">Executar onboarding</button>
          </div>
        </form>
      </section>
      <section class="panel">
        <h2>Parecer do onboarding</h2>
        ${onboardingResultPanel()}
      </section>
    </div>
  `;
}

function onboardingResultPanel() {
  const result = state.onboardingResult;
  if (!result) {
    return `<p class="muted">Nenhum onboarding executado nesta sessão.</p>`;
  }
  return `
    <div class="detail-grid">
      ${detail("Cliente", result.cliente?.nome || "-")}
      ${detail("Validação", result.importacao?.validation?.status || "-")}
      ${detail("Treino", result.treino?.executed ? "Executado" : "Não executado")}
      ${detail("Pronto para treino", result.prontidao_treino?.ready ? "Sim" : "Não")}
      ${detail("Base operacional", result.importacao?.output_dir || "-")}
      ${detail("Artefatos", result.ambiente?.MVP_ARTEFATOS_DIR || "-")}
    </div>
    <h3 style="margin-top: 18px;">Comandos prontos</h3>
    <pre class="code-block">${escapeHtml(result.proximos_comandos?.api || "")}</pre>
    <pre class="code-block">${escapeHtml(result.proximos_comandos?.dashboard || "")}</pre>
    <pre class="code-block">${escapeHtml(result.proximos_comandos?.frontend || "")}</pre>
  `;
}

function bindSupplierForm() {
  $("#supplierForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const id = String(form.get("id") || nextSupplierId()).trim();
    const risco = clamp(Number(form.get("risco") || 0), 0, 100);
    const supplier = {
      id,
      nome: String(form.get("nome") || "").trim(),
      documento: String(form.get("documento") || "").trim(),
      municipio: String(form.get("municipio") || "").trim(),
      polo: String(form.get("polo") || "").trim(),
      laticinio: String(form.get("laticinio") || "").trim(),
      sistema: String(form.get("sistema") || "").trim(),
      capacidadeLitros: Number(form.get("capacidadeLitros") || 0),
      historicoMeses: Number(form.get("historicoMeses") || 0),
      qualidade: String(form.get("qualidade") || "").trim(),
      operacionais: String(form.get("operacionais") || "").trim(),
      logisticos: String(form.get("logisticos") || "").trim(),
      financeiros: String(form.get("financeiros") || "").trim(),
      litrosDia: Number(form.get("capacidadeLitros") || 0),
      risco,
      classeRisco: classifyRisk(risco),
      scoreVolume: risco,
      scoreQualidade: Math.max(0, 100 - risco * 0.45),
      scoreLogistica: risco * 0.7,
      scoreContinuidade: Math.max(20, 100 - risco * 0.35),
      tendenciaPct: 0,
      descartePct: 0,
      ccs: 0,
      cbt: 0,
      recomendacao: "Fornecedor cadastrado para avaliação estratégica e acompanhamento gerencial."
    };

    if (!supplier.nome || !supplier.municipio || !supplier.laticinio) {
      alert("Informe nome, município e laticínio.");
      return;
    }

    try {
      const method = state.editingSupplierId ? "PUT" : "POST";
      const path = state.editingSupplierId ? `/suppliers/${encodeURIComponent(state.editingSupplierId)}` : "/suppliers";
      const saved = await apiFetch(path, {
        method,
        body: JSON.stringify(supplier)
      });
      suppliers = suppliers.filter((item) => item.id !== saved.id).concat(saved);
      state.selectedSupplier = saved.id;
      state.editingSupplierId = null;
      state.apiOnline = true;
      updateApiStatus(true);
      await refreshApiData();
    } catch (error) {
      suppliers = suppliers.filter((item) => item.id !== id).concat(supplier);
      state.selectedSupplier = id;
      state.editingSupplierId = null;
      state.apiOnline = false;
      updateApiStatus(false);
      persist();
      console.info("Fornecedor salvo localmente porque a API não respondeu.", error);
    }
    hydrateFilterOptions();
    render();
  });

  $("#resetSupplierForm").addEventListener("click", () => {
    state.editingSupplierId = null;
    renderManagement();
  });
}

function bindTableActions() {
  $$("[data-edit-supplier]").forEach((button) => {
    button.addEventListener("click", () => {
      state.editingSupplierId = button.dataset.editSupplier;
      renderManagement();
      $("#supplierForm")?.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });

  $$("[data-delete-supplier]").forEach((button) => {
    button.addEventListener("click", async () => {
      const id = button.dataset.deleteSupplier;
      const supplier = suppliers.find((item) => item.id === id);
      if (!supplier || !confirm(`Inativar ${supplier.nome}?`)) return;
      try {
        await apiFetch(`/suppliers/${encodeURIComponent(id)}`, { method: "DELETE" });
        suppliers = suppliers.filter((item) => item.id !== id);
        events = events.filter((item) => item.idFornecedor !== id);
        state.apiOnline = true;
        updateApiStatus(true);
        await refreshApiData();
      } catch (error) {
        suppliers = suppliers.filter((item) => item.id !== id);
        events = events.filter((item) => item.idFornecedor !== id);
        state.apiOnline = false;
        updateApiStatus(false);
        persist();
        console.info("Fornecedor inativado apenas localmente porque a API não respondeu.", error);
      }
      if (state.selectedSupplier === id) {
        state.selectedSupplier = suppliers[0]?.id || "";
      }
      hydrateFilterOptions();
      render();
    });
  });
}

function bindEventForm() {
  $("#eventForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const eventPayload = {
      id: crypto.randomUUID ? crypto.randomUUID() : String(Date.now()),
      idFornecedor: String(form.get("idFornecedor")),
      data: String(form.get("data") || new Date().toISOString().slice(0, 10)),
      categoria: String(form.get("categoria")),
      impactoLitros: Number(form.get("impactoLitros") || 0),
      valorFinanceiro: Number(form.get("valorFinanceiro") || 0),
      responsavel: String(form.get("responsavel") || "Gestor"),
      descricao: String(form.get("descricao") || "").trim()
    };
    try {
      const saved = await apiFetch("/management-events", {
        method: "POST",
        body: JSON.stringify(eventPayload)
      });
      events.unshift(saved);
      state.apiOnline = true;
      updateApiStatus(true);
      await refreshApiData();
    } catch (error) {
      events.unshift(eventPayload);
      state.apiOnline = false;
      updateApiStatus(false);
      persist();
      console.info("Lançamento salvo localmente porque a API não respondeu.", error);
    }
    render();
  });

  $("#clearEvents").addEventListener("click", () => {
    apiFetch("/management-events", { method: "DELETE" })
      .then(async () => {
        state.apiOnline = true;
        updateApiStatus(true);
        await refreshApiData();
      })
      .catch((error) => {
        state.apiOnline = false;
        updateApiStatus(false);
        console.info("Lançamentos limpos apenas localmente porque a API não respondeu.", error);
      })
      .finally(() => {
        events = [];
        persist();
        render();
      });
  });
}

function bindOnboardingForm() {
  $("#onboardingForm")?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const payload = {
      cliente: String(form.get("cliente") || "").trim(),
      inputDir: String(form.get("inputDir") || "").trim(),
      outputRoot: String(form.get("outputRoot") || "onboarding_clientes").trim(),
      climatePath: String(form.get("climatePath") || "").trim() || null,
      skipTrain: String(form.get("skipTrain") || "false") === "true"
    };

    if (!payload.cliente || !payload.inputDir) {
      alert("Informe o nome do cliente e a pasta do pacote.");
      return;
    }

    try {
      const result = await apiFetch("/onboarding/run", {
        method: "POST",
        body: JSON.stringify(payload)
      });
      state.onboardingResult = result;
      state.apiOnline = true;
      updateApiStatus(true);
      renderManagement();
    } catch (error) {
      state.apiOnline = false;
      updateApiStatus(false);
      alert(`Falha ao executar onboarding: ${error.message}`);
    }
  });
}

function bindPlanActions(data) {
  $("#syncSuggestedPlans")?.addEventListener("click", async () => {
    try {
      if (state.apiOnline) {
        const syncedPlans = await apiFetch("/action-plans/bootstrap", { method: "POST" });
        actionPlans = Array.isArray(syncedPlans) ? syncedPlans : actionPlans;
        state.apiData.actionPlans = actionPlans;
        updateApiStatus(true);
      } else {
        const suggested = buildActionPlans(data.length ? data : suppliers);
        const existingKeys = new Set(actionPlans.map((plan) => `${plan.fornecedorId || ""}|${plan.tipo}|${plan.status || ""}`));
        for (const plan of suggested) {
          const key = `${plan.fornecedorId || ""}|${plan.tipo}|${plan.status || ""}`;
          if (!existingKeys.has(key)) {
            actionPlans.unshift(plan);
          }
        }
        persist();
      }
      render();
    } catch (error) {
      console.info("Falha ao sincronizar planos sugeridos.", error);
    }
  });

  $$("[data-toggle-plan]").forEach((button) => {
    button.addEventListener("click", async () => {
      const planId = button.dataset.togglePlan;
      const current = actionPlans.find((plan) => String(plan.id) === String(planId));
      if (!current) return;
      const nextStatus = current.status === "Concluido" ? "Aberto" : "Concluido";
      try {
        const saved = await apiFetch(`/action-plans/${encodeURIComponent(planId)}`, {
          method: "PATCH",
          body: JSON.stringify({ status: nextStatus })
        });
        actionPlans = actionPlans.map((plan) => (String(plan.id) === String(planId) ? saved : plan));
        state.apiData.actionPlans = actionPlans;
        state.apiOnline = true;
        updateApiStatus(true);
      } catch (error) {
        actionPlans = actionPlans.map((plan) => (
          String(plan.id) === String(planId)
            ? { ...plan, status: nextStatus, concluidoEm: nextStatus === "Concluido" ? new Date().toISOString() : null }
            : plan
        ));
        state.apiOnline = false;
        updateApiStatus(false);
        persist();
        console.info("Plano atualizado apenas localmente porque a API não respondeu.", error);
      }
      render();
    });
  });

  $$("[data-edit-plan]").forEach((button) => {
    button.addEventListener("click", () => {
      state.editingPlanId = state.editingPlanId === button.dataset.editPlan ? null : button.dataset.editPlan;
      renderPlans(data);
    });
  });

  $$("[data-plan-form]").forEach((form) => {
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const formData = new FormData(event.currentTarget);
      const planId = String(formData.get("id"));
      const payload = {
        responsavel: String(formData.get("responsavel") || "").trim(),
        prazo: Number(formData.get("prazo") || 0),
        resultadoLitros: Number(formData.get("resultadoLitros") || 0),
        resultadoValor: Number(formData.get("resultadoValor") || 0),
        dataPrevista: String(formData.get("dataPrevista") || "").trim() || null,
        observacoes: String(formData.get("observacoes") || "").trim(),
        evidencias: String(formData.get("evidencias") || "").trim(),
        descricao: String(formData.get("descricao") || "").trim(),
        status: String(formData.get("status") || "Aberto")
      };
      try {
        const saved = await apiFetch(`/action-plans/${encodeURIComponent(planId)}`, {
          method: "PATCH",
          body: JSON.stringify(payload)
        });
        actionPlans = actionPlans.map((plan) => (String(plan.id) === planId ? saved : plan));
        state.apiData.actionPlans = actionPlans;
        state.apiOnline = true;
        updateApiStatus(true);
      } catch (error) {
        actionPlans = actionPlans.map((plan) => (
          String(plan.id) === planId
            ? {
                ...plan,
                ...payload,
                concluidoEm: payload.status === "Concluido" ? new Date().toISOString() : null,
                atualizadoEm: new Date().toISOString()
              }
            : plan
        ));
        state.apiOnline = false;
        updateApiStatus(false);
        persist();
        console.info("Plano atualizado apenas localmente porque a API não respondeu.", error);
      }
      state.editingPlanId = null;
      render();
    });
  });

  $$("[data-delete-plan]").forEach((button) => {
    button.addEventListener("click", async () => {
      const planId = button.dataset.deletePlan;
      try {
        await apiFetch(`/action-plans/${encodeURIComponent(planId)}`, { method: "DELETE" });
        state.apiOnline = true;
        updateApiStatus(true);
      } catch (error) {
        state.apiOnline = false;
        updateApiStatus(false);
        console.info("Plano removido apenas localmente porque a API não respondeu.", error);
      }
      actionPlans = actionPlans.filter((plan) => String(plan.id) !== String(planId));
      state.apiData.actionPlans = actionPlans;
      persist();
      render();
    });
  });
}

function renderPlans(data) {
  const plans = state.apiOnline && Array.isArray(state.apiData.actionPlans)
    ? state.apiData.actionPlans
    : actionPlans;
  const openPlans = plans.filter((plan) => plan.status !== "Concluido");
  const completedPlans = plans.filter((plan) => plan.status === "Concluido");
  const expectedLiters = sum(openPlans, "litros");
  const realizedLiters = sum(completedPlans, "resultadoLitros");
  const realizedValue = sum(completedPlans, "resultadoValor");
  const effectiveness = state.apiOnline && state.apiData.actionPlanEffectiveness
    ? state.apiData.actionPlanEffectiveness
    : buildPlanEffectiveness(plans);
  $("#planos").innerHTML = `
    <section class="panel">
      <h2>Planos de ação</h2>
      <p class="muted">Fila de execução para campo, qualidade, logística e relacionamento com fornecedores.</p>
      <div class="topbar-actions" style="margin-bottom: 18px;">
        <button class="ghost-button" type="button" id="syncSuggestedPlans">Sincronizar sugestões</button>
      </div>
      <div class="kpi-grid">
        ${kpi("Planos abertos", openPlans.length, "Ações priorizadas por risco")}
        ${kpi("Planos concluídos", completedPlans.length, "Histórico de execução")}
        ${kpi("Meta aberta", `${number.format(expectedLiters)} L`, "Proteção esperada em aberto")}
        ${kpi("Resultado concluído", `${number.format(realizedLiters)} L`, `${money.format(realizedValue)} realizados`)}
      </div>
      <div class="action-grid">
        ${plans.map((plan) => `
          <article class="action-card">
            <div>
              <span class="risk-pill risk-${plan.risco}">${plan.risco}</span>
              <p style="margin-top: 8px;"><span class="tag">${plan.tipo}</span></p>
              <p class="muted" style="margin-top: 8px;">${plan.status || "Aberto"}</p>
            </div>
            <div>
              <h3>${plan.titulo}</h3>
              <p>${plan.descricao}</p>
              <p class="muted">${plan.fornecedorNome ? `Fornecedor: ${plan.fornecedorNome}` : "Plano sem fornecedor vinculado"}</p>
            </div>
            <div>
              <strong>${plan.responsavel}</strong>
              <p class="muted">Prazo: ${number.format(plan.prazo)} dias</p>
              <p class="muted">Origem: ${plan.origem || "Manual"}</p>
            </div>
            <div>
              <strong>${number.format(plan.litros)} L/dia</strong>
              <p class="muted">${money.format(plan.valor)} por mês</p>
              <p class="muted">Realizado: ${number.format(plan.resultadoLitros || 0)} L | ${money.format(plan.resultadoValor || 0)}</p>
              <p class="muted">${planPerformanceLabel(plan)}</p>
              <div class="table-actions" style="margin-top: 12px;">
                <button class="icon-button" type="button" data-toggle-plan="${plan.id}">
                  ${plan.status === "Concluido" ? "Reabrir" : "Concluir"}
                </button>
                <button class="icon-button" type="button" data-edit-plan="${plan.id}">
                  ${state.editingPlanId === String(plan.id) ? "Fechar edição" : "Atualizar"}
                </button>
                <button class="icon-button danger" type="button" data-delete-plan="${plan.id}">Excluir</button>
              </div>
            </div>
            ${state.editingPlanId === String(plan.id) ? `
              <div class="action-card-editor">
                <form data-plan-form="${plan.id}" class="form-grid">
                  <input type="hidden" name="id" value="${escapeHtml(plan.id)}" />
                  ${input("responsavel", "Responsável", "", "", plan.responsavel || "")}
                  ${input("prazo", "Prazo (dias)", "number", "0", plan.prazo ?? 0)}
                  ${input("resultadoLitros", "Resultado obtido (L)", "number", "0", plan.resultadoLitros ?? 0)}
                  ${input("resultadoValor", "Resultado obtido (R$)", "number", "0", plan.resultadoValor ?? 0)}
                  ${input("dataPrevista", "Data prevista", "date", "", plan.dataPrevista || "")}
                  <label>
                    Status
                    <select name="status">
                      ${["Aberto", "Em andamento", "Concluido"].map((status) => `
                        <option value="${status}" ${status === (plan.status || "Aberto") ? "selected" : ""}>${status}</option>
                      `).join("")}
                    </select>
                  </label>
                  ${textarea("descricao", "Descrição da ação", plan.descricao || "")}
                  ${textarea("observacoes", "Observações de execução", plan.observacoes || "")}
                  ${textarea("evidencias", "Evidências", plan.evidencias || "")}
                  <div class="wide plan-meta">
                    <span class="muted">Criado em: ${formatDateTime(plan.criadoEm)}</span>
                    <span class="muted">Última atualização: ${formatDateTime(plan.atualizadoEm)}</span>
                    <span class="muted">Concluído em: ${formatDateTime(plan.concluidoEm)}</span>
                  </div>
                  <div class="wide form-actions">
                    <button class="primary-button" type="submit">Salvar andamento</button>
                  </div>
                </form>
              </div>
            ` : ""}
          </article>
        `).join("")}
      </div>
    </section>
    <section class="panel" style="margin-top: 18px;">
      <h2>Painel de efetividade</h2>
      <p class="muted">Leitura consolidada dos planos concluídos para entender o que realmente entregou resultado.</p>
      <div class="kpi-grid">
        ${kpi("Efetividade total", `${decimal.format(effectiveness.resumo.efetividadePct || 0)}%`, `${number.format(effectiveness.resumo.planosConcluidos || 0)} planos concluídos`)}
        ${kpi("Meta consolidada", `${number.format(effectiveness.resumo.metaLitros || 0)} L`, money.format(effectiveness.resumo.metaValor || 0))}
        ${kpi("Resultado consolidado", `${number.format(effectiveness.resumo.resultadoLitros || 0)} L`, money.format(effectiveness.resumo.resultadoValor || 0))}
        ${kpi("Desvio", `${number.format((effectiveness.resumo.resultadoLitros || 0) - (effectiveness.resumo.metaLitros || 0))} L`, money.format((effectiveness.resumo.resultadoValor || 0) - (effectiveness.resumo.metaValor || 0)))}
      </div>
      <div class="grid-3" style="margin-top: 18px;">
        <section>
          <h3>Por tipo</h3>
          ${effectivenessList(effectiveness.porTipo)}
        </section>
        <section>
          <h3>Por responsável</h3>
          ${effectivenessList(effectiveness.porResponsavel)}
        </section>
        <section>
          <h3>Por fornecedor</h3>
          ${effectivenessList(effectiveness.porFornecedor)}
        </section>
      </div>
    </section>
  `;
  bindPlanActions(data);
}

function renderImpact(data) {
  const apiImpact = shouldUseApiAggregates() ? state.apiData.impact : null;
  const riskLiters = apiImpact?.litrosRisco ?? sum(data.filter((item) => ["Alto", "Médio"].includes(item.classeRisco)), "litrosDia");
  const avoidableDiscard = apiImpact?.descarteAtacavel ?? sum(data, "litrosDia") * avg(data, "descartePct") / 100 * 0.32;
  const protectedRevenue = apiImpact?.valorMensalMonitorado ?? riskLiters * 2.25 * 30;
  const scenario = calculateScenario(data);

  $("#impacto").innerHTML = `
    <div class="simulator">
      <section class="panel">
        <h2>Simulador de impacto</h2>
        <p class="muted">Ajuste variáveis para estimar volume protegido e valor mensal incremental.</p>
        <div class="slider-list">
          ${slider("qualidade", "Melhoria em qualidade", state.scenario.qualidade, 0, 40, "%")}
          ${slider("logistica", "Melhoria em logística", state.scenario.logistica, 0, 35, "%")}
          ${slider("clima", "Pressão climática", state.scenario.clima, -30, 30, "%")}
        </div>
      </section>
      <section class="panel">
        <h2>Valor estratégico</h2>
        <div class="impact-grid">
          ${impactCard(`${number.format(riskLiters)} L/dia`, "Volume monitorado em risco")}
          ${impactCard(money.format(protectedRevenue), "Valor mensal sob gestão preditiva")}
          ${impactCard(`${number.format(avoidableDiscard)} L/dia`, "Descarte atacável")}
          ${impactCard(`${number.format(scenario.protectedLiters)} L/dia`, "Litros protegidos no cenário")}
          ${impactCard(money.format(scenario.monthlyValue), "Valor mensal incremental")}
          ${impactCard(`${number.format(apiImpact?.eventosGerenciais ?? events.length)}`, "Eventos gerenciais rastreados")}
        </div>
      </section>
    </div>
  `;

  $$("#impacto [data-scenario]").forEach((input) => {
    input.addEventListener("input", () => {
      state.scenario[input.dataset.scenario] = Number(input.value);
      renderImpact(getFilteredSuppliers());
    });
  });
}

function supplierTable(data, extended, manageable = false) {
  if (!data.length) return `<p class="muted">Nenhum fornecedor encontrado com os filtros atuais.</p>`;
  return `
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Fornecedor</th>
            <th>Laticínio</th>
            <th>Polo</th>
            <th>Risco</th>
            <th>Score</th>
            <th>Litros/dia</th>
            <th>Qualidade</th>
            ${extended ? "<th>Recomendação</th>" : ""}
            ${manageable ? "<th>Ações</th>" : ""}
          </tr>
        </thead>
        <tbody>
          ${data.map((item) => `
            <tr>
              <td><strong>${item.nome}</strong><br><span class="muted">${item.municipio} - ID ${item.id}</span></td>
              <td>${item.laticinio}</td>
              <td>${item.polo}</td>
              <td><span class="risk-pill risk-${item.classeRisco}">${item.classeRisco}</span></td>
              <td>${scoreBar(item.risco)}</td>
              <td>${number.format(item.litrosDia)} L</td>
              <td>CCS ${number.format(item.ccs)}<br>CBT ${number.format(item.cbt)}</td>
              ${extended ? `<td>${item.recomendacao}</td>` : ""}
              ${manageable ? `
                <td>
                  <div class="table-actions">
                    <button class="icon-button" type="button" data-edit-supplier="${item.id}">Editar</button>
                    <button class="icon-button danger" type="button" data-delete-supplier="${item.id}">Inativar</button>
                  </div>
                </td>
              ` : ""}
            </tr>
          `).join("")}
        </tbody>
      </table>
    </div>
  `;
}

function eventsTable() {
  if (!events.length) return `<p class="muted">Nenhum lançamento gerencial registrado.</p>`;
  return `
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Data</th>
            <th>Fornecedor</th>
            <th>Categoria</th>
            <th>Impacto</th>
            <th>Valor</th>
            <th>Responsável</th>
          </tr>
        </thead>
        <tbody>
          ${events.map((event) => {
            const supplier = suppliers.find((item) => item.id === event.idFornecedor);
            return `
              <tr>
                <td>${formatDate(event.data)}</td>
                <td>${supplier ? supplier.nome : event.idFornecedor}</td>
                <td>${event.categoria}</td>
                <td>${number.format(event.impactoLitros)} L</td>
                <td>${money.format(event.valorFinanceiro)}</td>
                <td>${event.responsavel}</td>
              </tr>
            `;
          }).join("")}
        </tbody>
      </table>
    </div>
  `;
}

function kpi(label, value, helper) {
  return `<article class="kpi"><span>${label}</span><strong>${value}</strong><small>${helper}</small></article>`;
}

function detail(label, value) {
  return `<article class="detail-item"><span class="mini-label">${label}</span><p>${value || "-"}</p></article>`;
}

function riskBars(data) {
  const apiDistribution = shouldUseApiAggregates() ? state.apiData.riskDistribution : null;
  const counts = Array.isArray(apiDistribution) ? apiDistribution.map((item) => ({
    label: item.classeRisco,
    value: item.fornecedores
  })) : ["Alto", "Médio", "Baixo"].map((risk) => ({
    label: risk,
    value: data.filter((item) => item.classeRisco === risk).length
  }));
  const max = Math.max(1, ...counts.map((item) => item.value));
  return `<div class="chart-bars">${counts.map((item) => barRow(item.label, item.value, max)).join("")}</div>`;
}

function barRow(label, value, max) {
  const width = max ? Math.max(4, (Number(value) / max) * 100) : 0;
  return `
    <div class="bar-row">
      <strong>${label}</strong>
      <div class="bar-track"><div class="bar-fill" style="width:${Math.min(100, width)}%"></div></div>
      <span>${decimal.format(Number(value) || 0)}</span>
    </div>
  `;
}

function scoreBar(score) {
  const level = score >= 75 ? "danger" : score >= 50 ? "warn" : "";
  return `
    <div class="score-bar">
      <strong>${decimal.format(score)}</strong>
      <div class="score-track"><div class="score-fill ${level}" style="width:${Math.min(100, score)}%"></div></div>
    </div>
  `;
}

function scoreCard(label, value) {
  return `<article class="score-card"><span>${label}</span><strong>${decimal.format(value)}</strong>${scoreBar(value)}</article>`;
}

function impactCard(value, label) {
  return `<article class="impact-card"><strong>${value}</strong><p class="muted">${label}</p></article>`;
}

function insightItem(label, value) {
  return `<article class="insight-item"><span>${label}</span><strong>${value}</strong></article>`;
}

function buildActionPlans(data) {
  const source = data.length ? data : suppliers;
  return source
    .filter((item) => item.risco >= 48 || item.scoreQualidade >= 70 || item.scoreLogistica >= 80)
    .slice(0, 9)
    .map((item) => {
      const tipo = item.scoreQualidade >= 70
        ? "Qualidade"
        : item.scoreLogistica >= 80
          ? "Logística"
          : item.tendenciaPct < -6
            ? "Campo"
            : "Relacionamento";
      const responsavel = {
        Qualidade: "Coordenação de Qualidade",
        Logística: "Gestão de Rotas",
        Campo: "Técnico de Campo",
        Relacionamento: "Captação Comercial"
      }[tipo];
      const prazo = tipo === "Qualidade" ? 10 : tipo === "Logística" ? 7 : tipo === "Campo" ? 14 : 21;
      const litros = item.litrosDia * (tipo === "Qualidade" ? 0.18 : tipo === "Logística" ? 0.12 : 0.15);
      return {
        id: crypto.randomUUID ? crypto.randomUUID() : `plan-${Date.now()}-${item.id}`,
        fornecedorId: item.id,
        fornecedorNome: item.nome,
        risco: item.classeRisco,
        tipo,
        responsavel,
        prazo,
        litros,
        valor: litros * 2.25 * 30,
        resultadoLitros: 0,
        resultadoValor: 0,
        dataPrevista: offsetDateIso(prazo),
        observacoes: "",
        evidencias: "",
        titulo: `${item.nome} - ${item.municipio}`,
        descricao: item.recomendacao,
        status: "Aberto",
        origem: "Sugestão"
      };
    });
}

function calculateScenario(data) {
  const baseLiters = sum(data.filter((item) => ["Alto", "Médio"].includes(item.classeRisco)), "litrosDia");
  const qualityGain = state.scenario.qualidade / 100;
  const logisticsGain = state.scenario.logistica / 100;
  const climatePressure = state.scenario.clima / 100;
  const protectedLiters = Math.max(0, baseLiters * (0.1 + qualityGain * 0.22 + logisticsGain * 0.18 - climatePressure * 0.16));
  return {
    protectedLiters,
    monthlyValue: protectedLiters * 2.25 * 30
  };
}

function slider(key, label, value, min, max, suffix) {
  return `
    <label>
      ${label}: ${value}${suffix}
      <input data-scenario="${key}" type="range" min="${min}" max="${max}" value="${value}" />
    </label>
  `;
}

function input(name, label, type = "", placeholder = "", value = "") {
  return `
    <label>
      ${label}
      <input name="${name}" type="${type || "text"}" placeholder="${placeholder}" value="${escapeHtml(value)}" ${name === "data" ? "required" : ""} />
    </label>
  `;
}

function textarea(name, label, value = "") {
  return `
    <label class="wide">
      ${label}
      <textarea name="${name}">${escapeHtml(value)}</textarea>
    </label>
  `;
}

function unique(values) {
  return [...new Set(values.filter(Boolean))].sort((a, b) => String(a).localeCompare(String(b), "pt-BR"));
}

function sum(data, key) {
  return data.reduce((acc, item) => acc + Number(item[key] || 0), 0);
}

function avg(data, key) {
  return data.length ? sum(data, key) / data.length : 0;
}

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function classifyRisk(score) {
  if (score >= 75) return "Alto";
  if (score >= 50) return "Médio";
  return "Baixo";
}

function nextSupplierId() {
  const max = suppliers.reduce((acc, item) => Math.max(acc, Number(item.id) || 0), 0);
  return String(max + 1);
}

function formatDate(value) {
  if (!value) return "-";
  return new Intl.DateTimeFormat("pt-BR", { timeZone: "UTC" }).format(new Date(`${value}T00:00:00Z`));
}

function formatDateTime(value) {
  if (!value) return "-";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "-";
  return new Intl.DateTimeFormat("pt-BR", {
    dateStyle: "short",
    timeStyle: "short",
    timeZone: "America/Sao_Paulo"
  }).format(date);
}

function planPerformanceLabel(plan) {
  const expected = Number(plan.litros || 0);
  const realized = Number(plan.resultadoLitros || 0);
  if (!realized) return "Sem resultado medido ainda";
  if (!expected) return "Resultado registrado sem meta inicial";
  const deltaPct = ((realized - expected) / expected) * 100;
  if (Math.abs(deltaPct) < 1) return "Resultado em linha com a meta";
  return deltaPct > 0
    ? `Resultado ${decimal.format(deltaPct)}% acima da meta`
    : `Resultado ${decimal.format(Math.abs(deltaPct))}% abaixo da meta`;
}

function buildPlanEffectiveness(plans) {
  const completed = plans.filter((plan) => plan.status === "Concluido");
  const summarize = (items, key, labelKey) => {
    const grouped = new Map();
    items.forEach((item) => {
      const groupKey = String(item[key] || "Não informado");
      if (!grouped.has(groupKey)) {
        grouped.set(groupKey, {
          label: item[labelKey || key] || groupKey,
          planos: 0,
          metaLitros: 0,
          resultadoLitros: 0,
          metaValor: 0,
          resultadoValor: 0
        });
      }
      const bucket = grouped.get(groupKey);
      bucket.planos += 1;
      bucket.metaLitros += Number(item.litros || 0);
      bucket.resultadoLitros += Number(item.resultadoLitros || 0);
      bucket.metaValor += Number(item.valor || 0);
      bucket.resultadoValor += Number(item.resultadoValor || 0);
    });
    return [...grouped.values()]
      .map((bucket) => ({
        ...bucket,
        desvioLitros: bucket.resultadoLitros - bucket.metaLitros,
        desvioValor: bucket.resultadoValor - bucket.metaValor,
        efetividadePct: bucket.metaLitros ? (bucket.resultadoLitros / bucket.metaLitros) * 100 : 0
      }))
      .sort((a, b) => b.efetividadePct - a.efetividadePct);
  };

  const resumo = {
    planosConcluidos: completed.length,
    metaLitros: sum(completed, "litros"),
    resultadoLitros: sum(completed, "resultadoLitros"),
    metaValor: sum(completed, "valor"),
    resultadoValor: sum(completed, "resultadoValor")
  };
  resumo.efetividadePct = resumo.metaLitros ? (resumo.resultadoLitros / resumo.metaLitros) * 100 : 0;

  return {
    resumo,
    porTipo: summarize(completed, "tipo"),
    porResponsavel: summarize(completed, "responsavel"),
    porFornecedor: summarize(completed, "fornecedorId", "fornecedorNome")
  };
}

function effectivenessList(items) {
  if (!items?.length) return `<p class="muted">Ainda não há planos concluídos suficientes para leitura de efetividade.</p>`;
  return `
    <div class="chart-bars">
      ${items.slice(0, 6).map((item) => `
        <article class="effectiveness-item">
          <div class="effectiveness-head">
            <strong>${item.label}</strong>
            <span>${decimal.format(item.efetividadePct || 0)}%</span>
          </div>
          <div class="bar-track"><div class="bar-fill" style="width:${Math.min(100, Math.max(4, item.efetividadePct || 0))}%"></div></div>
          <p class="muted">Meta ${number.format(item.metaLitros || 0)} L | Resultado ${number.format(item.resultadoLitros || 0)} L</p>
          <p class="muted">Desvio ${number.format(item.desvioLitros || 0)} L | ${money.format(item.desvioValor || 0)}</p>
        </article>
      `).join("")}
    </div>
  `;
}

function offsetDateIso(days) {
  const date = new Date();
  date.setHours(0, 0, 0, 0);
  date.setDate(date.getDate() + Number(days || 0));
  return date.toISOString().slice(0, 10);
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

init();
