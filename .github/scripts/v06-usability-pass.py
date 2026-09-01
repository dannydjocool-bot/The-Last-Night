from pathlib import Path

js_path = Path('v06-enhancements.js')
css_path = Path('v06-enhancements.css')
js = js_path.read_text()
css = css_path.read_text()

JS_MARK = '/* V0.6 PLAYER GUIDANCE + MOBILE DOCK */'
CSS_MARK = '/* V0.6 PLAYER GUIDANCE + MOBILE DOCK */'

js_append = r'''

/* V0.6 PLAYER GUIDANCE + MOBILE DOCK */
(function(){
const TIP_KEY='theLastNightV06GuidanceTips';
const hasGame=()=>typeof G!=='undefined'&&G&&Array.isArray(G.ps);
const combatNow=()=>typeof combat!=='undefined'?combat:null;
const getSeen=()=>{try{return new Set(JSON.parse(localStorage.getItem(TIP_KEY)||'[]'))}catch{return new Set()}};
const markSeen=k=>{const s=getSeen();s.add(k);localStorage.setItem(TIP_KEY,JSON.stringify([...s]))};
function ensureGuidanceUi(){
  if(!document.getElementById('v06Guidance')){
    const objective=document.querySelector('.story-objective');
    if(objective){
      const box=document.createElement('section');
      box.id='v06Guidance';box.className='v06-guidance';
      box.innerHTML='<div class="v06-guidance-head"><b>🧭 NEXT STEP</b><button id="v06GuidanceHelp" type="button">?</button></div><div id="v06GuidanceText"></div><div id="v06GuidanceMeta"></div>';
      objective.insertAdjacentElement('afterend',box);
      box.querySelector('#v06GuidanceHelp').onclick=()=>showHelp();
    }
  }
  if(!document.getElementById('v06MobileDock')){
    document.body.insertAdjacentHTML('beforeend','<nav id="v06MobileDock" class="v06-mobile-dock" hidden aria-label="Quick game controls"><button id="v06DockJournal" type="button">📓<span>Journal</span><i id="v06JournalDot"></i></button><button id="v06DockLog" type="button">📜<span>Log</span></button><button id="v06DockPack" type="button">🎒<span>Pack</span></button></nav>');
    document.getElementById('v06DockJournal').onclick=()=>document.getElementById('v06JournalBtn')?.click();
    document.getElementById('v06DockLog').onclick=()=>document.getElementById('logButton')?.click();
    document.getElementById('v06DockPack').onclick=()=>{
      const toggle=document.getElementById('mobilePackToggle');
      if(toggle){toggle.click();return}
      document.getElementById('extraPocketsPanel')?.classList.toggle('mobile-pack-collapsed');
    };
  }
  if(!document.getElementById('v06Coach')){
    document.body.insertAdjacentHTML('beforeend','<aside id="v06Coach" class="v06-coach" hidden><button id="v06CoachClose" type="button" aria-label="Dismiss tip">×</button><b id="v06CoachTitle"></b><span id="v06CoachText"></span></aside>');
    document.getElementById('v06CoachClose').onclick=()=>{document.getElementById('v06Coach').hidden=true};
  }
}
function showHelp(){
  const title='HOW TO SURVIVE BLACKWOOD';
  const body='<div class="v06-help-grid"><div><b>Night AP</b><span>Used for travel, investigation, resting, and exploration.</span></div><div><b>Combat AP</b><span>Used only during fights. It is separate from Night AP.</span></div><div><b>Fear & Sanity</b><span>High Fear and low Sanity make the night more dangerous.</span></div><div><b>Story Objective</b><span>Follow the objective and the glowing map target when one is available.</span></div><div><b>Transformations</b><span>Transforming survivors unlock their form only at low health during combat.</span></div><div><b>Blocked?</b><span>If a creature is alive at your location, defeat it before traveling or ending the Night.</span></div></div>';
  if(typeof v06CloseOverlay==='function'&&document.getElementById('v06Overlay')){
    const card=document.getElementById('v06Card');
    if(card){card.innerHTML=`<div class="v06-kicker">FIELD GUIDE</div><div class="v06-title">${title}</div>${body}<button onclick="v06CloseOverlay()">Close</button>`;document.getElementById('v06Overlay').classList.add('open');document.body.style.overflow='hidden';}
  }
}
function objectiveText(){return (document.getElementById('storyObjectiveText')?.textContent||'').trim()}
function activeSurvivor(){return hasGame()?(G.ps[G.active]||G.ps.find(p=>!p.dead)||G.ps[0]):null}
function transformStatus(p){
  if(!p||!p.transform)return '';
  if(p.transformed)return '⚡ Transformation: ACTIVE';
  let threshold=.4;
  try{if(typeof transformationThreshold==='function')threshold=transformationThreshold(p)}catch{}
  const max=Number(p.maxHp||p.baseMaxHp||1),hp=Number(p.hp||0),pct=max?hp/max:1;
  const ready=!!combatNow()&&pct<=threshold;
  return ready?'⚡ Transformation: READY':`⚡ Transformation: LOCKED — reach ${Math.round(threshold*100)}% HP in combat`;
}
function nextStep(){
  if(!hasGame())return {text:'',kind:''};
  const p=activeSurvivor();
  const c=combatNow();
  if(c)return {text:`Defeat ${c.name}. Combat AP is used for attacks and Specials.`,kind:'danger'};
  try{if(typeof hostileAtCurrentLocation==='function'&&p&&hostileAtCurrentLocation(p))return {text:'A creature is blocking this location. Fight it before traveling or ending the Night.',kind:'danger'}}catch{}
  if(p&&Number(p.actions||0)<=0)return {text:'You are out of Night AP. End the Night to restore Night AP and continue.',kind:'warn'};
  const objective=objectiveText();
  if(objective)return {text:`Follow the Story Objective: ${objective}`,kind:'story'};
  return {text:'Choose a connected location, investigate for clues and supplies, then keep following the Story Objective.',kind:'story'};
}
function highlightObjective(){
  document.querySelectorAll('.loc.v06-objective-target').forEach(el=>el.classList.remove('v06-objective-target'));
  const objective=objectiveText().toLowerCase();
  if(!objective)return;
  let best=null,bestLen=0;
  document.querySelectorAll('.loc').forEach(card=>{
    const txt=(card.textContent||'').trim().toLowerCase();
    if(!txt)return;
    const title=(card.querySelector('b')?.textContent||'').trim().toLowerCase();
    const candidate=title||txt.split('\n')[0];
    if(candidate.length>3&&objective.includes(candidate)&&candidate.length>bestLen){best=card;bestLen=candidate.length}
  });
  if(best)best.classList.add('v06-objective-target');
}
function explainLocks(){
  document.querySelectorAll('.loc.locked').forEach(el=>{el.title='Locked by story progression. Follow NEXT STEP / Story Objective to unlock this location.'});
  document.querySelectorAll('button:disabled').forEach(btn=>{
    const label=(btn.textContent||'').trim();
    if(!btn.title)btn.title=label.toLowerCase().includes('end night')?'Cannot end the Night while a hostile creature is unresolved here.':'This action is unavailable right now. Check NEXT STEP for the current requirement.';
  });
}
function coach(key,title,text){
  if(getSeen().has(key))return;
  const el=document.getElementById('v06Coach');if(!el)return;
  el.querySelector('#v06CoachTitle').textContent=title;el.querySelector('#v06CoachText').textContent=text;el.hidden=false;markSeen(key);
}
function contextualTips(){
  if(!hasGame()||document.body.classList.contains('menu-mode'))return;
  const p=activeSurvivor(),seen=getSeen();
  if(!seen.has('start')){coach('start','Start Here','Follow NEXT STEP and the Story Objective. Locations needed for an objective will glow when the game can identify them.');return}
  if(combatNow()&&!seen.has('combat')){coach('combat','Combat AP','Combat AP is separate from Night AP. Use it for attacks and Specials; party members can rotate when needed.');return}
  if(G.v06NightModifier&&!seen.has('modifier')){coach('modifier','Night Modifier',`${G.v06NightModifier.name} changes the rules of this Night. The badge at the top shows its effect.`);return}
  if(p?.transform&&!seen.has('transform'))coach('transform','Transformation','Your form is health-gated. NEXT STEP shows when the active survivor is READY to transform.');
}
function journalDot(){
  if(!hasGame())return;
  const count=(G.v06Journal||[]).length,last=Number(sessionStorage.getItem('theLastNightJournalReadCount')||0),dot=document.getElementById('v06JournalDot');
  if(dot)dot.hidden=!(count>last);
  const journal=document.getElementById('v06JournalBtn');
  if(journal&&!journal.dataset.v06ReadHook){journal.dataset.v06ReadHook='1';journal.addEventListener('click',()=>{sessionStorage.setItem('theLastNightJournalReadCount',String((G.v06Journal||[]).length));if(dot)dot.hidden=true})}
}
function syncDock(){
  const dock=document.getElementById('v06MobileDock');if(!dock)return;
  const ingame=hasGame()&&!document.body.classList.contains('menu-mode');dock.hidden=!ingame;
}
function syncGuidance(){
  ensureGuidanceUi();syncDock();
  const box=document.getElementById('v06Guidance');
  if(!box)return;
  const ingame=hasGame()&&!document.body.classList.contains('menu-mode');box.hidden=!ingame;if(!ingame)return;
  const step=nextStep(),p=activeSurvivor(),meta=[];
  if(p)meta.push(`Night AP: ${Math.max(0,Number(p.actions||0))}`);
  if(combatNow()&&p)meta.push(`Combat AP: ${Math.max(0,Number(p.combatActions||0))}`);
  const ts=transformStatus(p);if(ts)meta.push(ts);
  if(G.v06NightModifier)meta.push(`${G.v06NightModifier.icon||'🌙'} ${G.v06NightModifier.name}`);
  const t=document.getElementById('v06GuidanceText');if(t){t.className=`v06-guidance-text ${step.kind||''}`;t.textContent=step.text}
  const m=document.getElementById('v06GuidanceMeta');if(m)m.innerHTML=meta.map(x=>`<span>${x}</span>`).join('');
  highlightObjective();explainLocks();contextualTips();journalDot();
}
ensureGuidanceUi();
setInterval(syncGuidance,700);
document.addEventListener('visibilitychange',()=>{if(!document.hidden)syncGuidance()});
window.addEventListener('resize',syncGuidance);
syncGuidance();
})();
'''

css_append = r'''

/* V0.6 PLAYER GUIDANCE + MOBILE DOCK */
.v06-guidance{margin:8px 0 13px;padding:12px 14px;border:1px solid #4d4540;border-left:4px solid #c89b50;border-radius:9px;background:linear-gradient(90deg,rgba(43,34,24,.82),rgba(16,18,20,.94));box-shadow:0 8px 24px rgba(0,0,0,.22)}
.v06-guidance[hidden]{display:none!important}.v06-guidance-head{display:flex;align-items:center;justify-content:space-between;gap:10px;color:#efd5a2;font-size:11px;letter-spacing:1.4px}.v06-guidance-head button{width:30px;height:30px;min-width:30px;margin:0;padding:0;border-radius:50%;font-weight:900}.v06-guidance-text{margin-top:7px;color:#e6e7e9;font-size:13px;line-height:1.5}.v06-guidance-text.danger{color:#ffb3b9}.v06-guidance-text.warn{color:#f0d493}.v06-guidance-meta{display:flex;flex-wrap:wrap;gap:6px;margin-top:9px}.v06-guidance-meta span{padding:5px 8px;border:1px solid #3d4145;border-radius:99px;background:#111315;color:#bfc4c8;font-size:10px}.loc.v06-objective-target{outline:2px solid #d8ad58!important;box-shadow:0 0 0 2px rgba(216,173,88,.18),0 0 30px rgba(216,173,88,.32)!important;animation:v06ObjectivePulse 1.8s ease-in-out infinite}.loc.v06-objective-target:before{content:'OBJECTIVE';position:absolute;z-index:5;left:7px;top:7px;padding:4px 6px;border-radius:6px;background:#c6943f;color:#120d05;font-size:8px;font-weight:1000;letter-spacing:1px}.loc{position:relative}@keyframes v06ObjectivePulse{0%,100%{filter:none}50%{filter:brightness(1.12)}}
.v06-help-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px;margin:16px 0 20px;text-align:left}.v06-help-grid div{padding:12px;border:1px solid #34383c;border-radius:10px;background:#101214}.v06-help-grid b,.v06-help-grid span{display:block}.v06-help-grid b{color:#f0d0d3;margin-bottom:5px}.v06-help-grid span{color:#adb3b8;font-size:12px;line-height:1.5}
.v06-coach{position:fixed;left:18px;bottom:18px;z-index:17500;width:min(360px,calc(100vw - 36px));padding:13px 42px 13px 14px;border:1px solid #69434a;border-radius:12px;background:rgba(13,15,17,.96);box-shadow:0 16px 45px #000}.v06-coach[hidden]{display:none!important}.v06-coach b,.v06-coach span{display:block}.v06-coach b{color:#e7bdc1;font-size:12px;letter-spacing:.5px}.v06-coach span{margin-top:4px;color:#bdc2c6;font-size:11px;line-height:1.5}.v06-coach button{position:absolute;right:6px;top:5px;width:30px;height:30px;margin:0;padding:0;background:transparent;border:0;font-size:20px}
.v06-mobile-dock{display:none}.v06-mobile-dock[hidden]{display:none!important}
#v06JournalDot{position:absolute;right:16px;top:7px;width:8px;height:8px;border-radius:50%;background:#e85260;box-shadow:0 0 10px #e85260}#v06JournalDot[hidden]{display:none}
body.reduce-motion .loc.v06-objective-target{animation:none!important}
@media(max-width:850px){
  body:not(.menu-mode) #logButton,body:not(.menu-mode) .v06-journal-btn{display:none!important}
  .v06-mobile-dock{position:fixed;left:8px;right:8px;bottom:max(8px,env(safe-area-inset-bottom));z-index:10060;display:grid;grid-template-columns:repeat(3,1fr);gap:6px;padding:7px;border:1px solid #54343a;border-radius:14px;background:rgba(8,9,11,.96);box-shadow:0 14px 40px #000;backdrop-filter:blur(12px)}
  .v06-mobile-dock button{position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;min-height:48px;margin:0;padding:6px 4px;font-size:16px}.v06-mobile-dock button span{font-size:9px;font-weight:900;letter-spacing:.5px}
  body:not(.menu-mode) #extraPocketsPanel{bottom:74px!important;max-height:min(58vh,480px)!important}
  body:not(.menu-mode) #extraPocketsPanel.mobile-pack-collapsed{bottom:74px!important;max-height:58px!important}
  #gameSite.wrap{padding-bottom:148px!important}
  .v06-coach{left:10px;right:10px;bottom:78px;width:auto}
  .v06-guidance{padding:11px 12px}.v06-guidance-meta{gap:5px}.v06-guidance-meta span{font-size:9px}
  .v06-help-grid{grid-template-columns:1fr}
}
@media(max-width:420px){.v06-mobile-dock{left:6px;right:6px}.v06-mobile-dock button{min-height:46px}.v06-guidance-text{font-size:12px}}
'''

if JS_MARK not in js:
    js_path.write_text(js + js_append)
if CSS_MARK not in css:
    css_path.write_text(css + css_append)

print('V0.6 usability guidance and mobile dock applied.')
