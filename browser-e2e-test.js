const { chromium, devices } = require('playwright');
const assert = require('assert');

const BASE = process.env.TEST_URL || 'https://the-last-night-git-dev-nada-f420.vercel.app';

async function settle(page, ms=250){ await page.waitForTimeout(ms); }
async function safeText(locator){ return ((await locator.textContent()) || '').replace(/\s+/g,' ').trim(); }

async function touchCenter(page,selector){
  const point=await page.locator(selector).evaluate(el=>{
    const r=el.getBoundingClientRect(),x=r.left+r.width/2,y=r.top+r.height/2,target=document.elementFromPoint(x,y);
    if(!(target===el||el.contains(target)))throw new Error(`${selector} touch center is covered by ${target?.tagName||'UNKNOWN'}#${target?.id||''}`);
    return {x,y};
  });
  await page.touchscreen.tap(point.x,point.y);
  await page.waitForTimeout(120);
}

async function desktopRun(browser){
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
  const page = await context.newPage();
  const pageErrors=[];
  page.on('pageerror', e=>pageErrors.push(String(e)));
  page.on('console', msg=>{ if(msg.type()==='error') pageErrors.push('console: '+msg.text()); });

  await page.goto(BASE, { waitUntil:'networkidle', timeout:60000 });
  assert.equal(await page.title(), 'The Last Night | Horror Card Game');
  await page.evaluate(()=>{ Math.random=()=>0.30; });

  await page.getByRole('button',{name:/Play The Last Night/i}).click();
  await page.locator('#setup').waitFor({state:'visible'});
  assert.match(await safeText(page.locator('#setup')), /V-0\.6 Beta/i);

  await page.getByRole('button',{name:/1\s*Survivor/i}).click();
  await page.locator('#game').waitFor({state:'visible'});
  assert.match(await safeText(page.locator('#storyObjectiveText')), /Police Station/i);
  assert.equal(await page.locator('#extraPocketsCount').textContent().then(t=>t.trim()), '0 / 30 Slots');

  const station=page.locator('.loc').filter({hasText:'Police Station'});
  await station.getByRole('button',{name:'Move'}).click();
  await settle(page);
  assert.match(await safeText(page.locator('#location')), /Police Station/i);

  const cluesBefore=await page.evaluate(()=>G.clues);
  await page.getByRole('button',{name:/Investigate/i}).click();
  await settle(page,350);
  const cluesAfter=await page.evaluate(()=>G.clues);
  assert.equal(cluesAfter, cluesBefore+1, 'Investigate should advance exactly one clue');
  assert.match(await safeText(page.locator('#storyObjectiveText')), /Town Library/i);
  const library=page.locator('.loc').filter({hasText:'Town Library'});
  assert(await library.evaluate(el=>el.classList.contains('v06-objective-target')), 'Current objective location should glow');
  assert(!(await station.evaluate(el=>el.classList.contains('v06-objective-target'))), 'Completed objective location should stop glowing');

  const cluesBeforeSearch=await page.evaluate(()=>G.clues);
  await page.getByRole('button',{name:/Search \(1 Action\)/i}).click();
  await settle(page);
  assert.equal(await page.evaluate(()=>G.clues), cluesBeforeSearch, 'Search must not advance story clues');

  await page.getByRole('button',{name:'Save Slot 1'}).first().click();
  await settle(page);
  assert(await page.evaluate(()=>!!localStorage.getItem('theLastNightSaveSlot1')), 'Save Slot 1 should exist in localStorage');

  await page.getByRole('button',{name:'📜 GAME LOG'}).click();
  assert(await page.locator('#logPanel').evaluate(el=>el.classList.contains('log-open')), 'Game Log should open');
  await page.locator('#logClose').click();

  const journal=page.locator('#v06JournalBtn');
  assert(await journal.isVisible(), 'Blackwood Journal button should be visible in gameplay');
  await journal.click();
  assert(await page.locator('#v06Overlay').evaluate(el=>el.classList.contains('open')), 'Blackwood Journal overlay should open');
  await page.getByRole('button',{name:'Close'}).click();

  await page.getByRole('button',{name:'Main Menu'}).click();
  await page.getByRole('button',{name:'Return to Menu'}).click();
  await page.locator('#setup').waitFor({state:'visible'});
  assert(!(await journal.isVisible()), 'Journal button should hide on the menu');
  await page.getByRole('button',{name:'Load'}).click();
  await page.locator('#game').waitFor({state:'visible'});
  assert.match(await safeText(page.locator('#storyObjectiveText')), /Town Library/i);

  await page.evaluate(()=>{
    const p=G.ps[G.active];
    const c={id:'e2e-creature',name:'The Drifter',hp:8,maxHp:8,atk:2,rarity:'Common',image:'drifter.png',ability:'Desperate Lunge',provoked:false,loc:p.loc};
    G.creatures.push(c); render();
  });
  await page.getByRole('button',{name:'Fight'}).click();
  await settle(page);
  assert.match(await safeText(page.locator('#actions')), /COMBAT: The Drifter/i);
  await page.getByRole('button',{name:'Attack'}).click();
  await page.getByRole('button',{name:'Attack'}).click();
  await settle(page,350);
  assert.match(await safeText(page.locator('#log')), /COUNTER-ATTACK|counterattacks/i);

  if(pageErrors.length) throw new Error('Desktop browser errors: '+pageErrors.join(' | '));
  await context.close();
}

async function mobileRun(browser){
  const context = await browser.newContext({ ...devices['iPhone 13'] });
  const page = await context.newPage();
  const pageErrors=[];
  page.on('pageerror', e=>pageErrors.push(String(e)));
  page.on('console', msg=>{ if(msg.type()==='error') pageErrors.push('console: '+msg.text()); });

  await page.goto(BASE, { waitUntil:'networkidle', timeout:60000 });
  await page.evaluate(()=>{ Math.random=()=>0.30; localStorage.clear(); });
  const viewport=await page.evaluate(()=>({width:window.innerWidth,height:window.innerHeight,dpr:window.devicePixelRatio}));
  console.log('IPHONE VIEWPORT:',JSON.stringify(viewport));
  assert(viewport.width>=360&&viewport.width<=430, `Unexpected iPhone CSS width: ${viewport.width}`);

  await page.getByRole('button',{name:/Play The Last Night/i}).tap();
  await page.getByRole('button',{name:/1\s*Survivor/i}).tap();
  await page.locator('#game').waitFor({state:'visible'});

  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth-window.innerWidth);
  assert(overflow<=4, `Mobile page has ${overflow}px horizontal overflow`);
  assert(await page.locator('#v06MobileDock').isVisible(), 'Mobile Journal/Log/Pack dock should be visible');
  assert(await page.locator('#v06DockJournal').isVisible(), 'Mobile Journal control should be visible');
  assert(await page.locator('#v06DockLog').isVisible(), 'Mobile Log control should be visible');
  assert(await page.locator('#v06DockPack').isVisible(), 'Mobile Pack control should be visible');

  for(const id of ['v06DockJournal','v06DockLog','v06DockPack']){
    const hit=await page.locator('#'+id).evaluate(el=>{
      const r=el.getBoundingClientRect(),x=r.left+r.width/2,y=r.top+r.height/2,target=document.elementFromPoint(x,y);
      return {id:target?.id||'',tag:target?.tagName||'',parentId:target?.parentElement?.id||'',x,y};
    });
    assert(hit.id===id||hit.parentId===id, `${id} touch center is covered by ${hit.tag}#${hit.id}`);
  }

  await touchCenter(page,'#v06DockLog');
  assert(await page.locator('#logPanel').evaluate(el=>el.classList.contains('log-open')), 'Mobile Log should open from dock');
  await touchCenter(page,'#logClose');

  await touchCenter(page,'#v06DockJournal');
  assert(await page.locator('#v06Overlay').evaluate(el=>el.classList.contains('open')), 'Mobile Journal should open from dock');
  await page.getByRole('button',{name:'Close'}).tap();

  const pack=page.locator('#extraPocketsPanel');
  const toggle=page.locator('#mobilePackToggle');
  assert(await toggle.isVisible(), 'Mobile pack toggle should be visible');
  assert(await pack.evaluate(el=>el.classList.contains('mobile-pack-collapsed')), 'Mobile pack should begin collapsed');
  await touchCenter(page,'#v06DockPack');
  assert(!(await pack.evaluate(el=>el.classList.contains('mobile-pack-collapsed'))), 'Mobile pack should expand from dock');
  await touchCenter(page,'#mobilePackToggle');
  assert(await pack.evaluate(el=>el.classList.contains('mobile-pack-collapsed')), 'Mobile pack should collapse');

  if(pageErrors.length) throw new Error('Mobile browser errors: '+pageErrors.join(' | '));
  await context.close();
}

(async()=>{
  const browser=await chromium.launch({headless:true});
  try{
    await desktopRun(browser);
    console.log('DESKTOP PLAYTHROUGH: PASS');
    await mobileRun(browser);
    console.log('MOBILE TOUCH PLAYTHROUGH: PASS');
    console.log('REAL BROWSER E2E: PASS');
  } finally {
    await browser.close();
  }
})().catch(err=>{ console.error(err.stack||err); process.exit(1); });
