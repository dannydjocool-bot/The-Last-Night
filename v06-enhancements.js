/* THE LAST NIGHT — V0.6 BLACKWOOD FEELS ALIVE */
(function(){
const MODS=[
{name:'Heavy Fog',icon:'🌫️',desc:'Travel may raise Fear.',kind:'fog'},
{name:'Blood Moon',icon:'🩸',desc:'Creatures deal +2 damage.',kind:'blood'},
{name:'Dead Silence',icon:'🔇',desc:'Travel may drain Sanity.',kind:'silence'},
{name:'Blackwood Storm',icon:'⛈️',desc:'Travel may cost 1 extra Night AP.',kind:'storm'},
{name:'Restless Dead',icon:'☠️',desc:'Travel may attract another creature.',kind:'restless'}
];
const LOC={
motel:['A room door clicks shut by itself.','The vacancy sign buzzes, then dies.'],gas:['A fuel pump ticks with no power.','Metal drags behind the pumps.'],store:['A shopping cart rolls one aisle and stops.','Glass crunches somewhere behind the counter.'],station:['A dead radio spits out half a sentence.','Footsteps cross the evidence corridor with nobody there.'],library:['A book falls open to a page with your name on it.','Shelves creak as if something is moving between them.'],apartments:['A television flickers on behind a chained door.','Someone walks across the floor above you.'],firestation:['The empty engine bay bell rings once.','A locker door slowly swings open.'],cemetery:['Wet soil shifts beside a fresh grave.','A stone angel seems to face a different direction.'],chapel:['The altar candles ignite without flame.','A whisper answers from beneath the pews.'],monastery:['A bell rings from a tower that collapsed years ago.','Robed footsteps circle the cloister.'],cabins:['A porch light glows inside an abandoned cabin.','A window curtain moves although there is no wind.'],forest:['Branches snap in a circle around you.','A whisper repeats a survivor’s name.'],huntercamp:['A cold campfire briefly gives off smoke.','A trap chain rattles somewhere in the brush.'],junkyard:['A car horn sounds beneath a crushed vehicle.','The scrap crane swings a few inches on its own.'],farm:['Dead corn bends away from the party.','Something heavy crosses the barn loft.'],sawmill:['A rusted saw blade turns once.','Wet boards knock together like footsteps.'],hospital:['A patient call light flashes in an empty ward.','A gurney wheel squeaks down the corridor.'],school:['A locker slams at the far end of the hall.','A classroom intercom whispers static and breathing.'],sewers:['Water ripples against the current.','A second set of footsteps splashes behind you.'],tunnel:['A maintenance light turns red ahead.','A voice echoes through the pipes.'],bridge:['A shadow crosses beneath the broken roadway.','Metal groans from the collapsed span.'],subway:['A dead train speaker announces a station that does not exist.','Something knocks from inside the derailed car.'],house:['A chair drags across the upstairs floor.','The front door locks behind the party.'],hotel:['The front desk bell rings twice.','An elevator indicator lights up with no power.'],factory:['A machine starts for one second and dies.','Chains swing above the flooded floor.'],mines:['A mine cart wheel turns in the darkness.','Rock dust falls as something moves above.'],massgrave:['A shovel shifts in the mud.','The ground settles like something exhaled beneath it.'],basement:['A lightbulb swings though the air is still.','Something scratches behind the foundation wall.'],slaughterhouse:['A hanging hook sways without wind.','Something wet drips behind the wall.'],prison:['Chains scrape behind a sealed cell.','A steel door slams three times.'],asylum:['A broken intercom whispers.','Someone laughs one floor above.'],laboratory:['A specimen tank bubbles although the power is dead.','A monitor flashes a heartbeat for one second.'],ritual:['The black altar feels warm to the touch.','The ritual circle darkens around your feet.'],hollow:['The darkness seems to inhale.','Your footsteps return one beat too late.'],root:['The walls pulse like a buried heart.','Roots tighten beneath the floor.'],gate:['Something stands beyond the county line, then vanishes.','The chains on the gate twitch by themselves.']
};
const BOSS=new Set(['Legendary','Mythic','Ancient','Abyssal']);
const pick=a=>a[Math.floor(Math.random()*a.length)];
const hasGame=()=>typeof G!=='undefined'&&G&&Array.isArray(G.ps);
const currentCombat=()=>typeof combat!=='undefined'?combat:null;
function j(text,type='EVENT'){if(!hasGame())return;G.v06Journal=G.v06Journal||[];G.v06Journal.unshift({night:G.night||1,type,text});G.v06Journal=G.v06Journal.slice(0,80)}
function lg(text,kind=''){if(hasGame()&&typeof log==='function'){log(text,kind);j(String(text).replace(/<[^>]+>/g,''))}}
function ui(){if(document.getElementById('v06JournalBtn'))return;document.body.insertAdjacentHTML('beforeend','<button id="v06JournalBtn" class="v06-journal-btn" hidden>📓 BLACKWOOD JOURNAL</button><div id="v06NightBadge" class="v06-night-badge" hidden></div><div id="v06Overlay" class="v06-overlay"><div id="v06Card" class="v06-card"></div></div>');document.getElementById('v06JournalBtn').onclick=openJournal}
function syncUi(){ui();const btn=document.getElementById('v06JournalBtn');const inGame=hasGame()&&!document.body.classList.contains('menu-mode');btn.hidden=!inGame;if(!inGame){const b=document.getElementById('v06NightBadge');if(b)b.hidden=true;const o=document.getElementById('v06Overlay');if(o&&o.classList.contains('open'))close()}}
function show(html){ui();document.getElementById('v06Card').innerHTML=html;document.getElementById('v06Overlay').classList.add('open');document.body.style.overflow='hidden'}
function close(){const o=document.getElementById('v06Overlay');if(o)o.classList.remove('open');document.body.style.overflow=''}
window.v06CloseOverlay=close;
function openJournal(){if(!hasGame()||document.body.classList.contains('menu-mode'))return;G.v06JournalReadCount=(G.v06Journal||[]).length;const rows=(G.v06Journal||[]).map(e=>`<div class="v06-journal-entry"><b>NIGHT ${e.night} · ${e.type}</b><br>${e.text}</div>`).join('')||'<p class="v06-copy">The journal is still empty.</p>';show(`<div class="v06-kicker">CASE NOTES</div><div class="v06-title">BLACKWOOD JOURNAL</div><p class="v06-copy">Events, hallucinations, discoveries, relationships, and warnings from this run.</p><div class="v06-journal-list">${rows}</div><button onclick="v06CloseOverlay()">Close</button>`)}
function mod(){return hasGame()?G.v06NightModifier||null:null}
function badge(){ui();const b=document.getElementById('v06NightBadge'),m=mod();if(!hasGame()||document.body.classList.contains('menu-mode')||!m){b.hidden=true;return}b.hidden=false;b.innerHTML=`<b>${m.icon} ${m.name}</b><br>${m.desc}`}
function newNightMod(){if(!hasGame()||document.body.classList.contains('menu-mode'))return;G.v06NightModifier={...pick(MODS)};const m=G.v06NightModifier;j(`${m.name}: ${m.desc}`,'NIGHT MODIFIER');badge();show(`<div class="v06-kicker">BLACKWOOD CHANGES</div><div class="v06-title">NIGHT ${G.night}</div><p class="v06-copy"><b>${m.icon} ${m.name}</b><br>${m.desc}</p><button onclick="v06CloseOverlay()">Enter the Night</button>`)}
function validateMind(p){if(p&&typeof check==='function')check(p,currentCombat())}
function psych(){if(!hasGame())return;const p=G.ps[G.active]||G.ps[0];document.body.classList.toggle('v06-fear-high',(p.fear||0)>=3);document.body.classList.toggle('v06-fear-critical',(p.fear||0)>=5);document.body.classList.toggle('v06-sanity-low',(p.san||0)<=3)}
function atmosphere(loc){if(Math.random()<.72)lg(`🎧 ${pick(LOC[loc]||['Something shifts beyond the light.'])}`);if(typeof ensureHorrorAudio==='function')ensureHorrorAudio()}
function hallucinate(){if(!hasGame())return;const p=G.ps[G.active];if((p.fear||0)>=4&&Math.random()<.22)lg(`👁️ ${p.name} swears someone is standing behind the party. There is nobody there.`,'bad');if((p.san||0)<=3&&Math.random()<.22)lg(`🧠 ${p.name} hears a familiar voice coming from somewhere impossible.`,'bad')}
function anomaly(){if(!hasGame()||Math.random()>=.035)return;document.body.classList.add('v06-glitch');setTimeout(()=>document.body.classList.remove('v06-glitch'),1100);const t=pick(['Every location name looks wrong for one second.','A survivor portrait appears to blink.','The event log shows a sentence that vanishes instantly.','A shape appears behind the interface, then is gone.']);lg(`⚠️ SOMETHING IS WRONG — ${t}`,'bad');j(t,'ANOMALY')}
function bonds(){if(!hasGame())return{};G.v06Bonds=G.v06Bonds||{};return G.v06Bonds}
function bk(a,b){return [a,b].sort().join('::')}
function grow(){if(!hasGame())return;const live=G.ps.filter(p=>!p.dead);for(let i=0;i<live.length;i++)for(let k=i+1;k<live.length;k++){const key=bk(live[i].originalName||live[i].name,live[k].originalName||live[k].name);bonds()[key]=(bonds()[key]||0)+1;if(bonds()[key]===3)lg(`🤝 ${live[i].name} and ${live[k].name} have developed Trust.`,'good')}}
function bestBond(p){let best=0;if(!hasGame())return 0;for(const o of G.ps){if(o===p||o.dead)continue;best=Math.max(best,bonds()[bk(p.originalName||p.name,o.originalName||o.name)]||0)}return best}
function travelMod(){const m=mod();if(!m||!hasGame())return;const p=G.ps[G.active];if(m.kind==='fog'&&Math.random()<.28){p.fear=Math.min(5,(p.fear||0)+1);lg(`🌫️ Heavy Fog closes around ${p.name}. +1 Fear.`,'bad');G.v06LastEffect='Heavy Fog: +1 Fear';G.v06LastEffectAt=Date.now();window.v06SyncGuidance?.()}if(m.kind==='silence'&&Math.random()<.25){p.san=Math.max(0,(p.san||0)-1);lg(`🔇 Dead Silence presses against ${p.name}. -1 Sanity.`,'bad');G.v06LastEffect='Dead Silence: -1 Sanity';G.v06LastEffectAt=Date.now();window.v06SyncGuidance?.();validateMind(p)}if(m.kind==='storm'&&p.actions>0&&Math.random()<.25){p.actions--;lg('⛈️ The Blackwood Storm steals 1 extra Night AP.','bad');G.v06LastEffect='Blackwood Storm: -1 Night AP';G.v06LastEffectAt=Date.now();window.v06SyncGuidance?.()}if(m.kind==='restless'&&Math.random()<.22&&typeof spawn==='function'){spawn(p.loc);lg(`☠️ Restless Dead follow the party into ${LM[p.loc][1]}.`,'bad');G.v06LastEffect='Restless Dead: another creature was attracted';G.v06LastEffectAt=Date.now();window.v06SyncGuidance?.()}psych()}
function phase(c){if(!c?.maxHp||c.hp<=0)return;const r=c.hp/c.maxHp,ph=r<=.25?3:r<=.5?2:r<=.75?1:0;c.v06Phase=c.v06Phase||0;if(ph<=c.v06Phase)return;while(c.v06Phase<ph){c.v06Phase++;const b=c.v06Phase===3?2:1;c.atk+=b;lg(`🩸 ${c.name} enters PHASE ${c.v06Phase+1}: wounded and more dangerous (+${b} ATK).`,'bad');j(`${c.name} entered phase ${c.v06Phase+1}.`,'CREATURE PHASE')}}
function bossIntro(c,id){c.v06Introduced=true;show(`<div class="v06-kicker">${c.rarity.toUpperCase()} ENCOUNTER</div><div class="v06-title">${c.name}</div><img src="${c.image}" alt="${c.name}" style="width:min(360px,80vw);max-height:44vh;object-fit:contain;background:#060708;border-radius:12px;border:1px solid #63333a"><p class="v06-copy">${c.ability||'Blackwood has sent something terrible.'}</p><button id="v06FaceBoss">FACE ${c.name.toUpperCase()}</button>`);document.getElementById('v06FaceBoss').onclick=()=>{close();if(typeof horrorTone==='function'){horrorTone('warning');setTimeout(()=>horrorTone('enemy'),250)}window.__v06StartCombat(String(id));const p=hasGame()?G.ps[G.active]:null;if(p&&bestBond(p)>=3&&currentCombat()){p.combatActions=(p.combatActions||0)+1;lg(`🤝 TRUST BONUS: ${p.name} gains +1 Combat Action.`,'good')}};j(`${c.name} revealed itself.`,'BOSS')}
function explore(original,args){const p=G.ps[G.active],name=LM?.[p.loc]?.[1]||p.loc;show(`<div class="v06-kicker">EXPLORATION CHOICE</div><div class="v06-title">${name}</div><p class="v06-copy">How does ${p.name} search?</p><div class="v06-choices"><button id="v06Careful">CAREFUL SEARCH<br><small>Steady investigation</small></button><button id="v06Deep">SEARCH DEEPER<br><small>Risk Fear for extra loot</small></button><button id="v06Listen">STOP & LISTEN<br><small>Risk Sanity for warning</small></button></div>`);document.getElementById('v06Careful').onclick=()=>{close();original.apply(window,args)};document.getElementById('v06Deep').onclick=()=>{close();p.fear=Math.min(5,(p.fear||0)+1);original.apply(window,args);if(!currentCombat()&&Math.random()<.55&&typeof gainItem==='function'){gainItem();lg(`🎒 ${p.name}'s deeper search uncovers an additional item.`,'good')}psych()};document.getElementById('v06Listen').onclick=()=>{close();p.san=Math.max(0,(p.san||0)-1);validateMind(p);original.apply(window,args);if(!currentCombat()&&Math.random()<.5)lg(`👂 ${p.name} hears movement before it reaches the room.`,'good');psych()}}
ui();syncUi();
new MutationObserver(()=>{syncUi();syncDock();}).observe(document.body,{attributes:true,attributeFilter:['class']});
if(typeof move==='function'){const o=move;window.move=async function(){const before=hasGame()?G.ps[G.active]?.loc:null;const r=await o.apply(this,arguments);if(hasGame()&&G.ps[G.active]?.loc!==before){atmosphere(G.ps[G.active].loc);travelMod();hallucinate();anomaly();badge()}return r}}
if(typeof search==='function'){const o=search;window.search=function(){if(hasGame()&&!currentCombat()&&Math.random()<.30){explore(o,arguments);return}const r=o.apply(this,arguments);hallucinate();anomaly();return r}}
if(typeof endNight==='function'){const o=endNight;window.endNight=function(){const old=hasGame()?G.night:null;const r=o.apply(this,arguments);if(hasGame()&&G.night!==old)setTimeout(newNightMod,1650);return r}}
if(typeof startCombat==='function'){const o=startCombat;window.__v06StartCombat=o;window.startCombat=function(id){const c=hasGame()?G.creatures?.find(x=>String(x.id)===String(id)):null;if(c&&BOSS.has(c.rarity)&&!c.v06Introduced){bossIntro(c,id);return}const r=o.apply(this,arguments);const p=hasGame()?G.ps[G.active]:null;if(p&&bestBond(p)>=3&&currentCombat()){p.combatActions=(p.combatActions||0)+1;lg(`🤝 TRUST BONUS: ${p.name} gains +1 Combat Action.`,'good')}return r}}
if(typeof creatureAttack==='function'){const o=creatureAttack;window.creatureAttack=function(c){phase(c);const blood=mod()?.kind==='blood';if(blood&&c){c.atk+=2;try{return o.apply(this,arguments)}finally{c.atk-=2}}return o.apply(this,arguments)}}
if(typeof showPostCombatReward==='function'){const o=showPostCombatReward;window.showPostCombatReward=function(){grow();return o.apply(this,arguments)}}
if(typeof render==='function'){const o=render;window.render=function(){const c=currentCombat();if(c)phase(c);const r=o.apply(this,arguments);psych();badge();syncUi();return r}}
setInterval(()=>{const c=currentCombat();if(c&&BOSS.has(c.rarity)&&typeof horrorTone==='function'&&Math.random()<.55)horrorTone(c.rarity==='Abyssal'?'enemy':'warning')},5200);
})();

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
      box.innerHTML='<div class="v06-guidance-head"><b>🧭 NEXT STEP</b><button id="v06GuidanceHelp" type="button">?</button></div><div id="v06GuidanceText"></div><div id="v06GuidanceLock" class="v06-guidance-lock" hidden></div><div id="v06GuidanceMeta"></div>';
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
  const body='<div class="v06-help-grid"><div><b>Night AP</b><span>Used for travel, investigation, resting, and exploration.</span></div><div><b>Combat AP</b><span>Used only during fights. It is separate from Night AP.</span></div><div><b>Fear & Sanity</b><span>High Fear and low Sanity make the night more dangerous.</span></div><div><b>Story Objective</b><span>Follow the objective and the glowing map target when one is available.</span></div><div><b>Transformations</b><span>Transforming survivors unlock their form only at low health during combat.</span></div><div><b>Blocked?</b><span>If a creature is alive at your location, defeat it before traveling or ending the Night.</span></div></div><button type="button" class="v06-show-tips" onclick="v06ResetTips()">Show Tips Again</button>';
  if(typeof v06CloseOverlay==='function'&&document.getElementById('v06Overlay')){
    const card=document.getElementById('v06Card');
    if(card){card.innerHTML=`<div class="v06-kicker">FIELD GUIDE</div><div class="v06-title">${title}</div>${body}<button onclick="v06CloseOverlay()">Close</button>`;document.getElementById('v06Overlay').classList.add('open');document.body.style.overflow='hidden';}
  }
}
function objectiveText(){return (document.getElementById('storyObjectiveText')?.textContent||'').trim()}
function activeObjectiveText(){
  if(hasGame()&&typeof STORY_OBJECTIVES!=='undefined'&&Array.isArray(STORY_OBJECTIVES)){
    const current=STORY_OBJECTIVES[Number(G.clues||0)];
    if(current?.text)return String(current.text).trim();
  }
  const el=document.getElementById('storyObjectiveText');
  const raw=(el?.innerText||el?.textContent||'').trim();
  const marker=raw.lastIndexOf('➡️');
  return marker>=0?raw.slice(marker+2).trim():raw;
}
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
  const objective=activeObjectiveText();
  if(objective)return {text:`Follow the Story Objective: ${objective}`,kind:'story'};
  return {text:'Choose a connected location, investigate for clues and supplies, then keep following the Story Objective.',kind:'story'};
}
function highlightObjective(){
  document.querySelectorAll('.loc.v06-objective-target').forEach(el=>el.classList.remove('v06-objective-target'));
  const objective=activeObjectiveText().toLowerCase();
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
window.v06RefreshObjectiveGlow=highlightObjective;
function visibleLockReason(){
  if(!hasGame())return '';
  const p=activeSurvivor(),c=combatNow();
  if(c)return `🔒 Travel and Night actions are locked until ${c.name} is defeated.`;
  try{if(typeof hostileAtCurrentLocation==='function'&&p&&hostileAtCurrentLocation(p))return '🔒 Travel is locked because a hostile creature is still at this location.'}catch{}
  if(p&&Number(p.actions||0)<=0)return '🔒 Exploration actions are locked because this survivor has no Night AP left.';
  return '';
}
function trustStatus(p){
  if(!p||!hasGame())return '';
  const names=[p.originalName||p.name,p.name].filter(Boolean),b=G.v06Bonds||{};let best=0;
  for(const [key,val] of Object.entries(b)){if(names.some(n=>key.split('::').includes(n)))best=Math.max(best,Number(val)||0)}
  return `🤝 Trust: ${Math.min(3,best)}/3`;
}
function rootProgress(){
  if(!hasGame())return '';
  const obj=objectiveText().toLowerCase(),n=Math.min(3,Array.isArray(G.rootGateMinionsDefeated)?G.rootGateMinionsDefeated.length:0);
  const relevant=n>0||G.rootFusionTriggered||G.rootFusionPending||G.rootFusionDefeated||G.rootGateUnlocked||obj.includes('root')||obj.includes('guardian')||obj.includes('triune');
  if(!relevant)return '';
  const triune=G.rootFusionDefeated?'✅':(G.rootFusionTriggered||G.rootFusionPending||n>=3?'⚔️':'🔒');
  const root=G.rootGateUnlocked?'⚔️':'🔒';
  return `🗝️ Guardians ${n}/3 · Triune ${triune} · Root ${root}`;
}
function resetNewRunTips(){
  if(!hasGame()||Number(G.night||1)!==1||G.v06GuidanceRunStarted)return;
  G.v06GuidanceRunStarted=true;
  const seen=getSeen();['start','ap','modifier','transform'].forEach(k=>seen.delete(k));localStorage.setItem(TIP_KEY,JSON.stringify([...seen]));
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
  const count=(G.v06Journal||[]).length,last=Number(G.v06JournalReadCount||0),dot=document.getElementById('v06JournalDot');
  if(dot)dot.hidden=!(count>last);
  const journal=document.getElementById('v06JournalBtn');
  if(journal&&!journal.dataset.v06ReadHook){journal.dataset.v06ReadHook='1';journal.addEventListener('click',()=>{G.v06JournalReadCount=(G.v06Journal||[]).length;if(dot)dot.hidden=true})}
}
function syncDock(){
  const dock=document.getElementById('v06MobileDock');if(!dock)return;
  const ingame=hasGame()&&!document.body.classList.contains('menu-mode');dock.hidden=!ingame;
}
function syncGuidance(){
  ensureGuidanceUi();syncDock();resetNewRunTips();
  const box=document.getElementById('v06Guidance');
  if(!box)return;
  const ingame=hasGame()&&!document.body.classList.contains('menu-mode');box.hidden=!ingame;if(!ingame)return;
  const step=nextStep(),p=activeSurvivor(),meta=[];
  if(p)meta.push(`Night AP: ${Math.max(0,Number(p.actions||0))}`);
  if(combatNow()&&p)meta.push(`Combat AP: ${Math.max(0,Number(p.combatActions||0))}`);
  const ts=transformStatus(p);if(ts)meta.push(ts);
  if(G.v06NightModifier)meta.push(`${G.v06NightModifier.icon||'🌙'} ${G.v06NightModifier.name}`);
  const trust=trustStatus(p);if(trust)meta.push(trust);
  const root=rootProgress();if(root)meta.push(root);
  if(G.v06LastEffect&&Date.now()-Number(G.v06LastEffectAt||0)<10000)meta.push(`⚠️ ${G.v06LastEffect}`);
  const t=document.getElementById('v06GuidanceText');if(t){t.className=`v06-guidance-text ${step.kind||''}`;t.textContent=step.text}
  const lock=document.getElementById('v06GuidanceLock'),reason=visibleLockReason();if(lock){lock.hidden=!reason;lock.textContent=reason}
  const m=document.getElementById('v06GuidanceMeta');if(m)m.innerHTML=meta.map(x=>`<span>${x}</span>`).join('');
  highlightObjective();explainLocks();contextualTips();journalDot();
}
window.v06SyncGuidance=syncGuidance;
window.v06ResetTips=()=>{localStorage.removeItem(TIP_KEY);const c=document.getElementById('v06Coach');if(c)c.hidden=true;if(typeof v06CloseOverlay==='function')v06CloseOverlay();syncGuidance();};
ensureGuidanceUi();
setInterval(syncGuidance,700);
document.addEventListener('visibilitychange',()=>{if(!document.hidden)syncGuidance()});
window.addEventListener('resize',syncGuidance);
syncGuidance();
})();
