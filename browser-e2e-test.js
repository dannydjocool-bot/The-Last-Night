const { chromium } = require('playwright');
const assert = require('assert');

const BASE = process.env.TEST_URL || 'https://the-last-night-git-dev-nada-f420.vercel.app';

async function settle(page, ms=250){ await page.waitForTimeout(ms); }
async function safeText(locator){ return ((await locator.textContent()) || '').replace(/\s+/g,' ').trim(); }

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

  // Real-browser combat interaction using an isolated test encounter.
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
  const context = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile:true, hasTouch:true, deviceScaleFactor:3 });
  const page = await context.newPage();
  const pageErrors=[];
  page.on('pageerror', e=>pageErrors.push(String(e)));
  page.on('console', msg=>{ if(msg.type()==='error') pageErrors.push('console: '+msg.text()); });

  await page.goto(BASE, { waitUntil:'networkidle', timeout:60000 });
  await page.evaluate(()=>{ Math.random=()=>0.30; localStorage.clear(); });
  await page.getByRole('button',{name:/Play The Last Night/i}).click();
  await page.getByRole('button',{name:/1\s*Survivor/i}).click();
  await page.locator('#game').waitFor({state:'visible'});

  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth-window.innerWidth);
  assert(overflow<=4, `Mobile page has ${overflow}px horizontal overflow`);
  assert(await page.locator('#v06MobileDock').isVisible(), 'Mobile Journal/Log/Pack dock should be visible');
  assert(await page.locator('#v06DockJournal').isVisible(), 'Mobile Journal control should be visible');
  assert(await page.locator('#v06DockLog').isVisible(), 'Mobile Log control should be visible');
  assert(await page.locator('#v06DockPack').isVisible(), 'Mobile Pack control should be visible');

  const dockHit=await page.locator('#v06DockLog').evaluate(el=>{
    const r=el.getBoundingClientRect(),x=r.left+r.width/2,y=r.top+r.height/2,hit=document.elementFromPoint(x,y),dock=el.closest('#v06MobileDock'),game=document.getElementById('gameSite');
    return {rect:{left:r.left,top:r.top,width:r.width,height:r.height},x,y,hitId:hit?.id||'',hitClass:hit?.className||'',hitTag:hit?.tagName||'',dockZ:getComputedStyle(dock).zIndex,dockPosition:getComputedStyle(dock).position,dockTransform:getComputedStyle(dock).transform,gameZ:getComputedStyle(game).zIndex,gamePosition:getComputedStyle(game).position,scrollY:window.scrollY,innerHeight:window.innerHeight};
  });
  console.log('MOBILE DOCK HIT TEST:',JSON.stringify(dockHit));
  assert(['v06DockLog','SPAN'].includes(dockHit.hitId)||dockHit.hitId==='v06DockLog'||dockHit.hitTag==='SPAN', `Mobile dock Log center is covered by ${dockHit.hitTag}#${dockHit.hitId}.${dockHit.hitClass}`);

  await page.locator('#v06DockLog').click();
  assert(await page.locator('#logPanel').evaluate(el=>el.classList.contains('log-open')), 'Mobile Log should open from dock');
  await page.locator('#logClose').click();

  await page.locator('#v06DockJournal').click();
  assert(await page.locator('#v06Overlay').evaluate(el=>el.classList.contains('open')), 'Mobile Journal should open from dock');
  await page.getByRole('button',{name:'Close'}).click();

  const pack=page.locator('#extraPocketsPanel');
  const toggle=page.locator('#mobilePackToggle');
  assert(await toggle.isVisible(), 'Mobile pack toggle should be visible');
  assert(await pack.evaluate(el=>el.classList.contains('mobile-pack-collapsed')), 'Mobile pack should begin collapsed');
  await toggle.click();
  assert(!(await pack.evaluate(el=>el.classList.contains('mobile-pack-collapsed'))), 'Mobile pack should expand');
  await toggle.click();

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
