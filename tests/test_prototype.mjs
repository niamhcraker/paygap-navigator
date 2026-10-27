// Demo Day regression checks run the actual functions extracted from docs/index.html.
// Node 20+; no external dependencies. Run: node --test tests/test_prototype.mjs
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const root=path.resolve(import.meta.dirname,'..');
const html=fs.readFileSync(path.join(root,'docs','index.html'),'utf8');
const js=html.match(/<script>([\s\S]*?)<\/script>/)?.[1];
assert.ok(js,'Embedded production script found');
new vm.Script(js,{filename:'docs/index.html'});
const core=js.slice(js.indexOf('const COLS='),js.indexOf('function setNav()'));
const context=vm.createContext({});
vm.runInContext(core+'\nthis.produced={parseCSV,validate,analyse,living,scenario,app,COLS};',context);
const {parseCSV,validate,analyse,living,scenario,app,COLS}=context.produced;
const sample=fs.readFileSync(path.join(root,'docs','sample_remuneration.csv'),'utf8');
const raw=parseCSV(sample);
const accepted=validate(raw);
const rows=accepted.rows;
const approx=(actual,expected,tol=1e-8)=>assert.ok(Math.abs(actual-expected)<=tol,`${actual} not near ${expected}`);
test('production CSV parser handles quotes, commas and escaped quotes',()=>{
  assert.equal(parseCSV('a,b\n"hello,world","say ""hi"""\n')[1][1],'say "hi"');
});
test('provided sample CSV is valid and contains 1200 records and correct headers',()=>{
 assert.deepEqual([...COLS],[...raw[0]]);assert.deepEqual([...accepted.fatal],[]);assert.equal(rows.length,1200);
});
test('annual total remuneration: top/bottom 5%, ratio',()=>{
 const v=analyse(rows);assert.equal(v.n5,60);approx(v.ratio,26.318409809088365);
});
test('Living Wage: supplied permanent full-time reference at 20000 net monthly',()=>{
 app.rows=rows;app.livingPopulation='Permanent full-time';
 const z=living(20000);assert.equal(z.population,1039);assert.equal(z.count,371);
 approx(z.share,35.707410972088546);assert.equal(z.median,5620);
 assert.equal(z.monthly,2121780);assert.equal(z.annual,25461360);
});
test('Living Wage population switch and no-below-benchmark edge',()=>{
 app.rows=rows;app.livingPopulation='All employment types';assert.equal(living(20000).population,1200);
 app.livingPopulation='Permanent full-time';const z=living(0);
 assert.equal(z.population,1039);assert.equal(z.count,0);assert.equal(z.median,0);assert.equal(z.monthly,0);assert.equal(z.annual,0);
});
test('scenario baseline unchanged, non-zero scenario finite and baseline protected',()=>{
 app.rows=rows;app.stats=analyse(rows);app.bottom=0;app.top=0;
 approx(scenario().stat.ratio,app.stats.ratio);
 app.bottom=20;app.top=-10;let result=scenario();
 assert.ok(Number.isFinite(result.stat.ratio));assert.ok(Number.isFinite(result.delta));
 approx(app.stats.ratio,26.318409809088365);app.bottom=0;app.top=0;
});
test('bad CSV inputs blocked by production validate',()=>{
 const rejected=(edit,fragment)=>{const arr=raw.map(r=>[...r]);edit(arr);assert.ok(validate(arr).fatal.some(x=>x.toLowerCase().includes(fragment)),fragment)};
 rejected(a=>{a[0].pop()},'missing required columns');
 rejected(a=>{a[2]=[...a[1]]},'duplicate');
 rejected(a=>{a[4][5]='-100'},'negative');
 rejected(a=>{a[5][9]='2'},'mismatch');
 rejected(a=>{a[6][1]='2025'},'one financial year');
 rejected(a=>{a[7].pop()},'unexpected number');
});
test('four screens and HTML demonstration download are present',()=>{
 assert.match(html,/data-view="living"/);assert.match(html,/href="sample_remuneration.csv"/);
 assert.match(html,/id="livingPopulation"/);
 const overview=html.slice(html.indexOf('function overview(){'),html.indexOf('function breakdownTable('));
 assert.doesNotMatch(overview,/Below net benchmark/);
 const explore=html.slice(html.indexOf('function explore(){'),html.indexOf('function render(){'));
 assert.doesNotMatch(explore,/livingPanel\(\)/);
});


test('internal remuneration Gini and cohort turnover respond to bottom-tail uplift',()=>{
  app.rows=rows;app.stats=analyse(rows);app.bottom=0;app.top=0;
  approx(app.stats.gini,0.4790855353254315,1e-12);
  app.bottom=30;const result=scenario();
  approx(result.stat.gini,0.4753588922046952,1e-12);
  assert.equal(result.bottomTurnover.original,60);
  assert.equal(result.bottomTurnover.remain,20);
  assert.equal(result.bottomTurnover.movedOut,40);
  assert.equal(result.bottomTurnover.movedIn,40);
  approx(result.stat.ratio,22.784947448462674,1e-12);
  app.bottom=0;app.top=0;
});

test('UI exposes Gini, cohort-turnover and precision caveats',()=>{
  assert.match(html,/Internal remuneration Gini/);
  assert.match(html,/Cohort turnover after re-ranking/);
  assert.match(html,/does not prescribe display precision/);
  assert.match(html,/some treated employees may leave the simulated bottom 5%/);
});


test('Lorenz curve is rendered from production remuneration values',()=>{
  assert.match(html,/function lorenzCurve\(stat\)/);
  assert.match(html,/Internal remuneration inequality/);
  assert.match(html,/Observed remuneration distribution/);
  assert.match(html,/Perfect equality/);
  assert.match(html,/Whole-distribution lens/);
  const overview=html.slice(html.indexOf('function overview(){'),html.indexOf('function breakdownTable('));
  assert.match(overview,/Statistical outlier summary/);
  assert.match(overview,/Internal remuneration inequality/);
  assert.doesNotMatch(overview,/Exploratory outlier check/);
});


test('compact horizontal Gini layout is present',()=>{
  assert.match(html,/gini-layout/);
  assert.match(html,/gini-summary/);
  assert.match(html,/gini-chart/);
  assert.match(html,/max-width:760px/);
});


test('responsible-use messaging is scoped to upload and sidebar',()=>{
  assert.match(html,/id="responsibleSide"/);
  assert.match(html,/Responsible use/);
  assert.match(html,/PAYGAP NAVIGATOR · PROTOTYPE V1 · DECISION SUPPORT/);
  assert.match(html,/Display convention: ratios are shown to two decimal places/);
  const disclaimerCalls=(html.match(/disclaimer\(\)/g)||[]).length;
  assert.equal(disclaimerCalls,2);
});
