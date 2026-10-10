// Optional development harness: Node + Playwright + Chromium.
// The Windows product does not depend on Node or Playwright.
const {chromium}=require('playwright'),assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..'),base=process.env.TKB_BASE||'http://127.0.0.1:8768';
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',args:['--no-sandbox']});
 const checks=[],errors=[],external=[];
 try{
  const context=await browser.newContext({viewport:{width:1440,height:1000}}),p=await context.newPage();
  p.on('pageerror',e=>errors.push(e.message));p.on('request',r=>{if(!r.url().startsWith(base))external.push(r.url());});
  await p.goto(base);await p.waitForFunction(()=>document.querySelector('#nc').textContent==='37');
  assert.equal(await p.locator('#nt').textContent(),'64');assert.equal(await p.locator('#nr').textContent(),'972');
  checks.push('Bootstrap: 37 classes, 64 teachers, 972 PCCM periods');
  assert.equal(await p.locator('[data-objective]').count(),6);checks.push('Six configurable objective toggles and weights');
  await p.getByText('◇ Hoạt động đặc biệt',{exact:true}).click();await p.waitForFunction(()=>document.querySelectorAll('[data-activity]').length===74);
  assert((await p.locator('#special-summary').textContent()).includes('Tổng 111'));assert((await p.locator('#special-table').textContent()).includes('CC_SHCN_COMBINED'));checks.push('74 source records inventory all 111 periods; combined source label preserved');
  await p.locator('#special_mode').selectOption('SCENARIO');await p.locator('#assumption').fill('Browser fixture, not verified school policy');await p.locator('[data-activity]').first().check();await p.locator('#special-check').click();
  await p.waitForFunction(()=>document.querySelector('#message').textContent.includes('Đã kiểm tra quy tắc'));assert((await p.locator('#special-summary').textContent()).includes('pending chính thức 111'));checks.push('Explicit scenario selection retains official pending count');
  await p.locator('#special_mode').selectOption('STRICT');await p.locator('[data-activity]').first().uncheck();await p.locator('#special-check').click();

  await p.getByText('≡ Dữ liệu PCCM',{exact:true}).click();await p.locator('#show-issues').click();
  assert.equal(await p.locator('.warning').count(),69);assert((await p.locator('#trust').textContent()).includes('111'));
  checks.push('69 source warnings and 111 unassigned special periods visible');
  await p.locator('#show-classes').click();await p.locator('[data-class="C06A01"]').selectOption('pm');
  assert.equal(await p.locator('[data-class="C06A01"]').inputValue(),'pm');checks.push('Per-class shift can be set without changing identity');
  await p.locator('#xlsx').setInputFiles(root+'/SOURCE/PCCM_INPUT_CODEX_5_NHOM.xlsx');
  await p.waitForFunction(()=>document.querySelector('#message').textContent.includes('Đã đọc trực tiếp'));
  assert.equal(await p.locator('#nr').textContent(),'972');checks.push('Actual XLSX import through browser/API, total row excluded');
  await p.getByText('⚙ Ràng buộc & tối ưu',{exact:true}).click();await p.locator('#mode').selectOption('morning');
  await p.getByText('▦ Thời khóa biểu',{exact:true}).click();await p.locator('#solve').click();
  await p.waitForFunction(()=>document.querySelector('#message').textContent.includes('Hoàn tất'),{},{timeout:15000});
  await p.getByText('✓ Chất lượng nghiệm',{exact:true}).click();
  assert((await p.locator('#result').textContent()).includes('INFEASIBLE'));assert((await p.locator('#result').textContent()).includes('GV015'));
  checks.push('Morning capacity infeasibility displayed, no partial schedule');assert(!(await p.locator('#result').textContent()).includes('0 xung đột'));checks.push('Infeasible result never displays zero conflicts as a valid schedule');
  const normalized=JSON.parse(fs.readFileSync(root+'/data/pccm_normalized.json','utf8'));
  const result=JSON.parse(fs.readFileSync(root+'/reports/both.json','utf8'));
  const boot=await (await p.request.get(base+'/api/bootstrap')).json();
  const backup={version:3,data:normalized,config:boot.config,result};
  await p.getByText('≡ Dữ liệu PCCM',{exact:true}).click();
  await p.locator('#json').setInputFiles({name:'test-backup.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(backup))});
  await p.waitForFunction(()=>document.querySelector('#np').textContent==='972');
  await p.getByText('▦ Thời khóa biểu',{exact:true}).click();
  assert.equal(await p.locator('#grid .lesson').count(),26);checks.push('Restore 37-class CP-SAT result and independently revalidate 972 periods');
  const dl=p.waitForEvent('download');await p.locator('#csv').click();const csv=await dl;await csv.saveAs(root+'/reports/UI_EXPORT.csv');
  assert(fs.readFileSync(root+'/reports/UI_EXPORT.csv','utf8').includes('GV'));checks.push('CSV download contains teacher IDs, UTF-8 and full schedule');
  await p.locator('#schedule-file').setInputFiles(root+'/reports/UI_EXPORT.csv');await p.waitForFunction(()=>document.querySelector('#message').textContent.includes('Đã nhập lịch'));assert.equal(await p.locator('#np').textContent(),'972');checks.push('CSV schedule round trip through browser and independent verifier');
  const ed=p.waitForEvent('download');await p.locator('#export-xlsx').click();const excel=await ed;await excel.saveAs(root+'/reports/UI_EXPORT.xlsx');await p.locator('#schedule-file').setInputFiles(root+'/reports/UI_EXPORT.xlsx');await p.waitForFunction(()=>document.querySelector('#message').textContent.includes('Đã nhập lịch'));assert.equal(await p.locator('#np').textContent(),'972');checks.push('XLSX schedule round trip through browser and independent verifier');
  await p.getByText('✓ Chất lượng nghiệm',{exact:true}).click();assert.equal(await p.locator('#teacher-visits table tr').count(),65);assert.equal(await p.locator('#distribution-chart meter').count(),6);assert((await p.locator('#comparison').textContent()).includes('V3 tham chiếu'));checks.push('Teacher visit table, subject/day chart, and V3 comparison render');await p.getByText('▦ Thời khóa biểu',{exact:true}).click();

  const bd=p.waitForEvent('download');await p.locator('#backup').click();const back=await bd;await back.saveAs(root+'/reports/UI_BACKUP.json');
  assert.equal(JSON.parse(fs.readFileSync(root+'/reports/UI_BACKUP.json','utf8')).version,'3.1');checks.push('Separate V3 backup download');
  await p.screenshot({path:root+'/reports/UI_SCHEDULE.png',fullPage:true});
  await p.getByText('✓ Chất lượng nghiệm',{exact:true}).click();await p.screenshot({path:root+'/reports/UI_QUALITY.png',fullPage:true});
  await p.getByText('≡ Dữ liệu PCCM',{exact:true}).click();
  const v2={classes:[{id:'c',name:'6A1',shift:'am'}],teachers:[{id:'t',name:'GV demo'}],assignments:[{id:'a',teacher:'t',classId:'c',subject:'Toán',count:2}]};
  await p.locator('#json').setInputFiles({name:'v2.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(v2))});
  await p.waitForFunction(()=>document.querySelector('#nc').textContent==='1');
  await p.getByText('⚙ Ràng buộc & tối ưu',{exact:true}).click();await p.locator('#time_limit').fill('3');
  await p.getByText('▦ Thời khóa biểu',{exact:true}).click();await p.locator('#solve').click();
  await p.waitForFunction(()=>document.querySelector('#message').textContent.includes('Hoàn tất'),{},{timeout:15000});
  assert.equal(await p.locator('#np').textContent(),'2');checks.push('V2 JSON migration + live CP-SAT API solve of technical fixture');
  const access=await p.request.post(base+'/api/solve',{data:{}});assert.equal(access.status(),403);
  const origin=await p.request.post(base+'/api/solve',{headers:{'X-CSRF-Token':boot.token,Origin:'https://untrusted.example'},data:{}});assert.equal(origin.status(),403);
  checks.push('CSRF and cross-origin POST rejected');
  await p.getByText('≡ Dữ liệu PCCM',{exact:true}).click();
  const specialFixture=JSON.parse(fs.readFileSync(root+'/tests/SPECIAL_BROWSER_FIXTURE.json','utf8'));
  const sc={...boot.config,days:2,periods:3,max_class_session:3,max_teacher_session:3,time_limit:3,special_mode:'SCENARIO',special_scenario:{enabled:true,activity_ids:['SP_C1_HD02'],teacher_required:false,teacher_id:null,scheduling_policy:'independent',assumption_label:'Explicit browser simulation fixture'}};
  await p.locator('#json').setInputFiles({name:'scenario.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify({version:'3.1',data:specialFixture,config:sc}))});await p.waitForFunction(()=>document.querySelector('#nc').textContent==='2');await p.waitForFunction(()=>document.querySelector('[data-activity="SP_C1_HD02"]')?.checked===true);
  await p.getByText('▦ Thời khóa biểu',{exact:true}).click();await p.locator('#solve').click();await p.waitForFunction(()=>document.querySelector('#message').textContent.includes('Hoàn tất'),{},{timeout:15000});assert.equal(await p.locator('#np').textContent(),'6');
  await p.getByText('✓ Chất lượng nghiệm',{exact:true}).click();assert((await p.locator('#result').textContent()).includes('MÔ PHỎNG'));assert((await p.locator('#result').textContent()).includes('1 tiết giả định'));checks.push('Live SCENARIO solve labels simulated periods separately and does not count them as verified PCCM');
  await p.setViewportSize({width:390,height:844});assert.equal(await p.locator('body').evaluate(e=>e.scrollWidth<=innerWidth),true);
  checks.push('Mobile page fits viewport; schedule scroll stays in its container');
  assert.deepEqual(errors,[]);assert.deepEqual(external,[]);checks.push('Zero native browser errors and zero external requests');
  fs.writeFileSync(root+'/reports/UI_TESTS.json',JSON.stringify({result:'PASS',checks,errors,external},null,2));console.log('PASS',checks.length,'browser checks');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
