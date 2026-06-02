const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
  const page = await ctx.newPage();

  const erros = [];
  page.on('pageerror', err => erros.push(`PAGEERROR: ${err.message}`));
  page.on('console', msg => {
    if (msg.type() === 'error') erros.push(`CONSOLE: ${msg.text()}`);
  });

  console.log('Carregando http://localhost:8766 ...');
  await page.goto('http://localhost:8766/', { waitUntil: 'networkidle', timeout: 20000 });
  await page.waitForTimeout(2000);

  // Captura screenshot
  await page.screenshot({ path: 'teste-corrente.png', fullPage: false });
  console.log('Screenshot mês corrente: teste-corrente.png');

  // Validações
  const resumo = await page.locator('#resumoTexto').textContent();
  const status = await page.locator('#footerStatus').textContent();
  const totalGasto = await page.locator('#totalGasto').textContent();
  const cards = await page.locator('.produto-card').count();
  const deltaBadges = await page.locator('.delta-comparacao').count();
  const legenda = await page.locator('.legenda').count();

  console.log(`  Total gasto:      ${totalGasto}`);
  console.log(`  Status:           ${status}`);
  console.log(`  Resumo executivo: ${resumo.slice(0, 100)}...`);
  console.log(`  Cards produto:    ${cards}`);
  console.log(`  Badges delta vs mês ant: ${deltaBadges}`);
  console.log(`  Legenda no rodapé: ${legenda > 0 ? 'OK' : 'FALTANDO'}`);

  // Clica no toggle Mês anterior
  console.log('\nClicando "Mês anterior"...');
  await page.click('#btnMesAnterior');
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'teste-anterior.png', fullPage: false });
  const totalAnt = await page.locator('#totalGasto').textContent();
  const resumoAnt = await page.locator('#resumoTexto').textContent();
  console.log(`  Total mês anterior: ${totalAnt}`);
  console.log(`  Resumo:             ${resumoAnt.slice(0, 100)}...`);

  if (erros.length > 0) {
    console.log('\n[ERROS JS]');
    erros.forEach(e => console.log('  ' + e));
  } else {
    console.log('\n[OK] Sem erros JS.');
  }

  await browser.close();
})();
