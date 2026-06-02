/**
 * Silva Pimenta + Magalhães Gomes — Dashboard de Orçamento
 *
 * Lê JSON do Apps Script (planilha "Gastos Maio 2026") + cotação USD via API do BCB.
 * Modo dev: usa data-mock.json se API_URL estiver vazia.
 */

// ============================================================
// CONFIG
// ============================================================
const API_URL = ''; // colar URL do Apps Script após Deploy → Web App
const REFRESH_MS = 5 * 60 * 1000; // 5 minutos
const FALLBACK_USD_BRL = 5.20;

// Cotação dólar via API do Banco Central (PTAX)
async function buscarTaxaUSD() {
  try {
    const hoje = new Date();
    // PTAX usa MM-DD-YYYY e só tem dados em dias úteis — tenta os últimos 5
    for (let i = 0; i < 5; i++) {
      const d = new Date(hoje);
      d.setDate(d.getDate() - i);
      const mm = String(d.getMonth() + 1).padStart(2, '0');
      const dd = String(d.getDate()).padStart(2, '0');
      const yyyy = d.getFullYear();
      const dataStr = `${mm}-${dd}-${yyyy}`;
      const url = `https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='${dataStr}'&$format=json`;
      try {
        const res = await fetch(url);
        const json = await res.json();
        if (json.value && json.value.length) {
          return { taxa: json.value[0].cotacaoVenda, fonte: `BCB ${dd}/${mm}` };
        }
      } catch (e) { /* tenta próximo dia */ }
    }
  } catch (e) {}
  return { taxa: FALLBACK_USD_BRL, fonte: 'fallback' };
}

// ============================================================
// ORÇAMENTOS (fonte: _contexto/orcamento.md)
// ============================================================
const PRODUTOS = [
  // Silva Pimenta
  { id: 'aux-moradia',     escritorio: 'silva',     nome: 'Aux. Moradia',  orcamento: 22252.40, plats: ['meta', 'google'] },
  { id: 'fies',            escritorio: 'silva',     nome: 'FIES',          orcamento: 26157.60, plats: ['meta', 'google'] },
  { id: 'fies-suspensao',  escritorio: 'silva',     nome: 'FIES Susp.',    orcamento:  1840.65, plats: ['meta', 'google'] },
  { id: 'direito-medico',  escritorio: 'silva',     nome: 'Direito Médico',orcamento: 15000.00, plats: ['google'] },
  { id: 'inss',            escritorio: 'silva',     nome: 'INSS',          orcamento:  3103.86, plats: ['meta'] },
  { id: 'provab',          escritorio: 'silva',     nome: 'PROVAB',        orcamento:   232.00, plats: ['meta'] },
  // Magalhães Gomes
  { id: 'seguro',          escritorio: 'magalhaes', nome: 'Seguro',        orcamento: 20534.15, plats: ['google'] },
  { id: 'livre-ir',        escritorio: 'magalhaes', nome: 'Livre IR',      orcamento: 15000.00, plats: ['meta', 'google'], encerrado: true, encerradoEm: '2026-05-26' },
  { id: 'seg-vida',        escritorio: 'magalhaes', nome: 'Seg Vida',      orcamento:  3000.00, plats: ['meta', 'google'] }
];

// Total considera só produtos ATIVOS (encerrados saem da régua mensal)
const TOTAL_ORCAMENTO = PRODUTOS.filter(p => !p.encerrado).reduce((s, p) => s + p.orcamento, 0);

// ============================================================
// SCALE — manter 1920x1080 dentro de qualquer tela
// ============================================================
function aplicarScale() {
  const container = document.querySelector('.dashboard-container');
  if (!container) return;
  const sx = window.innerWidth / 1920;
  const sy = window.innerHeight / 1080;
  const s = Math.min(sx, sy);
  container.style.transform = `scale(${s})`;
}
window.addEventListener('resize', aplicarScale);
window.addEventListener('load', aplicarScale);

// ============================================================
// FORMATAÇÃO
// ============================================================
const fmtBRL = (v) => 'R$ ' + (v || 0).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const fmtPct = (v) => (v || 0).toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

function statusDoConsumo(percAtual, percTempo) {
  // verde se consumo <= ritmo do mês + 5pp
  // amarelo se entre +5pp e +15pp
  // vermelho se acima de +15pp OU > 100%
  const dif = percAtual - percTempo;
  if (percAtual >= 100) return 'alert';
  if (dif > 15) return 'alert';
  if (dif > 5) return 'warn';
  return 'ok';
}

function projecao(gasto, diasPassados, diasMes) {
  if (!diasPassados) return 0;
  return (gasto / diasPassados) * diasMes;
}

// ============================================================
// RENDER
// ============================================================
function renderHeader(diaAtual, diasMes, mesNome, ano) {
  document.getElementById('diaAtual').textContent = diaAtual;
  document.getElementById('diasMes').textContent = diasMes;
  document.getElementById('mesNome').textContent = mesNome;
  document.getElementById('anoValue').textContent = ano;
}

function diariaDisponivel(orcamento, gasto, diasRestantes) {
  // dias restantes inclui o dia de hoje (gasto de hoje ainda pode subir)
  if (diasRestantes <= 0) return { valor: 0, estourou: gasto > orcamento, dif: orcamento - gasto };
  const restante = orcamento - gasto;
  return { valor: restante / diasRestantes, estourou: restante < 0, dif: restante };
}

function renderTotal(gastoTotal, diaAtual, diasMes) {
  document.getElementById('totalGasto').textContent = fmtBRL(gastoTotal);
  document.getElementById('totalOrcamento').textContent = fmtBRL(TOTAL_ORCAMENTO);

  const perc = (gastoTotal / TOTAL_ORCAMENTO) * 100;
  const tempoPerc = (diaAtual / diasMes) * 100;
  const proj = projecao(gastoTotal, diaAtual, diasMes);
  const status = statusDoConsumo(perc, tempoPerc);
  const diasRestantes = diasMes - diaAtual + 1; // inclui hoje
  const diaria = diariaDisponivel(TOTAL_ORCAMENTO, gastoTotal, diasRestantes);
  const diariaIdeal = TOTAL_ORCAMENTO / diasMes;

  const fill = document.getElementById('totalBarFill');
  fill.style.width = Math.min(perc, 100) + '%';
  fill.className = 'total-bar-fill' + (status === 'ok' ? '' : ' ' + status);

  document.getElementById('totalPercent').textContent = fmtPct(perc) + ' consumido';

  const saldoEl = document.getElementById('totalSaldo');
  if (perc > 100) {
    saldoEl.textContent = `Estouro: ${fmtBRL(gastoTotal - TOTAL_ORCAMENTO)}`;
    saldoEl.style.color = '#FCA5A5';
  } else {
    saldoEl.textContent = `Projeção mês: ${fmtBRL(proj)}`;
    saldoEl.style.color = proj > TOTAL_ORCAMENTO * 1.05 ? '#FCA5A5' : '';
  }

  // Diária disponível
  const diariaEl = document.getElementById('totalDiaria');
  const diariaInfoEl = document.getElementById('totalDiariaInfo');
  if (diaria.estourou) {
    diariaEl.textContent = '—';
    diariaEl.className = 'total-diaria-value alert';
    diariaInfoEl.textContent = `Estourou ${fmtBRL(Math.abs(diaria.dif))} · sem orçamento p/ os ${diasRestantes}d`;
  } else {
    diariaEl.textContent = fmtBRL(diaria.valor) + '/dia';
    const baseline = diaria.valor / diariaIdeal;
    diariaEl.className = 'total-diaria-value' + (baseline < 0.85 ? ' warn' : (baseline > 1.05 ? ' ok' : ''));
    diariaInfoEl.textContent = `${diasRestantes}d restantes · ritmo ideal ${fmtBRL(diariaIdeal)}/dia`;
  }
}

function renderProdutoCard(p, gastoMeta, gastoGoogle, diaAtual, diasMes) {
  const gasto = gastoMeta + gastoGoogle;

  // Produto encerrado: render simplificado, sem métricas diárias nem barra
  if (p.encerrado) {
    const dataFmt = p.encerradoEm ? p.encerradoEm.split('-').reverse().join('/') : '';
    const platBarsEnc = p.plats.map(plat => {
      const v = plat === 'meta' ? gastoMeta : gastoGoogle;
      const icon = plat === 'meta' ? 'Ⓜ' : 'G';
      const nome = plat === 'meta' ? 'Meta Ads' : 'Google Ads';
      const cls = plat === 'meta' ? 'plat-meta' : 'plat-google';
      const empty = v === 0 ? 'empty' : '';
      return `
        <div class="plat-row ${cls} ${empty}">
          <div class="plat-row-head">
            <span class="plat-row-icon">${icon}</span>
            <span class="plat-row-name">${nome}</span>
            <span class="plat-row-value">${fmtBRL(v)}</span>
          </div>
        </div>`;
    }).join('');
    return `
      <div class="produto-card encerrado ${p.escritorio === 'magalhaes' ? 'magalhaes' : ''}" data-id="${p.id}">
        <div class="produto-head">
          <div class="produto-head-left">
            <span class="produto-nome">${p.nome}</span>
            <span class="produto-status-pill encerrado">ENCERRADO${dataFmt ? ' ' + dataFmt : ''}</span>
          </div>
        </div>
        <div class="produto-valores">
          <span class="produto-gasto">${fmtBRL(gasto)}</span>
          <span class="produto-de">gasto final</span>
        </div>
        <div class="produto-encerrado-info">Orçamento ${fmtBRL(p.orcamento)} cancelado · sai do total mensal</div>
        <div class="produto-plats-separados">${platBarsEnc}</div>
      </div>
    `;
  }

  const perc = (gasto / p.orcamento) * 100;
  const tempoPerc = (diaAtual / diasMes) * 100;
  const status = statusDoConsumo(perc, tempoPerc);
  const diasRestantes = diasMes - diaAtual + 1;
  const diaria = diariaDisponivel(p.orcamento, gasto, diasRestantes);
  const saldo = p.orcamento - gasto;
  const gastoPorDia = diaAtual > 0 ? gasto / diaAtual : 0;

  const pillTxt = status === 'alert' ? 'ALERTA' : status === 'warn' ? 'ATENÇÃO' : 'OK';

  // Métrica 1: Gastando/dia (média atual) — cor conforme comparação com ideal
  const gastoIdeal = p.orcamento / diasMes;
  const gastoRatio = gastoIdeal > 0 ? gastoPorDia / gastoIdeal : 0;
  const gastoClsCorr = gastoRatio > 1.15 ? 'alert' : (gastoRatio > 1.05 ? 'warn' : 'neutral');

  // Métrica 2: Pode gastar/dia OU Cortar/dia
  let podeLabel, podeValor, podeCls;
  if (diaria.estourou) {
    podeLabel = 'Cortar p/ recup.';
    podeValor = fmtBRL(Math.abs(diaria.dif) / diasRestantes);
    podeCls = 'alert';
  } else {
    podeLabel = 'Pode gastar';
    podeValor = fmtBRL(diaria.valor);
    const idealDiaria = p.orcamento / diasMes;
    const ratio = diaria.valor / idealDiaria;
    podeCls = ratio < 0.85 ? 'warn' : (ratio > 1.05 ? 'ok' : 'neutral');
  }

  // Métrica 3: Ajuste — diferença entre "Pode gastar" e "Gastando"
  // positivo = pode AUMENTAR / negativo = precisa CORTAR
  let ajusteValor, ajusteCls, ajusteLabel;
  if (diaria.estourou) {
    const cortar = Math.abs(diaria.dif) / diasRestantes;
    ajusteLabel = 'Cortar';
    ajusteValor = '−' + fmtBRL(cortar + gastoPorDia);
    ajusteCls = 'alert';
  } else {
    const delta = diaria.valor - gastoPorDia;
    if (Math.abs(delta) < gastoIdeal * 0.05) {
      ajusteLabel = 'Ajuste';
      ajusteValor = 'Em linha';
      ajusteCls = 'neutral';
    } else if (delta > 0) {
      ajusteLabel = 'Pode +';
      ajusteValor = '+' + fmtBRL(delta);
      ajusteCls = 'ok';
    } else {
      ajusteLabel = 'Cortar';
      ajusteValor = '−' + fmtBRL(Math.abs(delta));
      ajusteCls = 'warn';
    }
  }

  // Métrica 4: Saldo restante
  const saldoCls2 = saldo < 0 ? 'alert' : (saldo < p.orcamento * 0.1 ? 'warn' : 'ok');
  const saldoValor = saldo < 0 ? '-' + fmtBRL(Math.abs(saldo)) : fmtBRL(saldo);

  // Meta e Google — bloco lado a lado com valor destacado
  const platBars = p.plats.map(plat => {
    const v = plat === 'meta' ? gastoMeta : gastoGoogle;
    const icon = plat === 'meta' ? 'Ⓜ' : 'G';
    const nome = plat === 'meta' ? 'Meta' : 'Google';
    const cls = plat === 'meta' ? 'plat-meta' : 'plat-google';
    const percPlat = p.orcamento > 0 ? Math.min((v / p.orcamento) * 100, 100) : 0;
    const empty = v === 0 ? 'empty' : '';
    return `
      <div class="plat-row ${cls} ${empty}">
        <div class="plat-row-head">
          <span class="plat-row-icon">${icon}</span>
          <span class="plat-row-name">${nome}</span>
        </div>
        <span class="plat-row-value">${fmtBRL(v)}</span>
        <div class="plat-row-bar"><div class="plat-row-fill" style="width:${percPlat}%"></div></div>
      </div>`;
  }).join('');

  return `
    <div class="produto-card ${p.escritorio === 'magalhaes' ? 'magalhaes' : ''} status-${status}" data-id="${p.id}">
      <div class="produto-head">
        <div class="produto-head-left">
          <span class="produto-nome">${p.nome}</span>
          <span class="produto-status-pill ${status}">${pillTxt}</span>
        </div>
        <div class="produto-saldo-top ${saldoCls2}">
          <span class="saldo-label">Saldo</span>
          <span class="saldo-value">${saldoValor}</span>
        </div>
      </div>
      <div class="produto-valores">
        <span class="produto-gasto">${fmtBRL(gasto)}</span>
        <span class="produto-de">/</span>
        <span class="produto-orcamento">${fmtBRL(p.orcamento)}</span>
        <span class="produto-percent-inline">${fmtPct(perc)}</span>
      </div>
      <div class="produto-bar">
        <div class="produto-bar-fill ${status === 'ok' ? '' : status}" style="width:${Math.min(perc, 100)}%"></div>
      </div>
      <div class="produto-metrics">
        <div class="metric metric-${gastoClsCorr}" title="Quanto está gastando por dia em média no mês até hoje. Fórmula: gasto total ÷ dias passados.">
          <span class="metric-label">Gastando</span>
          <span class="metric-value">${fmtBRL(gastoPorDia)}<span class="metric-unit">/dia</span></span>
        </div>
        <div class="metric metric-${podeCls}" title="Ritmo máximo permitido por dia até o fim do mês pra fechar exatamente no orçamento. NÃO é o quanto pode aumentar. Fórmula: (orçamento − gasto) ÷ dias restantes.">
          <span class="metric-label">${podeLabel}</span>
          <span class="metric-value">${podeValor}<span class="metric-unit">/dia</span></span>
        </div>
        <div class="metric metric-${ajusteCls}" title="Ajuste real: quanto AUMENTAR (verde +) ou CORTAR (vermelho −) por dia daqui pra frente. É a diferença entre Pode e Gastando.">
          <span class="metric-label">${ajusteLabel}</span>
          <span class="metric-value">${ajusteValor}${ajusteValor !== 'Em linha' ? '<span class="metric-unit">/dia</span>' : ''}</span>
        </div>
      </div>
      <div class="produto-plats-separados">${platBars}</div>
    </div>
  `;
}

function renderEscritorios(dados, diaAtual, diasMes) {
  const silvaEl = document.getElementById('silvaGrid');
  const magalhaesEl = document.getElementById('magalhaesGrid');
  silvaEl.innerHTML = '';
  magalhaesEl.innerHTML = '';

  PRODUTOS.forEach(p => {
    const g = (dados.gastos && dados.gastos[p.id]) || { meta: 0, google: 0 };
    const html = renderProdutoCard(p, g.meta || 0, g.google || 0, diaAtual, diasMes);
    if (p.escritorio === 'silva') silvaEl.insertAdjacentHTML('beforeend', html);
    else magalhaesEl.insertAdjacentHTML('beforeend', html);
  });
}

function renderPlataformas(totalMeta, totalGoogle, taxa, fonteUSD) {
  const total = totalMeta + totalGoogle;
  document.getElementById('metaTotal').textContent = fmtBRL(totalMeta);
  document.getElementById('googleTotal').textContent = fmtBRL(totalGoogle);
  document.getElementById('metaShare').textContent = total ? fmtPct((totalMeta / total) * 100) + ' do total' : '—';
  document.getElementById('googleShare').textContent = total ? fmtPct((totalGoogle / total) * 100) + ' do total' : '—';

  document.getElementById('usdRate').textContent = taxa.toLocaleString('pt-BR', { minimumFractionDigits: 4 });
  document.getElementById('usdSource').textContent = fonteUSD;
}

function renderFooter(status, atualizadoEm) {
  document.getElementById('footerStatus').textContent = status;
  if (atualizadoEm) {
    const d = new Date(atualizadoEm);
    document.getElementById('footerTime').textContent = d.toLocaleString('pt-BR');
  }
}

function renderResumoExecutivo(dados, diaAtual, diasMes) {
  const el = document.getElementById('resumoTexto');
  if (!el) return;
  const ritmoMes = (diaAtual / diasMes) * 100;

  let totalGasto = 0;
  let totalOrcamento = 0;
  const folgas = [];
  const estouros = [];
  PRODUTOS.filter(p => !p.encerrado).forEach(p => {
    const g = (dados.gastos && dados.gastos[p.id]) || { meta: 0, google: 0 };
    const gasto = (g.meta || 0) + (g.google || 0);
    const perc = (gasto / p.orcamento) * 100;
    totalGasto += gasto;
    totalOrcamento += p.orcamento;
    const dif = perc - ritmoMes;
    if (perc >= 100 || dif > 15) {
      estouros.push({ nome: p.nome, perc, dif });
    } else if (dif < -15) {
      folgas.push({ nome: p.nome, perc, dif });
    }
  });
  const percTotal = totalOrcamento > 0 ? (totalGasto / totalOrcamento) * 100 : 0;
  estouros.sort((a,b) => b.dif - a.dif);
  folgas.sort((a,b) => a.dif - b.dif);

  let frase = `Total consumido: <strong>${fmtPct(percTotal)}</strong> · ritmo do mês: ${fmtPct(ritmoMes)}.`;
  const partes = [];
  if (estouros.length > 0) {
    const nomes = estouros.slice(0, 3).map(e => e.nome).join(', ');
    partes.push(`Atenção em <span class="alert-txt">${nomes}</span> (estourando o ritmo)`);
  }
  if (folgas.length > 0) {
    const nomes = folgas.slice(0, 3).map(f => f.nome).join(', ');
    partes.push(`folga em <span class="ok-txt">${nomes}</span> (sub-gastando)`);
  }
  if (estouros.length === 0 && folgas.length === 0) {
    partes.push(`<span class="ok-txt">todos os produtos rodando dentro da margem</span>`);
  }
  el.innerHTML = frase + ' ' + partes.join('; ') + '.';
}

function renderComparativoMesAnterior(dadosCorrente, fechamentoAnt) {
  // Adiciona badge ▲/▼ no nome do produto comparando com mesmo dia do mês anterior (pro-rata)
  if (!fechamentoAnt || !fechamentoAnt.gastos) return;
  const hoje = new Date();
  const diaAtual = hoje.getDate();
  const diasMesAnt = fechamentoAnt.diasMes || new Date(hoje.getFullYear(), hoje.getMonth(), 0).getDate();
  PRODUTOS.forEach(p => {
    const corrente = (dadosCorrente.gastos && dadosCorrente.gastos[p.id]) || { meta: 0, google: 0 };
    const anterior = fechamentoAnt.gastos[p.id] || { meta: 0, google: 0 };
    const gastoAtual = (corrente.meta || 0) + (corrente.google || 0);
    const gastoMesAntInteiro = (anterior.meta || 0) + (anterior.google || 0);
    const proRataAnt = (gastoMesAntInteiro / diasMesAnt) * diaAtual;
    if (proRataAnt < 1) return;
    const delta = ((gastoAtual - proRataAnt) / proRataAnt) * 100;
    const cardEl = document.querySelector(`.produto-card[data-id="${p.id}"] .produto-nome`);
    if (!cardEl) return;
    let cls = 'flat', seta = '~';
    if (delta > 5) { cls = 'up'; seta = '▲'; }
    else if (delta < -5) { cls = 'down'; seta = '▼'; }
    const valorAbs = Math.abs(delta).toFixed(0);
    const badge = document.createElement('span');
    badge.className = `delta-comparacao ${cls}`;
    badge.title = `Mesmo dia do mês passado (pro-rata): ${fmtBRL(proRataAnt)}. Variação: ${delta >= 0 ? '+' : ''}${delta.toFixed(1)}%`;
    badge.textContent = `${seta} ${valorAbs}%`;
    cardEl.appendChild(badge);
  });
}

// ============================================================
// MODO DO DASHBOARD (corrente vs anterior)
// ============================================================
// 'corrente' = mês de hoje, lê data-mock.json, dia = hoje
// 'anterior' = mês passado, lê data-fechamento-YYYY-MM.json, dia = último dia do mês passado (mês "fechado")
let modoAtivo = 'corrente';

const MESES_PT = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'];

function calcularPeriodo(modo) {
  const hoje = new Date();
  if (modo === 'anterior') {
    // Último dia do mês passado
    const ultimoDiaMesPassado = new Date(hoje.getFullYear(), hoje.getMonth(), 0);
    const mes = ultimoDiaMesPassado.getMonth();
    const ano = ultimoDiaMesPassado.getFullYear();
    const diasMes = ultimoDiaMesPassado.getDate();
    return {
      modo: 'anterior',
      diaAtual: diasMes,            // mês fechado: dia atual = último dia
      diasMes,
      mes,
      ano,
      mesNome: MESES_PT[mes],
      arquivo: `data/data-fechamento-${ano}-${String(mes + 1).padStart(2, '0')}.json`,
    };
  }
  // corrente
  const diaAtual = hoje.getDate();
  const diasMes = new Date(hoje.getFullYear(), hoje.getMonth() + 1, 0).getDate();
  return {
    modo: 'corrente',
    diaAtual,
    diasMes,
    mes: hoje.getMonth(),
    ano: hoje.getFullYear(),
    mesNome: MESES_PT[hoje.getMonth()],
    arquivo: 'data/data.json',
  };
}

// Carrega fechamento do mês anterior (pra comparação ▲▼ nos cards do mês corrente)
let _cacheFechamentoAnterior = null;
async function fechamentoAnterior() {
  if (_cacheFechamentoAnterior !== null) return _cacheFechamentoAnterior;
  const p = calcularPeriodo('anterior');
  try {
    const res = await fetch(p.arquivo + '?t=' + Date.now());
    if (!res.ok) throw new Error(res.status);
    _cacheFechamentoAnterior = await res.json();
  } catch (e) {
    _cacheFechamentoAnterior = { gastos: {} };
  }
  return _cacheFechamentoAnterior;
}

// ============================================================
// FETCH
// ============================================================
async function carregar() {
  const p = calcularPeriodo(modoAtivo);
  renderHeader(p.diaAtual, p.diasMes, p.mesNome, p.ano);

  let dados;
  let usandoMock = false;
  let erroFetch = null;
  try {
    if (!API_URL || modoAtivo === 'anterior') {
      const res = await fetch(p.arquivo + '?t=' + Date.now());
      if (!res.ok) throw new Error(`HTTP ${res.status} ao buscar ${p.arquivo}`);
      dados = await res.json();
      usandoMock = true;
    } else {
      const res = await fetch(API_URL + '?t=' + Date.now());
      dados = await res.json();
    }
  } catch (e) {
    erroFetch = e.message;
    // Fallback amistoso: dashboard vazio com aviso, não morre
    dados = { gastos: {}, atualizadoEm: new Date().toISOString() };
  }

  const { taxa, fonte } = await buscarTaxaUSD();

  // Calcular totais por plataforma — só ATIVOS entram no total mensal
  const idsEncerrados = new Set(PRODUTOS.filter(p => p.encerrado).map(p => p.id));
  let totalMeta = 0, totalGoogle = 0;
  let totalMetaEncerrado = 0, totalGoogleEncerrado = 0;
  Object.entries(dados.gastos || {}).forEach(([id, g]) => {
    if (idsEncerrados.has(id)) {
      totalMetaEncerrado += g.meta || 0;
      totalGoogleEncerrado += g.google || 0;
    } else {
      totalMeta += g.meta || 0;
      totalGoogle += g.google || 0;
    }
  });
  const gastoTotal = totalMeta + totalGoogle;

  renderTotal(gastoTotal, p.diaAtual, p.diasMes);
  renderEscritorios(dados, p.diaAtual, p.diasMes);
  renderPlataformas(totalMeta, totalGoogle, taxa, fonte);
  renderResumoExecutivo(dados, p.diaAtual, p.diasMes);

  // Comparativo vs mês anterior (só no modo corrente)
  if (modoAtivo === 'corrente') {
    fechamentoAnterior().then(fa => renderComparativoMesAnterior(dados, fa));
  }

  let statusTxt;
  if (erroFetch) {
    statusTxt = `Erro ao carregar dados (${erroFetch})`;
  } else if (modoAtivo === 'anterior') {
    statusTxt = `Fechamento ${p.mesNome}/${p.ano} · ${fmtBRL(gastoTotal)} consumidos`;
  } else {
    statusTxt = usandoMock
      ? `Mês corrente · ${fmtBRL(gastoTotal)} consumidos`
      : `Ao vivo · ${fmtBRL(gastoTotal)} consumidos`;
  }
  renderFooter(statusTxt, dados.atualizadoEm || new Date().toISOString());
}

function ativarToggleMes() {
  const btnCorrente = document.getElementById('btnMesCorrente');
  const btnAnterior = document.getElementById('btnMesAnterior');
  if (!btnCorrente || !btnAnterior) return;
  function setModo(novoModo) {
    if (novoModo === modoAtivo) return;
    modoAtivo = novoModo;
    btnCorrente.classList.toggle('active', modoAtivo === 'corrente');
    btnAnterior.classList.toggle('active', modoAtivo === 'anterior');
    carregar();
  }
  btnCorrente.addEventListener('click', () => setModo('corrente'));
  btnAnterior.addEventListener('click', () => setModo('anterior'));
}

ativarToggleMes();
carregar();
setInterval(carregar, REFRESH_MS);
