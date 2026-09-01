from pathlib import Path
import re

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

# Objective glow: once the player successfully investigates the location named by the
# current objective, do not keep highlighting that same card while objective text catches up.
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
s,n=re.subn(highlight_pattern,highlight_replacement,s,count=1,flags=re.S)
if n!=1: raise SystemExit('highlightObjective function not found')

# Wrap investigate so a completed investigation clears the stale target immediately.
old="if(typeof investigate==='function'){const o=investigate;window.investigate=function(){if(hasGame()&&!currentCombat()&&Math.random()<.30){explore(o,arguments);return}const r=o.apply(this,arguments);hallucinate();anomaly();return r}}"
new="""if(typeof investigate==='function'){const o=investigate;window.investigate=function(){
  const p0=hasGame()?G.ps[G.active]:null,obj0=objectiveText().trim().toLowerCase(),loc0=p0?.loc,ap0=Number(p0?.actions||0);
  const finish=()=>{if(!hasGame())return;const p1=G.ps[G.active],ap1=Number(p1?.actions||0);if(p1?.loc===loc0&&ap1<ap0&&obj0){const card=[...document.querySelectorAll('.loc')].find(c=>{const title=(c.querySelector('b')?.textContent||'').trim().toLowerCase();return title&&obj0.includes(title)});if(card){const title=(card.querySelector('b')?.textContent||'').trim().toLowerCase();const key=card.dataset?.loc||card.getAttribute('data-location')||title;G.v06ClearedObjectiveTarget={objective:obj0,loc:key,title};}}window.v06SyncGuidance?.()};
  if(hasGame()&&!currentCombat()&&Math.random()<.30){explore(function(){const r=o.apply(this,arguments);setTimeout(finish,0);setTimeout(finish,120);return r},arguments);return}
  const r=o.apply(this,arguments);setTimeout(finish,0);setTimeout(finish,120);hallucinate();anomaly();return r
}}"""
if old in s:
    s=s.replace(old,new,1)
elif 'G.v06ClearedObjectiveTarget={objective:obj0' not in s:
    raise SystemExit('investigate wrapper not found')

if 'theLastNightJournalReadCount' in s: raise SystemExit('shared Journal read-state still present')
if "document.body.classList.contains('menu-mode'))return;G.v06JournalReadCount" not in s: raise SystemExit('Journal menu guard missing')
if 'last=Number(G.v06JournalReadCount||0)' not in s: raise SystemExit('save-local Journal unread state missing')
if 'G.v06ClearedObjectiveTarget' not in s: raise SystemExit('objective glow clear state missing')
if 'setTimeout(finish,120)' not in s: raise SystemExit('investigation refresh missing')

p.write_text(s,encoding='utf-8')
print('patched Journal isolation and objective glow refresh')
