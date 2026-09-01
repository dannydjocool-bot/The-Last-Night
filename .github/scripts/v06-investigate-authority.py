from pathlib import Path

# 1) Core game: Search must never advance story objectives.
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='''function search(){

let p=G.ps[G.active];
let r=d6();

log(`${p.name} searches and rolls ${r}.`);

if(r===1){
encounter();
}
else if(r<=3){
log("Nothing useful.");
}
else if(r===4){
gainItem();
}
else if(r===5){
gainClue();
}
else{
gainItem();
gainClue();
}
}'''
new='''function search(){

let p=G.ps[G.active];
let r=d6();

log(`${p.name} searches and rolls ${r}.`);

if(r===1){
encounter();
}
else if(r<=3){
log("Nothing useful.");
}
else{
gainItem();
}
}'''
if old not in s:
    if new not in s:
        raise SystemExit('core search function did not match expected source')
else:
    s=s.replace(old,new,1)

# Make successful Investigate visibly authoritative and objective-specific.
marker='''  const before=G.clues;
  const advanced=gainClue();'''
replacement='''  const before=G.clues;
  const currentObjective=STORY_OBJECTIVES[G.clues];
  if(currentObjective&&p.loc!==currentObjective.loc){
    log(`📜 INVESTIGATE TARGET: ${currentObjective.text}`,"bad");
    updateStoryObjective();
    render();
    return false;
  }
  const advanced=gainClue();'''
if marker in s:
    s=s.replace(marker,replacement,1)
elif '📜 INVESTIGATE TARGET:' not in s:
    raise SystemExit('investigate progression marker not found')

p.write_text(s,encoding='utf-8')

# 2) V0.6 enhancement: exploration choices belong to Search, not Investigate.
p=Path('v06-enhancements.js')
s=p.read_text(encoding='utf-8')
old="""if(typeof investigate==='function'){const o=investigate;window.investigate=function(){
  const p0=hasGame()?G.ps[G.active]:null,obj0=objectiveText().trim().toLowerCase(),loc0=p0?.loc,clues0=Number(G?.clues||0);
  const finish=()=>{if(!hasGame())return;const p1=G.ps[G.active],clues1=Number(G?.clues||0);if(p1?.loc===loc0&&clues1>clues0&&obj0){const card=[...document.querySelectorAll('.loc')].find(c=>{const title=(c.querySelector('b')?.textContent||'').trim().toLowerCase();return title&&obj0.includes(title)});if(card){const title=(card.querySelector('b')?.textContent||'').trim().toLowerCase();const key=card.dataset?.loc||card.getAttribute('data-location')||title;G.v06ClearedObjectiveTarget={objective:obj0,loc:key,title};}}window.v06SyncGuidance?.()};
  if(hasGame()&&!currentCombat()&&Math.random()<.30){explore(function(){const r=o.apply(this,arguments);setTimeout(finish,0);setTimeout(finish,120);return r},arguments);return}
  const r=o.apply(this,arguments);setTimeout(finish,0);setTimeout(finish,120);hallucinate();anomaly();return r
}}"""
new="""if(typeof search==='function'){const o=search;window.search=function(){if(hasGame()&&!currentCombat()&&Math.random()<.30){explore(o,arguments);return}const r=o.apply(this,arguments);hallucinate();anomaly();return r}}
if(typeof investigate==='function'){const o=investigate;window.investigate=function(){
  const p0=hasGame()?G.ps[G.active]:null,obj0=objectiveText().trim().toLowerCase(),loc0=p0?.loc,clues0=Number(G?.clues||0);
  const r=o.apply(this,arguments);
  if(hasGame()&&Number(G?.clues||0)>clues0&&G.ps[G.active]?.loc===loc0){G.v06ClearedObjectiveTarget=null;window.v06SyncGuidance?.();highlightObjective();j(`Objective advanced after investigating ${LM?.[loc0]?.[1]||loc0}.`,'INVESTIGATION')}
  hallucinate();anomaly();return r
}}"""
if old not in s:
    if "if(typeof search==='function'){const o=search;window.search=function()" not in s:
        raise SystemExit('V0.6 investigate wrapper did not match expected source')
else:
    s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')

print('Search is loot/events only; Investigate is authoritative story progression')