from pathlib import Path
import re

# --- V0.6 enhancement layer ---
p=Path('v06-enhancements.js')
s=p.read_text(encoding='utf-8')

# Keep Journal UI scoped to active gameplay/save.
s=s.replace("if(!inGame){const b=document.getElementById('v06NightBadge');if(b)b.hidden=true}","if(!inGame){const b=document.getElementById('v06NightBadge');if(b)b.hidden=true;const o=document.getElementById('v06Overlay');if(o&&o.classList.contains('open'))close()}",1)
s=s.replace("function openJournal(){if(!hasGame())return;","function openJournal(){if(!hasGame()||document.body.classList.contains('menu-mode'))return;G.v06JournalReadCount=(G.v06Journal||[]).length;",1)

pattern=r"function journalDot\(\)\{.*?\n\}"
replacement="""function journalDot(){
  if(!hasGame())return;
  const count=(G.v06Journal||[]).length,last=Number(G.v06JournalReadCount||0),dot=document.getElementById('v06JournalDot');
  if(dot)dot.hidden=!(count>last);
  const journal=document.getElementById('v06JournalBtn');
  if(journal&&!journal.dataset.v06ReadHook){journal.dataset.v06ReadHook='1';journal.addEventListener('click',()=>{G.v06JournalReadCount=(G.v06Journal||[]).length;if(dot)dot.hidden=true})}
}"""
s,n=re.subn(pattern,replacement,s,count=1,flags=re.S)
if n!=1: raise SystemExit('journalDot function not found')

highlight_pattern=r"function highlightObjective\(\)\{.*?\n\}"
highlight_replacement="""function highlightObjective(){
  document.querySelectorAll('.loc.v06-objective-target').forEach(el=>el.classList.remove('v06-objective-target'));
  const objective=objectiveText().toLowerCase();
  if(!objective)return;
  const cleared=hasGame()?G.v06ClearedObjectiveTarget:null;
  let best=null,bestLen=0;
  document.querySelectorAll('.loc').forEach(card=>{
    const txt=(card.textContent||'').trim().toLowerCase();
    if(!txt)return;
    const title=(card.querySelector('b')?.textContent||'').trim().toLowerCase();
    const candidate=title||txt.split('\\n')[0];
    const locKey=card.dataset?.loc||card.getAttribute('data-location')||candidate;
    if(cleared&&cleared.objective===objective&&(cleared.loc===locKey||cleared.title===candidate))return;
    if(candidate.length>3&&objective.includes(candidate)&&candidate.length>bestLen){best=card;bestLen=candidate.length}
  });
  if(best)best.classList.add('v06-objective-target');
}"""
s,n=re.subn(highlight_pattern,lambda _m: highlight_replacement,s,count=1,flags=re.S)
if n!=1: raise SystemExit('highlightObjective function not found')

# Objective glow completion must follow actual clue progression, not AP consumption.
wrap_pattern=r"if\(typeof investigate==='function'\)\{const o=investigate;window\.investigate=function\(\)\{.*?\n\}\}"
wrap_replacement="""if(typeof investigate==='function'){const o=investigate;window.investigate=function(){
  const p0=hasGame()?G.ps[G.active]:null,obj0=objectiveText().trim().toLowerCase(),loc0=p0?.loc,clues0=Number(G?.clues||0);
  const finish=()=>{if(!hasGame())return;const p1=G.ps[G.active],clues1=Number(G?.clues||0);if(p1?.loc===loc0&&clues1>clues0&&obj0){const card=[...document.querySelectorAll('.loc')].find(c=>{const title=(c.querySelector('b')?.textContent||'').trim().toLowerCase();return title&&obj0.includes(title)});if(card){const title=(card.querySelector('b')?.textContent||'').trim().toLowerCase();const key=card.dataset?.loc||card.getAttribute('data-location')||title;G.v06ClearedObjectiveTarget={objective:obj0,loc:key,title};}}window.v06SyncGuidance?.()};
  if(hasGame()&&!currentCombat()&&Math.random()<.30){explore(function(){const r=o.apply(this,arguments);setTimeout(finish,0);setTimeout(finish,120);return r},arguments);return}
  const r=o.apply(this,arguments);setTimeout(finish,0);setTimeout(finish,120);hallucinate();anomaly();return r
}}"""
s,n=re.subn(wrap_pattern,lambda _m: wrap_replacement,s,count=1,flags=re.S)
if n!=1: raise SystemExit('investigate wrapper not found')

if 'theLastNightJournalReadCount' in s: raise SystemExit('shared Journal read-state still present')
if 'clues1>clues0' not in s: raise SystemExit('objective glow is not tied to clue advancement')
if "txt.split('\\n')[0]" not in s: raise SystemExit('objective title fallback newline escape missing')
p.write_text(s,encoding='utf-8')

# --- Core investigate/story progression ---
p=Path('index.html')
h=p.read_text(encoding='utf-8')

investigate_pattern=r"\s*function investigate\(\)\{.*?\n\}\nfunction flashlightSceneFor"
investigate_replacement="""
function ensureStoryProgress(){
  if(!G)return 0;
  if(!(G.foundClues instanceof Set)){
    const raw=Array.isArray(G.foundClues)?G.foundClues:[];
    G.foundClues=new Set(raw);
  }
  const stored=Math.max(0,Math.min(10,Number(G.clues)||0));
  if(G.foundClues.size===0&&stored>0){
    for(let i=0;i<stored&&i<STORY_OBJECTIVES.length;i++)G.foundClues.add(STORY_OBJECTIVES[i].loc);
  }
  let ordered=0;
  while(ordered<STORY_OBJECTIVES.length&&G.foundClues.has(STORY_OBJECTIVES[ordered].loc))ordered++;
  G.clues=ordered;
  return ordered;
}

function investigate(){
  const p=G.ps[G.active];
  if(combat||hostileAtCurrentLocation(p)){
    log(`⚔️ ${p.name} cannot Investigate while a creature controls this location.`,"bad");
    render();
    return false;
  }

  ensureStoryProgress();
  const free=!p.freeInvestigateUsed;
  if(!free&&p.actions<1){
    log(`⚡ ${p.name} needs 1 Action to Investigate again.`,"bad");
    render();
    return false;
  }

  const before=G.clues;
  const advanced=gainClue();
  if(!advanced){
    updateStoryObjective();
    render();
    return false;
  }

  if(free){
    p.freeInvestigateUsed=true;
    log(`🔎 ${p.name} uses their FREE Investigate for Night ${G.night}.`,"good");
  }else{
    p.actions-=1;
    log(`🔎 ${p.name} Investigates for 1 Action.`,"good");
  }
  updateStoryObjective();
  log(`📍 Objective advanced: ${before+1} → ${G.clues}.`,"good");
  render();
  return true;
}
function flashlightSceneFor"""
h,n=re.subn(investigate_pattern,lambda _m: investigate_replacement,h,count=1,flags=re.S)
if n!=1: raise SystemExit('core investigate function not found')

gain_pattern=r"function gainClue\(\)\{.*?\n\}\n\nfunction encounter\(\)"
gain_replacement="""function gainClue(){
  const p=G.ps[G.active];
  ensureStoryProgress();
  const currentObjective=STORY_OBJECTIVES[G.clues];
  const clue=STORY_CLUES[p.loc];

  if(currentObjective&&p.loc!==currentObjective.loc){
    log(`📜 CURRENT OBJECTIVE: ${currentObjective.text}`,"bad");
    return false;
  }
  if(!clue){
    log(`🔎 There is no major story clue at ${LM[p.loc][1]}.`);
    return false;
  }
  if(G.foundClues.has(p.loc)){
    ensureStoryProgress();
    updateStoryObjective();
    log(`📖 ${LM[p.loc][1]} was already investigated. The next objective is now shown.`,"good");
    return false;
  }

  G.foundClues.add(p.loc);
  ensureStoryProgress();
  log(`📖 STORY CLUE FOUND: <b>${clue.name}</b>`,"good");
  log(`${clue.story}`,"good");
  updateStoryObjective();
  if(G.clues===10){
    log(`📖 ALL 10 STORY CLUES FOUND! The truth of Blackwood has been uncovered. New story objectives await.`,"good");
  }
  return true;
}

function encounter()"""
h,n=re.subn(gain_pattern,lambda _m: gain_replacement,h,count=1,flags=re.S)
if n!=1: raise SystemExit('gainClue function not found')

if 'function ensureStoryProgress()' not in h: raise SystemExit('story progress repair missing')
if 'const advanced=gainClue();' not in h: raise SystemExit('investigate advancement guard missing')
if 'return true;\n}\n\nfunction encounter()' not in h: raise SystemExit('gainClue success return missing')
p.write_text(h,encoding='utf-8')
print('repaired Investigate, ordered objective progression, and objective glow completion')